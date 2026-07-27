import type {Metadata,Viewport} from "next";
import {Inter} from "next/font/google";
import "./globals.css";
import {CartProvider} from "@/components/cart-provider";
import {Header} from "@/components/header";
import {Footer} from "@/components/footer";
import {MobileNav} from "@/components/mobile-nav";
import {PwaShell} from "@/components/pwa-shell";
import {MotionProvider} from "@/components/motion-provider";
const inter=Inter({subsets:["latin"],variable:"--font-inter"});
const siteUrl=process.env.NEXT_PUBLIC_SITE_URL||"http://localhost:3000";
export const metadata:Metadata={metadataBase:new URL(siteUrl),title:{default:"Shield Pharmacy — Trusted care, delivered",template:"%s — Shield Pharmacy"},description:"Genuine medicines, wellness essentials and pharmacist-led support delivered across Nairobi.",openGraph:{title:"Shield Pharmacy",description:"Your pharmacy, made easier.",type:"website"}};
export const viewport:Viewport={width:"device-width",initialScale:1,maximumScale:5,viewportFit:"cover",themeColor:"#FAFAF8"};
export default function RootLayout({children}:{children:React.ReactNode}){return <html lang="en"><body className={`${inter.variable} font-sans antialiased`}><CartProvider><a href="#content" className="fixed -top-20 left-4 z-[100] bg-white p-3 focus:top-4">Skip to content</a><Header/><main id="content" className="mobile-app-content"><MotionProvider>{children}</MotionProvider></main><Footer/><MobileNav/><PwaShell/></CartProvider></body></html>}
