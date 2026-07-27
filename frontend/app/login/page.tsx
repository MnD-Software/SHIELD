import { Suspense } from "react";
import { AuthForm } from "@/components/auth-form";
export default function LoginPage(){return <Suspense fallback={<div className="min-h-[60vh]"/>}><AuthForm mode="login"/></Suspense>}
