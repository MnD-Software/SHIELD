"use client";

import Link from "next/link";
import { useState } from "react";
import {
  Bars3Icon,
  MagnifyingGlassIcon,
  ShoppingBagIcon,
  UserCircleIcon,
  XMarkIcon,
} from "@heroicons/react/24/outline";
import { useCart } from "./cart-provider";
import { CartDrawer } from "./cart-drawer";

const categories = [
  ["✦", "All", "/shop"],
  ["✓", "Everyday relief", "/shop?category=over-the-counter"],
  ["☀", "Vitamins", "/shop?category=vitamins-supplements"],
  ["♡", "Baby care", "/shop?category=baby-care"],
  ["◇", "Personal care", "/shop?category=personal-care"],
  ["⌁", "Equipment", "/shop?category=medical-equipment"],
  ["+", "First aid", "/shop?category=first-aid"],
  ["%", "Offers", "/shop?offers=true"],
];

export function Header() {
  const { count, setOpen } = useCart();
  const [menu, setMenu] = useState(false);
  const pharmacyUrl = process.env.NEXT_PUBLIC_BACKEND_URL || "http://127.0.0.1:5000";

  return (
    <>
      <div className="desktop-announcement bg-shield-900 px-4 py-2 text-white">
        <div className="container-page flex items-center justify-between text-[9px] font-semibold tracking-[.08em]">
          <span>Same-day Nairobi delivery available · Free over KSh 3,000</span>
          <Link href="/contact" className="text-emerald-200">Ask our pharmacy team →</Link>
        </div>
      </div>
      <header className="app-header sticky top-0 z-40 border-b bg-white/95 backdrop-blur-2xl">
        <div className="container-page app-header-inner flex h-[82px] items-center gap-6">
          <button onClick={() => setMenu(true)} className="grid min-h-11 min-w-11 place-items-center rounded-full hover:bg-pearl md:hidden" aria-label="Open menu">
            <Bars3Icon className="h-5 w-5" />
          </button>
          <Link href="/" className="app-brand flex items-center gap-2 font-bold tracking-[.13em]">
            <img src="/shield-logo.svg" alt="" className="h-11 w-11 object-contain" />
            <span className="app-brand-name">SHIELD<small className="block text-[7px] tracking-[.3em] text-shield-600">PHARMACY</small></span>
          </Link>
          <Link href="/shop" className="market-search mx-auto hidden items-center rounded-full border bg-white p-1.5 shadow-[0_3px_14px_rgba(0,0,0,.10)] transition hover:shadow-[0_5px_20px_rgba(0,0,0,.14)] md:flex">
            <span className="border-r px-5 text-xs font-semibold">What do you need?</span>
            <span className="border-r px-5 text-xs font-semibold">Health category</span>
            <span className="px-5 text-xs text-muted">Ready to deliver</span>
            <i className="grid h-9 w-9 place-items-center rounded-full bg-shield-600 text-white"><MagnifyingGlassIcon className="h-4 w-4" /></i>
          </Link>
          <div className="app-header-actions ml-auto flex items-center gap-1">
            <Link href="/shop" className="header-search grid min-h-11 min-w-11 place-items-center rounded-full hover:bg-pearl md:hidden" aria-label="Search pharmacy"><MagnifyingGlassIcon className="h-5 w-5" /></Link>
            <a href={`${pharmacyUrl}/account`} className="hidden items-center gap-2 rounded-full px-3 py-2 text-xs font-semibold hover:bg-pearl sm:flex"><UserCircleIcon className="h-5 w-5" /><span className="hidden lg:block">My care</span></a>
            <button onClick={() => setOpen(true)} className="header-bag relative flex min-h-11 items-center gap-2 rounded-full border px-3 py-2 hover:shadow-sm" aria-label={`Bag with ${count} items`}><ShoppingBagIcon className="h-5 w-5" /><span className="hidden text-xs font-semibold sm:block">Bag</span><span className="grid h-5 min-w-5 place-items-center rounded-full bg-ink px-1 text-[9px] text-white">{count}</span></button>
          </div>
        </div>
        <form action="/shop" className="mobile-market-search mx-4 mb-3 hidden items-center gap-3 rounded-full border border-black/10 bg-white px-4 py-2.5 shadow-[0_3px_14px_rgba(0,0,0,.08)]">
          <MagnifyingGlassIcon className="h-4 w-4 text-shield-700" />
          <input name="q" aria-label="Search products" placeholder="Search medicines and wellness" className="min-w-0 flex-1 bg-transparent text-xs font-semibold outline-none placeholder:font-normal placeholder:text-slate-400" />
          <span className="rounded-full bg-[#e7f1ed] px-2.5 py-1 text-[8px] font-bold uppercase tracking-wider text-shield-700">Nairobi</span>
        </form>
        <nav className="market-category-rail hide-scrollbar container-page flex gap-8 overflow-x-auto border-t py-3" aria-label="Shop by category">
          {categories.map(([icon, label, href]) => <Link key={label} href={href} className="flex min-w-max items-center gap-2 border-b-2 border-transparent pb-2 text-[10px] font-semibold text-muted transition hover:border-ink hover:text-ink"><i className="text-base not-italic">{icon}</i>{label}</Link>)}
        </nav>
      </header>
      <div className={`fixed inset-0 z-50 md:hidden ${menu ? "pointer-events-auto" : "pointer-events-none"}`} aria-hidden={!menu}>
        <button onClick={() => setMenu(false)} className={`absolute inset-0 bg-ink/45 transition ${menu ? "opacity-100" : "opacity-0"}`} aria-label="Close menu" />
        <aside className={`absolute left-0 top-0 flex h-full w-[min(88%,360px)] flex-col bg-porcelain p-6 shadow-2xl transition duration-300 ${menu ? "translate-x-0" : "-translate-x-full"}`}>
          <div className="flex items-center justify-between border-b pb-5"><b className="tracking-[.14em]">SHIELD <small className="text-shield-600">PHARMACY</small></b><button onClick={() => setMenu(false)} className="grid min-h-11 min-w-11 place-items-center rounded-full border"><XMarkIcon className="h-5 w-5" /></button></div>
          <nav className="flex flex-col py-5">
            {[["Shop", "/shop"], ["Categories", "/categories"], ["Brands", "/brands"], ["Saved", "/wishlist"], ["Health tips", "/health-tips"], ["FAQ", "/faq"], ["About", "/about"]].map(([label, href]) => <Link onClick={() => setMenu(false)} key={label} href={href} className="border-b py-4 text-base font-semibold">{label}<span className="float-right text-shield-600">→</span></Link>)}
          </nav>
          <Link onClick={() => setMenu(false)} href="/contact" className="primary mt-auto w-full">Ask a pharmacist</Link>
        </aside>
      </div>
      <CartDrawer />
    </>
  );
}
