from fastapi import FastAPI, APIRouter, status, Request,Depends
from fastapi.responses import JSONResponse,StreamingResponse
from routes.schemes.nlp import PushRequest, SearchRequest,PushMessageRequest
from models import ConversationModel,ChunkModel,CurrentUser,MessageModel
from controllers import NLPController
from models import ResponseSignal
from guard.authGuard import guard
from helpers.config import get_settings, Settings
from helpers.serialise import Serializer
import json
import logging

logger = logging.getLogger('uvicorn.error')

nlp_router = APIRouter(
    prefix="/api/v1/nlp",
    tags=["api_v1", "nlp"],
    dependencies=[Depends(guard)] 
)

@nlp_router.post("/index/push/{conversation_id}")
async def index_conversation(request: Request, conversation_id: str, push_request: PushRequest, user: CurrentUser = Depends(guard)):

    conversation_model = await ConversationModel.create_instance(
        db_client=request.app.db_client
    )

    chunk_model = await ChunkModel.create_instance(
        db_client=request.app.db_client
    )

    conversation = await conversation_model.get_conversation_or_create_one(
        conversation_id=conversation_id,
        user_id=user.id  
    )

    if not conversation:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.CONVERSATION_NOT_FOUND_ERROR.value
            }
        )
    
    nlp_controller = NLPController(
        vectordb_client=request.app.vectordb_client,
        generation_client=request.app.generation_client,
        embedding_client=request.app.embedding_client,
        template_parser=request.app.template_parser,
    )

    has_records = True
    page_no = 1
    inserted_items_count = 0
    idx = 0

    while has_records:
        page_chunks = await chunk_model.get_conversation_chunks(conversation_id=conversation.id, page_no=page_no)
        if len(page_chunks):
            page_no += 1
        
        if not page_chunks or len(page_chunks) == 0:
            has_records = False
            break

        chunks_ids =  list(range(idx, idx + len(page_chunks)))
        idx += len(page_chunks)
        
        is_inserted = nlp_controller.index_into_vector_db(
            conversation=conversation,
            chunks=page_chunks,
            do_reset=push_request.do_reset,
            chunks_ids=chunks_ids
        )

        if not is_inserted:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "signal": ResponseSignal.INSERT_INTO_VECTORDB_ERROR.value
                }
            )
        
        inserted_items_count += len(page_chunks)
        
    return JSONResponse(
        content={
            "signal": ResponseSignal.INSERT_INTO_VECTORDB_SUCCESS.value,
            "inserted_items_count": inserted_items_count
        }
    )

@nlp_router.get("/index/info/{conversation_id}")
async def get_conversation_index_info(request: Request, conversation_id: str,user: CurrentUser = Depends(guard)):
    
    conversation_model = await ConversationModel.create_instance(
        db_client=request.app.db_client
    )

    conversation = await conversation_model.get_conversation_or_create_one(
        conversation_id=conversation_id,
        user_id=user.id
    )

    nlp_controller = NLPController(
        vectordb_client=request.app.vectordb_client,
        generation_client=request.app.generation_client,
        embedding_client=request.app.embedding_client,
        template_parser=request.app.template_parser,
    )

    collection_info = nlp_controller.get_vector_db_collection_info(conversation=conversation)

    return JSONResponse(
        content={
            "signal": ResponseSignal.VECTORDB_COLLECTION_RETRIEVED.value,
            "collection_info": collection_info
        }
    )

@nlp_router.post("/index/search/{conversation_id}")
async def search_index(request: Request, conversation_id: str, search_request: SearchRequest,user: CurrentUser = Depends(guard)):
    
    conversation_model = await ConversationModel.create_instance(
        db_client=request.app.db_client
    )

    conversation = await conversation_model.get_conversation_or_create_one(
        conversation_id=conversation_id,
        user_id=user.id
    )

    nlp_controller = NLPController(
        vectordb_client=request.app.vectordb_client,
        generation_client=request.app.generation_client,
        embedding_client=request.app.embedding_client,
        template_parser=request.app.template_parser,
    )

    results = nlp_controller.search_vector_db_collection(
        conversation=conversation, text=search_request.text, limit=search_request.limit
    )

    if not results:
        return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "signal": ResponseSignal.VECTORDB_SEARCH_ERROR.value
                }
            )
    
    return JSONResponse(
        content={
            "signal": ResponseSignal.VECTORDB_SEARCH_SUCCESS.value,
            "results": [ result.dict()  for result in results ]
        }
    )

