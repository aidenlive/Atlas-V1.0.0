---
version: 1.0
name: Neue
description: >-
  Neue is a monochrome, editorial system for products that are read as much as
  they are used: long-form publishing, design-system reference, and the tool
  surfaces around them. Its material thesis is paper and hairline: flat
  achromatic surfaces separated by 1px rules rather than shadow, with elevation
  reserved for things that have genuinely left the page. Its typographic thesis
  is one voice at two temperaments: a single geometric sans (DM Sans) at weight
  400/500 only carrying every reading and interface role, and a monospace
  (JetBrains Mono) marking everything machine-authored: section numbers, token
  names, code. Color is achromatic by default; chroma appears only where it
  carries meaning (status, syntax, data series). Its structural thesis is that
  every layout decision is measured against the space a region was given, never
  against the device it is running on. All base token values in this file are
  the LIGHT theme; `themes.dark` overrides by role.

# =============================================================================
# ramps: extension group. 11-step OKLCH ramps per the org color standard.
# Shade meanings are fixed: 50 soft bg · 100 subtle fill · 200 interactive bg ·
# 300 border · 400 muted accent · 500 canonical · 600 hover · 700 active ·
# 800 high emphasis · 900 strong contrast · 950 maximum depth.
# Components NEVER reference a ramp. Ramps exist so the semantic layer has a
# principled source and so a re-theme is a ramp swap, not a hunt.
# (Named `ramps`, not `palettes`, because `palettes` is a reserved group in the
# DESIGN.md format with different semantics: see Assumptions.)
# =============================================================================
ramps:
  neutral-0:     "oklch(1 0 0)"
  neutral-50:    "oklch(0.985 0 0)"
  neutral-100:   "oklch(0.97 0 0)"
  neutral-200:   "oklch(0.94 0 0)"
  neutral-300:   "oklch(0.89 0 0)"
  neutral-400:   "oklch(0.76 0 0)"
  neutral-500:   "oklch(0.62 0 0)"
  neutral-600:   "oklch(0.52 0 0)"
  neutral-700:   "oklch(0.44 0 0)"
  neutral-800:   "oklch(0.32 0 0)"
  neutral-900:   "oklch(0.18 0 0)"
  neutral-950:   "oklch(0.11 0 0)"

  red-50:        "oklch(0.97 0.014 25)"
  red-100:       "oklch(0.94 0.030 25)"
  red-200:       "oklch(0.88 0.060 25)"
  red-300:       "oklch(0.80 0.100 25)"
  red-400:       "oklch(0.68 0.160 25)"
  red-500:       "oklch(0.58 0.200 25)"
  red-600:       "oklch(0.52 0.200 25)"
  red-700:       "oklch(0.46 0.180 25)"
  red-800:       "oklch(0.39 0.150 25)"
  red-900:       "oklch(0.32 0.120 25)"
  red-950:       "oklch(0.22 0.080 25)"

  amber-50:      "oklch(0.97 0.020 75)"
  amber-100:     "oklch(0.95 0.040 75)"
  amber-200:     "oklch(0.90 0.070 75)"
  amber-300:     "oklch(0.83 0.100 75)"
  amber-400:     "oklch(0.72 0.120 75)"
  amber-500:     "oklch(0.62 0.120 75)"
  amber-600:     "oklch(0.50 0.110 75)"
  amber-700:     "oklch(0.44 0.100 75)"
  amber-800:     "oklch(0.37 0.085 75)"
  amber-900:     "oklch(0.30 0.070 75)"
  amber-950:     "oklch(0.21 0.050 75)"

  green-50:      "oklch(0.97 0.018 150)"
  green-100:     "oklch(0.94 0.036 150)"
  green-200:     "oklch(0.89 0.065 150)"
  green-300:     "oklch(0.81 0.095 150)"
  green-400:     "oklch(0.70 0.125 150)"
  green-500:     "oklch(0.60 0.135 150)"
  green-600:     "oklch(0.50 0.130 150)"
  green-700:     "oklch(0.43 0.115 150)"
  green-800:     "oklch(0.36 0.095 150)"
  green-900:     "oklch(0.29 0.075 150)"
  green-950:     "oklch(0.20 0.055 150)"

  blue-50:       "oklch(0.97 0.018 250)"
  blue-100:      "oklch(0.94 0.038 250)"
  blue-200:      "oklch(0.88 0.070 250)"
  blue-300:      "oklch(0.80 0.110 250)"
  blue-400:      "oklch(0.68 0.150 250)"
  blue-500:      "oklch(0.58 0.170 250)"
  blue-600:      "oklch(0.50 0.160 250)"
  blue-700:      "oklch(0.44 0.145 250)"
  blue-800:      "oklch(0.37 0.120 250)"
  blue-900:      "oklch(0.30 0.095 250)"
  blue-950:      "oklch(0.21 0.070 250)"

  # Categorical series for data visualisation. Hues are spaced around the wheel
  # and every entry is tuned to clear 3:1 against both page surfaces in both
  # themes, so a series color is legible as a 2px line, not only as a fill.
  indigo-50: oklch(0.97 0.017 275)
  indigo-100: oklch(0.94 0.037 275)
  indigo-200: oklch(0.88 0.068 275)
  indigo-300: oklch(0.80 0.107 275)
  indigo-400: oklch(0.68 0.146 275)
  indigo-500: oklch(0.58 0.165 275)
  indigo-600: oklch(0.50 0.155 275)
  indigo-700: oklch(0.44 0.141 275)
  indigo-800: oklch(0.37 0.116 275)
  indigo-900: oklch(0.30 0.092 275)
  indigo-950: oklch(0.21 0.068 275)
  violet-50: oklch(0.97 0.018 300)
  violet-100: oklch(0.94 0.038 300)
  violet-200: oklch(0.88 0.070 300)
  violet-300: oklch(0.80 0.110 300)
  violet-400: oklch(0.68 0.150 300)
  violet-500: oklch(0.58 0.170 300)
  violet-600: oklch(0.50 0.160 300)
  violet-700: oklch(0.44 0.145 300)
  violet-800: oklch(0.37 0.120 300)
  violet-900: oklch(0.30 0.095 300)
  violet-950: oklch(0.21 0.070 300)
  teal-50: oklch(0.97 0.012 185)
  teal-100: oklch(0.94 0.025 185)
  teal-200: oklch(0.88 0.045 185)
  teal-300: oklch(0.80 0.071 185)
  teal-400: oklch(0.68 0.097 185)
  teal-500: oklch(0.58 0.110 185)
  teal-600: oklch(0.50 0.104 185)
  teal-700: oklch(0.44 0.094 185)
  teal-800: oklch(0.37 0.078 185)
  teal-900: oklch(0.30 0.061 185)
  teal-950: oklch(0.21 0.045 185)
  cyan-50: oklch(0.97 0.014 215)
  cyan-100: oklch(0.94 0.029 215)
  cyan-200: oklch(0.88 0.054 215)
  cyan-300: oklch(0.80 0.084 215)
  cyan-400: oklch(0.68 0.115 215)
  cyan-500: oklch(0.58 0.130 215)
  cyan-600: oklch(0.50 0.122 215)
  cyan-700: oklch(0.44 0.111 215)
  cyan-800: oklch(0.37 0.092 215)
  cyan-900: oklch(0.30 0.073 215)
  cyan-950: oklch(0.21 0.054 215)
  orange-50: oklch(0.97 0.016 50)
  orange-100: oklch(0.94 0.035 50)
  orange-200: oklch(0.88 0.064 50)
  orange-300: oklch(0.80 0.100 50)
  orange-400: oklch(0.68 0.137 50)
  orange-500: oklch(0.58 0.155 50)
  orange-600: oklch(0.50 0.146 50)
  orange-700: oklch(0.44 0.132 50)
  orange-800: oklch(0.37 0.109 50)
  orange-900: oklch(0.30 0.087 50)
  orange-950: oklch(0.21 0.064 50)
  pink-50: oklch(0.97 0.017 350)
  pink-100: oklch(0.94 0.037 350)
  pink-200: oklch(0.88 0.068 350)
  pink-300: oklch(0.80 0.107 350)
  pink-400: oklch(0.68 0.146 350)
  pink-500: oklch(0.58 0.165 350)
  pink-600: oklch(0.50 0.155 350)
  pink-700: oklch(0.44 0.141 350)
  pink-800: oklch(0.37 0.116 350)
  pink-900: oklch(0.30 0.092 350)
  pink-950: oklch(0.21 0.068 350)
  viz-1:         "oklch(0.55 0.160 250)"
  viz-2:         "oklch(0.58 0.145 150)"
  viz-3:         "oklch(0.58 0.180 25)"
  viz-4:         "oklch(0.60 0.125 75)"
  viz-5:         "oklch(0.55 0.170 305)"
  viz-6:         "oklch(0.60 0.110 195)"
  viz-7:         "oklch(0.52 0.140 335)"
  viz-8:         "oklch(0.62 0.130 115)"

colors:
  # ---- brand / action ------------------------------------------------------
  primary:            "oklch(0.18 0 0)"      # near-black; the single action color
  primary-hover:      "oklch(0.28 0 0)"
  primary-active:     "oklch(0.12 0 0)"
  on-primary:         "oklch(0.98 0 0)"

  # ---- surfaces (ordinal, not semantic-depth) ------------------------------
  background:         "oklch(0.965 0 0)"     # page field
  surface:            "oklch(1 0 0)"         # cards, nav islands, inputs, menus
  surface-2:          "oklch(0.98 0 0)"      # recessed wells, code, table zebra
  surface-3:          "oklch(0.95 0 0)"      # tracks, disabled fills, skeletons

  # ---- ink -----------------------------------------------------------------
  on-surface:         "oklch(0.18 0 0)"      # primary text
  on-surface-2:       "oklch(0.38 0 0)"      # secondary text, deks
  on-surface-3:       "oklch(0.52 0 0)"      # muted labels, captions, placeholders
  on-background:      "{colors.on-surface}"

  # ---- lines ---------------------------------------------------------------
  outline:            "oklch(0.92 0 0)"      # decorative hairline (non-essential)
  outline-soft:       "oklch(0.95 0 0)"      # internal dividers
  outline-strong:     "oklch(0.62 0 0)"      # boundary of an interactive control (>=3:1)

  # ---- focus + scrims ------------------------------------------------------
  focus:              "{colors.primary}"     # focus indicator color
  focus-offset:       "{colors.surface}"     # gap color between control and ring
  focus-halo:         "oklch(0.18 0 0 / 0.16)"   # forced-colors fallback only
  scrim:              "oklch(0.18 0 0 / 0.05)"   # hover wash on ghost controls
  scrim-strong:       "oklch(0.18 0 0 / 0.09)"   # active wash
  overlay:            "oklch(0.14 0 0 / 0.44)"   # modal / drawer / sheet backdrop
  fade:               "oklch(1 0 0 / 0)"         # transparent end of a scroll-edge fade

  # ---- status (text- and icon-safe on surface..surface-3) ------------------
  error:              "oklch(0.52 0.20 25)"
  success:            "oklch(0.50 0.13 150)"
  warning:            "oklch(0.50 0.11 75)"
  info:               "oklch(0.50 0.16 250)"
  error-surface:      "oklch(0.96 0.02 25)"
  success-surface:    "oklch(0.96 0.02 150)"
  warning-surface:    "oklch(0.96 0.03 75)"
  info-surface:       "oklch(0.96 0.02 250)"

  # ---- code / syntax (all >=4.5:1 on `code-surface`) -----------------------
  # --- content accents -------------------------------------------------------
  # One hue per DOMAIN of content, not per component. The same accent marks a
  # standard in the sidebar, on its page eyebrow, in its badge, and on its tag,
  # so a reader learns the mapping once and it holds everywhere.
  #
  # Chroma stays out of structure. These never tint a surface, a rule, or a
  # navigation rail; they colour a 2px marker, a glyph, or text on a tinted
  # chip. The interface remains achromatic and the accent remains information.
  accent-spec: "{ramps.indigo-600}"
  accent-spec-soft: "{ramps.indigo-50}"
  accent-spec-line: "{ramps.indigo-200}"
  accent-work: "{ramps.blue-600}"
  accent-work-soft: "{ramps.blue-50}"
  accent-work-line: "{ramps.blue-200}"
  accent-docs: "{ramps.teal-600}"
  accent-docs-soft: "{ramps.teal-50}"
  accent-docs-line: "{ramps.teal-200}"
  accent-library: "{ramps.amber-700}"
  accent-library-soft: "{ramps.amber-50}"
  accent-library-line: "{ramps.amber-200}"
  accent-cli: "{ramps.violet-600}"
  accent-cli-soft: "{ramps.violet-50}"
  accent-cli-line: "{ramps.violet-200}"
  # --- tags ------------------------------------------------------------------
  # A tag is a chip: soft tinted ground, saturated text, hairline of the same
  # hue. Never a solid fill, which would compete with a status pill.
  tag-ink: "{colors.on-surface-2}"
  tag-surface: "{colors.surface-2}"
  tag-line: "{colors.outline}"
  code-surface:       "{colors.surface-2}"
  code-gutter:        "oklch(0.52 0 0)"
  code-plain:         "oklch(0.28 0 0)"
  code-comment:       "oklch(0.52 0 0)"
  code-keyword:       "oklch(0.45 0.19 300)"
  code-string:        "oklch(0.45 0.13 150)"
  code-number:        "oklch(0.48 0.15 45)"
  code-function:      "oklch(0.45 0.17 255)"
  code-attr:          "oklch(0.48 0.14 80)"
  code-tag:           "oklch(0.48 0.19 20)"
  code-punctuation:   "oklch(0.55 0 0)"
  code-added:         "oklch(0.48 0.14 150)"
  code-removed:       "oklch(0.52 0.20 25)"
  code-highlight:     "oklch(0.18 0 0 / 0.06)"

  # ---- data visualisation --------------------------------------------------
  # Series roles. Charts read these, never `ramps.viz-*` directly, so a product
  # can re-map the series order without touching a chart config.
  series-1:           "{ramps.viz-1}"
  series-2:           "{ramps.viz-2}"
  series-3:           "{ramps.viz-3}"
  series-4:           "{ramps.viz-4}"
  series-5:           "{ramps.viz-5}"
  series-6:           "{ramps.viz-6}"
  series-7:           "{ramps.viz-7}"
  series-8:           "{ramps.viz-8}"
  chart-grid:         "oklch(0.92 0 0)"      # gridlines: decorative, not a boundary
  chart-axis:         "oklch(0.62 0 0)"      # axis rule and ticks (>=3:1)
  chart-label:        "oklch(0.52 0 0)"      # axis labels (>=4.5:1)
  chart-track:        "oklch(0.94 0 0)"      # the unfilled part of a bar or gauge
  chart-tooltip:      "oklch(0.18 0 0)"      # tooltip surface (inverted)
  on-chart-tooltip:   "oklch(0.98 0 0)"

  # ---- org standard aliases ------------------------------------------------
  # The org color standard names surfaces and text differently from this
  # system. Both vocabularies point at the same values; neither is a second
  # source of truth. Neue components use the names above; org tooling uses these.
  border:             "{colors.outline}"
  text:               "{colors.on-surface}"
  text-secondary:     "{colors.on-surface-2}"
  text-muted:         "{colors.on-surface-3}"

typography:
  headline-display:
    fontFamily: "DM Sans"
    fontSize: "56px"          # fluid: clamp(36px, 8vw, 56px): ceiling recorded
    fontWeight: 500
    lineHeight: 1.05
    letterSpacing: "-0.025em"
  headline-lg:
    fontFamily: "DM Sans"
    fontSize: "44px"          # fluid: clamp(32px, 6vw, 44px)
    fontWeight: 500
    lineHeight: 1.1
    letterSpacing: "-0.025em"
  headline-md:
    fontFamily: "DM Sans"
    fontSize: "32px"          # fluid: clamp(26px, 4vw, 32px)
    fontWeight: 500
    lineHeight: 1.15
    letterSpacing: "-0.015em"
  headline-sm:
    fontFamily: "DM Sans"
    fontSize: "22px"
    fontWeight: 500
    lineHeight: 1.25
    letterSpacing: "-0.015em"
  headline-xs:
    fontFamily: "DM Sans"
    fontSize: "18px"
    fontWeight: 500
    lineHeight: 1.3
    letterSpacing: "-0.015em"
  body-lg:
    fontFamily: "DM Sans"
    fontSize: "18px"
    fontWeight: 400
    lineHeight: 1.55
    letterSpacing: "-0.015em"
  body-md:
    fontFamily: "DM Sans"
    fontSize: "17px"
    fontWeight: 400
    lineHeight: 1.7
    letterSpacing: "0em"
  body-sm:
    fontFamily: "DM Sans"
    fontSize: "15px"
    fontWeight: 400
    lineHeight: 1.55
    letterSpacing: "0em"
  body-xs:
    fontFamily: "DM Sans"
    fontSize: "14px"
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: "0em"
  label-lg:
    fontFamily: "DM Sans"
    fontSize: "15px"
    fontWeight: 500
    lineHeight: 1.2
    letterSpacing: "0em"
  label-md:
    fontFamily: "DM Sans"
    fontSize: "14px"
    fontWeight: 500
    lineHeight: 1.2
    letterSpacing: "0em"
  label-sm:
    fontFamily: "DM Sans"
    fontSize: "13px"
    fontWeight: 500
    lineHeight: 1.2
    letterSpacing: "0em"
  caption-md:
    fontFamily: "DM Sans"
    fontSize: "12px"
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: "0.06em"
  mono-md:
    fontFamily: "JetBrains Mono"
    fontSize: "13px"
    fontWeight: 400
    lineHeight: 1.65
    letterSpacing: "0em"
  mono-sm:
    fontFamily: "JetBrains Mono"
    fontSize: "12px"
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: "0.06em"
  mono-xs:
    fontFamily: "JetBrains Mono"
    fontSize: "11px"
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: "0.06em"

