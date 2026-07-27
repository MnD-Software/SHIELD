import Image from "next/image";
import Link from "next/link";
import type { Metadata } from "next";
import { getProduct } from "@/lib/api";
import { ProductPurchase } from "@/components/product-purchase";
import { ProductCard } from "@/components/product-card";

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const { slug } = await params;
  const { data } = await getProduct(slug);
  return { title: data.name, description: data.description, openGraph: { images: [data.image] } };
}

export default async function ProductPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const { data: product, variations = [], related, reviews } = await getProduct(slug);
  const details = [["Benefits", product.benefits], ["How to use", product.usage], ["Ingredients", product.ingredients], ["Important", product.warnings]];

  return (
    <>
      <section className="py-8 md:py-12">
        <div className="container-page">
          <nav className="mb-6 text-[10px] text-slate-500"><Link href="/shop">Shop</Link> / {product.category.name} / {product.name}</nav>
          <div className="grid gap-9 md:grid-cols-[1.15fr_.85fr] md:gap-20">
            <div>
              <div className="overflow-hidden rounded-2xl bg-mist"><Image src={product.image} alt={product.name} width={900} height={820} priority className="h-[330px] w-full object-cover md:h-[620px]" /></div>
              <div className="mt-3 grid grid-cols-3 gap-2">
                {[["100%", "Genuine"], ["✓", "Verified source"], ["24h", "Support"]].map(([value, label]) => <div key={label} className="grid h-20 place-items-center rounded-xl border bg-white text-center md:h-24"><span className="font-bold text-shield-600">{value}<small className="block text-[8px] text-slate-500 md:text-[9px]">{label}</small></span></div>)}
              </div>
            </div>
            <ProductPurchase product={product} variations={variations} />
          </div>
        </div>
      </section>
      <section className="bg-mist py-14 md:py-20"><div className="container-page grid gap-3 sm:grid-cols-2 md:grid-cols-4">{details.map(([title, text], index) => <article key={title} className="rounded-2xl bg-white p-5 md:p-6"><span className="eyebrow">0{index + 1}</span><h2 className="mt-5 font-bold">{title}</h2><p className="mt-3 text-xs leading-6 text-slate-500">{text}</p></article>)}</div></section>
      {reviews.length > 0 && <section className="py-14 md:py-20"><div className="container-page"><h2 className="text-3xl font-semibold">Verified experiences</h2><div className="mt-6 grid gap-4 md:grid-cols-2">{reviews.map((review) => <article key={review.id} className="rounded-2xl border bg-white p-5"><div className="flex justify-between text-xs font-bold"><span>{review.customer_name}</span><span className="text-amber-500">{"★".repeat(review.rating)}</span></div><p className="mt-3 text-sm text-slate-600">{review.body}</p></article>)}</div></div></section>}
      {related.length > 0 && <section className="bg-mist py-14 md:py-20"><div className="container-page"><h2 className="text-3xl font-semibold">You may also like</h2><div className="compact-product-grid mt-8 grid grid-cols-2 gap-4 md:grid-cols-4 md:gap-6">{related.map((item) => <ProductCard key={item.id} product={item} />)}</div></div></section>}
    </>
  );
}
