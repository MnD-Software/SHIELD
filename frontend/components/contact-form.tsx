"use client";
import {useState} from "react";

type State={kind:"idle"|"sending"|"success"|"error";message?:string};
export function ContactForm(){
  const [state,setState]=useState<State>({kind:"idle"});
  async function submit(formData:FormData){
    setState({kind:"sending"});
    const payload=Object.fromEntries(formData.entries());
    try{
      const response=await fetch("/backend/api/v1/contact",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(payload)});
      const result=await response.json();
      if(!response.ok)throw new Error(result.message||"We could not send your message.");
      setState({kind:"success",message:result.message});
    }catch(error){setState({kind:"error",message:error instanceof Error?error.message:"Please try again."})}
  }
  if(state.kind==="success")return <div className="rounded-3xl bg-shield-50 p-8 md:p-12"><span className="eyebrow">Message received</span><h2 className="mt-4 text-3xl font-semibold">We’ll be in touch.</h2><p className="mt-3 text-sm text-muted">{state.message}</p><button onClick={()=>setState({kind:"idle"})} className="pill mt-7">Send another message</button></div>;
  return <form action={submit} className="rounded-3xl border bg-white p-6 shadow-soft md:p-10"><span className="eyebrow">Private support</span><h2 className="mt-3 text-3xl font-semibold">How can we help?</h2><div className="mt-8 grid gap-5 md:grid-cols-2"><label className="text-xs font-semibold">Full name<input name="name" required className="mt-2 min-h-12 w-full rounded-xl border px-4" autoComplete="name"/></label><label className="text-xs font-semibold">Email address<input name="email" required type="email" className="mt-2 min-h-12 w-full rounded-xl border px-4" autoComplete="email"/></label><label className="text-xs font-semibold md:col-span-2">Topic<select name="subject" className="mt-2 min-h-12 w-full rounded-xl border bg-white px-4"><option>Product question</option><option>Order support</option><option>Pharmacist guidance</option><option>Business enquiry</option></select></label><label className="hidden">Website<input name="website" tabIndex={-1} autoComplete="off"/></label><label className="text-xs font-semibold md:col-span-2">Message<textarea name="message" required minLength={10} rows={5} className="mt-2 w-full rounded-xl border p-4"/></label></div>{state.kind==="error"&&<p role="alert" className="mt-4 text-sm text-red-700">{state.message}</p>}<button disabled={state.kind==="sending"} className="primary mt-6 min-h-12 w-full">{state.kind==="sending"?"Sending…":"Send message"}</button></form>;
}