spacing:
  # ---- 4px rhythm scale (ordinal, non-linear above s-6) --------------------
  s-1:  "4px"
  s-2:  "8px"
  s-3:  "12px"
  s-4:  "16px"
  s-5:  "20px"
  s-6:  "24px"
  s-7:  "32px"
  s-8:  "40px"
  s-9:  "48px"
  s-10: "64px"
  s-11: "80px"
  s-12: "112px"

  # ---- page metrics --------------------------------------------------------
  gutter:           "{spacing.s-4}"   # page inline padding, base
  gutter-md:        "{spacing.s-6}"   # page inline padding, >= sm
  gutter-lg:        "{spacing.s-7}"   # page inline padding, >= lg

  # ---- containers ----------------------------------------------------------
  content:          "780px"    # reading column: prose, forms, single-column demos
  wide:             "1120px"   # break-out: galleries, wide tables, image rows
  rail:             "248px"    # BOTH shell rails: one token, so they cannot drift
  rail-min:         "148px"    # rail floor before the third track is withdrawn
  shell:            "1468px"   # derived: content + 2*rail + 2*s-10 + 2*gutter-lg
  surface-max:      "1280px"   # working-surface cap in an app shell
  surface-max-wide: "1600px"   # dashboards, galleries, boards
  region-min:       "280px"    # a docked region below this width is withdrawn

  # ---- reading measures (follow the font, not the screen) ------------------
  measure-narrow:   "44ch"     # leads, empty states, callout bodies
  measure:          "72ch"     # hard cap on prose line length
  measure-wide:     "88ch"     # tables, code, log output

  # ---- chrome --------------------------------------------------------------
  nav-top:          "12px"     # float gap from the top of the viewport
  nav-h:            "56px"     # navigation island height
  nav-stack:        "80px"     # derived: nav-top + nav-h + nav-top
  scroll-offset:    "112px"    # derived: nav-stack + s-7. Anchor offset AND rail pin.

  # ---- control metrics -----------------------------------------------------
  control-h-sm:     "36px"
  control-h:        "44px"     # default button height
  control-h-lg:     "52px"
  field-h:          "48px"     # text input height
  hairline:         "1px"      # the only rule weight in the system

  # ---- pointer targets (read the pointer, not the platform) ----------------
  target-fine:      "28px"     # mouse, trackpad, stylus: dense pointer-only surfaces
  target-coarse:    "44px"     # finger: the system-wide default floor
  target-remote:    "56px"     # directional pad

  # ---- icon sizes ----------------------------------------------------------
  icon-xs:          "16px"     # button-sm, pills, inline chips
  icon-sm:          "18px"     # callouts, list rows
  icon-md:          "20px"     # default button, form controls
  icon-lg:          "22px"     # navigation islands
  icon-xl:          "24px"     # standalone, toolbar
  icon-2xl:         "32px"     # empty states

rounded:
  none: "0px"
  xs:   "6px"
  sm:   "10px"
  md:   "16px"
  lg:   "24px"
  xl:   "32px"
  pill: "999px"
  full: "50%"

elevation:
  # Extension group. Each key is an elevation TIER; `components.*.shadow` names a
  # tier, never a raw shadow. Tiers are documented in "Elevation & Depth".
  flat:    "none"
  raised:  "0 1px 2px oklch(0.18 0 0 / 0.04), 0 2px 8px oklch(0.18 0 0 / 0.04)"
  float:   "0 2px 6px oklch(0.18 0 0 / 0.05), 0 12px 28px oklch(0.18 0 0 / 0.07)"
  popover: "0 4px 10px oklch(0.18 0 0 / 0.06), 0 18px 42px oklch(0.18 0 0 / 0.10)"
  modal:   "0 8px 20px oklch(0.18 0 0 / 0.08), 0 36px 72px oklch(0.18 0 0 / 0.16)"

motion:
  ease:             "cubic-bezier(0.22, 1, 0.36, 1)"
  ease-out:         "cubic-bezier(0.16, 1, 0.3, 1)"
  ease-in-out:      "cubic-bezier(0.65, 0, 0.35, 1)"
  ease-spring:      "cubic-bezier(0.34, 1.4, 0.64, 1)"
  duration-instant: "90ms"
  duration-fast:    "180ms"
  duration-normal:  "280ms"
  duration-slow:    "520ms"
  duration-theme:   "280ms"
  stagger-step:     "60ms"

breakpoints:
  # VIEWPORT thresholds. Govern presentation: fluid type ceilings, page gutters,
  # gallery column counts, page-level chrome. Never used for region structure.
  xs:   "480px"
  sm:   "560px"
  md:   "768px"
  lg:   "1024px"
  xl:   "1280px"
  "2xl": "1536px"

sizeClasses:
  # CONTAINER thresholds, resolved from the width of the region itself.
  # Govern structure: how many panes, where navigation lives, whether a docked
  # region survives. Never used for type or page gutters. See "The two axes".
  compact:   "0px"
  medium:    "600px"
  expanded:  "905px"
  large:     "1280px"
  xlarge:    "1920px"

grid:
  # Fluid column grid, stepped by size class. Extension group.
  columns:
    compact: 4
    medium: 8
    expanded: 12
    large: 12
    xlarge: 12
  gutter:
    compact: "{spacing.s-4}"
    medium: "{spacing.s-5}"
    expanded: "{spacing.s-6}"
    large: "{spacing.s-6}"
    xlarge: "{spacing.s-7}"
  margin:
    compact: "{spacing.s-4}"
    medium: "{spacing.s-6}"
    expanded: "{spacing.s-7}"
    large: "{spacing.s-8}"
    xlarge: "{spacing.s-10}"

regions:
  # The seven named regions any shell is assembled from. Extension group.
  # `priority` resolves contention: when docked widths exceed the space
  # available, regions release in ascending priority order.
  banner:
    role: banner
    edge: top
    height: "{spacing.s-8}"
    priority: 10
  navigation:
    role: navigation
    edge:
      compact: bottom
      medium: start
      expanded: start
      large: start
      xlarge: start
    height:
      compact: "{spacing.nav-h}"
    width:
      medium: "80px"
      expanded: "80px"
      large: "80px"
      xlarge: "280px"
    min: "80px"
    max: "280px"
    priority: 90
  toolbar:
    role: toolbar
    edge: top
    height: "{spacing.s-10}"
    priority: 80
  content:
    role: main
    edge: fill
    min: "{spacing.region-min}"
    max: "{spacing.surface-max}"
    priority: 100
  panel:
    role: complementary
    edge: start
    width: "320px"
    min: "240px"
    max: "480px"
    priority: 60
  inspector:
    role: complementary
    edge: end
    width: "320px"
    min: "260px"
    max: "440px"
    priority: 40
  footer:
    role: contentinfo
    edge: bottom
    min: "{spacing.s-10}"
    priority: 20

adaptation:
  # The normative adaptation policy: data, not branching code, so it can be
  # inspected, diffed and proved equal across platforms. Values are rungs on the
  # ladder `docked -> inline -> overlay -> sheet -> hidden`, which only ever
  # runs one way as space shrinks.
  banner:
    compact: hidden
    medium: docked
    expanded: docked
    large: docked
    xlarge: docked
  navigation:
    compact: docked
    medium: docked
    expanded: docked
    large: docked
    xlarge: docked
  toolbar:
    compact: docked
    medium: docked
    expanded: docked
    large: docked
    xlarge: docked
  content:
    compact: docked
    medium: docked
    expanded: docked
    large: docked
    xlarge: docked
  panel:
    compact: sheet
    medium: overlay
    expanded: docked
    large: docked
    xlarge: docked
  inspector:
    compact: sheet
    medium: sheet
    expanded: overlay
    large: docked
    xlarge: docked
  footer:
    compact: docked
    medium: docked
    expanded: docked
    large: docked
    xlarge: docked

overflow:
  # Declared per region, never decided at render time.
  banner: collapse
  navigation: collapse
  toolbar: collapse
  content: scroll
  panel: scroll
  inspector: scroll
  footer: wrap

shells:
  # Named region sets. A shell is declared with one attribute; it is not new CSS.
  app:     [navigation, toolbar, content, inspector, footer]
  browse:  [navigation, panel, toolbar, content, footer]
  canvas:  [navigation, toolbar, content, panel, inspector]
  reading: [toolbar, content, inspector]
  site:    [banner, toolbar, content, footer]
  focus:   [content, panel]

primitives:
  # Layout primitives. They arrange their children and nothing else: no color,
  # no type, no self-positioning. Every knob is a custom property.
  container: { arranges: "one child, centered, with gutters",              knobs: [max, gutter] }
  stack:     { arranges: "children vertically",                            knobs: [gap, align] }
  row:       { arranges: "children horizontally, wrapping",                knobs: [gap, align, justify] }
  grid:      { arranges: "equal cells, count derived from a cell minimum", knobs: [min, gap] }
  columns:   { arranges: "cells on the fluid grid",                        knobs: [gap, span] }
  split:     { arranges: "aside plus content, stacking intrinsically",     knobs: [aside, threshold] }
  switcher:  { arranges: "equal peers, all across or all stacked",         knobs: [threshold] }
  frame:     { arranges: "one child, aspect-ratio crop",                   knobs: [ratio, fit] }
  center:    { arranges: "one child at a measure",                         knobs: [measure] }
  cover:     { arranges: "a principal child, filling",                     knobs: [minHeight] }
  scroller:  { arranges: "peers on one axis, with snap",                   knobs: [item, gap] }
  sticky:    { arranges: "one child, pinned",                              knobs: [top] }

density:
  # Multiplier on the spacing scale and control heights. Never on type size;
  # never below a pointer target floor. Results snap to 2px.
  compact:      0.875
  comfortable:  1
  spacious:     1.125

environment:
  safeArea: respect      # added to the page margin, never replacing it
  overscan: 0.045        # reserved per edge where no safe area is reported (TV)
  hinge: "32px"          # gutter reserved across a book-posture fold

themes:
  light:
    color-scheme: "light"      # base token values above already are the light theme
  dark:
    accent-spec: "{ramps.indigo-400}"
    accent-spec-soft: oklch(0.26 0.055 275)
    accent-spec-line: oklch(0.36 0.080 275)
    accent-work: "{ramps.blue-400}"
    accent-work-soft: oklch(0.26 0.055 250)
    accent-work-line: oklch(0.36 0.080 250)
    accent-docs: "{ramps.teal-400}"
    accent-docs-soft: oklch(0.25 0.040 185)
    accent-docs-line: oklch(0.35 0.055 185)
    accent-library: "{ramps.amber-400}"
    accent-library-soft: oklch(0.26 0.045 75)
    accent-library-line: oklch(0.36 0.060 75)
    accent-cli: "{ramps.violet-400}"
    accent-cli-soft: oklch(0.26 0.055 300)
    accent-cli-line: oklch(0.36 0.080 300)
    tag-ink: oklch(0.72 0 0)
    tag-surface: oklch(0.20 0 0)
    tag-line: oklch(0.30 0 0)
    color-scheme: "dark"
    primary:            "oklch(0.97 0 0)"
    primary-hover:      "oklch(0.90 0 0)"
    primary-active:     "oklch(1 0 0)"
    on-primary:         "oklch(0.17 0 0)"
    background:         "oklch(0.14 0 0)"
    surface:            "oklch(0.18 0 0)"
    surface-2:          "oklch(0.21 0 0)"
    surface-3:          "oklch(0.24 0 0)"
    on-surface:         "oklch(0.97 0 0)"
    on-surface-2:       "oklch(0.80 0 0)"
    on-surface-3:       "oklch(0.68 0 0)"
    outline:            "oklch(0.28 0 0)"
    outline-soft:       "oklch(0.24 0 0)"
    outline-strong:     "oklch(0.54 0 0)"
    focus-halo:         "oklch(0.97 0 0 / 0.20)"
    scrim:              "oklch(1 0 0 / 0.07)"
    scrim-strong:       "oklch(1 0 0 / 0.12)"
    overlay:            "oklch(0.08 0 0 / 0.64)"
    fade:               "oklch(0.18 0 0 / 0)"
    error:              "oklch(0.72 0.17 25)"
    success:            "oklch(0.78 0.16 150)"
    warning:            "oklch(0.83 0.13 75)"
    info:               "oklch(0.76 0.13 250)"
    error-surface:      "oklch(0.26 0.06 25)"
    success-surface:    "oklch(0.26 0.05 150)"
    warning-surface:    "oklch(0.26 0.05 75)"
    info-surface:       "oklch(0.26 0.05 250)"
    code-surface:       "oklch(0.16 0 0)"
    code-gutter:        "oklch(0.60 0 0)"
    code-plain:         "oklch(0.90 0 0)"
    code-comment:       "oklch(0.65 0 0)"
    code-keyword:       "oklch(0.78 0.14 300)"
    code-string:        "oklch(0.82 0.15 150)"
    code-number:        "oklch(0.83 0.13 60)"
    code-function:      "oklch(0.80 0.13 255)"
    code-attr:          "oklch(0.86 0.14 90)"
    code-tag:           "oklch(0.76 0.15 20)"
    code-punctuation:   "oklch(0.70 0 0)"
    code-added:         "oklch(0.80 0.15 150)"
    code-removed:       "oklch(0.75 0.16 25)"
    code-highlight:     "oklch(1 0 0 / 0.07)"
    # Data visualisation: chrome inverts; the series ramps do not, because a hue
    # that reads on both page surfaces reads on both themes.
    chart-grid:         "oklch(0.28 0 0)"
    chart-axis:         "oklch(0.54 0 0)"
    chart-label:        "oklch(0.72 0 0)"
    chart-track:        "oklch(0.26 0 0)"
    chart-tooltip:      "oklch(0.95 0 0)"
    on-chart-tooltip:   "oklch(0.18 0 0)"
    # Elevation is re-tuned for dark: a light-theme shadow over a dark surface
    # reads as haze, so the tiers tighten and borders carry more of the load.
    elevation-raised:   "0 1px 2px oklch(0 0 0 / 0.30)"
    elevation-float:    "0 4px 14px oklch(0 0 0 / 0.44)"
    elevation-popover:  "0 8px 24px oklch(0 0 0 / 0.52)"
    elevation-modal:    "0 24px 64px oklch(0 0 0 / 0.64)"

