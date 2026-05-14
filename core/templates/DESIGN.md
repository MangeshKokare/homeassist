---
name: Premium Service Minimalist
colors:
  surface: '#faf8ff'
  surface-dim: '#d9d9e4'
  surface-bright: '#faf8ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f3f3fd'
  surface-container: '#ededf8'
  surface-container-high: '#e7e7f2'
  surface-container-highest: '#e1e2ec'
  on-surface: '#191b23'
  on-surface-variant: '#434654'
  inverse-surface: '#2e3038'
  inverse-on-surface: '#f0f0fb'
  outline: '#737685'
  outline-variant: '#c3c6d6'
  surface-tint: '#0c56d0'
  primary: '#003d9b'
  on-primary: '#ffffff'
  primary-container: '#0052cc'
  on-primary-container: '#c4d2ff'
  inverse-primary: '#b2c5ff'
  secondary: '#515f74'
  on-secondary: '#ffffff'
  secondary-container: '#d5e3fd'
  on-secondary-container: '#57657b'
  tertiary: '#7b2600'
  on-tertiary: '#ffffff'
  tertiary-container: '#a33500'
  on-tertiary-container: '#ffc6b2'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dae2ff'
  primary-fixed-dim: '#b2c5ff'
  on-primary-fixed: '#001848'
  on-primary-fixed-variant: '#0040a2'
  secondary-fixed: '#d5e3fd'
  secondary-fixed-dim: '#b9c7e0'
  on-secondary-fixed: '#0d1c2f'
  on-secondary-fixed-variant: '#3a485c'
  tertiary-fixed: '#ffdbcf'
  tertiary-fixed-dim: '#ffb59b'
  on-tertiary-fixed: '#380d00'
  on-tertiary-fixed-variant: '#812800'
  background: '#faf8ff'
  on-background: '#191b23'
  surface-variant: '#e1e2ec'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-lg:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 4px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  xxl: 48px
  safe-margin: 20px
  gutter: 16px
---

## Brand & Style
The design system focuses on a high-end service experience, prioritizing clarity and trust. It utilizes a **Minimalist** approach with **Corporate Modern** refinements to evoke a sense of professional reliability. The interface uses generous whitespace to reduce cognitive load, ensuring that users feel a sense of calm while navigating home maintenance tasks. Visual elements are characterized by light, airy surfaces and precise accents, mirroring the cleanliness and quality expected from a premium home service provider.

## Colors
The palette is intentionally restrained to maintain a high-end feel. **Pure White (#FFFFFF)** serves as the primary canvas, creating an expansive and clean environment. The **Brand Blue (#0052CC)** is used strategically for high-priority calls to action and active states, providing a confident focal point. Text utilizes **Slate Gray (#334155)** to maintain readability without the harshness of pure black. Subtle UI definition is achieved through **Very Light Gray (#F1F5F9)** for borders and dividers, ensuring the interface remains lightweight.

## Typography
This design system utilizes **Inter** for its neutral, highly legible character. A strict typographic hierarchy is established through weight variation rather than excessive size shifts. Headings use **Semi-Bold (600)** weights to provide clear section anchors. Body text is set with generous line heights to ensure long-form service descriptions remain accessible. Labels for metadata and small buttons use a slightly heavier weight at smaller sizes to maintain visual presence against the white background.

## Layout & Spacing
The system follows a **Mobile-First, Fluid Grid** philosophy. Standard layouts utilize a 4-column grid for mobile with a 20px outer margin and 16px gutters. Spacing follows a strict 4pt / 8pt increment system to ensure rhythmic consistency. Vertical rhythm is driven by the "generous whitespace" directive, using 32px or 48px gaps between major sections to prevent the UI from feeling cluttered. Content containers should typically span the full width minus safe margins, while specialized service cards can utilize horizontal scrolling patterns.

## Elevation & Depth
Depth is articulated through **Ambient Shadows** and tonal layering. This design system avoids heavy borders in favor of soft, elegant shadows.
- **Low Elevation:** Used for cards and interactive surfaces. (Shadow: 0px 4px 20px, 5% Opacity, #334155).
- **High Elevation:** Used for floating buttons or sticky bottom bars. (Shadow: 0px -4px 24px, 8% Opacity, #334155).
- **Surface Tiers:** Backgrounds are `#FFFFFF`. For secondary content containers, a very subtle fill of `#F8FAFC` may be used to differentiate between the page and a background card.

## Shapes
The shape language is friendly yet professional, characterized by **Rounded** corners. Standard containers and service cards use a radius between **16px and 24px** (standardized at 20px) to create a soft, approachable container for high-quality service imagery. Small interactive elements like buttons use a slightly tighter 12px radius to maintain a sense of precision. Icons should utilize a consistent 2px stroke width with rounded caps and joins to match the outer container geometry.

## Components

### Buttons
- **Primary:** Solid Brand Blue (#0052CC) with white text. 12px radius. 16px horizontal padding.
- **Secondary:** Surface color (#FFFFFF) with a 1px border (#F1F5F9) and Slate Gray (#334155) text.
- **Ghost:** No background or border. Primary Blue text for "View All" or "Cancel" actions.

### Cards
- **Service Card:** White background, 20px radius, 5% opacity shadow. Uses a top-heavy layout with a high-resolution image followed by a 16px padded content area for the title and price.

### Inputs & Selection
- **Text Fields:** 10px radius, `#F1F5F9` border. On focus, the border transitions to Primary Blue with a 1px width.
- **Chips:** Highly rounded (pill-shaped) for categories. Unselected: Light gray background; Selected: Primary Blue background with white text.

### Lists & Navigation
- **Service List:** Clean lines with `#F1F5F9` dividers. 16px vertical padding for each item.
- **Navigation Bar:** Fixed bottom position, white background, subtle top-only shadow. Clean line icons with labels in `label-sm` typography.

### Icons
- Use thin-stroke line icons (2px stroke). Avoid filled icons unless indicating an active state in the navigation bar. Use Slate Gray for inactive and Brand Blue for active states.