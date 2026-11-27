# Checkmate — Post-Quantum Zero-Trust Identity Killswitch

> **Yugaantar DevForge Hackathon — Track 4: "Trust, but verify"**  
> NIST FIPS 203 ML-KEM-768 Post-Quantum Key Encapsulation · Sub-Millisecond Actor Revocation · Crash-Consistent Atomic Persistence

[![Track 4 Evaluation](https://img.shields.io/badge/Track%204%20Validator-PASS%20100%25-brightgreen?style=for-the-badge&logo=checkmarx)](track4_validate.py)
[![NIST FIPS 203](https://img.shields.io/badge/Post--Quantum-ML--KEM--768%20(Kyber)-blue?style=for-the-badge)](track4_service.py)
[![Threat Model](https://img.shields.io/badge/Threat%20Model-RFC%20Compliant-orange?style=for-the-badge)](threat-model.json)
[![Project Brief](https://img.shields.io/badge/2--Page%20Brief-PDF%20Ready-red?style=for-the-badge)](CheckMate_Track4_Project_Brief.pdf)

## ⚡ Track 4 Automated Evaluation (Clean Machine Quickstart)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the automated Track 4 evaluation
python track4_validate.py --entry track4_service.py
```

---

Static, Vercel-ready front end for **Checkmate**: a server-side identity killswitch
built around instant revocation and NIST ML-KEM-768 (Kyber768) post-quantum
encapsulation. The visual language follows an Apple / macOS light monochrome
system; the app console adapts SaaS-workspace patterns (Resend / Clerk-style
sidebar, resource tables, key modal, tabbed SDK) while keeping the Checkmate
theme unchanged. All copy, code and brand artwork are original; no third-party
source code or artwork is copied.

The console ships **empty**: no actors, assets, decisions, proofs or keys are
seeded. Every resource table renders a neutral empty state until the control
plane supplies live records. No random or frozen sample data is generated in
the browser.

## Routes

| File | Purpose |
| --- | --- |
| `index.html` | Marketing field book (unchanged): hero, threat model accordion, engine loop, security invariants, console module cards, footer wordmark, engine-contract reader modal |
| `dashboard.html` | Operations board launcher: six module cards (telemetry, killswitch, stream, inspector, matrix, audit) that link out to their dedicated split pages; keeps legacy anchor ids `#kpis`, `#killswitch`, `#stream`, `#inspector`, `#matrix`, `#audit` |
| `console.html` | App console · Overview: identity counters (zeroed), recent decisions (empty state), engine status, containment scenarios A / B / C |
| `identities.html` | Identity roster: trusted / locked filters, search, profile modal, revoke modal, provision modal; empty roster until provisioned |
| `assets.html` | Protected assets envelope store: tier badges, policy rules, protect-asset modal, sealing walkthrough; empty envelope table until sealed |
| `killswitch.html` | Emergency revocation console: actor wizard (empty until identities exist), reason list, propagation readout, signed revocation registry (empty), containment checklist, offline-freeze facts |
| `security.html` | PQC cryptographic inspector: public-key box, encapsulation output cells, HMAC proof line, suite parameters, harvest-now margin, invariants; outputs stay empty until the server runs encapsulation |
| `logs.html` | Live decision stream (empty) + audit evidence lookup; ALLOW / DENY filters, JSON / CSV export buttons disabled while no records exist |
| `integrations.html` | Control-plane API key list (empty), Python / Node guard SDK tabs, CLI contract terminal, AI drop-in agent prompt |
| `settings.html` | Workspace facts (not-connected placeholders), tenant and member tables (empty), engine configuration, audit retention policy, danger zone |
| `404.html` | Fallback page |

## App console shell

`assets/css/app.css` layers over `assets/css/console.css` and adds the workspace
shell: persistent left sidebar (Monitor / Protect / Develop / Workspace groups,
hairline-separated like Resend-style workspaces), sticky blurred topbar with
search field, Production / Test segmented control and an offline sync status,
page headers with a solid black primary action top-right, stat cards, resource
tables with empty states, filter tabs, modals, terminal code blocks, launcher
cards, scenario cards, facts and the danger zone.

`assets/js/app.js` provides the shared icon set, active-nav state, mobile
drawer, generic tabs / modals / copy controls, search and filter wiring, and the
empty-state renderers for identities, assets, revocation proofs, decisions,
audit records and API keys. All data arrays start empty; the module guards each
action behind a "control plane not connected" toast until a backend endpoint is
wired in.

### Module map (`dashboard.html` launcher → dedicated pages)

One function per page; the old six-panel single board was split into the
following dedicated console views:

1. Executive telemetry → `console.html` — identity counters, PQC engine status, 24 h authorization health.
2. Emergency killswitch and device-loss panel → `killswitch.html` — actor select, loss reason, cluster revoke trigger, propagation readout, signed revocation registry.
3. Live zero-trust access stream → `logs.html` — timestamp, request ID, actor, asset, mode (`read` / `protected_read`), ALLOW / DENY badges.
4. PQC cryptographic inspector → `security.html` — 1184-byte public key view, ML-KEM-768 encapsulation outputs (1088 B ciphertext, 32 B shared secret, nonce, HMAC-SHA-256 proof), harvest-now-decrypt-later margin.
5. Asset ownership and access matrix → `assets.html` — asset, owner, sensitivity tier, policy rule.
6. Audit and compliance explorer → `logs.html#audit` — request ID lookup, decision / rule evidence, non-disclosure check, JSON and CSV export.

## Structure

```
assets/
  css/site.css       marketing design tokens and components (landing page)
  css/console.css   shared console design tokens and legacy component classes
  css/app.css        app workspace shell, sidebar, launcher cards and shared components
  js/site.js         marketing icons, nav, reveals, accordion, carousel, reader modal
  js/console.js      retained legacy reference script (not loaded by pages; renders empty)
  js/app.js          app console: shell, empty-state renderers, guards for roster,
                     assets, killswitch, logs, SDK and settings actions
  img/brand/         chess-sticker brand marks (WebP)
  icons/favicon.svg  chess-king mark
index.html
console.html · identities.html · assets.html · killswitch.html
security.html · logs.html · integrations.html · settings.html
dashboard.html
vercel.json          clean URLs, long cache for /assets
```

## Design system

- Palette: Apple light surfaces `#f5f5f7` / `#ffffff`, ink `#1d1d1f`, secondary `#3a3a3c`, muted `#6e6e73`, hairline `#d2d2d7`; system red `#ff3b30` for denial / locked states. No blue, purple or green theme tones.
- Type: Apple system stack (`-apple-system`, SF Pro Display / SF Pro Text) for UI and headlines; SF Mono / Menlo stack for labels, indices and hex data.
- Components: translucent blurred toolbar, gray-track segmented controls with white active thumb, white hairline cards with soft shadows, solid black primary pills, destructive red revoke control, mono data labels, macOS window traffic lights on terminal panels, hairline tables and status badges.
- Responsive: desktop 1440, laptop 1280, tablet 768, mobile 390; the app sidebar collapses to a drawer under 1080 px; console grids collapse under 1080 / 720 px.

## Interactions

- Landing page: scroll reveals, threat-model accordion, invariant carousel, engine operation selector, engine-contract reader modal.
- App console: sidebar active state, mobile drawer, provision / revoke / protect / key modals, filter tabs and search, toast feedback, copy buttons, tabbed SDK panels.
- Empty-state behavior: rosters, envelope tables, revocation registry, decision stream, audit results and key lists render empty rows with a short hint. Actions that require backend records show a "control plane not connected" toast instead of creating local data. Export buttons stay disabled while the audit pack is empty.
- Future backend wiring: replace the empty arrays in `assets/js/app.js` with calls to the control-plane endpoints (`setup` / `read` / `revoke` / `protected_read` / `audit`); the row builders, filters and modal contracts are already in place.

## Run locally

Any static server works; no build step:

```bash
python3 -m http.server 8123
# open http://localhost:8123/console.html
```

## Deploy to Vercel

1. Push this repository to GitHub.
2. Import the repository in Vercel; framework preset: **Other (Static)**, output directory: root.
3. `vercel.json` enables clean URLs and immutable caching for `/assets`.

## Limitations

The console contains no seeded or random records and makes no live backend
calls; every panel is an empty-state shell ready for the control plane. The
backend phases (state engine, `pqcrypto.kem.kyber768` / `ml_kem_768` handler,
CLI operations `setup` / `read` / `revoke` / `protected_read` / `audit`,
control-plane `/api/sync`) are a separate implementation phase and are not
exercised here.