components:
  # ---- buttons -------------------------------------------------------------
  button:
    height: "{spacing.control-h}"
    padding: "0 {spacing.s-5}"
    rounded: "{rounded.pill}"
    typography: "{typography.label-lg}"
    gap: "{spacing.s-2}"
    borderWidth: "{spacing.hairline}"
    borderColor: "transparent"
    shadow: "flat"
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
  button-primary-hover:
    backgroundColor: "{colors.primary-hover}"
  button-primary-active: {}                     # transform-only: scale(0.97)
  button-primary-disabled:
    backgroundColor: "{colors.surface-3}"
    textColor: "{colors.on-surface-3}"
  button-secondary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
    borderColor: "{colors.outline-strong}"
  button-secondary-hover:
    backgroundColor: "{colors.surface-2}"
    borderColor: "{colors.primary}"
  button-ghost:
    backgroundColor: "transparent"
    textColor: "{colors.on-surface}"
  button-ghost-hover:
    backgroundColor: "{colors.scrim}"
  button-danger:
    backgroundColor: "{colors.error}"
    textColor: "oklch(1 0 0)"
  button-icon:
    width: "{spacing.control-h}"
    height: "{spacing.control-h}"
    padding: "0px"
    rounded: "{rounded.pill}"
    backgroundColor: "{colors.surface}"
    borderColor: "{colors.outline-strong}"
    textColor: "{colors.on-surface}"
  button-icon-sm:
    width: "{spacing.control-h-sm}"
    height: "{spacing.control-h-sm}"
  button-sm:
    height: "{spacing.control-h-sm}"
    padding: "0 {spacing.s-4}"
    typography: "{typography.label-md}"
  button-lg:
    height: "{spacing.control-h-lg}"
    padding: "0 {spacing.s-6}"

  # ---- navigation ----------------------------------------------------------
  nav-island:
    height: "{spacing.nav-h}"
    backgroundColor: "{colors.surface}"
    borderColor: "{colors.outline}"
    borderWidth: "{spacing.hairline}"
    rounded: "{rounded.pill}"
    padding: "{spacing.s-2}"
    gap: "{spacing.s-1}"
    shadow: "float"
  nav-island-scrolled:
    shadow: "popover"
  nav-link:
    height: "{spacing.control-h-sm}"
    padding: "0 {spacing.s-4}"
    rounded: "{rounded.pill}"
    typography: "{typography.label-sm}"
    textColor: "{colors.on-surface-2}"
  nav-link-hover:
    backgroundColor: "{colors.scrim}"
    textColor: "{colors.on-surface}"
  nav-link-current:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
  sidebar-link:
    height: "{spacing.control-h-sm}"
    padding: "0 {spacing.s-3}"
    rounded: "{rounded.sm}"
    typography: "{typography.body-xs}"
    textColor: "{colors.on-surface-2}"
  sidebar-link-current:
    backgroundColor: "{colors.surface-3}"
    textColor: "{colors.on-surface}"
  sidebar-group-label:
    typography: "{typography.mono-xs}"
    textColor: "{colors.on-surface-3}"
    padding: "{spacing.s-4} {spacing.s-3} {spacing.s-2}"
  breadcrumb:
    typography: "{typography.body-xs}"
    textColor: "{colors.on-surface-3}"
    gap: "{spacing.s-2}"
  breadcrumb-current:
    textColor: "{colors.on-surface}"
  drawer:
    width: "min(88vw, 380px)"
    backgroundColor: "{colors.surface}"
    borderColor: "{colors.outline}"
    padding: "{spacing.s-6} {spacing.s-5}"
    shadow: "modal"
  skip-link:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    padding: "{spacing.s-3} {spacing.s-5}"
    rounded: "{rounded.pill}"
    typography: "{typography.label-md}"
    shadow: "popover"
  tablist:
    gap: "{spacing.s-1}"
    borderColor: "{colors.outline}"
    borderWidth: "{spacing.hairline}"
  tab:
    height: "{spacing.control-h}"
    padding: "0 {spacing.s-4}"
    typography: "{typography.label-md}"
    textColor: "{colors.on-surface-2}"
    borderColor: "transparent"
    borderWidth: "2px"
  tab-selected:
    textColor: "{colors.on-surface}"
    borderColor: "{colors.primary}"

  # ---- form controls -------------------------------------------------------
  input:
    height: "{spacing.field-h}"
    padding: "0 {spacing.s-4}"
    rounded: "{rounded.md}"
    typography: "{typography.body-sm}"
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
    borderColor: "{colors.outline-strong}"
    borderWidth: "{spacing.hairline}"
  input-hover:
    borderColor: "{colors.on-surface-3}"
  input-focus: {}                               # ring only; the border does not change
  input-invalid:
    borderColor: "{colors.error}"
  input-disabled:
    backgroundColor: "{colors.surface-3}"
    textColor: "{colors.on-surface-3}"
  input-readonly:
    backgroundColor: "{colors.surface-2}"
  textarea:
    rounded: "{rounded.md}"
    padding: "{spacing.s-4} {spacing.s-5}"
    height: "auto"
    typography: "{typography.body-sm}"
  input-group:
    rounded: "{rounded.md}"
    padding: "{spacing.s-1}"
    gap: "{spacing.s-1}"
    backgroundColor: "{colors.surface}"
    borderColor: "{colors.outline-strong}"
    borderWidth: "{spacing.hairline}"
  field-label:
    typography: "{typography.label-md}"
    textColor: "{colors.on-surface}"
  field-hint:
    typography: "{typography.body-xs}"
    textColor: "{colors.on-surface-3}"
  field-error:
    typography: "{typography.body-xs}"
    textColor: "{colors.error}"
    gap: "{spacing.s-2}"
  checkbox:
    size: "20px"
    rounded: "{rounded.xs}"
    backgroundColor: "{colors.surface}"
    borderColor: "{colors.outline-strong}"
    borderWidth: "{spacing.hairline}"
  checkbox-checked:
    backgroundColor: "{colors.primary}"
    borderColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
  radio:
    size: "20px"
    rounded: "{rounded.full}"
    borderColor: "{colors.outline-strong}"
    borderWidth: "{spacing.hairline}"
  radio-checked:
    backgroundColor: "{colors.primary}"
    borderColor: "{colors.primary}"
  toggle-track:
    width: "44px"
    height: "26px"
    rounded: "{rounded.pill}"
    backgroundColor: "{colors.surface-3}"
    borderColor: "{colors.outline-strong}"
    borderWidth: "{spacing.hairline}"
  toggle-track-checked:
    backgroundColor: "{colors.primary}"
    borderColor: "{colors.primary}"
  toggle-thumb:
    size: "20px"
    rounded: "{rounded.full}"
    backgroundColor: "{colors.surface}"
    shadow: "raised"
  select-trigger:
    height: "{spacing.field-h}"
    padding: "0 {spacing.s-3} 0 {spacing.s-4}"
    rounded: "{rounded.md}"
    typography: "{typography.body-sm}"
    backgroundColor: "{colors.surface}"
    borderColor: "{colors.outline-strong}"
    borderWidth: "{spacing.hairline}"
    gap: "{spacing.s-3}"
  select-menu:
    rounded: "{rounded.md}"
    padding: "{spacing.s-2}"
    backgroundColor: "{colors.surface}"
    borderColor: "{colors.outline}"
    borderWidth: "{spacing.hairline}"
    shadow: "popover"
  select-option:
    height: "{spacing.control-h-sm}"
    padding: "0 {spacing.s-3}"
    rounded: "{rounded.sm}"
    typography: "{typography.body-sm}"
    gap: "{spacing.s-3}"
  select-option-active:
    backgroundColor: "{colors.surface-3}"
  select-option-selected:
    textColor: "{colors.on-surface}"
    backgroundColor: "{colors.scrim}"
  segmented:
    height: "{spacing.control-h}"
    rounded: "{rounded.md}"
    padding: "{spacing.s-1}"
    gap: "2px"
    backgroundColor: "{colors.surface-2}"
    borderColor: "{colors.outline}"
    borderWidth: "{spacing.hairline}"
  segmented-item:
    height: "{spacing.control-h-sm}"
    padding: "0 {spacing.s-4}"
    rounded: "{rounded.sm}"
    typography: "{typography.label-md}"
    textColor: "{colors.on-surface-2}"
  segmented-item-selected:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
    borderColor: "{colors.outline}"
    shadow: "raised"
  otp-cell:
    width: "48px"
    height: "56px"
    rounded: "{rounded.sm}"
    typography: "{typography.headline-sm}"
    backgroundColor: "{colors.surface}"
    borderColor: "{colors.outline-strong}"
    borderWidth: "{spacing.hairline}"
  otp-cell-filled:
    borderColor: "{colors.on-surface-3}"
  otp-cell-invalid:
    borderColor: "{colors.error}"

  # ---- disclosure / overlay ------------------------------------------------
  modal:
    width: "min(92vw, 520px)"
    rounded: "{rounded.lg}"
    padding: "{spacing.s-6}"
    gap: "{spacing.s-5}"
    backgroundColor: "{colors.surface}"
    borderColor: "{colors.outline}"
    borderWidth: "{spacing.hairline}"
    shadow: "modal"
  modal-sm:
    width: "min(92vw, 400px)"
  modal-lg:
    width: "min(92vw, 720px)"
  modal-backdrop:
    backgroundColor: "{colors.overlay}"
  sheet:
    width: "100%"
    height: "min(88dvh, 640px)"
    rounded: "{rounded.lg} {rounded.lg} {rounded.none} {rounded.none}"
    padding: "{spacing.s-5} {spacing.s-5} {spacing.s-6}"
    backgroundColor: "{colors.surface}"
    borderColor: "{colors.outline}"
    borderWidth: "{spacing.hairline}"
    shadow: "modal"
  menu:
    width: "260px"
    rounded: "{rounded.md}"
    padding: "{spacing.s-2}"
    backgroundColor: "{colors.surface}"
    borderColor: "{colors.outline}"
    borderWidth: "{spacing.hairline}"
    shadow: "popover"
  menu-item:
    height: "{spacing.control-h-sm}"
    padding: "0 {spacing.s-3}"
    rounded: "{rounded.sm}"
    typography: "{typography.body-sm}"
    gap: "{spacing.s-3}"
  menu-item-hover:
    backgroundColor: "{colors.surface-3}"
  menu-item-danger:
    textColor: "{colors.error}"
  tooltip:
    rounded: "{rounded.xs}"
    padding: "{spacing.s-2} {spacing.s-3}"
    typography: "{typography.label-sm}"
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    shadow: "popover"
  toast:
    width: "min(92vw, 380px)"
    rounded: "{rounded.md}"
    padding: "{spacing.s-4}"
    gap: "{spacing.s-3}"
    typography: "{typography.body-sm}"
    backgroundColor: "{colors.surface}"
    borderColor: "{colors.outline}"
    borderWidth: "{spacing.hairline}"
    shadow: "popover"
  accordion-item:
    borderColor: "{colors.outline}"
    borderWidth: "{spacing.hairline}"
    rounded: "{rounded.md}"
    backgroundColor: "{colors.surface}"
  accordion-trigger:
    padding: "{spacing.s-4} {spacing.s-5}"
    typography: "{typography.headline-xs}"
    gap: "{spacing.s-4}"
    textColor: "{colors.on-surface}"
  accordion-panel:
    padding: "0 {spacing.s-5} {spacing.s-5}"
    typography: "{typography.body-sm}"
    textColor: "{colors.on-surface-2}"

  # ---- display -------------------------------------------------------------
  card:
    rounded: "{rounded.lg}"
    padding: "{spacing.s-5}"
    backgroundColor: "{colors.surface}"
    borderColor: "{colors.outline}"
    borderWidth: "{spacing.hairline}"
    shadow: "flat"
  card-hover:
    borderColor: "{colors.outline-strong}"
    shadow: "raised"
  divider:
    height: "{spacing.hairline}"
    backgroundColor: "{colors.outline}"
  pill:
    height: "34px"
    padding: "0 {spacing.s-4}"
    rounded: "{rounded.pill}"
    typography: "{typography.label-sm}"
    backgroundColor: "{colors.surface}"
    borderColor: "{colors.outline}"
    borderWidth: "{spacing.hairline}"
    gap: "{spacing.s-2}"
  pill-filled:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    borderColor: "transparent"
  badge-dot:
    size: "7px"
    rounded: "{rounded.full}"
  kbd:
    height: "22px"
    padding: "0 {spacing.s-2}"
    rounded: "{rounded.xs}"
    typography: "{typography.mono-xs}"
    backgroundColor: "{colors.surface-2}"
    borderColor: "{colors.outline}"
    borderWidth: "{spacing.hairline}"
    textColor: "{colors.on-surface-2}"
  callout:
    rounded: "{rounded.md}"
    padding: "{spacing.s-4} {spacing.s-5}"
    gap: "{spacing.s-3}"
    backgroundColor: "{colors.surface}"
    borderColor: "{colors.outline}"
    borderWidth: "{spacing.hairline}"
  callout-error:
    backgroundColor: "{colors.error-surface}"
    borderColor: "{colors.error}"
  callout-success:
    backgroundColor: "{colors.success-surface}"
    borderColor: "{colors.success}"
  callout-warning:
    backgroundColor: "{colors.warning-surface}"
    borderColor: "{colors.warning}"
  callout-info:
    backgroundColor: "{colors.info-surface}"
    borderColor: "{colors.info}"
  table:
    typography: "{typography.body-xs}"
    rounded: "{rounded.md}"
    borderColor: "{colors.outline}"
    borderWidth: "{spacing.hairline}"
    backgroundColor: "{colors.surface}"
  table-header:
    typography: "{typography.caption-md}"
    textColor: "{colors.on-surface-3}"
    padding: "{spacing.s-4}"
    backgroundColor: "{colors.surface-2}"
  table-cell:
    padding: "{spacing.s-4}"
    borderColor: "{colors.outline-soft}"
  avatar:
    size: "48px"
    rounded: "{rounded.full}"
    backgroundColor: "{colors.surface-2}"
    borderColor: "{colors.outline}"
    borderWidth: "{spacing.hairline}"
  avatar-xs: { size: "28px" }
  avatar-sm: { size: "36px" }
  avatar-lg: { size: "64px" }
  avatar-xl: { size: "88px" }
  code-inline:
    typography: "{typography.mono-md}"
    padding: "2px 6px"
    rounded: "{rounded.xs}"
    backgroundColor: "{colors.code-surface}"
    borderColor: "{colors.outline}"
    borderWidth: "{spacing.hairline}"
    textColor: "{colors.on-surface}"
  code-block:
    typography: "{typography.mono-md}"
    padding: "{spacing.s-4} 0"
    rounded: "{rounded.md}"
    backgroundColor: "{colors.code-surface}"
    borderColor: "{colors.outline}"
    borderWidth: "{spacing.hairline}"
    textColor: "{colors.code-plain}"
  code-toolbar:
    height: "{spacing.control-h-sm}"
    padding: "0 {spacing.s-3} 0 {spacing.s-4}"
    typography: "{typography.mono-xs}"
    textColor: "{colors.on-surface-3}"
    backgroundColor: "{colors.surface-2}"
    borderColor: "{colors.outline}"
  scroll-region:
    rounded: "{rounded.md}"
    borderColor: "{colors.outline}"
    borderWidth: "{spacing.hairline}"
    gap: "{spacing.s-4}"

  # ---- feedback ------------------------------------------------------------
  skeleton:
    rounded: "{rounded.sm}"
    backgroundColor: "{colors.surface-3}"
  spinner:
    size: "{spacing.icon-xs}"
    borderWidth: "2px"
    borderColor: "currentColor"
  progress-track:
    height: "{spacing.s-1}"
    rounded: "{rounded.pill}"
    backgroundColor: "{colors.surface-3}"
  progress-fill:
    height: "{spacing.s-1}"
    rounded: "{rounded.pill}"
    backgroundColor: "{colors.primary}"
  empty-state:
    padding: "{spacing.s-9} {spacing.s-5}"
    gap: "{spacing.s-3}"
    width: "{spacing.measure-narrow}"
    textColor: "{colors.on-surface-2}"
---

# Neue

## Overview

Neue is one design system covering two things that usually get two systems: a
**reading surface** (long-form articles, documentation, reference) and a
**working surface** (the tools and product screens around it). Everything it
renders is either *prose to be read* or *reference to be scanned*, and the
system is tuned so the two can sit on the same page without fighting: prose
gets a measured column and generous leading; reference gets hairline rules,
monospace labels, and dense rows.

The material is paper. Surfaces are flat and achromatic, separated by 1px rules
rather than by shadow or by tint. Shadow is not decoration here. It is a claim
that an element has physically left the page, so only four things ever carry it:
floating navigation, popovers, drawers, and modals.

The palette is greyscale by construction. `primary` is near-black in light and
near-white in dark; there is no brand hue. Chroma is a semantic signal and
appears in exactly three places: **status**, **syntax**, and **data series**. If
something is colored, it means something.

The structure is measured, not guessed. Every structural decision: how many
panes, where navigation sits, whether a supporting region survives: resolves
from the width of the region it is asked about, not from the width of the
window and never from the name of a device.

### How to read this file

- **The YAML frontmatter is normative.** If a value appears in a component, in
  a build, or on a screen, it resolves to a token above. Prose is context for
  how to apply tokens; it never introduces a value a build needs.
- **`{group.token}` references resolve at build time.** A reference is never
  copied to a literal.
- **This file supersedes `NEUE_DESIGN.md` and `NEUE_LAYOUT.md`**, which are
  archived. There is no second source of truth for color, type, spacing,
  region behavior, or component anatomy.
- Terminology is fixed. The glossary below is the vocabulary the rest of the
  document uses, and no synonym for any of it is introduced later.

| Term | Means |
|---|---|
| **Token** | A named value in the frontmatter. The only legal source of a visual value. |
| **Role** | A token named for its job (`surface-2`, `outline-strong`), never for its appearance or its content. |
| **Region** | One of seven named structural slots (`banner`, `navigation`, `toolbar`, `content`, `panel`, `inspector`, `footer`). |
| **Shell** | A named set of regions. Six exist; a screen picks one and turns regions off. |
| **Primitive** | A layout component that arranges children and does nothing else. Twelve exist. |
| **Size class** | A **container** width threshold: `compact` … `xlarge`. Governs structure. |
| **Breakpoint** | A **viewport** width threshold: `xs` … `2xl`. Governs presentation. |
| **Tier** | A named elevation step. Components name a tier; they never write a shadow. |
| **Island** | One of the three clusters in the navigation row (brand · navigation · actions). |
| **Measure** | A cap on line length, expressed in `ch` because it follows the font, not the screen. |

## Design Philosophy

**Hairline over shadow.** Separation is drawn, not implied. A 1px rule at
`outline` is the default boundary between any two regions. Reach for elevation
only when an element genuinely floats and must stay readable against arbitrary
content scrolling beneath it.

**One typeface, two temperaments.** DM Sans at 400 and 500 carries every human
sentence. JetBrains Mono carries everything a machine authored or a machine
consumes: token names, section numbers, code, keyboard shortcuts, IDs. The
switch in typeface is itself information, never use mono for emphasis.

**Weight 400 and 500 only.** Hierarchy comes from size, color, and space. Bold
(600+) is not in the system. If a heading is not loud enough, it is the wrong
size or it is sitting in the wrong amount of space.

**Color means something.** Achromatic by default; chroma reserved for status,
syntax, and data series. A decorative accent hue would erode the only signal
the palette has.

**The measure is sacred.** Prose never exceeds `measure` (72ch) regardless of
how wide the viewport or the container becomes. A wider container buys wider
*tables, galleries, and code*, never wider paragraphs. Surplus width becomes
margin.

**Round or square, never in between.** Radius is trimodal and each mode carries
one meaning: `pill` means *press me*, `sm`/`md` means *type in me or read me*,
`md`/`lg` means *I contain other controls*. In a palette with no accent color,
shape is what makes "is this clickable?" answerable at a glance.

**Measure the space, not the device.** Every structural rule is written against
a container width. A tablet in a split view is narrower than a phone in
landscape; a phone cast to a television is a ten-foot interface driven by a
touchscreen; a desktop window is whatever width someone last dragged it to.
Every rule written against a device name has an exception already shipping.

**Policy is data, not code.** Which regions dock, overlay, or withdraw is a
table in the frontmatter, not a branch in a stylesheet. A table can be
inspected, diffed across four platforms, and proved consistent; branching code
drifts.

**Reduced motion is a first-class theme.** Every animation has a defined still
state, and that still state is the *finished* state, never a mid-transition
frame with `opacity: 0`.

## Target Users

| Audience | What they need from the system |
|---|---|
| **Readers** (primary) — arrive from search or a shared link, read one long article on mobile, may never return | Immediate legibility, no layout shift, no interaction required to read, a theme that matches OS preference on first paint |
| **Writers and editors** — publish long-form content through a CMS, do not write CSS | A prose contract: any heading, list, quote, table, figure, or code block they author renders correctly with zero classes |
| **Product engineers** — implement screens against this file | Complete tokens, named component states, explicit keyboard contracts, a layout kit that removes the need for per-screen layout CSS |
| **AI coding agents** — generate or modify UI from this file alone | Machine-readable tokens with no values hiding in prose; one canonical name per concept; behavior stated as rules rather than examples |
| **Assistive-technology users** (cuts across all four) | AA contrast in both themes, a visible focus indicator on every interactive element, full keyboard operation, no meaning carried by color alone |

Assumed environment: evergreen browsers with support for `oklch()`, CSS custom
properties, container queries, `:focus-visible`, `dvh` units, and
`prefers-reduced-motion`. Mobile is the majority-traffic case and is the default
drawing of every component. The system is framework-agnostic. Nothing in it
requires a component library, a build step beyond token substitution, or a
runtime.

## Colors

The palette is defined in OKLCH so the greyscale ramp is perceptually even and
the dark theme is a lightness inversion rather than a hand-tuned second palette.
OKLCH values are the source of truth; the hex values in the verification tables
are sRGB conversions supplied for tooling that cannot parse OKLCH.

### Roles

| Role | Use | Never use for |
|---|---|---|
| `background` | The page field, behind everything | Cards, inputs |
| `surface` | Cards, nav islands, inputs, menus, modals | Full-page background |
| `surface-2` | Recessed wells: code, table headers, input groups | Anything that should read as raised |
| `surface-3` | Tracks, disabled fills, skeletons, current-item wash | Text backgrounds in prose |
| `on-surface` | Body text, headings, icons that carry meaning | Decorative rules |
| `on-surface-2` | Deks, secondary copy, inactive nav labels | Body text at ≤14px on `surface-3` |
| `on-surface-3` | Captions, placeholders, mono labels, disabled text | Anything the reader must act on |
| `outline` | Decorative and structural hairlines | The boundary of an interactive control |
| `outline-strong` | The boundary of an interactive control (input, secondary button, select, OTP cell) | Prose dividers — it is deliberately loud |
| `primary` | The single action color: filled buttons, current nav item, focus ring | Large fields of color |
| `error` / `success` / `warning` / `info` | Status text and icons | Decorative accents |
| `*-surface` (status) | Tinted callout backgrounds only | Text color |
| `series-1…8` | Categorical data series | Anything that is not a chart |

