# Shield Pharmacy digital flagship design system

## Positioning

Shield is a private medical concierge expressed through a luxury retail system. The interface is clinically clear, editorially composed, and deliberately quiet. It must never resemble a supermarket, hospital portal, or generic component-library demo.

## Reference principles

- Apple: progressive disclosure, decisive hierarchy, and one dominant story per viewport.
- Aesop and Augustinus Bader: material restraint, generous margins, and product photography treated as editorial content.
- Bang & Olufsen and Rimowa: precise geometry, quiet interaction, and craftsmanship communicated through detail rather than decoration.
- Mr Porter: disciplined merchandising, curation, and product information that remains highly scannable.
- Cleveland Clinic and Mayo Clinic: expert provenance, plain language, visible safety boundaries, and accessible decision paths.

No layouts, visual assets, trade dress, or branded patterns are copied from these references.

## Foundations

### Colour

| Role | Value | Usage |
| --- | --- | --- |
| Canvas | `#FAFAF8` | Default page background |
| Surface | `#FFFFFF` | Cards and elevated content |
| Shield emerald | `#134E4A` | Primary actions and clinical trust |
| Deep emerald | `#0B2E2B` | Editorial dark sections |
| Clinical blue | `#1E3A8A` | Rare informational emphasis |
| Heritage gold | `#D4AF37` | Tiny premium accents only |
| Ink | `#111827` | Primary text |
| Slate | `#6B7280` | Supporting text |
| Hairline | `rgba(0,0,0,.05)` | Quiet separation |

Gold never fills large surfaces or primary buttons. Blue and gold must not compete in the same component.

### Type

Inter Variable is the product typeface. Large display copy uses tight tracking and controlled line breaks; body copy stays between 45 and 72 characters per line. Typography is the principal visual element.

- Display XL: clamp 64–112px, 0.92–0.98 line height
- Display: clamp 48–80px, 0.98–1.04 line height
- H2: clamp 36–56px, 1.05 line height
- H3: 20–28px, 1.2 line height
- Body large: 18px / 30px
- Body: 15–16px / 24–28px
- Label: 10–12px, uppercase only for short metadata

### Space and geometry

All intentional spacing resolves to an 8px grid. Default page gutters are 20px mobile, 32px tablet, and 48px desktop. Major sections use 96–160px vertical space. Cards use 20px radius; feature panels may use 32px. Hairline borders are preferred to heavy shadows.

### Imagery

Product images occupy roughly 70% of merchandise cards. Photography uses soft natural light, clean neutral backgrounds, believable medical professionalism, and no exaggerated wellness claims. Decorative imagery must not obscure product identity or safety information.

## Interaction and motion

Motion explains hierarchy and state. Default entrance: opacity 0→1, blur 8→0, y 16→0 over 700ms with `[0.22,1,0.36,1]`. Hover transitions last 180–360ms. Parallax travel stays below 6% of the viewport. No bounce, spin, flash, looping scale, or elastic easing.

Every motion component must respect `prefers-reduced-motion`. Content must remain present and usable with JavaScript or animation disabled.

## Component rules

- Navigation: glass only when contrast remains AA; maximum five primary links; pharmacist access is always visible.
- Buttons: one primary action per decision group; minimum 44px target; verbs describe the outcome.
- Product cards: dominant image, brand, two-line product name, availability, price, and one fast action. Never add promotional clutter.
- Forms: persistent labels, inline errors, helpful examples, and a calm confirmation state.
- Medical content: state author/reviewer and review date when content becomes clinical guidance; always show the emergency-care boundary.
- Feedback: loading, success, empty, and error states are designed as first-class surfaces.

## Accessibility contract

WCAG AA is the release floor. Keyboard order follows visual order. Focus is never removed. Icon-only controls require accessible names. Touch targets are at least 44×44px. Colour is never the only state indicator. Text zoom at 200% and reduced motion must preserve every workflow.

## Current audit and phased remediation

1. Foundation: hard-coded colour and spacing values exist; tokens now provide the migration target.
2. Components: header, product card, drawer, buttons, inputs, and section primitives need consolidation.
3. Routes: categories, brands, login, register, dashboard, wishlist, FAQ, health tips, contact, and legal routes must be added to Next.js or intentionally proxied behind one domain.
4. Motion: Framer Motion and GSAP are named in the architecture but are not yet installed; add them only when motion primitives are implemented.
5. Content: seeded product photography is inconsistent and temporary contact/location data must be replaced before launch.
6. Quality: Lighthouse, keyboard, contrast, responsive, structured-data, and production security audits belong to the final release gate.
