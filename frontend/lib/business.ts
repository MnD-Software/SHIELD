export const business = {
  name: process.env.NEXT_PUBLIC_BUSINESS_NAME || "Shield Pharmacy",
  phone: process.env.NEXT_PUBLIC_BUSINESS_PHONE || "+254 700 123 456",
  phoneHref: process.env.NEXT_PUBLIC_BUSINESS_PHONE_HREF || "+254700123456",
  email: process.env.NEXT_PUBLIC_BUSINESS_EMAIL || "care@shieldpharmacy.co.ke",
  address: process.env.NEXT_PUBLIC_BUSINESS_ADDRESS || "Nairobi, Kenya",
  hours: {
    weekdays: process.env.NEXT_PUBLIC_BUSINESS_HOURS || "Mon–Sat, 8:00–20:00",
    sunday: "Sunday, 9:00–18:00",
  },
  whatsapp: process.env.NEXT_PUBLIC_WHATSAPP_NUMBER || "254700123456",
  mapQuery: process.env.NEXT_PUBLIC_MAP_QUERY || "Nairobi, Kenya",
} as const;
