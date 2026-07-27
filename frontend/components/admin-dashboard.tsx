"use client";

import { useCallback, useEffect, useState } from "react";
import { AnimatePresence, motion } from "motion/react";
import { useRouter } from "next/navigation";

type Overview = {
  metrics: Record<string, number>;
  orders: Array<{id:number;reference:string;customer_name:string;total:number;status:string}>;
  leads: Array<{id:number;name:string;company?:string;email:string;stage:string;owner:string;opportunity_value:number}>;
  tasks: Array<{id:number;lead_name:string;title:string;assigned_to:string;priority:string;status:string;due_at?:string}>;
  messages: Array<{id:number;name:string;email:string;subject:string;message:string;status:string}>;
  audit: Array<{id:number;action:string;entity_type:string;summary:string;created_at:string}>;
};

const tabs = ["overview","orders","crm","messages","audit"] as const;
const nextStatus: Record<string,string[]> = {Pending:["Processing","Cancelled"],Processing:["Ready","Cancelled"],Ready:["Dispatched","Cancelled"],Dispatched:["Completed"]};

export function AdminDashboard() {
  const router=useRouter();
  const [data,setData]=useState<Overview|null>(null);
  const [tab,setTab]=useState<(typeof tabs)[number]>("overview");
  const [error,setError]=useState("");
  const [busy,setBusy]=useState("");

  const load=useCallback(async()=>{
    const response=await fetch("/backend/api/v1/admin/overview",{credentials:"include",cache:"no-store"});
    if(response.status===401||response.status===403){router.replace("/login?next=/admin");return}
    if(!response.ok)throw new Error("The operations API is unavailable.");
    setData((await response.json()).data);
  },[router]);

  useEffect(()=>{load().catch((reason)=>setError(reason.message))},[load]);

  async function patch(path:string,payload:Record<string,string>,key:string){
    setBusy(key);setError("");
    const response=await fetch(`/backend${path}`,{method:"PATCH",credentials:"include",headers:{"Content-Type":"application/json"},body:JSON.stringify(payload)});
    if(!response.ok){const body=await response.json().catch(()=>({}));setError(body.message||"Update failed.");setBusy("");return}
    await load();setBusy("");
  }

  if(error&&!data)return <State title="Dashboard unavailable" detail={error}/>;
  if(!data)return <State title="Opening operations" detail="Loading live pharmacy data…"/>;

  return <div className="min-h-screen bg-[#f6f4ef] px-4 py-10 text-slate-950 sm:px-8">
    <div className="mx-auto max-w-7xl">
      <div className="flex flex-col gap-5 border-b border-slate-200 pb-7 sm:flex-row sm:items-end sm:justify-between">
        <div><p className="text-xs font-bold uppercase tracking-[.22em] text-emerald-700">Shield command centre</p><h1 className="mt-2 text-4xl font-semibold tracking-tight">Pharmacy operations</h1><p className="mt-2 text-slate-600">Orders, customer care and commercial pipeline in one live workspace.</p></div>
        <button onClick={()=>load()} className="rounded-full bg-slate-950 px-5 py-3 text-sm font-semibold text-white">Refresh data</button>
      </div>
      <nav className="my-6 flex gap-2 overflow-x-auto" aria-label="Admin sections">{tabs.map((item)=><button key={item} onClick={()=>setTab(item)} className={`relative rounded-full px-4 py-2 text-sm font-semibold capitalize ${tab===item?"text-white":"bg-white text-slate-700"}`}>{tab===item&&<motion.span layoutId="admin-tab" className="absolute inset-0 -z-10 rounded-full bg-emerald-700"/>}{item}</button>)}</nav>
      {error&&<p className="mb-5 rounded-2xl bg-red-50 p-4 text-red-700">{error}</p>}
      <AnimatePresence mode="wait"><motion.section key={tab} initial={{opacity:0,y:8}} animate={{opacity:1,y:0}} exit={{opacity:0,y:-8}}>
        {tab==="overview"&&<><div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">{Object.entries(data.metrics).map(([label,value])=><article key={label} className="rounded-3xl border border-white bg-white p-6 shadow-sm"><p className="text-sm capitalize text-slate-500">{label.replace("_"," ")}</p><p className="mt-2 text-3xl font-semibold">{label==="revenue"?"KSh ":""}{value.toLocaleString()}</p></article>)}</div><Panel title="Priority tasks"><TaskTable tasks={data.tasks}/></Panel></>}
        {tab==="orders"&&<Panel title="Order fulfilment"><div className="overflow-x-auto"><table className="w-full text-left text-sm"><thead><tr className="text-slate-500"><th className="py-3">Order</th><th>Customer</th><th>Total</th><th>Status</th><th>Action</th></tr></thead><tbody>{data.orders.map(o=><tr key={o.id} className="border-t border-slate-100"><td className="py-4 font-semibold">{o.reference}</td><td>{o.customer_name}</td><td>KSh {o.total.toLocaleString()}</td><td>{o.status}</td><td><div className="flex gap-2">{(nextStatus[o.status]||[]).map(status=><button disabled={busy===`order-${o.id}`} onClick={()=>patch(`/api/v1/admin/orders/${o.id}`,{status},`order-${o.id}`)} key={status} className="rounded-full border px-3 py-1.5 text-xs font-semibold">{status}</button>)}</div></td></tr>)}</tbody></table></div></Panel>}
        {tab==="crm"&&<><Panel title="Opportunity pipeline"><div className="grid gap-4 md:grid-cols-2">{data.leads.map(lead=><article key={lead.id} className="rounded-2xl border p-5"><div className="flex justify-between gap-4"><div><h3 className="font-semibold">{lead.name}</h3><p className="text-sm text-slate-500">{lead.company||lead.email}</p></div><strong>KSh {lead.opportunity_value.toLocaleString()}</strong></div><div className="mt-4 flex flex-wrap gap-2">{["New","Qualified","Opportunity","Converted","Lost"].map(stage=><button disabled={busy===`lead-${lead.id}`||stage===lead.stage} onClick={()=>patch(`/api/v1/admin/crm/leads/${lead.id}`,{stage},`lead-${lead.id}`)} key={stage} className={`rounded-full px-3 py-1 text-xs ${stage===lead.stage?"bg-emerald-700 text-white":"bg-slate-100"}`}>{stage}</button>)}</div></article>)}</div></Panel><Panel title="Follow-up tasks"><TaskTable tasks={data.tasks}/></Panel></>}
        {tab==="messages"&&<Panel title="Customer care inbox"><div className="grid gap-4">{data.messages.map(m=><article key={m.id} className="rounded-2xl border p-5"><div className="flex justify-between gap-4"><div><h3 className="font-semibold">{m.subject}</h3><p className="text-sm text-slate-500">{m.name} · {m.email}</p></div><span className="text-sm font-semibold text-emerald-700">{m.status}</span></div><p className="mt-3 text-slate-700">{m.message}</p></article>)}</div></Panel>}
        {tab==="audit"&&<Panel title="Audit trail"><div className="divide-y">{data.audit.map(a=><article key={a.id} className="py-4"><p className="font-semibold">{a.summary}</p><p className="mt-1 text-sm text-slate-500">{a.action} · {a.entity_type} · {new Date(a.created_at).toLocaleString()}</p></article>)}</div></Panel>}
      </motion.section></AnimatePresence>
    </div>
  </div>;
}

function Panel({title,children}:{title:string;children:React.ReactNode}){return <section className="mt-6 rounded-3xl border border-white bg-white p-6 shadow-sm"><h2 className="mb-5 text-xl font-semibold">{title}</h2>{children}</section>}
function TaskTable({tasks}:{tasks:Overview["tasks"]}){return <div className="grid gap-3">{tasks.length?tasks.map(t=><div key={t.id} className="flex flex-col justify-between gap-2 rounded-2xl bg-slate-50 p-4 sm:flex-row"><div><p className="font-semibold">{t.title}</p><p className="text-sm text-slate-500">{t.lead_name} · {t.assigned_to}</p></div><span className="text-sm font-semibold">{t.priority} · {t.status}</span></div>):<p className="text-slate-500">No tasks need attention.</p>}</div>}
function State({title,detail}:{title:string;detail:string}){return <div className="mx-auto flex min-h-[60vh] max-w-xl flex-col items-center justify-center px-6 text-center"><div className="h-3 w-3 animate-pulse rounded-full bg-emerald-600"/><h1 className="mt-5 text-3xl font-semibold">{title}</h1><p className="mt-2 text-slate-600">{detail}</p></div>}
