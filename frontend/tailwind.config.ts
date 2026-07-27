import type {Config} from "tailwindcss";

export default {
  content:["./app/**/*.{js,ts,jsx,tsx}","./components/**/*.{js,ts,jsx,tsx}","./features/**/*.{js,ts,jsx,tsx}"],
  theme:{extend:{
    colors:{
      shield:{50:"#F1F7F5",100:"#DCEBE7",500:"#176B63",600:"#134E4A",700:"#103F3C",900:"#0B2E2B"},
      clinical:"#1E3A8A",gold:"#D4AF37",ink:"#111827",muted:"#6B7280",mist:"#F5F6F3",porcelain:"#FAFAF8",pearl:"#F0F1ED"
    },
    fontFamily:{sans:["var(--font-inter)","Inter","sans-serif"],serif:["var(--font-inter)","Inter","sans-serif"]},
    fontSize:{"display-xl":["clamp(4rem,8vw,7rem)",{lineHeight:".94",letterSpacing:"-.065em"}],display:["clamp(3rem,6vw,5rem)",{lineHeight:"1",letterSpacing:"-.055em"}],lead:["1.125rem",{lineHeight:"1.75rem"}]},
    spacing:{18:"4.5rem",22:"5.5rem",30:"7.5rem",40:"10rem"},
    boxShadow:{soft:"0 1px 2px rgba(17,24,39,.04),0 12px 40px rgba(17,24,39,.05)",lift:"0 2px 8px rgba(17,24,39,.04),0 32px 90px rgba(17,24,39,.10)"},
    borderRadius:{xl:"1rem","2xl":"1.25rem","3xl":"2rem"},
    transitionTimingFunction:{luxury:"cubic-bezier(.22,1,.36,1)"},
    transitionDuration:{360:"360ms",700:"700ms"}
  }},plugins:[]
} satisfies Config;
