import type {Category,Product,Review} from "./types";
const API=process.env.BACKEND_URL||"http://127.0.0.1:5000";
async function request<T>(path:string):Promise<T>{const response=await fetch(`${API}${path}`,{next:{revalidate:60}});if(!response.ok)throw new Error(`API request failed: ${response.status}`);return response.json()}
export async function getProducts():Promise<Product[]>{return (await request<{data:Product[]}>("/api/v1/products")).data}
export async function getCategories():Promise<Category[]>{return (await request<{data:Category[]}>("/api/v1/categories")).data}
export async function getProduct(slug:string):Promise<{data:Product;variations:Product[];related:Product[];reviews:Review[]}>{return request(`/api/v1/products/${slug}`)}