@nlp_router.post("/index/answer/{conversation_id}")
async def answer_rag(
    request: Request,
    conversation_id: str,
    search_request: SearchRequest,
    user: CurrentUser = Depends(guard),
    app_settings: Settings = Depends(get_settings)
):
    conversation_model = await ConversationModel.create_instance(
        db_client=request.app.db_client
    )

    conversation = await conversation_model.get_conversation_or_create_one(
        conversation_id=conversation_id,
        user_id=user.id
    )

    nlp_controller = NLPController(
        vectordb_client=request.app.vectordb_client,
        generation_client=request.app.generation_client,
        embedding_client=request.app.embedding_client,
        template_parser=request.app.template_parser,
    )

    documents, answer, full_prompt, updated_chat_history = nlp_controller.answer_rag_question(
        conversation=conversation,
        query=search_request.text,
        limit=search_request.limit,
        chat_history=search_request.chat_history,
        stream=app_settings.STREAMING
    )
    logger.info(f"streaming = {app_settings.STREAMING} streaming_type={type(app_settings.STREAMING)}")
    logger.info(f"answer type: {type(answer)}, answer: {answer}")
    if not answer:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.RAG_ANSWER_ERROR.value
            }
        )

    # Ensure chat_history is a list of objects with 'content' and 'role'
    formatted_chat_history = [
        {"content": item.get("content"), "role": item.get("role")}
        for item in updated_chat_history
    ] if updated_chat_history else []

    return JSONResponse(
        content={
            "signal": ResponseSignal.RAG_ANSWER_SUCCESS.value,
            "answer": answer,
            "full_prompt": full_prompt,
            "chat_history": formatted_chat_history
        }
    )

@nlp_router.post("/index/stream/{conversation_id}")
async def answer_rag(
    request: Request,
    conversation_id: str,
    search_request: SearchRequest,
    user: CurrentUser = Depends(guard),
    app_settings: Settings = Depends(get_settings)
):
    conversation_model = await ConversationModel.create_instance(
        db_client=request.app.db_client
    )

    conversation = await conversation_model.get_conversation_or_create_one(
        conversation_id=conversation_id,
        user_id=user.id
    )

    nlp_controller = NLPController(
        vectordb_client=request.app.vectordb_client,
        generation_client=request.app.generation_client,
        embedding_client=request.app.embedding_client,
        template_parser=request.app.template_parser,
    )

    documents, answer, full_prompt, updated_chat_history = nlp_controller.stream_rag_question(
        conversation=conversation,
        query=search_request.text,
        limit=search_request.limit,
        chat_history=search_request.chat_history,
        stream=app_settings.STREAMING
    )
    if not answer:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.RAG_ANSWER_ERROR.value
            }
        )
    def token_stream():
        # answer_rag_question should yield tokens if stream=True
        for token in answer:
            yield token
    return StreamingResponse(token_stream(), media_type="text/plain")


@nlp_router.post("/index/message/{conversation_id}")
async def index_message(
    request: Request,
    conversation_id: str,
    push_message_request: PushMessageRequest,
    user: CurrentUser = Depends(guard)
):
    
    conversation_model = await ConversationModel.create_instance(
        db_client=request.app.db_client
    )

    conversation = await conversation_model.get_conversation_or_create_one(
        conversation_id=conversation_id,
        user_id=user.id
    )

    message_model = await MessageModel.create_instance(
        db_client=request.app.db_client
    )

    if not conversation:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.CONVERSATION_NOT_FOUND_ERROR.value
            }
        )

    new_message = await message_model.create_message(
        content=push_message_request.content,
        role=push_message_request.role,
        conversation_id=conversation.id
    )
    logger.info(f"New message created: {new_message}")
    if not new_message:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.MESSAGE_CREATED_ERROR.value
            }
        )

    return JSONResponse(
        content={
            "signal": ResponseSignal.MESSAGE_CREATED_SUCCESS.value,
            "message": Serializer.serialise(new_message)
        }
    )

@nlp_router.get("/index/messages/{conversation_id}")
async def get_messages(
    request: Request,
    conversation_id: str,
    user: CurrentUser = Depends(guard)
):
    message_model = await MessageModel.create_instance(
        db_client=request.app.db_client
    )

    messages = await message_model.get_messages_by_conversation_id(conversation_id=conversation_id)
    logger.info(f"Retrieved messages: {messages}")
    return JSONResponse(
        content={
            "signal": ResponseSignal.MESSAGE_RETRIEVED_SUCCESS.value,
            "messages": [Serializer.serialise(message.dict()) for message in messages]
        }
    )