"use client";
import Link from "next/link";
import {usePathname} from "next/navigation";
import {HomeIcon,ShoppingBagIcon,Squares2X2Icon,UserCircleIcon} from "@heroicons/react/24/outline";
import {HomeIcon as HomeSolid,Squares2X2Icon as ShopSolid} from "@heroicons/react/24/solid";
import {useCart} from "./cart-provider";

export function MobileNav(){
  const pathname=usePathname();
  const {count,setOpen}=useCart();
  const shopActive=pathname.startsWith("/shop")||pathname.startsWith("/product");
  const itemClass=(active:boolean)=>`mobile-nav-item ${active?"is-active":""}`;
  return <nav className="mobile-tabbar" aria-label="Mobile navigation">
    <Link href="/" className={itemClass(pathname==="/")} aria-current={pathname==="/"?"page":undefined}>{pathname==="/"?<HomeSolid/>:<HomeIcon/>}<span>Home</span></Link>
    <Link href="/shop" className={itemClass(shopActive)} aria-current={shopActive?"page":undefined}>{shopActive?<ShopSolid/>:<Squares2X2Icon/>}<span>Shop</span></Link>
    <button onClick={()=>setOpen(true)} className={itemClass(false)} aria-label={`Open bag with ${count} items`}><span className="relative"><ShoppingBagIcon/>{count>0&&<b>{count}</b>}</span><span>Bag</span></button>
    <Link href="/care" className={itemClass(pathname.startsWith("/care"))}><UserCircleIcon/><span>My care</span></Link>
  </nav>;
}
