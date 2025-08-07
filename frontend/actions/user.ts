"use server";
import { createClient } from "@/lib/server";
import { parseStringify } from "@/lib/utils";

export const getCurrentUser = async () => {
  const supabase = await createClient();
  const { data, error } = await supabase.auth.getUser();
  if (!data || !data.user) return null;

  return parseStringify(data.user);
};
