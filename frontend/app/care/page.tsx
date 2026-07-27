import Link from "next/link";

const pharmacyUrl=process.env.NEXT_PUBLIC_BACKEND_URL||"http://127.0.0.1:5000";

export default function CarePage(){
  return <section className="container-page py-8 md:py-16">
    <div className="care-mobile-hero">
      <span>SHIELD CARE</span><h1>Your health, in one place.</h1>
      <p>Manage orders, pharmacist conversations and the next steps in your care journey.</p>
    </div>
    <div className="care-action-grid">
      <a href={`${pharmacyUrl}/account`}><i>01</i><b>Orders & account</b><span>Track purchases and saved products</span></a>
      <a href={`${pharmacyUrl}/contact`}><i>02</i><b>Ask a pharmacist</b><span>Private support from the care team</span></a>
      <article className="is-coming"><i>03</i><b>Prescription wallet</b><span>Secure upload and approval workflow</span><em>Next</em></article>
      <article className="is-coming"><i>04</i><b>Refill planner</b><span>Consent-led medication reminders</span><em>Next</em></article>
    </div>
    <div className="care-privacy"><b>Designed for discretion</b><p>Clinical features will require authenticated access, consent records and pharmacist oversight before release.</p><Link href="/privacy">Privacy controls →</Link></div>
  </section>;
}
