import type {MetadataRoute} from "next";
import {getProducts} from "@/lib/api";

export default async function sitemap():Promise<MetadataRoute.Sitemap>{
  const base=process.env.NEXT_PUBLIC_SITE_URL||"http://localhost:3000";
  const routes=["","/shop","/categories","/brands","/about","/faq","/health-tips","/contact","/privacy","/terms","/wishlist"];
  const products=await getProducts();
  const staticEntries:MetadataRoute.Sitemap=routes.map(route=>({
    url:`${base}${route}`,
    changeFrequency:route===""?"daily":"weekly",
    priority:route===""?1:.7,
  }));
  const productEntries:MetadataRoute.Sitemap=products.map(product=>({
    url:`${base}/product/${product.slug}`,
    changeFrequency:"weekly",
    priority:.8,
  }));
  return [...staticEntries,...productEntries];
}
