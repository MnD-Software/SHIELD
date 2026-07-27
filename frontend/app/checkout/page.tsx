"use client";
import {FormEvent,useState} from "react";
import Link from "next/link";
import {useCart} from "@/components/cart-provider";

export default function Checkout(){
  const {lines,total,clear}=useCart();
  const [step,setStep]=useState(1),[loading,setLoading]=useState(false),[error,setError]=useState(""),[reference,setReference]=useState("");
  const delivery=total>=3000?0:250;
  async function submit(e:FormEvent<HTMLFormElement>){
    e.preventDefault();setLoading(true);setError("");
    const form=new FormData(e.currentTarget),customer=Object.fromEntries(form.entries());
    try{
      const response=await fetch("/backend/api/v1/orders",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({customer,items:lines.map(l=>({product_id:l.product.id,quantity:l.quantity}))})});
      const body=await response.json();if(!response.ok)throw new Error(body.message||"Could not place order");
      setReference(body.data.reference);clear();
    }catch(err){setError(err instanceof Error?err.message:"Could not place order")}finally{setLoading(false)}
  }
  if(reference)return <section className="grid min-h-[70vh] place-items-center px-5 text-center"><div><span className="mx-auto grid h-20 w-20 place-items-center rounded-full bg-shield-100 text-4xl text-shield-600">✓</span><span className="eyebrow mt-6 block">Order confirmed</span><h1 className="mt-3 text-5xl font-semibold">Thank you.</h1><p className="mt-4 text-sm text-slate-500">Your reference is <b>{reference}</b>. We’re preparing your order.</p><Link className="primary mt-8" href="/shop">Continue shopping</Link></div></section>;
  if(!lines.length)return <section className="grid min-h-[65vh] place-items-center text-center"><div><h1 className="text-4xl font-bold">Your bag is empty.</h1><Link className="primary mt-6" href="/shop">Explore products</Link></div></section>;
  return <section className="bg-mist py-16"><div className="container-page">
    <div className="mb-10 flex justify-center gap-6">{["Delivery","Payment","Review"].map((label,i)=><div key={label} className={`text-xs font-bold ${step>=i+1?"text-shield-600":"text-slate-400"}`}><i className={`mr-2 inline-grid h-7 w-7 place-items-center rounded-full not-italic ${step>=i+1?"bg-shield-600 text-white":"border"}`}>{i+1}</i>{label}</div>)}</div>
    <div className="grid items-start gap-12 md:grid-cols-[1.3fr_.7fr]">
      <form onSubmit={submit} className="rounded-2xl bg-white p-7 md:p-10">
        <div className={step===1?"":"hidden"}><span className="eyebrow">Step 1 of 3</span><h1 className="mt-3 text-4xl font-semibold">Delivery details</h1><div className="mt-8 grid gap-5 md:grid-cols-2">
          {[["name","Full name","text"],["email","Email address","email"],["phone","Phone number","tel"],["address","Street / building","text"],["town","Town","text"]].map(([name,label,type])=><label key={name} className={name==="address"?"md:col-span-2":""}><span className="text-xs font-bold">{label}</span><input required name={name} type={type} defaultValue={name==="town"?"Nairobi":""} className="mt-2 w-full rounded-xl border p-3 text-sm"/></label>)}
          <label><span className="text-xs font-bold">County</span><select required name="county" className="mt-2 w-full rounded-xl border p-3 text-sm"><option>Nairobi</option><option>Kiambu</option><option>Machakos</option><option>Kajiado</option></select></label>
        </div><button type="button" onClick={()=>setStep(2)} className="primary mt-8">Continue to payment →</button></div>
        <div className={step===2?"":"hidden"}><button type="button" onClick={()=>setStep(1)} className="text-xs">← Delivery</button><span className="eyebrow mt-6 block">Step 2 of 3</span><h1 className="mt-3 text-4xl font-semibold">Payment method</h1><div className="mt-8 space-y-3">
          <label className="flex items-center gap-4 rounded-xl border p-5"><input type="radio" name="payment_method" value="mpesa" defaultChecked/><span><b className="block text-sm">M-Pesa</b><small className="text-slate-500">Secure prompt sent to your phone</small></span></label>
          <label className="flex items-center gap-4 rounded-xl border p-5"><input type="radio" name="payment_method" value="cash"/><span><b className="block text-sm">Cash on delivery</b><small className="text-slate-500">Pay when your order arrives</small></span></label>
        </div><button type="button" onClick={()=>setStep(3)} className="primary mt-8">Review order →</button></div>
        <div className={step===3?"":"hidden"}><button type="button" onClick={()=>setStep(2)} className="text-xs">← Payment</button><span className="eyebrow mt-6 block">Step 3 of 3</span><h1 className="mt-3 text-4xl font-semibold">Ready to place?</h1><p className="mt-4 text-sm text-slate-500">Your delivery and payment details will be validated securely by Shield.</p>{error&&<p className="mt-5 rounded-xl bg-red-50 p-4 text-xs text-red-700">{error}</p>}<label className="mt-8 flex gap-3 text-xs"><input type="checkbox" required/>I agree to the terms and confirm my details are correct.</label><button disabled={loading} className="primary mt-8 w-full py-4">{loading?"Placing order…":`Place order · KSh ${(total+delivery).toLocaleString()}`}</button></div>
      </form>
      <aside className="sticky top-28 rounded-2xl border bg-white p-7"><h2 className="font-bold">Order summary</h2>{lines.map(l=><div key={l.product.id} className="flex justify-between border-b py-4 text-xs"><span>{l.quantity} × {l.product.name}</span><b>KSh {(l.quantity*l.product.effective_price).toLocaleString()}</b></div>)}<div className="mt-5 flex justify-between text-lg"><span>Total</span><b>KSh {(total+delivery).toLocaleString()}</b></div></aside>
    </div>
  </div></section>
}
