import Link from "next/link";
import {
  ArrowRightIcon,
  ChatBubbleLeftRightIcon,
  CheckBadgeIcon,
  ClockIcon,
  MapPinIcon,
  ShieldCheckIcon,
} from "@heroicons/react/24/outline";
import { getCategories, getProducts } from "@/lib/api";
import { ProductCard } from "@/components/product-card";

const collections = [
  {
    title: "Everyday relief",
    copy: "Pain, cold and allergy care",
    href: "/shop?category=everyday-relief",
    tone: "bg-[#dfeee7]",
    accent: "bg-[#b9d9ca]",
    label: "Most searched",
  },
  {
    title: "Daily wellness",
    copy: "Vitamins and supplements",
    href: "/shop?category=vitamins-supplements",
    tone: "bg-[#f5ead8]",
    accent: "bg-[#ead1a9]",
    label: "Build a routine",
  },
  {
    title: "Baby & family",
    copy: "Gentle care for little ones",
    href: "/shop?category=baby-care",
    tone: "bg-[#eee7f2]",
    accent: "bg-[#d9cae2]",
    label: "Family favourites",
  },
];

export default async function Home() {
  const [products, categories] = await Promise.all([getProducts(), getCategories()]);
  const featured = products.filter((product) => product.featured).slice(0, 8);

  return (
    <>
      <section className="bg-white pb-12 pt-8 md:pb-16 md:pt-12">
        <div className="container-page">
          <div className="gel-hero relative overflow-hidden rounded-[28px] bg-[#103f35] px-6 py-10 text-white shadow-[0_24px_70px_rgba(16,63,53,.18)] md:min-h-[430px] md:px-14 md:py-16">
            <div className="absolute -right-20 -top-28 h-80 w-80 rounded-full bg-[#2d7462] opacity-70" />
            <div className="absolute -bottom-40 right-[18%] h-96 w-96 rounded-full border-[70px] border-white/[.06]" />
            <div className="relative z-10 max-w-2xl">
              <span className="inline-flex items-center gap-2 rounded-full bg-white/10 px-3 py-2 text-[10px] font-bold uppercase tracking-[.16em] text-emerald-100 backdrop-blur">
                <MapPinIcon className="h-4 w-4" />
                Pharmacy care across Nairobi
              </span>
              <h1 className="mt-6 max-w-xl text-[42px] font-semibold leading-[.96] tracking-[-.055em] md:text-7xl">
                Feel better, without the pharmacy run.
              </h1>
              <p className="mt-5 max-w-lg text-sm leading-6 text-emerald-50/75 md:text-base">
                Discover trusted health essentials, clear guidance and convenient delivery—all in one calm place.
              </p>
              <div className="mt-8 flex flex-wrap gap-3">
                <Link href="/shop" className="rounded-xl bg-white px-6 py-3.5 text-xs font-bold text-shield-900 transition hover:-translate-y-0.5">
                  Explore the pharmacy
                </Link>
                <Link href="/contact" className="rounded-xl border border-white/25 px-6 py-3.5 text-xs font-bold text-white transition hover:bg-white/10">
                  Ask a pharmacist
                </Link>
              </div>
            </div>
            <div className="hero-trust-strip relative z-10 mt-10 grid gap-2 sm:grid-cols-3 md:absolute md:bottom-8 md:right-8 md:mt-0 md:w-[44%]">
              {[
                ["Same-day", "Selected Nairobi areas"],
                ["Genuine care", "Approved supply channels"],
                ["Here to help", "Real pharmacy support"],
              ].map(([title, copy]) => (
                <div key={title} className="rounded-2xl border border-white/15 bg-white/10 p-4 backdrop-blur-md">
                  <b className="block text-xs">{title}</b>
                  <span className="mt-1 block text-[9px] leading-4 text-emerald-50/65">{copy}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      <section className="bg-white py-10 md:py-16">
        <div className="container-page">
          <div className="flex items-end justify-between gap-4">
            <div>
              <p className="eyebrow">Curated for real life</p>
              <h2 className="mt-2 text-2xl font-semibold tracking-[-.035em] md:text-4xl">Start with how you want to feel</h2>
            </div>
            <Link href="/categories" className="hidden items-center gap-1 text-xs font-bold underline underline-offset-4 sm:flex">
              Browse all <ArrowRightIcon className="h-3.5 w-3.5" />
            </Link>
          </div>
          <div className="mobile-collection-rail mt-7 grid gap-4 md:grid-cols-3">
            {collections.map((collection, index) => (
              <Link key={collection.title} href={collection.href} className="group">
                <div className={`gel-card relative aspect-[1.45/1] overflow-hidden rounded-[22px] ${collection.tone}`}>
                  <div className={`absolute -bottom-12 -right-8 h-48 w-48 rounded-full ${collection.accent} transition duration-500 group-hover:scale-110`} />
                  <div className="absolute bottom-5 right-7 grid h-28 w-24 rotate-6 place-items-center rounded-[28px] bg-white/70 shadow-[0_18px_35px_rgba(31,41,35,.12)] backdrop-blur">
                    <span className="text-4xl">{["✚", "☀", "♡"][index]}</span>
                  </div>
                  <span className="absolute left-5 top-5 rounded-full bg-white/80 px-3 py-1.5 text-[9px] font-bold uppercase tracking-wider backdrop-blur">
                    {collection.label}
                  </span>
                </div>
                <h3 className="mt-3 text-base font-semibold">{collection.title}</h3>
                <p className="mt-0.5 text-xs text-slate-500">{collection.copy}</p>
              </Link>
            ))}
          </div>
        </div>
      </section>

      <section className="bg-[#faf9f7] py-12 md:py-20">
        <div className="container-page">
          <div className="flex items-end justify-between gap-5">
            <div>
              <p className="eyebrow">Popular near you</p>
              <h2 className="mt-2 text-2xl font-semibold tracking-[-.035em] md:text-4xl">Pharmacy favourites</h2>
              <p className="mt-2 text-xs text-slate-500 md:text-sm">Frequently chosen essentials, ready when you need them.</p>
            </div>
            <Link href="/shop" className="shrink-0 text-xs font-bold underline underline-offset-4">Show all</Link>
          </div>
          <div className="compact-product-grid mt-8 grid grid-cols-2 gap-x-3 gap-y-9 md:grid-cols-4 md:gap-x-6">
            {featured.map((product) => <ProductCard key={product.id} product={product} />)}
          </div>
        </div>
      </section>

      <section className="bg-white py-12 md:py-20">
        <div className="container-page">
          <div className="gel-panel grid overflow-hidden rounded-[28px] border border-black/[.06] bg-[#f0f6f3] lg:grid-cols-[1.1fr_.9fr]">
            <div className="p-7 md:p-12">
              <span className="inline-flex rounded-full bg-white px-3 py-1.5 text-[9px] font-bold uppercase tracking-[.14em] text-shield-700">Care, not guesswork</span>
              <h2 className="mt-5 max-w-lg text-3xl font-semibold leading-tight tracking-[-.045em] md:text-5xl">A pharmacist is part of the experience.</h2>
              <p className="mt-4 max-w-lg text-sm leading-6 text-slate-600">Questions about products, prescriptions or combining medicines? Get private, human guidance before you order.</p>
              <Link href="/contact" className="mt-7 inline-flex items-center gap-2 rounded-xl bg-shield-700 px-5 py-3 text-xs font-bold text-white">
                <ChatBubbleLeftRightIcon className="h-4 w-4" /> Talk to our team
              </Link>
            </div>
            <div className="grid gap-px bg-black/[.06] sm:grid-cols-2 lg:grid-cols-1">
              {[
                [CheckBadgeIcon, "Authenticity first", "Products from traceable, approved channels."],
                [ShieldCheckIcon, "Private by design", "Discreet packing and secure checkout."],
                [ClockIcon, "Clear expectations", "See availability and delivery details upfront."],
              ].map(([Icon, title, copy]) => {
                const CareIcon = Icon as typeof CheckBadgeIcon;
                return (
                  <div key={title as string} className="flex gap-4 bg-white p-6 md:p-8">
                    <CareIcon className="h-6 w-6 shrink-0 text-shield-700" />
                    <div><h3 className="text-sm font-semibold">{title as string}</h3><p className="mt-1 text-[11px] leading-5 text-slate-500">{copy as string}</p></div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </section>

      <section className="border-t border-black/[.06] bg-white py-10">
        <div className="container-page">
          <p className="mb-5 text-[10px] font-bold uppercase tracking-[.15em] text-slate-400">Explore every aisle</p>
          <div className="flex gap-2 overflow-x-auto pb-2 scrollbar-hide">
            {categories.map((category) => (
              <Link key={category.id} href={`/shop?category=${category.slug}`} className="whitespace-nowrap rounded-full border border-black/10 bg-white px-4 py-2.5 text-xs font-semibold transition hover:border-black hover:shadow-sm">
                {category.name}
              </Link>
            ))}
          </div>
        </div>
      </section>
    </>
  );
}
