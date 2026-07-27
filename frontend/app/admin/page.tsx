import { redirect } from "next/navigation";

export default function AdminPage() {
  const backendUrl =
    process.env.NEXT_PUBLIC_BACKEND_URL?.replace(/\/$/, "") ??
    "http://127.0.0.1:5000";

  redirect(`${backendUrl}/admin`);
}
