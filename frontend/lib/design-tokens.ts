/** Shield's canonical visual language. Tailwind and CSS variables mirror these values. */
export const designTokens = {
  color: {
    canvas: "#FAFAF8",
    surface: "#FFFFFF",
    primary: "#134E4A",
    primaryDeep: "#0B2E2B",
    secondary: "#1E3A8A",
    accent: "#D4AF37",
    text: "#111827",
    textMuted: "#6B7280",
    border: "rgba(0,0,0,0.05)",
    success: "#147D64",
    warning: "#A16207",
    danger: "#B42318",
  },
  space: {1: "8px", 2: "16px", 3: "24px", 4: "32px", 5: "40px", 6: "48px", 8: "64px", 10: "80px", 12: "96px", 15: "120px"},
  radius: {small: "8px", control: "12px", card: "20px", feature: "32px", pill: "999px"},
  shadow: {
    quiet: "0 1px 2px rgba(17,24,39,.04), 0 12px 40px rgba(17,24,39,.05)",
    elevated: "0 2px 8px rgba(17,24,39,.04), 0 32px 90px rgba(17,24,39,.10)",
  },
  motion: {
    fast: 180,
    standard: 360,
    reveal: 700,
    ease: [0.22, 1, 0.36, 1] as const,
  },
} as const;

export type DesignTokens = typeof designTokens;
