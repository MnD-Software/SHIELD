import type {MetadataRoute} from "next";

export default function manifest():MetadataRoute.Manifest{
  return {
    name:"Shield Pharmacy",
    short_name:"Shield",
    description:"Pharmacist-led care, genuine products and delivery from Shield Pharmacy.",
    start_url:"/?source=pwa",
    display:"standalone",
    background_color:"#f7faf8",
    theme_color:"#0b5d4b",
    orientation:"portrait",
    icons:[
      {src:"/shield-logo.svg",sizes:"any",type:"image/svg+xml",purpose:"maskable"},
    ],
    shortcuts:[
      {name:"Shop medicines",short_name:"Shop",url:"/shop?source=shortcut"},
      {name:"My care",short_name:"My care",url:"/care?source=shortcut"},
      {name:"View basket",short_name:"Basket",url:"/cart?source=shortcut"},
    ],
  };
}
