import { Suspense } from "react";
import { AuthForm } from "@/components/auth-form";
export default function RegisterPage(){return <Suspense fallback={<div className="min-h-[60vh]"/>}><AuthForm mode="register"/></Suspense>}