`primary` equals `on-surface` at the same lightness in both themes. That is
intentional: a filled button here is an *inversion of the page*, not a colored
object. The pair is still exposed as two tokens, because a downstream product
may introduce a brand hue for `primary` without touching text color.

### The interactive-boundary rule

`outline` (1.27:1 against `surface`) is a **decorative** hairline, permitted
only where the boundary is not needed to identify a control: card edges,
dividers, table rules, nav island edges. The perimeter of any control a user
must find and operate uses `outline-strong` (3.64:1), satisfying WCAG 1.4.11
Non-text Contrast.

This is the single most common way the system gets implemented wrong. A text
input drawn with `outline` looks correct and fails.

### Status color is never alone

Every status use pairs the hue with a second channel: an icon glyph, a text
label, or both. A dot on its own is decorative; a dot plus its label is the
component. This satisfies WCAG 1.4.1 Use of Color.

### Verification: measured contrast (sRGB)

Light theme, ratio against `background` / `surface` / `surface-2` / `surface-3`:

| Token | sRGB | vs bg | vs surface | vs s-2 | vs s-3 | Verdict |
|---|---|---|---|---|---|---|
| `on-surface` | `#121212` | 16.99 | 18.81 | 17.75 | 16.25 | AAA |
| `on-surface-2` | `#424242` | 9.05 | 10.01 | 9.45 | 8.65 | AAA |
| `on-surface-3` | `#696969` | 4.98 | 5.51 | 5.20 | 4.76 | AA |
| `error` | `#C21725` | 5.53 | 6.12 | 5.77 | 5.29 | AA |
| `success` | `#137738` | 5.10 | 5.65 | 5.33 | 4.88 | AA |
| `warning` | `#875800` | 5.52 | 6.11 | 5.77 | 5.28 | AA |
| `info` | `#0064B9` | 5.36 | 5.94 | 5.60 | 5.13 | AA |

Dark theme:

| Token | sRGB | vs bg | vs surface | vs s-2 | vs s-3 | Verdict |
|---|---|---|---|---|---|---|
| `on-surface` | `#F5F5F5` | 18.25 | 17.24 | 16.24 | 15.08 | AAA |
| `on-surface-2` | `#BEBEBE` | 10.66 | 10.07 | 9.48 | 8.81 | AAA |
| `on-surface-3` | `#989898` | 6.91 | 6.53 | 6.15 | 5.71 | AA |
| `error` | `#FD736D` | 7.45 | 7.04 | 6.63 | 6.16 | AA |
| `success` | `#5FD37F` | 10.57 | 9.98 | 9.41 | 8.73 | AAA |
| `warning` | `#F9BA5F` | 11.60 | 10.96 | 10.33 | 9.59 | AAA |
| `info` | `#6DB6FF` | 9.31 | 8.79 | 8.28 | 7.69 | AAA |

Non-text and paired values:

| Pair | Light | Dark | Requirement |
|---|---|---|---|
| `outline-strong` on `surface` | 3.64 | 3.72 | ≥3.0 (1.4.11) |
| `outline-strong` on `background` | 3.29 | 3.93 | ≥3.0 |
| `outline-strong` on `surface-3` | 3.09 | 3.25 | ≥3.0 — the worst case in the system |
| `primary` on `on-primary` (filled button) | 17.75 | 17.53 | ≥4.5 |
| `focus` on `surface` | 18.81 | 17.24 | ≥3.0 (2.4.13) |
| `error` on `error-surface` | 5.41 | 5.94 | ≥4.5 |
| `success` on `success-surface` | 5.06 | 8.11 | ≥4.5 |
| `warning` on `warning-surface` | 5.43 | 9.11 | ≥4.5 |
| `info` on `info-surface` | 5.29 | 7.25 | ≥4.5 |

Every syntax token clears 4.5:1 against `code-surface` in both themes; the
lowest is `code-punctuation` at 4.58 (light). Every `series-*` token clears 3:1
against `background` and `surface` in both themes, so a series is legible as a
2px line and not only as a large fill.

Two roles are **theme-invariant by design**: `focus-offset` follows `surface`,
and the `primary`/`on-primary` *relationship* inverts rather than being
re-picked. Everything else in `themes.dark` is an explicit override.

### Ramps and the org standard

Every color resolves to an **11-step OKLCH ramp** under `ramps`, per the org
color standard: `50` soft background · `100` subtle fill · `200` interactive
background · `300` border · `400` muted accent · `500` canonical · `600` hover ·
`700` active · `800` high emphasis · `900` strong contrast · `950` maximum
depth. Five families are defined: `neutral`, `red`, `amber`, `green`, `blue` —
plus the `viz-*` categorical series.

**Components never reference a ramp.** They read semantic tokens. That is the
standard's central rule and also what makes the two themes a values-only change.
Ramps exist so the semantic layer has a principled source and so a re-theme is a
ramp swap rather than a hunt.

Neue is achromatic by construction, so it defines the five families it actually
uses rather than the sixteen the standard lists. Adding a family later means
adding a ramp; it does not mean touching a component.

**Two vocabularies, one set of values.** The org standard names surfaces and
text differently from this system, which has 101 component definitions
referencing its own names. Rather than rename them: a large, purely lexical
change with real breakage risk: both vocabularies are published and the
org-standard names are defined as references:

| Org standard | Neue | Resolves to |
|---|---|---|
| `--color-border` | `--color-outline` | `neutral-300` |
| `--color-text` | `--color-on-surface` | `neutral-900` |
| `--color-text-secondary` | `--color-on-surface-2` | `neutral-700`-ish |
| `--color-text-muted` | `--color-on-surface-3` | `neutral-600` |
| `--color-background` `--color-surface` `--color-surface-2` `--color-surface-3` | *(identical)* | `neutral-50/0/100/200` |
| `--color-primary{,-hover,-active}` | *(identical)* | `neutral-900/800/950` |
| `--color-success` `--color-warning` `--color-error` `--color-info` | *(identical)* | green/amber/red/blue `600` |

Neither is a second source of truth: the aliases are `{colors.*}` references,
so they cannot drift. Whether to keep both is tracked in Open Questions.

**A note on the `500` rule.** The standard makes `500` canonical for every
family. Neue's semantic status colors point at `600`, because `500` in these
ramps lands at roughly 3.6–4.2:1 on white: fine as a fill, short of 4.5:1 as
text, and status colors here are text. The shade *meanings* are preserved; the
semantic layer selects the step that meets the contrast floor, which is the
point of having a semantic layer.

## Typography

### Families

- **DM Sans**: `fontFamily: "DM Sans"`, weights 400 and 500 only. Fallback
  stack: `-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`.
- **JetBrains Mono**: `fontFamily: "JetBrains Mono"`, weights 400 and 500.
  Fallback: `ui-monospace, SFMono-Regular, Menlo, monospace`.

Both load with `font-display: swap` and are self-hosted; the fallback stacks are
metric-similar enough that the swap does not reflow layout beyond one line in a
headline. `font-feature-settings: "ss01", "cv11"` is applied at the root for DM
Sans's single-storey `a` alternates, which are a large part of the system's
voice. Tabular figures (`font-variant-numeric: tabular-nums`) are applied to
every numeric column, timer, counter, and metric so digits do not shuffle as
values change.

### Scale

| Token | Size | Weight | Line height | Tracking | Applied to |
|---|---|---|---|---|---|
| `headline-display` | 56px fluid | 500 | 1.05 | −0.025em | Page title, one per page |
| `headline-lg` | 44px fluid | 500 | 1.10 | −0.025em | Article H1 in prose |
| `headline-md` | 32px fluid | 500 | 1.15 | −0.015em | Section title (H2) |
| `headline-sm` | 22px | 500 | 1.25 | −0.015em | Subsection (H3), card title, accordion trigger |
| `headline-xs` | 18px | 500 | 1.30 | −0.015em | H4, modal title, dense card title, empty-state title |
| `body-lg` | 18px | 400 | 1.55 | −0.015em | Deck or lede under a page title |
| `body-md` | 17px | 400 | 1.70 | 0 | Prose paragraphs |
| `body-sm` | 15px | 400 | 1.55 | 0 | UI default: inputs, menu items, list rows |
| `body-xs` | 14px | 400 | 1.50 | 0 | Table cells, helper text, footnotes |
| `label-lg` | 15px | 500 | 1.20 | 0 | Default button |
| `label-md` | 14px | 500 | 1.20 | 0 | Field label, small button, segmented item |
| `label-sm` | 13px | 500 | 1.20 | 0 | Pill, nav link, tag, tooltip |
| `caption-md` | 12px | 500 | 1.40 | +0.06em | Eyebrows, table headers (uppercase) |
| `mono-md` | 13px | 400 | 1.65 | 0 | Code blocks, inline code |
| `mono-sm` | 12px | 500 | 1.40 | +0.06em | Section numbers, keyboard hints |
| `mono-xs` | 11px | 500 | 1.40 | +0.06em | Sub-labels, token names, code toolbar, group labels |

### Line height and tracking as one rule

Line height is a function of size and job, not a taste. Three bands, and every
token sits in one of them:

| Band | Line height | Who is in it | Why |
|---|---|---|---|
| **Display** | 1.05–1.30 | All `headline-*` | Large type needs less leading; at 44px, 1.5 opens a gap that reads as two blocks |
| **Reading** | 1.50–1.70 | `body-*`, `mono-md` | The prose band. `body-md` gets the loosest setting (1.7) because it carries the longest lines |
| **Interface** | 1.20–1.40 | `label-*`, `caption-md`, `mono-sm/xs` | Single-line strings inside a fixed-height control; leading here only makes the control taller |

Tracking is a function of size and case:

- Negative tracking scales with size: −0.025em above 32px, −0.015em from
  18–31px, 0 below 18px. Never apply negative tracking to `body-md` or smaller.
- Positive tracking (+0.06em) belongs only to uppercase text, and uppercase
  belongs only to `caption-md`, `mono-sm`, and `mono-xs`.
- Headings are never uppercase, never letter-spaced positive, never bold.

### Fluid sizes

Three tokens are fluid. The token records the **desktop ceiling**; the clamp
formula lives here because `Dimension` cannot express `clamp()`:

```css
--type-headline-display: clamp(36px, 8vw, 56px);
--type-headline-lg:      clamp(32px, 6vw, 44px);
--type-headline-md:      clamp(26px, 4vw, 32px);
```

The `vw` middle terms are chosen so all three reach their ceiling at the `md`
breakpoint (768px): headlines stop growing exactly where the container starts
growing, so a desktop page never has a headline that overwhelms its column.

### Prose defaults

Authors write markup, not classes. The following apply to any content inside a
prose container with no author intervention:

- `p`, `li`, `blockquote` cap at `measure`. Prose sets `text-wrap: pretty`;
  headlines set `text-wrap: balance`.
- Heading spacing comes from the vertical-rhythm contract, not from margins the
  author sets.
- `blockquote` takes a 2px left rule at `outline-strong`: the only 2px rule in
  the system, where the weight is doing typographic work.
- Lists use `s-2` between items and hang their markers outside the measure.
- `hr` renders as a `divider`.
- Links are underlined in prose with `text-underline-offset: 0.15em` and
  `text-decoration-thickness: 1px`; they are *not* underlined in chrome, where
  position and role already identify them.
- Minimum rendered size anywhere in the system is 11px, and 11px is only ever
  mono, uppercase, and used for labels of at most three words.

## Layout & Spacing

### The two axes

This is the rule the rest of the section depends on, and the one worth stating
twice.

| | `sizeClasses` (container) | `breakpoints` (viewport) |
|---|---|---|
| Measures | The width of the region being laid out | The width of the window |
| Governs | Structure: pane count, region presentation, where navigation lives | Presentation: fluid type ceilings, page gutters, gallery column counts |
| Queried with | `@container` | `@media (min-width: …)` |
| Names | `compact` `medium` `expanded` `large` `xlarge` | `xs` `sm` `md` `lg` `xl` `2xl` |

A pane should respond to the room it was given; a headline should respond to the
screen a person is holding. The two groups have deliberately different names, at
deliberately different values, so that using one for the other's job is visible
in review rather than invisible in a stylesheet.

The practical consequence is that a shell can be nested inside itself. An
embedded preview pane 380dp wide resolves to `compact` and grows a bottom bar,
inside a window that resolved to `large` and has a drawer. Neither knows about
the other, and no code was written to make that work.

**Inside a shell, size against the container; only page-level chrome may size
against the viewport.** A gallery inside the reading column is not the width of
the viewport: the two rails take `rail` each as they appear. Driving that
gallery from viewport media queries adds a column at the exact moment its
container *loses* 248px, and the cards visibly jump and re-wrap while a window is
being dragged.

### Size classes

Five, resolved from container width. There is no sixth, on purpose: a layout
that appears to need one usually needs a different primitive, and if it truly
needs one, that belongs in Open Questions rather than in a private breakpoint
nobody else knows about.

| Class | Width | Panes | Navigation | Inspector |
|---|---|---|---|---|
| `compact` | 0–599 | 1 | bottom bar | sheet |
| `medium` | 600–904 | 1–2 | rail | sheet |
| `expanded` | 905–1279 | 2 | rail | overlay |
| `large` | 1280–1919 | 2–3 | drawer | docked |
| `xlarge` | 1920+ | 2–3 | drawer | docked |

At `xlarge` nothing new appears. The surplus width becomes margin.

### The 4px rhythm

Every spatial value in the system is a multiple of 4 and comes from `s-1`…`s-12`.
The scale is deliberately non-linear: tight at the bottom for control interiors,
loose at the top for section rhythm.

| Token | Value | ×4 | Role |
|---|---|---|---|
| `s-1` | 4px | 1 | Icon-to-text in dense chips, control insets, focus bleed |
| `s-2` | 8px | 2 | Icon-to-label, stacked label + field, list item gaps |
| `s-3` | 12px | 3 | Related controls in a row, list row padding |
| `s-4` | 16px | 4 | Card interior (dense), page gutter on mobile |
| `s-5` | 20px | 5 | Card interior (default), field horizontal padding |
| `s-6` | 24px | 6 | Between subsection blocks |
| `s-7` | 32px | 8 | Between a heading and its content, page gutter at `lg` |
| `s-8` | 40px | 10 | Between subsections |
| `s-9` | 48px | 12 | Section vertical padding (mobile) |
| `s-10` | 64px | 16 | Section vertical padding (desktop), shell column gap |
| `s-11` | 80px | 20 | Page header padding |
| `s-12` | 112px | 28 | Major page breaks, pre-footer |

**If a gap is not on this scale, it is a bug.** Two exceptions, both inside
controls and both documented: `2px` optical nudges for icon baselines, and the
`2px` inner gap in the segmented track. Everything else, including every gap
inside every primitive, is a step.

### Vertical rhythm

Rhythm is a contract between blocks, not a set of margins each block chooses.
Blocks declare *no* outer margin; the container declares the gap.

| Between | Gap |
|---|---|
| Section and section | `s-9` (base), `s-10` at `md`+, separated by a 1px `outline` rule; the first section on a page has no top rule |
| Section head and its first block | `s-7` |
| Subsection and subsection | `s-8` |
| Heading and its own paragraph | `s-4` |
| Paragraph and paragraph | `s-5` |
| Label and field | `s-2` |
| Field and its hint or error | `s-2` |
| Field and field | `s-5` |
| Last field and the actions row | `s-7` |

Anchor targets set `scroll-margin-top: var(--scroll-offset)` so a deep-linked
heading lands *below* the navigation stack rather than under it. `scroll-offset`
is derived (`nav-stack` (80px) plus one step of rhythm (`s-7`)) and it is the
same line the sticky rails pin to, so a heading and the rail heading beside it
sit level. This is a WCAG 2.4.11 requirement, not a nicety.

### Alignment and distribution

Symmetry is produced by rules, not by eye. These are the ones that do the work:

- **One gap per group.** Everything inside a group is separated by a single
  token; a group never mixes two gaps on the same axis. If two different gaps
  are needed, there are two groups.
- **Padding is symmetric unless an optical correction says otherwise.** The two
  cases where it is not: a control with a trailing chevron pads `s-3` on the
  chevron side and `s-4` on the label side, because the glyph carries its own
  sidebearing; and text that sits beside an icon aligns to the icon's optical
  center, not its box.
- **Icons align to cap height, not to the line box**, and sit `s-2` from their
  label. In a fixed-height control, the icon and label are centered as one unit,
  never independently.
- **Numbers right-align, text left-aligns, and nothing centres in a table.**
  Centred columns make ragged edges on both sides and defeat scanning.
- **Optical centring for glyph-only controls.** A single glyph in a round
  control is centered on its own bounding box, then nudged up to 2px where the
  glyph's mass is off-center (play triangles, chevrons).
- **Baselines align across columns.** Where two columns sit side by side, their
  first text baselines match; achieved by giving both the same top padding, not
  by nudging one.
- **Hairlines land on device pixels.** Rules are always exactly 1px
  (`hairline`), never 0.5px or 2px, which render inconsistently across DPRs.
- **Nested radius.** A child's radius is the parent's radius minus the padding
  between them, snapped to the nearest token: an `sm` (10px) menu item inside an
  `md` (16px) menu with `s-2` (8px) padding: 16 − 8 = 8, snapped up to 10. Never
  nest two `pill` shapes with less than `s-1` between them.
- **Media reserves its box.** Every image, video, chart, and skeleton declares
  `aspect-ratio` (16/9 figures, 16/10 card media, 1.6/1 swatches) rather than a
  fixed height, so nothing shifts as assets load.

### Containers and measures

| Token | Width | Contents |
|---|---|---|
| `content` | 780px | Prose, forms, section headers, single-column demos |
| `wide` | 1120px | Component galleries, color grids, wide tables, image rows |
| `rail` | 248px | Both shell rails — one token, so the two sides cannot drift apart |
| `shell` | 1468px | Outermost bound of the reading shell, rails included |
| `surface-max` | 1280px | Working-surface cap inside an app shell |
| `surface-max-wide` | 1600px | Dashboards, boards, galleries |
| `measure-narrow` | 44ch | Leads, empty states, callout bodies |
| `measure` | 72ch | Hard cap on paragraph line length inside any container |
| `measure-wide` | 88ch | Tables, code, log output |

