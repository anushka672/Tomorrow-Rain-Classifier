# Design System Specification: Editorial Trust & Organic Growth

This design system is engineered to move beyond the utilitarian "dashboard" aesthetic. For an NGO-focused platform, we must balance institutional authority with the warmth of community. Our approach rejects the rigid, "boxed-in" layout of traditional SaaS in favor of **Tonal Layering** and **Asymmetric Breathing Room**. 

We do not just display data; we curate stories of impact.

---

### 1. Overview & Creative North Star: "The Living Archive"

The Creative North Star for this system is **The Living Archive**. 

Unlike standard platforms that feel static and cold, this system should feel like a premium, high-end editorial publication—one that is alive and evolving. We achieve this by:
*   **Intentional Asymmetry:** Breaking the 12-column grid with staggered content blocks to create a sense of human touch.
*   **Depth through Tone:** Replacing harsh borders with soft shifts in background values.
*   **Typographic Authority:** Using oversized, high-contrast display type to guide the eye and signal importance.

---

### 2. Colors & Surface Architecture

The palette is rooted in deep forest greens (`primary: #004f45`) and airy aquatic teals (`secondary: #006b5f`), creating a spectrum of "Growth."

#### The "No-Line" Rule
**Explicit Instruction:** Do not use 1px solid borders to define sections. Layout boundaries must be established solely through background color shifts or whitespace. 
*   *Example:* A `surface-container-low` (`#e6f6ff`) sidebar sitting against a `surface` (`#f3faff`) main canvas.

#### Surface Hierarchy & Nesting
Treat the UI as a series of stacked, semi-translucent sheets. 
*   **Base:** `surface` (#f3faff)
*   **Sectioning:** `surface-container-low` (#e6f6ff) or `surface-container` (#dbf1fe)
*   **Emphasis (Cards/Popovers):** `surface-container-highest` (#cfe6f2) or `surface-container-lowest` (#ffffff) for maximum lift.

#### The "Glass & Gradient" Rule
To add "soul" to the platform:
*   **Main CTAs:** Use a subtle linear gradient from `primary` (#004f45) to `primary_container` (#00695c) at a 135° angle.
*   **Floating Navigation:** Apply `surface_container_lowest` with a 12px `backdrop-blur` and 80% opacity to create a sophisticated glassmorphism effect.

---

### 3. Typography: Editorial Authority

We use a duo-font system to balance character with readability.

*   **Display & Headlines (Manrope):** Chosen for its geometric precision and modern warmth. Use `display-lg` (3.5rem) for hero impact statements. Headlines should always use a tighter letter-spacing (-0.02em) to feel "locked" and professional.
*   **Body & Labels (Inter):** The workhorse for high-trust data. Inter provides exceptional legibility at small scales. 
*   **The Hierarchy of Trust:** Use `title-lg` (#071e27) for section headers and `body-md` (#3e4946) for descriptive text to create a clear, accessible reading path.

---

### 4. Elevation & Depth: Tonal Layering

Traditional drop shadows are often too "heavy" for a clean NGO aesthetic. Instead, we use **Tonal Layering**.

*   **The Layering Principle:** Depth is achieved by placing a lighter surface on a darker one. Place a `surface-container-lowest` card on a `surface-container-low` background to create a "natural lift."
*   **Ambient Shadows:** If a shadow is required (e.g., for a modal), use a highly diffused shadow: `0px 24px 48px rgba(7, 30, 39, 0.06)`. Note that the shadow is tinted with the `on_surface` color, not pure black.
*   **The "Ghost Border" Fallback:** If accessibility requires a stroke (e.g., in high-contrast mode), use `outline_variant` (#bec9c5) at **20% opacity**. Never use a 100% opaque border.

---

### 5. Component Guidelines

#### Buttons & Action Elements
*   **Primary:** Uses the Primary-to-Container gradient. Corner radius: `xl` (0.75rem).
*   **Secondary:** Ghost style using `on_secondary_container` text. No border—interaction is signaled via a subtle `surface_container_high` background fill on hover.

#### Status Badges & Progress Steppers
*   **Badges:** Use a "Soft Fill" approach. A `success` badge should use `primary_fixed` (#a0f2e1) as a background with `on_primary_fixed_variant` (#005046) text. Avoid harsh red/green vibrations.
*   **Steppers:** Use thin, 2px tracks using `outline_variant`. Active states should use a `secondary` (#006b5f) glow effect rather than a solid block.

#### Input Fields
*   **Layout:** Labels (`label-md`) must always be top-aligned with `spacing-2` (0.5rem) padding.
*   **State:** Use `surface_container_low` as the default fill. Upon focus, transition the background to `surface_container_lowest` and add a 2px "Ghost Border" in `primary`.

#### Data Visualization & Cards
*   **Forbid Dividers:** Do not use lines to separate list items. Use `spacing-4` (1rem) of vertical whitespace or a subtle background toggle between `surface_container_low` and `surface_container_lowest`.
*   **Visual Soul:** Data charts should utilize the full teal/green spectrum, using `tertiary` (#004f49) for baseline data and `primary` for "Impact" metrics.

---

### 6. Do’s and Don’ts

#### Do:
*   **Embrace Whitespace:** Use `spacing-12` (3rem) and `spacing-16` (4rem) between major sections to let the content breathe.
*   **Layer Surfaces:** Use `surface_container` tiers to group related content instead of drawing boxes around them.
*   **Mix Typography:** Pair a `display-sm` Manrope headline with an `inter` body-lg lead-in paragraph for an editorial feel.

#### Don’t:
*   **No "Box-Shadow" Abuse:** Never use standard CSS shadows; only the Ambient Shadow defined in Section 4.
*   **No Pure Black:** Ensure all "dark" text uses `on_surface` (#071e27) for a softer, more premium contrast.
*   **No Grid-Rigidity:** Avoid filling every column. Use offset margins (e.g., `spacing-20`) to create asymmetric focus points for important NGO stories.

---

### 7. Implementation Note for Junior Designers
When in doubt, simplify. This system relies on the quality of the typography and the subtle shifts in the green/teal palette. If a screen feels "cluttered," remove a line and add 1rem of spacing. High-trust design is found in the gaps between the elements, not just the elements themselves.