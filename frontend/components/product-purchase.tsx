"use client";

import Link from "next/link";
import { HeartIcon } from "@heroicons/react/24/outline";
import type { Product } from "@/lib/types";
import { useCart } from "./cart-provider";

export function ProductPurchase({ product, variations = [] }: { product: Product; variations?: Product[] }) {
  const { add, toggleWishlist, wishlist } = useCart();

  return (
    <aside className="self-start md:sticky md:top-28">
      <div className="flex items-start gap-5">
        <div className="flex-1">
          <span className="eyebrow">{product.brand} · {product.sku}</span>
          <h1 className="mt-3 text-4xl font-semibold leading-tight tracking-[-.04em]">{product.name}</h1>
        </div>
        <button onClick={() => toggleWishlist(product.id)} className={`rounded-full border p-3 ${wishlist.includes(product.id) ? "bg-rose-50 text-rose-500" : ""}`} aria-label="Save product">
          <HeartIcon className="h-5 w-5" />
        </button>
      </div>
      <p className="mt-4 text-xs font-semibold underline">★ 4.8 · Verified customer reviews</p>
      {variations.length > 1 && (
        <div className="mt-6">
          <p className="text-[10px] font-bold uppercase tracking-[.14em] text-slate-500">Choose a variation</p>
          <div className="mt-3 flex flex-wrap gap-2">
            {variations.map((variation) => (
              <Link
                key={variation.id}
                href={`/product/${variation.slug}`}
                className={`rounded-xl border px-4 py-3 text-xs font-semibold transition ${variation.id === product.id ? "border-shield-700 bg-shield-700 text-white shadow-sm" : "bg-white hover:border-shield-500"}`}
              >
                {variation.variation_label || variation.name}
              </Link>
            ))}
          </div>
        </div>
      )}
      <p className="mt-5 text-sm leading-6 text-slate-600">{product.description}</p>
      <div className="mt-5 flex items-center gap-3">
        <b className="text-2xl">KSh {product.effective_price.toLocaleString()}</b>
        {product.sale_price && <>
          <del className="text-xs text-slate-400">KSh {product.price.toLocaleString()}</del>
          <span className="rounded bg-shield-100 px-2 py-1 text-[9px] font-bold text-shield-600">SAVE {Math.round((product.price-product.sale_price)/product.price*100)}%</span>
        </>}
      </div>
      <div className="mt-6 divide-y rounded-xl border">
        <div className="p-4"><b className="block text-xs">Delivery today</b><span className="text-[10px] text-slate-500">Order before 3:00 PM in Nairobi</span></div>
        <div className="p-4"><b className="block text-xs">Free delivery over KSh 3,000</b><span className="text-[10px] text-slate-500">Carefully packed and discreet</span></div>
      </div>
      <p className="mt-4 text-[11px] font-semibold text-shield-600">● {product.stock > 0 ? "In stock and ready to dispatch" : "Currently unavailable"}</p>
      <button onClick={() => add(product)} disabled={!product.stock} className="primary mt-5 w-full py-4">Add to bag</button>
      <p className="mt-4 text-center text-[10px]">Unsure if this is right? <Link href="/contact" className="font-bold text-shield-600">Ask our pharmacist →</Link></p>
    </aside>
  );
}