`content` is derived, not chosen: 780px is the widest container in which
`body-md` (17px/1.7) still lands under 72ch with gutters applied. A measure is a
cap on a *line*, which is why it is expressed in `ch` and not in px: it should
follow the font, not the screen.

`wide` is a **break-out**, not a page mode: a `wide` block sits inside a
`content` page and extends symmetrically past it. On viewports narrower than
`wide` plus gutters, the break-out collapses back to full width with no visual
change other than the loss of the extra room.

```css
.content { width: 100%; max-width: var(--content); margin-inline: auto;
           padding-inline: var(--gutter); }
.content > .bleed-wide {
  --w: min(var(--wide), 100cqw - var(--gutter) * 2);
  width: var(--w); margin-inline: calc(50% - var(--w) / 2);
}
.prose :is(p, li, blockquote) { max-width: var(--measure); }
```

Content regions cap at `surface-max` unless they have a reason not to.
Dashboards and galleries take `surface-max-wide`. Canvases, maps, and timelines
are uncapped, because for those surfaces width *is* the content.

### Regions

Seven named regions. A shell is this set with some of them turned off; it is not
a new layout.

- **banner.** Global announcement or environment strip. First to go.
- **navigation.** The only region that may never be hidden at any size class.
- **toolbar.** Actions scoped to the current surface.
- **content.** The working surface. `priority: 100`; everything else yields.
- **panel.** A list, a file tree, a layer stack. Attaches at the start edge.
- **inspector.** Properties of the current selection. Attaches at the end edge.
- **footer.** Legal, status, secondary links.

`priority` is what makes the shell resolvable rather than negotiable. When
docked widths exceed the space available, regions release in ascending priority
order, and two regions never argue about which of them gives way.

### Adaptation

Every collapsible region moves down the same ladder as space runs out:

```
docked  →  inline  →  overlay  →  sheet  →  hidden
```

The `adaptation` table in the frontmatter is the normative part of this
document. It is data rather than branching code, so it can be inspected, tested,
and diffed across platforms: the same table exists as a JavaScript object, a
Kotlin `when`, and a Swift `switch`, and a conformance tool can prove they agree.

The line it draws is the one that keeps a product consistent: **the product owns
whether a region is open; the shell owns how an open region presents.** A product
that sets presentation by hand will set it differently on the fourth screen than
on the first, and the inconsistency reads as sloppiness rather than as the
accumulation of eleven reasonable local decisions.

The ladder only ever runs one way. A region does not become more prominent as
space shrinks. That property is checkable, and it is checked.

### Shells

Six named region sets, declared with one attribute:

| Shell | Regions | For |
|---|---|---|
| `app` | `navigation` `toolbar` `content` `inspector` `footer` | The default product screen. The other five are specialisations of it. |
| `browse` | `navigation` `panel` `toolbar` `content` `footer` | An index and the thing it indexes. |
| `canvas` | `navigation` `toolbar` `content` `panel` `inspector` | Editors, maps, timelines — chrome floats, the surface pans. |
| `reading` | `toolbar` `content` `inspector` | Articles and documentation at a measure. This is the documentation shell below. |
| `site` | `banner` `toolbar` `content` `footer` | Marketing and docs — the one shell where the *page* scrolls. |
| `focus` | `content` `panel` | One task, no navigation, because navigation is a way out of it. |

`tv` is not a seventh shell. It is `app` with `data-platform="tv"`, which
reserves `environment.overscan` manually (televisions report no safe area),
scales metrics, and promotes focus to the primary state because a remote cannot
hover.

### Primitives

Twelve primitives arrange children and do nothing else: no color, no type, no
self-positioning. Every knob is a custom property, so any of them is tunable
inline (`<div class="l-grid" style="--min: 320px">`) without a new class.

`Container` `Stack` `Row` `Grid` `Columns` `Split` `Switcher` `Frame` `Center`
`Cover` `Scroller` `Sticky`: with the arrangement and knobs of each declared in
`primitives` in the frontmatter.

Together with the six shells they are meant to cover any deliverable the
organisation ships without a single screen needing layout CSS of its own. **If a
screen is growing its own layout rules, the arrangement it wants is almost always
a primitive nobody reached for.** Reach for an intrinsic primitive before
reaching for a size class: a `Grid` whose cells declare a minimum width needs no
breakpoints at all.

### The documentation shell

The `reading` shell at `lg` and above is a three-track grid. Both rails are
sticky, scroll independently, and are `overflow-y: auto` with their own thin
scrollbars.

```
>= xl (1280px)                     shell, capped at 1468px
+-----------+------------------------------+-----------+
| sidebar   |  content 780px               | contents  |
| rail      |  (prose, forms)              | rail      |
| sticky    |  ...wide 1120px break-out... | sticky    |
+-----------+------------------------------+-----------+

>= lg (1024px)      three tracks; the end rail is an empty spacer
+-----------+------------------------------+-----------+
| sidebar   |  content                     |           |
+-----------+------------------------------+-----------+

< lg                single column; sidebar -> drawer,
                    contents -> drawer section list
+-------------------------------------------------------+
|  content (full width, gutter)                          |
+-------------------------------------------------------+
```

```css
.shell {
  display: grid; gap: var(--s-10);
  max-width: var(--shell); margin-inline: auto;
  padding-inline: var(--gutter);
  grid-template-columns: minmax(0, 1fr);
}
@media (min-width: 1024px) {
  .shell {
    padding-inline: var(--gutter-lg);
    grid-template-columns:
      minmax(var(--rail-min), var(--rail))
      minmax(0, var(--content))
      minmax(var(--rail-min), var(--rail));
    justify-content: center;
  }
}
```

Three properties of that definition are load-bearing:

- **`minmax(0, …)` on the content track.** Without the `0` minimum, a wide code
  block or table forces the grid past the viewport and breaks the sticky rails.
- **Both rails are one token.** `rail` is used on both sides so they cannot
  drift apart, and the third track exists from `lg` upward even while it is
  empty. The reading column is therefore centered in the viewport rather than
  pushed left by a wide rail with a narrower one opposite, and crossing `xl`
  changes what is *in* the end rail, never the geometry.
- **The rails compress before the content does, and stop at `rail`.** Between
  `lg` and `shell` the rails sit somewhere between `rail-min` and `rail`; at
  `shell` they reach `rail` exactly, and past it the surplus becomes page
  margin. `shell` is derived: `content + 2·rail + 2·s-10 + 2·gutter-lg` —
  which is why it is 1468px and not a round number.

The cost of symmetry is honest: at 1024px the reading column lands near 536px
rather than the ~640px an asymmetric two-track grid would give it. At `body-md`
that is still under 63ch, comfortably inside the measure, and it buys a page
that does not move sideways when the window is resized.

The column gap is `s-10` rather than `s-9`: at the tighter value the contents
rail reads as an edge of the content column rather than as a sibling of it.

### Grid patterns

| Pattern | Cell minimum | Gap |
|---|---|---|
| Color swatches | 160px | `s-3` |
| Card gallery | 280px | `s-6` |
| Component demo pairs | 340px | `s-6` |
| Footer columns | 200px | `s-6` |

Every gallery is intrinsic: `repeat(auto-fit, minmax(min(<floor>, 100%), 1fr))`
— and queries its own container, not the viewport. `min(<floor>, 100%)` is what
stops a 340px floor from overflowing a 300px container. Column *counts* are
never declared; they are a consequence of the floor and the space available,
which is why the table above has no breakpoint columns in it.

### Overflow, truncation, and constrained content

When content exceeds its region, exactly one of these happens, declared per
region rather than decided at render time:

| Answer | Behaviour | Belongs to |
|---|---|---|
| **scroll** | The region scrolls on its long axis | Content surfaces, panels, inspectors, tables, code |
| **collapse** | Items move into a menu, in priority order | Chrome: toolbars, banners, navigation |
| **wrap** | Items flow onto a new line | Footers, tag rows, filter rows |
| **paginate** | Content splits into discrete pages | Print, TV, kiosk |
| **clip** | Content is cut | Requires a stated reason; almost always the wrong answer |

The failure this prevents is the one every layout system has shipped: a toolbar
that neither collapses nor scrolls, so its last button sits four pixels outside
a phone in landscape and nobody notices for a release. **Declare an overflow
answer for every region, including the ones you are confident will never
overflow.**

**Horizontal scrolling is a component, not an accident.** There is no horizontal
page scroll, ever; `html, body { overflow-x: clip }` is a safety net, not a
strategy. Every wide child owns its own scroll container, and that container:

- takes `tabindex="0"` and an `aria-label` naming what it holds, because a
  scrollable region a keyboard user cannot reach is a WCAG failure;
- shows an edge affordance: a `s-6` gradient from `surface` to `fade` on
  whichever edge has content beyond it, driven by scroll position, so the
  scrollability is visible before the user drags;
- keeps a visible scrollbar on pointer devices (`scrollbar-width: thin`) rather
  than hiding it for tidiness;
- uses `scroll-snap-type: inline mandatory` only when items are equal-width
  peers (card rails, image strips), never for free-form content like a table.

**Truncation is a last resort, and it is always reversible.** In order of
preference: let it wrap, give it more room, shorten the source string, and only
then truncate.

| Case | Treatment |
|---|---|
| Single-line label in a fixed control | `text-overflow: ellipsis` with `min-width: 0` on the flex child — the missing `min-width: 0` is why ellipsis "does not work" in a flex row |
| Multi-line summary (card dek, list row) | `-webkit-line-clamp` at 2 or 3 lines; never more than 3, because a fourth clamped line reads as a paragraph that broke |
| Identifiers where the tail matters (file paths, IDs, hashes) | Middle-truncation: keep the first 8 and last 6 characters around a `…`. Never end-truncate an identifier |
| Table cell | The cell does not truncate; the scroll container carries the overflow |
| Code and token names | Never wrap and never truncate. A token name broken mid-string (`--color-` / `outline`) reads as two different identifiers. It scrolls |

Any truncated string keeps its full value accessible: the element carries the
complete text as its accessible name, and a pointer or focus reveals it in a
`tooltip`. A string that has been truncated with no way to recover it is data
loss, not a layout choice.

### Density

`data-density` on any subtree, opt-in, so a dense table can sit inside a
comfortable page without either leaking. It multiplies the spacing scale and
control heights and nothing else:

| Value | Multiplier | For |
|---|---|---|
| `compact` | 0.875 | Data grids, inspectors, long reference tables |
| `comfortable` | 1 | The default everywhere |
| `spacious` | 1.125 | Reading-first pages, TV, low-vision presets |

Rules: results snap to 2px so the rhythm stays on-grid; type is never scaled
below its token size; and no control drops below the pointer target floor in
force for that input, whatever the multiplier says. Density changes how much air
a layout has, never what it says or whether it can be hit.

### Environment

Safe-area insets are respected and are **added** to the page margin rather than
replacing it, because a notch is not a design decision.

`environment.overscan` reserves a fraction of each edge on surfaces that cannot
report a safe area: televisions, mostly. `environment.hinge` reserves a gutter
across a book-posture foldable.

Hit targets read the pointer, not the platform: `target-fine` (28px) for a
mouse, trackpad, or stylus; `target-coarse` (44px) for a finger; `target-remote`
(56px) for a directional pad. A phone with a mouse attached gets `fine`; a
laptop with a touchscreen gets `coarse` on touch. `target-fine` is permitted
only on pointer-only dense surfaces such as data grids, and even there it stays
above the 24px WCAG 2.5.8 floor. Everywhere else the system holds 44px,
including for controls whose visible box is smaller: a 34px `pill` that is
interactive carries `margin-block: 5px` so its *spacing-inclusive* target clears
the floor.

## Responsive Strategy

Mobile-first: every rule is written for the narrow case and widened with
`min-width` queries only. There are no `max-width` queries in the system except
the reduced-motion and print blocks.

| Breakpoint | Min width | What changes |
|---|---|---|
| *(base)* | 0 | Single column, gutter `s-4`, drawer navigation, stacked forms |
| `xs` | 480px | Brand wordmark appears beside the mark; OTP cells reach full width |
| `sm` | 560px | Gutter → `gutter-md`; modal footers go horizontal; demo rows stop scrolling |
| `md` | 768px | Fluid headlines reach their ceiling; paired form fields may go two-up; modal gains its 520px cap |
| `lg` | 1024px | Navigation island gains inline links; sidebar rail appears (drawer retired); gutter → `gutter-lg`; section padding `s-10` |
| `xl` | 1280px | Contents rail is populated; `wide` break-outs reach full 1120px |
| `2xl` | 1536px | No new layout. The shell caps at 1468px and surplus becomes margin. Reserved for future editorial spreads |

### Rules that hold at every width

- **No horizontal page scroll, ever.** Every wide child owns its own scroll
  container; the page never does. See Overflow above.
- **Touch targets never shrink.** The floor is the target in force for the
  pointer, and it does not vary by breakpoint.
- **Type does not scale down.** No token drops below its stated size on mobile;
  fluid headlines scale *up* from their floor, never below it.
- **`dvh` for full-height surfaces** (drawer, sheet, mobile modal) so mobile
  browser chrome does not clip the bottom of a dialog.
- **Orientation-agnostic.** Nothing is locked to portrait; a landscape phone
  gets the wider layout naturally, because the query is about width.
- **Reflow at 400% zoom** to a single column with no horizontal scroll and no
  loss of function (WCAG 1.4.10).

### Container query recipes

Four containers are named, and everything inside a shell queries one of them:

```css
main            { container: content / inline-size; }
.panel          { container: panel / inline-size; }
.inspector      { container: inspector / inline-size; }
.card           { container: card / inline-size; }

/* Structure resolves from the region, using the size-class values. */
@container content (min-width: 905px) { /* expanded and up */ }
@container card (min-width: 420px)    { .card { grid-template-columns: 96px 1fr } }
```

Two habits make this reliable: a container element cannot also be the element
that responds to the query, so every container has an inner wrapper; and the
size-class values are used as the query thresholds, never fresh numbers, so a
region and the shell around it agree on what `expanded` means.

## Elevation & Depth

Depth is expressed by **rules first, shadow last**. Five tiers exist; the tier
name is what components reference in `components.*.shadow`.

| Tier | Used by | Reads as |
|---|---|---|
| `flat` | Cards, callouts, tables, code blocks, inputs, buttons | On the page |
| `raised` | Card hover, segmented selected thumb, toggle knob | Lifted a hair |
| `float` | The navigation islands at rest | Floating above scrolling content |
| `popover` | Select menu, dropdown, tooltip, toast, skip link, islands once scrolled | Temporarily above everything |
| `modal` | Modal dialog, drawer, sheet | Owns the screen |

Rules:

- A component may not invent a shadow. If `flat` is wrong, the answer is the
  next tier up or a border, never a bespoke `box-shadow`.
- Nothing gains elevation on hover except `card` (`flat` → `raised`). Buttons
  respond to hover with color and to press with scale, not with depth.
- **Dark theme re-tunes, it does not reuse.** A light-theme shadow over a dark
  surface reads as haze. `themes.dark` overrides all four non-flat tiers with
  tighter, darker, higher-alpha values, and dark surfaces lean on `outline` to
  carry the separation the shadow no longer can.
- Elevation and border are additive, not alternatives: every floating surface
  also carries a 1px `outline`, so it stays legible when the shadow is invisible
  (dark theme, forced colors, low-quality displays).
- `z-index` is a fixed ladder, never ad hoc:

| Layer | z |
|---|---|
| Inline (stacking contexts inside content) | 1 |
| Sticky rails | 10 |
| Docked region chrome | 20 |
| Navigation islands | 30 |
| Dropdown, select menu, tooltip | 40 |
| Drawer, sheet, and their backdrops | 50 |
| Modal and its backdrop | 60 |
| Skip link, toast | 70 |

## Motion

Motion in a reading system exists to explain state changes, never to entertain.
Four durations, four easings, one rule about where each belongs.

| Token | Value | Use |
|---|---|---|
| `duration-instant` | 90ms | Press feedback (`scale(0.97)`), checkbox tick |
| `duration-fast` | 180ms | Hover, focus ring, color, small toggles |
| `duration-normal` | 280ms | Theme change, accordion panel, menu open |
| `duration-slow` | 520ms | Drawer and sheet slide, modal entrance, first-paint reveal |
| `ease` | `cubic-bezier(0.22, 1, 0.36, 1)` | Default; everything unless listed below |
| `ease-out` | `cubic-bezier(0.16, 1, 0.3, 1)` | Entrances: menus, modals, reveals |
| `ease-in-out` | `cubic-bezier(0.65, 0, 0.35, 1)` | Reversible movement: drawer, segmented thumb |
| `ease-spring` | `cubic-bezier(0.34, 1.4, 0.64, 1)` | Exactly one place: the OTP cell fill pop |
| `stagger-step` | 60ms | Delay increment for sequenced reveals, maximum four steps |

Patterns:

- **Entrance**: `opacity 0→1` plus `translateY(12px→0)` over `duration-slow`
  with `ease`. Staggered at most four items; the fifth and beyond share the
  fourth's delay. Used on first paint for navigation, title, dek, and rails only.
- **Scroll reveal**: `IntersectionObserver` adds `.in`; threshold 0.15, fires
  once, `rootMargin: 0px 0px -10% 0px`. Content is visible without JavaScript;
  the observer only adds the transition, and the no-JS state is the final state.
- **Press**: `transform: scale(0.97)` on `:active` for buttons, `0.95` for icon
  buttons. This is the system's only transform-based affordance, and it is why
  `button-primary-active` is an empty variant map.
- **Theme change**: `background-color` and `color` transition over
  `duration-theme`; `box-shadow` and `border-color` do not, because animating
  four shadow layers across a full page drops frames.
- **Region adaptation.** A region entering `overlay` or `sheet` slides from its
  own edge over `duration-slow` with `ease-in-out`; the reverse on exit. A
  region never fades in place, because the movement is what says where it came
  from and where it will go back to.
- Only `transform`, `opacity`, `background-color`, `border-color`, `color`, and
  `box-shadow` are animated. Never `height`, `width`, `top`, or `left`: the
  accordion animates `grid-template-rows: 0fr → 1fr`, which is compositor-safe
  and needs no measured height.

