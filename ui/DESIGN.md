---
name: Luminous Finance
colors:
  surface: '#f8f9fa'
  surface-dim: '#d9dadb'
  surface-bright: '#f8f9fa'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f3f4f5'
  surface-container: '#edeeef'
  surface-container-high: '#e7e8e9'
  surface-container-highest: '#e1e3e4'
  on-surface: '#191c1d'
  on-surface-variant: '#3c4a43'
  inverse-surface: '#2e3132'
  inverse-on-surface: '#f0f1f2'
  outline: '#6b7b72'
  outline-variant: '#bacac1'
  surface-tint: '#006c4f'
  primary: '#006c4f'
  on-primary: '#ffffff'
  primary-container: '#00d09c'
  on-primary-container: '#00533c'
  inverse-primary: '#2fe0aa'
  secondary: '#5f5e5e'
  on-secondary: '#ffffff'
  secondary-container: '#e5e2e1'
  on-secondary-container: '#656464'
  tertiary: '#5e5e5e'
  on-tertiary: '#ffffff'
  tertiary-container: '#b8b7b7'
  on-tertiary-container: '#484848'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#59fdc5'
  primary-fixed-dim: '#2fe0aa'
  on-primary-fixed: '#002116'
  on-primary-fixed-variant: '#00513b'
  secondary-fixed: '#e5e2e1'
  secondary-fixed-dim: '#c8c6c5'
  on-secondary-fixed: '#1c1b1b'
  on-secondary-fixed-variant: '#474646'
  tertiary-fixed: '#e3e2e2'
  tertiary-fixed-dim: '#c7c6c6'
  on-tertiary-fixed: '#1b1c1c'
  on-tertiary-fixed-variant: '#464747'
  background: '#f8f9fa'
  on-background: '#191c1d'
  surface-variant: '#e1e3e4'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-md:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
    letterSpacing: 0.01em
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  container-max: 1280px
  sidebar-width: 320px
  chat-max-width: 800px
  gutter: 24px
  margin-mobile: 16px
  margin-desktop: 40px
  stack-gap: 12px
---

## Brand & Style
The design system focuses on a premium, trust-oriented experience for mutual fund exploration. It targets both novice and seasoned investors who value clarity, speed, and precision. The aesthetic is strictly minimalist, utilizing a distraction-free environment that prioritizes information architecture over decorative elements.

By leveraging a "soft-utilitarian" approach, the UI evokes a sense of security and modern sophistication. It draws heavily from modern minimalism, featuring heavy whitespace and high-quality typography to ensure that complex financial data feels approachable and easy to digest.

## Colors
The palette is anchored by the signature primary teal, used strategically for primary actions, success states, and brand highlights. To maintain a premium feel, the secondary color is a deep, near-black neutral used for high-contrast typography.

The background utilizes a soft neutral off-white to reduce eye strain during long reading sessions. A specific warning accent is reserved for regulatory disclaimers and risk disclosures, ensuring they are prominent without breaking the clean aesthetic.

## Typography
Inter is used exclusively to maintain a systematic and functional tone. The hierarchy is designed for high readability in a chat-based Q&A format. 

Headlines use tighter letter spacing and heavier weights to provide strong visual anchors. Body text is set with generous line heights to facilitate comfortable reading of long-form financial explanations. Labels use medium weights and slight tracking for clarity in navigation and metadata.

## Layout & Spacing
The layout employs a fixed-sidebar model for navigation and history, with a centralized fluid chat interface. The content is centered to reduce horizontal eye movement, creating a focused "reading lane."

- **Desktop:** A 12-column grid is used within the main content area. The sidebar is fixed to the left, while the chat window occupies the center 8 columns.
- **Tablet:** The sidebar collapses into a drawer, and margins are reduced to 24px.
- **Mobile:** A single-column layout with 16px margins. The chat interface fills the full width to maximize readability.
- **Spacing Rhythm:** All spacing follows an 8px base grid to ensure consistent alignment and vertical rhythm.

## Elevation & Depth
The design system avoids heavy shadows, opting instead for **Tonal Layers** and **Low-contrast outlines**.

1.  **Level 0 (Background):** The primary page background.
2.  **Level 1 (Cards/Sidebar):** Pure white surfaces with a subtle 1px border (#E5E7EB).
3.  **Level 2 (Chat Bubbles/Popovers):** Slight elevation using a very soft, diffused ambient shadow (0px 4px 20px rgba(0, 0, 0, 0.04)) to distinguish active elements from the background.
4.  **Interactive States:** Elements slightly lift or change border-color to the primary teal when hovered, providing tactile feedback without visual clutter.

## Shapes
The design system utilizes a generous corner radius to feel approachable and modern. 
- **Standard UI Elements:** Use `rounded-lg` (16px) for cards and input groups.
- **Chat Bubbles:** Use a variable radius—large corners (24px) on most sides, with a sharper corner (4px) on the origin side to indicate the speaker.
- **Buttons & Pills:** Use `rounded-xl` (24px) or full pill shapes to create a friendly, "tap-friendly" appearance.

## Components
- **Chat Bubbles:** User bubbles are high-contrast (Primary Teal background, white text); assistant bubbles are low-contrast (Neutral background, dark text). Both feature 24px rounded corners.
- **Action Pills:** Primary buttons are pill-shaped with the brand teal. Ghost buttons use a subtle border and no fill for secondary actions like "View Source."
- **Input Field:** A prominent, wide search/input bar at the bottom of the chat, featuring a soft shadow and 16px corner radius.
- **Warning Banner:** Fixed-width component with a light amber background (#FFFBEB) and a bold left-border. Used for mandatory mutual fund risk disclaimers.
- **History List:** Clean, text-only list items in the sidebar with a vertical "active" indicator line in the primary teal.
- **Cards:** Used for fund summaries or FAQ categories, featuring a 1px border and 16px corner radius.