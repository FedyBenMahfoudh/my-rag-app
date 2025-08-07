import { redirect } from "next/navigation";

import { LogoutButton } from "@/components/logout-button";
import { createClient } from "@/lib/server";
import { CurrentUserAvatar } from "@/components/current-user-avatar";
import { ModeToggle } from "@/components/mode-toggle";

export default async function ProtectedPage() {
  const supabase = await createClient();

  const { data, error } = await supabase.auth.getClaims();
  if (error || !data?.claims) {
    redirect("/auth/login");
  }
  return (
    <div className="flex h-svh w-full items-center justify-center gap-2">
      <p className="flex flex-col items-center gap-2 text-center">
        <CurrentUserAvatar />
        Hello <span>{data.claims.email}</span>
        <LogoutButton />
        <ModeToggle />
      </p>
    </div>
  );
}