### Reduced motion

`prefers-reduced-motion: reduce` is honoured globally, and the still state is
always the *finished* state:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 1ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 1ms !important;
    scroll-behavior: auto !important;
  }
  .fade-up, .reveal { opacity: 1 !important; transform: none !important; }
}
```

Three behaviors change beyond duration: smooth anchor scrolling becomes an
instant jump, sliding surfaces (drawer, sheet, modal) appear in place, and the
scroll-reveal observer is skipped entirely rather than run at 1ms. State changes
stay *visible*: an accordion still opens, it just does not animate.

## Shapes

Radius is trimodal, and the three modes carry meaning. Shape is the affordance
signal in a palette with no accent color.

| Shape | Meaning | Components |
|---|---|---|
| `pill` | *Press me* | Buttons, icon buttons, tag pills, switches, avatars, nav islands |
| `sm` / `md` | *Type in me, or read me* | Inputs, textareas, select triggers, OTP cells, segmented controls |
| `md` / `lg` | *I contain other controls* | Cards, menus, modals, accordions, code blocks, drawers |

| Token | Value | Applied to |
|---|---|---|
| `none` | 0 | Rules, dividers, table cell edges, full-bleed media |
| `xs` | 6px | Inline code, checkbox, keyboard key, tooltip |
| `sm` | 10px | Menu items, sidebar links, OTP cells, skeletons |
| `md` | 16px | Containers: callouts, code blocks, tables, textareas, menus, frames |
| `lg` | 24px | Large containers: cards, modals, sheets, footer |
| `xl` | 32px | Full-bleed hero panels |
| `pill` | 999px | Controls you press |
| `full` | 50% | Avatars, status dots, radio buttons |

Text entry is visibly rectangular rather than capsule-shaped. When every
interactive control is a `pill`, the capsule stops meaning "press" and becomes
decoration; a rectangular field also gives the caret a square well to sit in and
stops long values colliding with the curve.

## Iconography

**Vocabulary: Phosphor. Delivery: inline SVG sprite.** The org icon standard
specifies Phosphor and ships three webfont stylesheets. This system adopts
Phosphor as the icon *vocabulary*: the same names, the same 24px grid, the same
regular / fill / duotone weight split, and delivers it as an inline sprite.

That deviation is deliberate and narrow, and the reasoning is worth stating
because it is not a matter of taste:

- An icon font that fails to load renders **tofu** inside icon-only controls.
  Every one of those controls is unusable until the CDN recovers; the label *is*
  the icon, so there is nothing left.
- Ligature-based icon fonts are announced as their ligature text by several
  screen readers, so an icon-only button reads out its glyph name.
- A third-party request in the critical path of every page contradicts the
  system's no-network-dependency rule, which also governs fonts and charts.

**How to comply if the webfont is mandatory.** Nothing else depends on the
delivery mechanism: swap the sprite `<use>` for `<i class="ph ph-magnifying-glass">`,
keep the labelling contract below unchanged, and add a `font-display: block`
fallback. Brand marks follow the standard directly: Simple Icons at 24px,
`alt=""`, since those are third-party logos we should not be redrawing.

### Drawing rules

- **Grid:** 24×24 viewBox, 1.5px stroke, round caps and joins, `currentColor`
  for both stroke and fill.
- **Sizing** comes from the `icon-*` tokens and is chosen by the control, not by
  the glyph: `icon-xs` in `button-sm` and pills, `icon-sm` in callouts and list
  rows, `icon-md` in default buttons and form controls, `icon-lg` in the
  navigation islands, `icon-xl` standalone, `icon-2xl` in empty states.
- **Weight pairing:** stroke icons everywhere; filled icons only for *state* —
  checkbox tick, selected radio, current theme, status glyph in a callout.
  Filled means "this is on".
- **Alignment:** icons in a text row center on the cap height, not the line box,
  and sit `s-2` from their label.
- **Directionality:** chevrons rotate rather than swap glyphs (accordion and
  select 0→180°, drawer arrow 0→90°) so the transition is a single transform.
  In RTL, directional glyphs mirror; status and brand glyphs do not.

### Icon-only controls

An icon-only control is a control whose *entire label* is a picture, so it
carries a stricter contract than an icon beside text:

- It takes `aria-label`, always, and the label is the same string a labelled
  version of that control would use. A tooltip is a supplement, never the
  substitute: the label ships either way.
- It gets a `tooltip` on hover **and** on keyboard focus, after a 400ms delay on
  hover and immediately on focus, dismissible with `Escape` (WCAG 1.4.13).
- It holds the full pointer target even when the glyph is small; the glyph is
  centered in the target, not the target sized to the glyph.
- It is used only for actions that are **either** universally recognized (close,
  search, menu, copy, back) **or** repeated so often in that surface that the
  label becomes noise (a toolbar of formatting actions). A rare or destructive
  action always keeps its text label.
- Where a labelled button collapses to icon-only in a narrow container, the
  collapse is driven by a container query, and the accessible name does not
  change across the collapse: only the visible text is hidden, with the
  `aria-label` already present at every width so nothing is announced
  differently at one size than another.

## Component Guidelines

Every component is specified as **anatomy → variants → states → keyboard →
notes**. All visual values resolve to `components.*` in the frontmatter; none
are restated here as raw numbers. States common to every interactive component —
hover, press, focus, disabled: are defined once in Interaction Patterns and are
not repeated per component.

### Button

Anatomy: `[optional leading icon] label [optional trailing icon]`, centered, in a
`pill` at `control-h`.

Variants: `primary` (inverted fill: one per view, the single most important
action), `secondary` (surface plus `outline-strong`), `ghost` (no chrome, for
tertiary actions in dense rows), `danger` (destructive confirmation only), `icon`
(square, `aria-label` required), sizes `sm` / default / `lg`.

States: hover (color only), active (`scale(0.97)`), focus-visible (the system
ring), disabled (`surface-3` fill, `on-surface-3` text; `aria-disabled` rather
than the `disabled` attribute when the control must stay focusable to explain
itself), loading (spinner replaces the leading icon, label stays, width locked to
prevent reflow, `aria-busy="true"`).

Keyboard: `Enter` and `Space` activate. Never remove a button from the tab order
to "disable" it.

Notes: a `ghost` button beside a `secondary` is the correct pattern for "Cancel";
never use `secondary` for both actions in a pair. Icon-only buttons in a toolbar
get `s-1` between them and rely on the pointer target, not on the visible box.

### Input, Textarea, Input group

Anatomy: `field-label` → field (`field-h`, radius `md`) → `field-hint` or
`field-error`. The label is always present and always visible; a placeholder is
never a label substitute.

Variants: text input; textarea (radius `md`, min-height 120px, `resize: vertical`
only); input group (a field and a button sharing one boundary, with the ring
drawn on the group via `:focus-within`).

States: rest, hover, focus (ring only: the border does not change), filled,
invalid (`error` border, message, `aria-invalid="true"`), disabled, read-only
(`surface-2` fill, no border change).

Notes: the field boundary uses `outline-strong`, not `outline`. Invalid is never
color-only: the message below is the actual signal and is linked with
`aria-describedby`.

### Checkbox, Radio, Toggle

Anatomy: a 20px box (`xs` radius) or circle (`full`), plus a clickable label at
`body-sm`. The real `<input>` is visually hidden but focusable, and the ring is
drawn on the visual box.

States: unchecked, checked (`primary` fill, `on-primary` glyph), indeterminate
(checkbox only, horizontal bar), disabled, invalid (group level only).

Toggle is for *immediate, self-saving* settings; a checkbox is for values
submitted with a form. A toggle never appears inside a form with a Save button.
The toggle track carries a 1px `outline-strong` border so the off state is
identifiable at 3:1 without relying on the fill.

Keyboard: `Space` toggles. Radio groups: arrow keys move *and* select within the
group; `Tab` enters and leaves the group as one stop.

### Select

A button-triggered listbox. Used instead of `<select>` when options need icons,
descriptions, or grouping; native `<select>` remains correct for long, plain,
data-entry lists (dates, countries) where the platform picker is better.

Anatomy: `select-trigger` (value plus chevron) → `select-menu` (popover
elevation, max-height 320px, own scroll) → `select-option` rows (leading check
slot, label, optional description).

Roles: trigger `role="combobox"` with `aria-expanded`, `aria-haspopup="listbox"`,
`aria-controls`; menu `role="listbox"`; rows `role="option"` with
`aria-selected`. The active row is tracked with `aria-activedescendant`: DOM
focus stays on the trigger throughout, which keeps `Escape` handling trivial.

States: closed, open, option-active (`surface-3` wash under pointer or keyboard),
option-selected (check glyph plus `scrim` wash), disabled option (`aria-disabled`,
skipped by arrow keys), empty (see Empty States).

Keyboard: `Space` / `Enter` / `↓` / `↑` open; `↓` / `↑` move the active row;
`Home` / `End` jump; type-ahead matches by prefix within a 500ms buffer; `Enter`
selects and closes; `Escape` closes and restores the previous value; `Tab` closes
and commits.

Notes: the menu sits below the trigger and flips above when it would overflow;
it matches the trigger width unless content forces it wider. Opening does not
trap focus. This is a listbox, not a dialog.

### Segmented control

A single-choice control for two to five short, mutually exclusive, immediately
applied options (view mode, theme, timeframe). Not a substitute for tabs, which
change page regions.

Anatomy: a track at `surface-2` containing equal-width items; the selected item
is a `surface` thumb with `outline` and `raised` elevation.

Roles: `role="radiogroup"` with `role="radio"` items, or `role="tablist"` when it
genuinely switches panels. Never both.

States: rest, hover (label darkens to `on-surface`), selected, disabled,
focus-visible (ring on the item, not the track).

Keyboard: `Tab` enters at the selected item; `←` / `→` / `Home` / `End` move and
select; the group is a single tab stop.

Notes: the thumb animates by `transform: translateX()` between fixed-width slots
over `duration-fast` with `ease-in-out`; it never resizes mid-transition. Labels
are `label-md`, one or two words, sentence case. When the container cannot hold
every item above the pointer target floor, the control becomes a select rather
than shrinking: the swap is driven by a container query, not by a viewport
breakpoint.

### Tabs

For switching between panels of related content in the same region. Anatomy:
`tablist` with a 1px `outline` baseline → `tab` items marked by a 2px `primary`
underline when selected.

Roles: `role="tablist"` / `role="tab"` / `role="tabpanel"`, with
`aria-controls` and `aria-selected`; the selected panel is the only one in the
tab order.

Keyboard: the tablist is one tab stop; `←` / `→` move between tabs and activate
them; `Home` / `End` jump. When a tablist overflows its container it scrolls
horizontally with the edge affordance from Overflow: it never wraps to a second
row, because a wrapped tablist changes height as the selection moves.

### Multi-input / OTP field

Anatomy: label → a row of four to eight `otp-cell` boxes with `s-2` between them
and a wider `s-4` gap at the group midpoint for six or more → hint or error line.

Implementation: one visually hidden `<input inputmode="numeric"
autocomplete="one-time-code" maxlength="6">` holds the real value, and the cells
are presentational boxes driven by it. This is what makes paste, platform
autofill, and password managers work: the most common failure of hand-rolled OTP
fields and a WCAG 2.2 (3.3.8) requirement, since users must not be forced to
transcribe by hand.

States: empty, focused (ring on the group, caret in the current cell), filled
(border firms to `on-surface-2`, `ease-spring` pop), complete (auto-submits after
a 150ms settle), invalid (all cells `error`, message below, value preserved so
the user can correct rather than retype), disabled.

Keyboard: digits advance; `Backspace` on an empty cell steps back and clears the
previous; `←` / `→` move; paste fills from the clipboard with non-digits
stripped; `Escape` clears the group.

Notes: announce progress politely through a live region ("3 of 6 entered")
rather than announcing each keystroke. Never mask the digits.

### Menu (including the account menu)

Anatomy: trigger: an avatar at `avatar-sm` in the navigation, with an optional
name at `md`+ → `menu` → header (avatar, name, email at `body-xs` /
`on-surface-3`) → `divider` → item groups → destructive item last, separated and
colored `error`.

Roles: trigger `<button aria-haspopup="menu" aria-expanded>`, menu `role="menu"`,
items `role="menuitem"`, or `menuitemradio` for the theme row, which is a
segmented control inside the menu.

Keyboard: `Enter` / `Space` / `↓` open and focus the first item; `↑` opens
focusing the last; arrows wrap; type-ahead by first letter; `Escape` closes and
returns focus to the trigger; `Tab` closes the menu and continues through the
page.

Notes: unlike the select, DOM focus *moves into* the menu: menus own their
focus, listboxes do not. The menu is aligned to the trigger's end edge and flips
to the start edge within 280px of the container edge. In a `compact` container it
becomes a sheet with the same roles and the same items.

### Accordion

Anatomy: a stack of items, each `[trigger: heading + chevron]` plus `[panel]`.
The trigger is a full-width `<button>` inside a heading whose level matches the
surrounding document outline.

Variants: **bordered** (each item its own card, `s-3` between: for FAQ lists) and
**flush** (items separated by `outline` hairlines, no card: for dense reference
and inside rails); single-open or multi-open.

States: collapsed, expanded (`aria-expanded="true"`, chevron 180°), hover
(trigger background `scrim`), focus-visible, disabled item.

Keyboard: `Enter` / `Space` toggle; `↑` / `↓` move between triggers; `Home` /
`End` jump to first and last. Each trigger is a tab stop; panel content joins the
tab order only when expanded.

Notes, all three of which are the ways this component is usually built wrong:

**Open state lives on the item, not the trigger.** The trigger sits inside its
heading, so the panel is a sibling of the heading, not of the button. A selector
written as `.accordion-trigger[aria-expanded="true"] + .accordion-panel` matches
nothing and the panel never opens.

```css
.accordion-item[data-open="true"] > .accordion-panel { grid-template-rows: 1fr; }

/* Same result without JavaScript, where :has() is available */
.accordion-item:has(.accordion-trigger[aria-expanded="true"]) > .accordion-panel {
  grid-template-rows: 1fr;
}
```

`aria-expanded` on the trigger remains the accessibility truth; `data-open` on
the item is the styling hook, and the script sets both together.

**The panel owes its trigger a gap.** The trigger paints a full-bleed wash on
hover and while expanded, so panel content starts `s-4` below it (`s-3` flush)
and ends `s-6` above the item's edge. Without the top padding the answer sits
flush against the washed trigger and reads as part of the question.

**Find-in-page and the animation are sequenced, not simultaneous.**
`hidden="until-found"` applies `content-visibility: hidden`, which makes the
panel unmeasurable, so it cannot be removed and animated in the same frame. On
open, the attribute is dropped first and `data-open` is set on the next animation
frame; on close, `data-open` is cleared and the attribute is restored on
`transitionend`, with a timeout fallback. Where `beforematch` is unsupported the
attribute is skipped entirely. Deep links to an anchor inside a collapsed panel
open that panel before scrolling.

### Modal, drawer, sheet

The three overlay surfaces are one behavior at three anchors: `modal` is
centered, `drawer` enters from an inline edge, `sheet` enters from the bottom edge.
All three carry `modal` elevation, trap focus, close on `Escape`, lock body
scroll with scrollbar-width compensation, and return focus to the invoking
element.

Modal is built on `<dialog>` with `showModal()`; the native element supplies the
top layer, backdrop, focus trap, and `Escape` handling, and the polyfilled path
exists only for browsers that lack it.

Anatomy: backdrop (`overlay`) → dialog → header (title `headline-xs` plus a close
icon button) → body (scrollable, `body-sm`) → footer (actions, end-aligned at
`sm`+, full-width stacked below, primary action last in DOM and last visually).

Sizes: `modal-sm` for confirmations, `modal` default, `modal-lg` for forms. In a
`compact` container the modal becomes a `sheet`.

States: closed, entering (`opacity` plus `translateY(16px)` plus `scale(0.98)`
over `duration-slow`, `ease-out`), open, exiting (reverse over `duration-normal`).

Notes: `aria-labelledby` points at the title, `aria-describedby` at the body's
lead paragraph. A modal never opens another modal: a destructive confirmation
replaces the current modal's content instead.

### Pill, tag, badge, status dot, kbd

`pill` is the display chip (category, filter, meta). A filled `pill` is
attention-carrying and rare: one per card at most. Dots are 7px, `full`, and
always adjacent to a text label. An icon-only pill takes `aria-label`.
Interactive pills (filters) get hover and focus states and the full pointer
target; static pills get neither and are `<span>`, not `<button>`. `kbd` renders
a single key or chord in `mono-xs` on `surface-2`.

### Callout

`[status icon] [title (label-lg)] [body (body-xs)]` in an `md` container with a
tinted `*-surface` background and a 1px status border. Four tones: error,
success, warning, info: plus a neutral tone (`surface` and `outline`) for
asides. A callout announcing a *result of the user's action* takes `role="status"`
(polite) or `role="alert"` (assertive, errors only); an editorial callout takes
no role. Body copy caps at `measure-narrow`.

### Card

`lg` container, `flat` at rest, `raised` plus `outline-strong` on hover, media at
16/10 above an `s-5` body. When the whole card is a link, the anchor wraps the
title and is stretched over the card with a pseudo-element, never wrap the
entire card in an `<a>` containing other interactive elements. Card titles are
`headline-sm`; a card never contains an `h1` or `h2`. Card internals resolve from
the `card` container query, so the same card lays out correctly in a `wide`
gallery and in a 320px inspector.

### Table

Wrapped in a scroll region (`md` radius, `outline` border) with a `min-width` on
the table itself. Header row: `caption-md` uppercase on `surface-2`. Cells:
`body-xs`, `s-4` padding, `outline-soft` row rules, last row ruleless. Numeric
columns are right-aligned and tabular. The scroll container takes `tabindex="0"`
and an `aria-label`, and it owns the horizontal overflow: cells do not truncate,
and code inside a cell never wraps.

Below `medium`, a table with more than four columns may switch to a stacked
row-per-record presentation, in which each cell is prefixed by its header. That
is a presentation change only; the DOM stays a `<table>`.

### Code block

Structure and behavior are in Interaction Patterns → Code presentation.
Visually: `md` radius, `code-surface` fill, a `code-toolbar` strip carrying
filename, language, and copy, optional line numbers in a `code-gutter` column,
and `code-highlight` washes for called-out lines. Long lines scroll horizontally;
they never wrap by default, and a wrap toggle sits in the toolbar.

### Avatar

`full` radius, `surface-2` fill, 1px `outline`. Sizes `avatar-xs` through
`avatar-xl`. The fallback is initials at `label-md` centered on `surface-3`, never
a generic silhouette. Stacked groups overlap by 30% with a 2px `surface` ring and
a `+N` counter chip after the fourth.

### Charts

A chart is a picture of a table, and the table is always in the DOM, not as a
fallback, but as the representation the chart is rendered *from*. Treating it as
a fallback is exactly how it ends up stale, unlabelled, or dropped in a refactor,
which is the usual reason charts are inaccessible in practice.

**Library.** ApexCharts, bundled rather than loaded from a CDN, and themed rather
than restyled. A theme adapter reads the computed value of every chart token and
returns an options object; the caller's options are deep-merged underneath it. A
token change therefore reaches every chart at once, and a theme change re-reads
the tokens rather than re-creating the chart. If the token layer cannot be read,
the series ramp falls back to literal values rather than letting the library use
its own off-system palette. With the library absent entirely, the plot is hidden
and the table takes over.

**Tokens.** `series-1…8` are categorical roles pointing at `ramps.viz-*`; charts
read the roles, never the ramp. `chart-grid`, `chart-axis`, `chart-label`,
`chart-track`, `chart-tooltip`, and `on-chart-tooltip` carry the chrome and are
all re-tuned in dark. The series hues are **not** re-tuned: a hue chosen to clear
3:1 on both page surfaces already clears it on both themes.

**Never color alone.** Legend keys carry a shape as well as a hue, lines carry a
dash pattern past four series, and a delta carries an arrow and a sign. Past four
categorical series a palette stops communicating. Use direct labelling, small
multiples, or "top four and the rest".

**The legend is ours.** The library's legend is suppressed and replaced with real
`<button aria-pressed>` entries, so a series can be toggled from the keyboard and
announces its state. The plot carries `role="img"` with `aria-labelledby` on the
title and `aria-describedby` on the table.

**Degradation is specified, not incidental.** Under `prefers-reduced-motion`
entrance animation is disabled in the options object so it never runs; under
`forced-colors` the plot is hidden entirely, because an SVG plot loses its
palette and becomes a set of identical shapes; in a `compact` container a figure
marked `data-collapse="table"` shows the table instead.

## Navigation Patterns

A page asks two independent "where am I" questions: *what product is this* and
*where am I inside this page*. The chrome answers only the first. In-page
navigation lives in the rails and the drawer, never in a second row, because a
second row costs vertical space on every screen to answer a question most
readers are not asking.

### One row, three islands

```
+------------------+        +--------------------------------+        +---------------+
| [mark]  Neue     |        | Overview  Foundations  ...     |        | [Q] [O] [=]   |
+------------------+        +--------------------------------+        +---------------+
   brand                            navigation                            actions
   1fr, justify start               auto, centered                         1fr, justify end
      <---- page scrolls visibly through these gaps ---->
