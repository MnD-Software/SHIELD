import type {Metadata} from "next";import {getProducts} from "@/lib/api";import {WishlistClient} from "@/components/wishlist-client";
export const metadata:Metadata={title:"Saved products"};
export default async function Wishlist(){const products=await getProducts();return <section className="py-16 md:py-24"><div className="container-page"><span className="eyebrow">My care</span><h1 className="mt-4 text-display">Saved for later.</h1><div className="mt-12"><WishlistClient products={products}/></div></div></section>}
