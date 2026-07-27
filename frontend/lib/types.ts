export type Category={id:number;name:string;slug:string;icon:string;description:string;product_count:number};
export type Product={id:number;name:string;slug:string;brand:string;sku:string;category:{name:string;slug:string};price:number;sale_price:number|null;effective_price:number;stock:number;image:string;featured:boolean;popularity:number;description:string;benefits?:string;usage?:string;ingredients?:string;warnings?:string;variation_group?:string|null;variation_label?:string|null};
export type Review={id:number;customer_name:string;rating:number;body:string;verified:boolean};
export type CartLine={product:Product;quantity:number};