```

The navigation stack is `position: sticky; top: 0` with `nav-top` of padding,
holding a single row. That row is a three-column grid (`1fr auto 1fr`) capped
at `shell` and carrying **the same responsive gutters as the shell**. The shared
gutter is what makes the brand island's start edge land on the sidebar rail and
the actions island's end edge land on the contents rail, at every width,
orientation, and window size.

The `1fr auto 1fr` split is what balances the row: the navigation island is
optically centered regardless of how wide the brand or the action cluster
happens to be, and neither outer island can push it off center. Each island is
`nav-h`, `pill`, 1px `outline`, `float` elevation, with a translucent `surface`
and a backdrop blur where supported.

**The gaps are real.** The row sets `pointer-events: none` and each island
re-enables it, so the space between islands is not an invisible click blocker
across the top of the page. Content scrolls visibly through it, which is the
point of a floating navigation in a reading-first system: the page still reads as
a page rather than as a screen with a sealed top edge.

**They do not move.** No hide-on-scroll, no condense, no translate. Past 8px of
scroll the shadow deepens from `float` to `popover` and nothing else changes, so
the layout underneath never shifts. A navigation that disappears while you are
reading is one you have to hunt for.

**Each island declares its own track** (`grid-column: 1 | 2 | 3`). This is not
decoration: with the center island hidden, auto-placement flows the actions
island into the vacated `auto` track and the two islands bunch toward the middle
instead of spreading to the edges. An empty `auto` track collapses to zero width,
so explicit placement is what keeps the outer islands anchored.

| Width | Brand island | Navigation island | Actions island |
|---|---|---|---|
| `< xs` | Mark only — wordmark drops | Hidden (drawer) | Search · theme · menu |
| `xs`–`lg` | Mark and wordmark | Hidden (drawer) | Search · theme · menu |
| `lg`+ | Mark and wordmark | Inline links, current one filled | Search · theme (menu retired) |

Below `lg` the center track is empty and the two remaining islands sit at
opposite ends of the row, which is the correct narrow shape: two thumb-reachable
clusters with the whole width between them, rather than three cramped pills.

### In-page navigation

There is no second row. Section links live in the **contents rail** at `xl`+, in
the **drawer** below `lg`, and (at any width) in the page's own headings, which
are anchor targets. None of these occupies vertical space in the reading column.

**Sidebar rail (`lg`+).** At `lg` the drawer is retired and its contents become a
sticky start rail: grouped links, group labels at `mono-xs` uppercase, current
item on `surface-3` with a 2px `on-surface` start marker. The marker is an
absolutely positioned pseudo-element with `border-radius: 0`, not a border: a
border inherits the link's `sm` corner radius and bows away from the text edge,
which reads as a rendering error rather than an indicator. The rail is
`<nav aria-label="Docs">`, scrolls independently, and preserves its scroll
position across page loads.

**Contents rail (`xl`+).** A second sticky rail, `<nav aria-label="On this
page">`, listing `h2` and `h3` anchors with the active one marked. Scrollspy is
driven by `IntersectionObserver` with `rootMargin: "-{scroll-offset} 0px -70%
0px"`, which resolves "which heading is current" to the topmost heading in the
upper third of the viewport. The active link carries `aria-current="location"`.

**Drawer (below `lg`).** An end-edge sheet at `min(88vw, 380px)`, `modal`
elevation, sliding over `duration-slow` with `ease-in-out`. Contains the primary
links at `headline-sm`, the full documentation tree as a flush accordion, and the
theme control. Focus is trapped while open, `Escape` closes, the trigger's
`aria-expanded` reflects state, body scroll is locked, and focus returns to the
trigger on close.

### Navigation rules

- Exactly one item is `aria-current` per navigation region. The navigation island
  uses `aria-current="page"`; the rails use `aria-current="location"`.
- Current state is never color-only: the island's current link is a filled
  inversion, the contents rail carries a start marker, and the sidebar carries
  both a wash and a marker.
- The skip link is the first focusable element on the page, visible on focus, and
  jumps to `#main`, which carries `tabindex="-1"`.
- In-page anchors scroll with `scroll-behavior: smooth` (auto under reduced
  motion) and *move focus* to the target, not just the scroll position.
- Breadcrumbs appear only at three levels deep or more; below that the sidebar's
  current-item marker is sufficient and a breadcrumb is noise.
- **Navigation is never hidden at any size class.** It changes edge and
  presentation; it does not disappear.

## Interaction Patterns

### The focus system

Browser default focus rings are removed **globally and replaced globally**. The
two failure modes this avoids are `outline: none` with no replacement, and a ring
that is invisible in one of the two themes.

```css
:where(a, button, input, select, textarea, summary, [tabindex]):focus { outline: none; }

:where(a, button, input, select, textarea, summary, [tabindex]):focus-visible,
.focus-ring:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
  border-radius: inherit;
}

/* Grouped controls draw one ring on the group, not on each child. */
:is(.input-group, .otp-group, .segmented):focus-within {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
}

/* Programmatic focus on containers is silent. */
[tabindex="-1"]:focus { outline: none; }
```

Contract:

- **`:focus-visible`, never `:focus`.** Mouse users never see a ring; keyboard and
  switch users always do.
- **One indicator, and only one.** 2px of `focus` at a 2px offset of
  `focus-offset`, and nothing else: no darkened border, no halo, no glow. Stacked
  treatments read as a band of chrome around the control and make a focused field
  look like an error. `focus-halo` is retained as a token for forced-colors
  fallback work and is applied by no component.
- **Against every surface in both themes the indicator clears 17:1**, far past the
  3:1 required by 2.4.11 and 2.4.13.
- `outline-offset` is positive so the ring never overlaps the control's own
  border; `border-radius: inherit` keeps it concentric on both pill and
  rounded-rectangle controls.
- **Composite widgets draw the ring on the visual element**, not the hidden input
  (`.check input:focus-visible ~ .box`), and grouped controls draw one ring via
  `:focus-within`. Only one ring is ever visible at a time.
- **A member does not repeat what its group already says.** While the OTP group
  is focused it draws the ring, so the active cell firms its border by one step
  and shows the caret rather than taking a `primary` border.
- **Composite fields size to their contents, not their column**
  (`align-self: start; width: max-content`). As a stretched flex child, an OTP
  group is full-column width and the ring is drawn around the column rather than
  around the cells.
- **Every field reserves 3px of bleed.** The ring paints outside the border box,
  so a control flush against its container's edge gets it clipped. Field
  wrappers carry `padding: 3px; margin: -3px`, which reserves the space and then
  removes it from the layout: spacing is unchanged and the ring always has
  somewhere to land.
- **Nothing the sticky chrome could cover.** Focusable elements set
  `scroll-margin-top: var(--scroll-offset)`, so a focused element never comes to
  rest under the navigation stack (2.4.11 and 2.4.12).
- `@media (forced-colors: active)` swaps to `outline: 2px solid CanvasText` and
  restores system colors; no token is trusted in forced-colors mode.

### Hover, press, and disabled

Hover is a *color* change (`scrim` wash, border darkening, opacity on filled
surfaces) over `duration-fast`. Press is a *transform* (`scale(0.97)`, icon
buttons `0.95`) over `duration-instant`. Hover states are suppressed under
`@media (hover: none)` so touch devices do not get sticky hover. Disabled
controls lose pointer events and drop to `surface-3` / `on-surface-3`; when the
reason matters, `aria-disabled` is used instead so the control stays focusable
and can explain itself.

### Controllers bind once

Every controller is bound inside a single `boot()` guarded by a flag on the root
element. A double-bound toggle fires an even number of times and cancels itself
out, which presents as "the control does nothing" rather than as an error: the
hardest class of bug to see. The guard makes a duplicate script include harmless.

### Code presentation

Code is a first-class content type here, not styled `<pre>`.

- **Structure:** `figure.code` → `figcaption.code-toolbar`
  (`[lang badge] filename … [wrap] [copy]`) → `pre[tabindex="0"]` → `code`.
  `tabindex="0"` on the `pre` makes the horizontally scrollable region keyboard
  reachable, and it carries an `aria-label` naming the sample.
- **Tokenisation:** highlighting wraps tokens in `<span class="tok-*">`, one class
  per `colors.code-*` role. Every syntax color is a token; there is no
  hard-coded hex in any theme. Languages covered by the reference implementation:
  HTML, CSS, JavaScript/JSX, JSON, Markdown, Bash, YAML. An unknown language
  degrades to plain `code-plain`, never to an approximate highlighter, which
  produces confidently wrong colors.
- **Semantics over rainbow:** seven roles carry meaning (keyword, string, number,
  function, attribute, tag, comment) and comments are deliberately the lowest
  contrast in the set (still ≥4.5:1) so they recede without disappearing.
- **Line numbers** are an opt-in `data-line-numbers` attribute, rendered as a
  `code-gutter` column that is `user-select: none` so copied code stays clean.
- **Highlighted lines** (`data-highlight="3,7-9"`) get a full-bleed
  `code-highlight` wash plus a 2px `primary` start marker, not color alone.
- **Diff** lines use `code-added` / `code-removed` for the text *and* a `+` / `−`
  gutter glyph.
- **Wrapping:** off by default. Code scrolls; a wrap toggle in the toolbar is
  per-block and remembered for the session.
- **Copy** writes to the clipboard, swaps the icon to a check for 1600ms, and
  announces "Copied" through a polite live region.
- **Inline chips are tinted when (and only when) the whole chip is one
  machine-readable pattern.** In an achromatic system, token names and values set
  in neutral ink blend into the prose around them, so a chip whose entire content
  is a token (`--color-primary`), a value (`16px`), a quoted string, or a literal
  (`true`) takes the matching audited syntax role. Mixed or prose-ish chips: file
  names, phrases, attribute-and-value pairs: stay neutral. Whole-chip is the line
  because substring painting turns color back into decoration, and the point of
  the tint is a guarantee: *this exact string is machine-readable as written*.
  Inline chips sit on `code-surface` so they inherit the audited contrast
  guarantees without a second audit matrix. Inline code never appears inside a
  heading.

### Scroll and reveal

Sticky elements are `position: sticky` with explicit `top` values from the
z-ladder. Scroll-linked reveals fire once. Anchor navigation both scrolls and
moves focus. `scroll-padding-top: var(--scroll-offset)` is set on the root so
browser-native anchor jumps (back button, find-in-page) also clear the chrome.

### Copy, feedback, and undo

Every action that changes state confirms it in the same vocabulary as the control
that triggered it: "Publish" produces "Published". Confirmations for destructive
actions are modals with the destructive verb on the button ("Delete draft", never
"OK"). Where undo is possible it is offered in the confirmation rather than the
action being blocked by a dialog.

## Forms

### Structure

`<form>` → a `fieldset` per logical group (legend at `label-md`, styled as a
`mono-xs` uppercase eyebrow) → field rows → actions. Fields stack in a single
column at all widths; two-up rows appear only in an `expanded` container and only
for genuinely paired values (first and last name, city and postcode). Vertical
rhythm comes from the contract in Layout & Spacing.

### Labels and help

- Every field has a visible `<label for>`. Placeholder text is an *example*, not
  a label, and disappears on input. It is never the only description.
- Hint text sits below the field at `body-xs` / `on-surface-3`, is linked with
  `aria-describedby`, and states the constraint *before* the user hits it ("At
  least 12 characters"), not after.
- Optional fields are marked "(optional)"; required fields are not marked with an
  asterisk. Where most fields are required, marking the exceptions is less noise
  and unambiguous for screen readers.

### Validation

- **Validate on submit, and on blur only for fields the user has already
  completed and left invalid.** Never validate on keystroke: it flags a
  half-typed email as wrong.
- An invalid field gets `aria-invalid="true"`, an `error` border, and a message
  below in `error` with a leading status icon. Three channels, not color alone.
- On failed submit, focus moves to the first invalid field and a `role="alert"`
  callout appears above the actions listing the failures as links to each field.
- Error text names the fix, not the failure: "Enter a date in the future", not
  "Invalid input".
- Success is a `role="status"` callout plus the form returning to a clean state.
  A form that has just submitted successfully never silently resets.

### WCAG 2.2 specifics

- **3.3.7 Redundant Entry.** Information already given in this process is
  pre-filled or offered for selection ("same as billing address").
- **3.3.8 Accessible Authentication.** The OTP field accepts paste and autofill;
  no field in the system blocks paste; no step requires transcription,
  puzzle-solving, or memorisation.
- **2.5.7 Dragging Movements.** Nothing in the system requires a drag; any future
  reorder control must ship keyboard and click alternatives.
- **3.2.6 Consistent Help.** The help affordance sits in the same place in the
  actions island on every page.
- Autocomplete tokens (`name`, `email`, `one-time-code`, `new-password`) are set
  on every field that has one.

## Loading States

Loading is communicated by the shape of the thing that is coming, at the place it
will appear. Three mechanisms, each with one job.

| Mechanism | Use when | Behaviour |
|---|---|---|
| **Skeleton** | The layout is known and the wait is >300ms | `surface-3` blocks matching the real content's shape; a 1.6s shimmer that stops after 10s and holds still. Never for text under two lines |
| **Inline spinner** | A control is working (submit, copy, refresh) | `spinner` replaces the leading icon; label unchanged; button width locked; `aria-busy="true"` on the control |
| **Progress bar** | Determinate work with a known total (upload) | `progress-track` plus `progress-fill`, with `aria-valuenow` |

Rules. Nothing shows a loading state before 300ms: a fast response that flashes
a skeleton feels slower than no indicator at all. The region being replaced is
`aria-busy="true"`, and the result is announced once through a polite live region
("12 components loaded"), never per item. A skeleton is `aria-hidden`; the live
region carries the meaning. Under reduced motion the shimmer is replaced by a
static fill.

**Skeletons preserve the exact final layout**, so there is zero cumulative layout
shift on resolve. That is a size contract, not a resemblance: a skeleton block
carries the same box as the thing it replaces: a media skeleton declares the same
`aspect-ratio` as the media, with `flex: 0 0 auto` so it cannot absorb its card's
spare height. It must **not** be capped with `max-height`: on a stretched flex
child the browser resolves *width* from the ratio once height is constrained, and
the block comes out narrower and taller than its card and breaks out of it.

## Empty States

An empty screen is an instruction, not an apology. Every empty state has three
parts and, unless the emptiness is a *result the user caused*, a fourth.

1. **Icon**: `icon-2xl`, `on-surface-3`, stroke, naming the missing thing.
2. **Title**: `headline-xs`, stating what is not here in the user's words: "No
   components yet".
3. **Body**: `body-sm`, `on-surface-2`, one sentence saying what to do: "Add your
   first component to see it in this gallery."
4. **Action.** A `primary` button performing exactly that, when there is an
   action to take.

Three flavours:

- **First run** (nothing has been created): all four parts; the action is the
  point of the screen.
- **No results** (a filter or search excluded everything): the title names the
  query, the body suggests a broader term, the action is "Clear filters". Never
  show a first-run illustration here: the user has data, they just cannot see it.
- **Cleared** (the user emptied it deliberately): a quiet single line, no
  illustration, no action. Do not congratulate someone for reaching zero twice.

Layout: `empty-state`, centered in the region it replaces, capped at
`measure-narrow`, on `surface` inside the container's existing border: an empty
state never introduces its own card. In menus and selects it shrinks to a single
`body-sm` / `on-surface-3` row ("No matches") and the region carries
`role="status"` so the change is announced.

## Error States

Errors are matched to blast radius. The system distinguishes four.

| Scope | Presentation | Recovery |
|---|---|---|
| **Field** | `error` border, message below, `aria-invalid` | Inline and immediate; the value is preserved |
| **Form** | `role="alert"` callout above the actions, linking to each failed field | Fix and resubmit |
| **Region** | The region's content is replaced by an inline error block (icon, one-line cause, "Try again") | Retry that region only; the rest of the page stays usable |
| **Page** | Full-page state using the empty-state layout at `headline-md` | "Reload", plus a route back to something that works |

Rules:

- **Say what happened and what to do.** "Could not load components. Check your
  connection and try again." Not "Something went wrong."
- **Never blame, never apologise.** Errors are in the interface's voice, not a
  person's. No "Oops", no "Sorry", no exclamation marks.
- **Preserve the user's work.** A failed submit never clears fields. A failed save
  keeps the draft and says the save failed, rather than reverting.
- **Expose technical detail behind a disclosure**, not in the message. A flush
  accordion labelled "Technical details" containing the request ID and status in
  `mono-md` serves support without taxing everyone else.
- **Errors announce once.** `role="alert"` on the container; retries update the
  same node rather than stacking new alerts.
- **Offline is a distinct state**, not a generic error: a `warning` callout pinned
  below the navigation stack, auto-dismissing when connectivity returns.
- 404 and 500 pages use the page scope, keep the full navigation: a broken URL
  should not also strip the way out, and offer search.

## Accessibility

**Target: WCAG 2.2 Level AA, in both themes, at every size class and every
breakpoint.** Where the system already exceeds it, the stricter value is the
requirement.

**Color and contrast.** Body text ≥4.5:1, large text ≥3:1 (the system holds
≥4.5:1 for all text), interactive boundaries and state indicators ≥3:1. Full
measurements are in Colors. No information is carried by hue alone anywhere:
status pairs hue with icon and text, the current navigation item pairs it with
fill, validity pairs it with a message, diff lines pair it with `+` / `−` glyphs,
and chart series pair it with shape and dash.

**Keyboard.** Every interactive element is reachable and operable by keyboard, in
DOM order, with a visible `:focus-visible` indicator. No positive `tabindex`.
Focus is trapped only inside modals, drawers, and sheets, and is always restored
to the invoking element on close. Composite widgets follow APG roving-tabindex or
`aria-activedescendant` patterns as documented per component. `Escape` closes the
topmost dismissible layer and nothing else.

**Structure and semantics.** One `h1` per page; heading levels never skip.
Landmarks come from the region roles in the frontmatter: `banner`, `navigation`,
`toolbar`, `main` (`id="main"`, `tabindex="-1"`), `complementary`, `contentinfo` —
and each repeated landmark type is labelled. Lists are lists, buttons are buttons,
links navigate and buttons act. `lang` is set on `<html>`. Page titles are unique
and lead with the page name.

**Motion, timing, targets.** Reduced motion is honoured globally with complete
still states. Nothing auto-plays, auto-advances, flashes more than three times per
second, or imposes a time limit. Pointer targets meet the floor for the pointer in
use, which is 44px for touch. All pointer-driven functionality has a keyboard
equivalent; nothing requires a drag (2.5.7) or a path-based gesture (2.5.1).

**Adaptive behavior is an accessibility contract, not only a layout one.** A
region that withdraws to `sheet` or `overlay` keeps the same accessible name,
role, and item order it had while docked. Presentation changes; the semantics do
not. This is what makes a screen learnable on one device and usable on another.

| WCAG 2.2 SC | How this system satisfies it |
|---|---|
| 2.4.11 Focus Not Obscured (Min) | `scroll-margin-top` / `scroll-padding-top` at `scroll-offset` |
| 2.4.12 Focus Not Obscured (Enh) | The navigation stack is a fixed height that the scroll offset always clears, so no focused element ever comes to rest beneath it. The chrome does not hide on scroll; the offset does the work |
| 2.4.13 Focus Appearance | 2px indicator at 2px offset, ≥17:1 against every adjacent surface |
| 2.5.7 Dragging Movements | No drag-only interaction exists |
| 2.5.8 Target Size (Min) | 44px floor for touch, well past the 24px requirement |
| 3.2.6 Consistent Help | Help sits in the actions island, in the same position sitewide |
| 3.3.7 Redundant Entry | Previously entered values are pre-filled or selectable |
| 3.3.8 Accessible Authentication (Min) | OTP accepts paste and autofill; no transcription or cognitive test |

**Assistive-technology behavior.** Live regions are used sparingly and politely:
one polite region for copy and status confirmations, `role="alert"` reserved for
errors the user must act on. Icon-only controls carry `aria-label`. Decorative SVG
is `aria-hidden`. Images have meaningful `alt`, or `alt=""` when decorative.
`prefers-contrast: more` thickens hairlines to `outline-strong` and raises muted
ink to `on-surface-2`. `forced-colors: active` drops all backgrounds and shadows
and relies on system colors with `CanvasText` borders.

**Testing floor.** Before a component is considered done: keyboard-only pass,
screen-reader pass (VoiceOver/Safari and NVDA/Firefox), 200% zoom with no loss of
function, 400% zoom reflow to a single column with no horizontal scroll, both
themes, reduced motion, forced colors, every size class from `compact` to
`xlarge`, and automated axe-core with zero violations.

## Do's and Don'ts

### Tokens

| Do | Don't |
|---|---|
| Resolve every value to a token: `var(--color-on-surface-2)` | Write `#424242`, `rgba(0,0,0,.5)`, or `13px` in a component |
| Add a token when a genuinely new role appears | Add a token for a one-off tint |
| Name tokens by role, appearance, or function | Name tokens by content or page: `hero-grey`, `docs-border` |
| Override by role name in `themes.dark` | Duplicate the whole color block for dark |
| Put consumable scales in the frontmatter | Leave a scale in a prose table where a build cannot read it |

### Color

| Do | Don't |
|---|---|
| Use `outline-strong` for the boundary of any control | Draw an input with `outline` — it looks right and fails 1.4.11 |
| Pair every status hue with an icon and a label | Rely on a red border alone to mean "invalid" |
| Keep the palette achromatic | Introduce a decorative accent hue; it would break the "color means something" contract |
| Use `*-surface` tints for callout backgrounds only | Set status colors as text on saturated fills |

### Typography

| Do | Don't |
|---|---|
| Build hierarchy from size, color, and space | Reach for weight 600+; it does not exist here |
| Use mono for machine-authored content | Use mono for emphasis or for a "technical" mood |
| Cap prose at `measure` | Let paragraphs stretch to the full `wide` container |
| Set negative tracking above 18px only | Letter-space body text or lowercase labels |
| Keep a truncated string recoverable | Ellipsis a value the user then has no way to read |

### Layout

| Do | Don't |
|---|---|
| Resolve every structural decision from container width | Write a media query against the viewport in a shell that can be nested |
| Reach for an intrinsic primitive before a size class | Add a sixth size class; add a primitive, or record the gap |
| Break wide content out of the reading column | Widen the reading column to fit a table |
| Let surplus width become margin | Treat a wider screen as a license for a longer line of text |
| Use the 4px scale for every gap | Type `18px` because `16px` "looked tight" |
| Give every wide child its own scroll container | Rely on `overflow-x` on the page to hide a layout bug |
| Set `minmax(0, 1fr)` on grid content tracks | Let a code block blow out the shell grid |
| Declare an overflow answer for every region | Ship a toolbar that neither collapses nor scrolls |
| Keep the adaptation policy as data | Branch on size class in component code; a policy that cannot be diffed will drift |

### Components and interaction

| Do | Don't |
|---|---|
| Replace the focus ring globally when you remove it | Write `outline: none` anywhere without the paired `:focus-visible` rule |
| Use `pill` for controls, `md`/`lg` for containers | Mix the two, since shape is the affordance signal in a colorless palette |
| Use `<dialog>` and native `showModal()` | Hand-roll a focus trap when the platform ships one |
| Keep one `primary` button per view | Stack two filled buttons side by side |
| Let the OTP field accept paste and autofill | Build six separate inputs that break password managers |
| Give a scrollable region `tabindex="0"` and a label | Ship a table a keyboard user cannot scroll |
| Give an icon-only control a real `aria-label` | Let a tooltip be the only label |
| Let a region change presentation as space shrinks | Let a region become *more* prominent as space shrinks |

### Motion and content

| Do | Don't |
|---|---|
| Animate `transform` and `opacity` | Animate `height`, `top`, or `width` |
| Give reduced motion a complete still state | Leave `opacity: 0` behind when animation is disabled |
| Write errors that name the fix | Write "Oops! Something went wrong." |
| Say "Publish" → "Published" | Say "Submit" → "Success!" |

## Assumptions

Everything in this section is inference, not confirmed requirement. Each item
states what was assumed and what it was inferred from.

### About the product

1. **Product and scope.** The source artefacts are a style guide for "Neue": a
   reading site plus its design-system documentation, and a separate layout kit
   authored under the name "Studio". They are assumed to be one product family:
   a publication, its reference documentation, and the tool surfaces around them.
   No product brief, roadmap, or analytics were supplied.
2. **Default theme is light.** The source sets the light theme explicitly on
   first paint. Retained, with an added `prefers-color-scheme` default and a
   persisted user override.
3. **The palette carries no brand hue.** The source is achromatic except for four
   status colors. Treated as intent rather than as an unfinished palette;
   `primary` and `on-primary` are exposed separately so a brand hue can be
   introduced later without touching text roles.
4. **No content model, auth, search backend, or i18n requirement was given.**
   Search is specified as a UI affordance only. The system is LTR-authored;
   logical properties are used throughout so RTL is mechanical, but RTL is
   untested.
5. **Six shells cover the organisation's deliverables.** Taken from the layout
   kit, which had already validated the set. Adapted rather than adopted: its
   cascade layers, class prefix, and adapter targets were left behind; the region
   vocabulary, size classes, and primitive API were kept, because they are the
   parts a second team has to agree with.

### About the design decisions

6. **Contrast corrections were required and are non-negotiable.** The source's
   muted ink reached only ~4.0:1 on the page field and was used at 11–12px, and
   its control borders reached 1.27:1. Muted ink was darkened and `outline-strong`
   was introduced. These change the rendering slightly; the alternative was
   shipping known AA failures.
7. **`content` is 780px because it is derived.** It is the widest container in
   which `body-md` still lands under 72ch with gutters applied. "Better utilises
   modern displays" was read as *more room for non-prose*, which is why `wide`
   exists rather than a wider reading column.
8. **One navigation row, and no second row.** The split floating navigation was
   the requirement; a sticky section rail beneath it was not, and it cost 124px
   of viewport and gave the page a third alignment. In-page discovery moved to
   the rails, which were carrying it at `lg`+ anyway.
9. **Phosphor is the icon vocabulary, not the delivery mechanism**, and fonts and
   charts are bundled rather than fetched. One no-network-dependency rule now
   governs icons, fonts, and the charting library; the source had a CDN in each.
10. **Syntax scheme is authored, not adopted.** No highlighting theme was
    specified, so a seven-role scheme was derived from the palette and tuned to
    ≥4.5:1 on `code-surface` in both themes. Any highlighter can be adapted by
    mapping its classes onto `colors.code-*`.
11. **ApexCharts is the charting library.** Stated as a preference, taken as a
    decision. The theme adapter is a thin translation layer, so a move to another
    library would be a rewrite of that adapter and nothing else. No chart token is
    library-specific.
12. **Component states are inferred from convention** (WAI-ARIA Authoring
    Practices) wherever the source had no equivalent component.

### About the format

13. **`elevation`, `ramps`, `sizeClasses`, `grid`, `regions`, `adaptation`,
    `overflow`, `shells`, `primitives`, `density`, and `environment` are
    extension token groups.** The DESIGN.md format standard accepts unknown token
    groups with a warning. Each of these is consumed by a build, so each is
    tokenised rather than described in prose, and each is documented in the
    section that governs it.
14. **`ramps`, not `palettes`.** The format standard reserves `palettes` for
    swappable section role-sets bound through abstract active-palette roles. This
    system's ramps are a raw source layer that components never read, which is a
    different mechanism; naming it `palettes` would claim a behavior the system
    does not have. If section-scoped role-sets are needed later, a real `palettes`
    group can be added alongside without disturbing this one.
15. **Section naming follows the format standard where it differs from the brief's
    wording.** "Color System" maps to §4 Colors; "Layout & Spacing", "Component
    Guidelines", and "Navigation Patterns" are accepted aliases; the three state
    sections ship top-level in the standard's required order (Loading, Empty,
    Error).

### Inconsistencies resolved in consolidation

The two source documents disagreed in the following places. Each was resolved in
one direction, and the reasoning is recorded so the decision is reviewable rather
than silent.

| Conflict | Sources | Resolution |
|---|---|---|
| Two spacing scales: `s-1…s-12` and a `0…24` multiplier scale | design / layout | Kept `s-1…s-12`; it is referenced by 101 component definitions. The ×4 multiplier is documented as a column in the scale table |
| Two rail widths (`sidebar` 260px, `toc` 220px) alongside a single symmetric `rail` 248px | design internal | One token, `rail`. Symmetric rails were the stated intent; two tokens made drift possible |
| `shell` stated as 1440px, but its own parts sum to more | design internal | `shell` is now derived (1468px) and the derivation is written down |
| `scroll-offset` 108px in tokens, 140px in prose, `rail-top` as a third name | design internal | One derived token: `nav-stack` + `s-7` = 112px, used for both the anchor offset and the rail pin |
| Density `0.75 / 1 / 1.35` versus `0.875 / 1 / 1.125` | design / layout | Took the layout kit's gentler pair. At 0.75 the scale falls off the 4px grid at every step and small controls approach the target floor |
| One pointer target (`tap-min` 44px) versus three (`fine` / `coarse` / `remote`) | design / layout | Kept all three, with `target-coarse` (44px) as the system-wide default floor and `fine` restricted to pointer-only dense surfaces |
| Focus ring offset given as 1px in one bullet and 2px in the CSS and the WCAG table | design internal | 2px, matching the CSS, the token, and the measured 17:1 |
| Input radius described as `pill` in prose but `md` in tokens | design internal | `md`. The Shapes section's trimodal rule is the governing statement |
| Navigation described as "one sticky bar in three sections" and as "three floating islands" | design internal | One row, three islands. Both terms now name distinct things in the glossary |
| WCAG 2.4.12 justified by "the nav hides on scroll", which the Navigation section forbids | design internal | Rewritten: the offset clears the fixed chrome; nothing hides |
| Charts loaded from a CDN against a stated no-network-dependency rule | design internal | Bundled. The rule now covers icons, fonts, and charts alike |
| Gallery column counts given both as a breakpoint table and as an intrinsic rule | design internal | Intrinsic only. The table now declares cell minimums and gaps, not counts |
| Two layout vocabularies for the same idea (`sizes` versus `sizeClasses`) | design / layout | `sizeClasses`, matching the layout kit and avoiding collision with the component `size` property |

## Open Questions

Each of these is a decision this document cannot make on its own.

1. **Is there a brand hue coming?** If a marketing palette exists, `primary` and
   `on-primary` are the only tokens that should change, and the status ramp would
   need re-checking against it. Confirm before anyone hard-codes "primary =
   black".
2. **One color vocabulary, or two?** The org standard's names (`--color-border`,
   `--color-text`) and this system's (`--color-outline`, `--color-on-surface`) are
   both published, with the standard's defined as references. Two vocabularies is
   a comprehension cost even when it is not a correctness one. If the org wants a
   single set, the rename is one mechanical pass.
3. **Does the `500`-is-canonical rule survive contact with the contrast floor?**
   Status colors point at `600` because `500` does not reach 4.5:1 as text on
   white in these ramps. Either the standard's ramps should darken at `500`, or
   the rule should read "`500` is canonical for fills; text selects the first step
   that meets the floor". Worth resolving centrally rather than per product.
4. **Should the layout kit ship as a separate package?** A second product adopting
   the shells but not the component library would want the layout layer alone,
   which argues for splitting it, but a split invites the two halves to drift, and
   the drift between the two source documents is what this consolidation just
   spent its effort undoing.
5. **Should `wide` break-outs exist below `xl`?** They currently reach full width
   only at `xl`, which means a 1180px laptop shows galleries at roughly 940px
   while the sidebar takes its rail. An alternative is to suppress the sidebar on
   gallery-heavy pages. Needs a decision informed by real traffic widths.
6. **Is the symmetry cost at `lg` acceptable?** Holding three tracks from `lg`
   upward gives a 536px reading column at 1024px, against roughly 640px from an
   asymmetric two-track grid, in exchange for a page that does not shift sideways
   on resize. The trade is stated, not hidden; it should be confirmed against real
   traffic.
7. **Search: local or backend?** The actions island reserves the slot and the
   keyboard shortcut, but scope, indexing, and result presentation are undefined.
   If it is remote it needs its own loading, empty, and error states from this
   file's patterns.
8. **Toast and notification stack.** `toast` is tokenised and has a z-ladder slot,
   but the stack position, maximum count, dismissal contract, and interaction with
   the polite live region are unspecified.
9. **Dark-theme first paint.** The reference implementation reads
   `prefers-color-scheme` in a blocking inline script to avoid a flash. Confirm
   this is acceptable to the CMS's script policy, or move the theme attribute to
   server-side rendering.
10. **Localisation and long strings.** Segmented control labels and navigation
    links are sized for English. German or Finnish would overflow the segmented
    control in a `compact` container; the fallback to a select is specified but
    the threshold is a guess. RTL is mechanical but untested.
11. **Print styles.** Not specified. A reading-first system probably wants them:
    hide chrome, expand accordions, print link URLs, force the light theme, and
    switch region overflow to `paginate`.
12. **Does the OTP field need a resend timer?** The component handles entry but not
    the surrounding flow (send, expiry, resend cooldown) which is a product
    decision with its own copy requirements.
13. **Which chart types still need specifying?** Area, bar, line, scatter, and
    sparkline are specified. Stacked bars, box plots, histograms, heatmaps, and
    geographic maps have tokens but no worked pattern and no accessibility
    contract yet.
14. **Is there a second typographic identity to reconcile?** The layout kit
    shipped a different, licensed font stack. Neue stays on DM Sans and JetBrains
    Mono. If the org intends one typographic identity across both, that is a
    decision above this document, and a licensing question before it is a design
    one.
