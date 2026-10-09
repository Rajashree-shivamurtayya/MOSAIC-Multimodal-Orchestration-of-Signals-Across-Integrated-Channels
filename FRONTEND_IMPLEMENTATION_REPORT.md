# FRONTEND IMPLEMENTATION REPORT

## Architecture
The Phase 10 MOSAIC frontend is built using Next.js 15 (React 19) with the App Router, providing a robust, highly responsive single-page application experience. The design system leverages Tailwind CSS v4 and adheres to strict professional, technical, and accessibility standards without relying on generic external UI kits (e.g., Bootstrap, Material).

## Component Architecture
A custom UI component library was developed in `frontend/src/components/ui`, ensuring visual consistency and reusability:
- **Card**: Glassmorphism containers with dark-mode aesthetic for information grouping.
- **Button**: Interactive elements with precise state handling (hover, focus, disabled).
- **Badge**: Semantic indicators mapped to system statuses (e.g., SUCCESS, WARNING, ERROR, PROCESSING).
- **AppShell**: A global layout wrapper that provides the structural grid for the `Sidebar`, `TopBar`, and `BottomBar`.

## State Management
Global state is managed via `SystemContext` (`src/context/SystemContext.tsx`). This handles:
- **Hardware/Pipeline Connection Status** for all modalities.
- **Session Data**: Active trial IDs and participant tracking.
- **Data Source Verification**: Explicit toggling and tracking of `SIMULATED DATA` vs `LIVE SENSOR DATA`.

## Pages Implemented
1. **Home / System Overview** (`/`): High-level system dashboard with global connection statuses, session control, and Data Source toggles.
2. **Live Monitoring** (`/live`): Real-time inference UI. Features a simulated camera feed, physiology time-series chart (`recharts`), audio metric bars, and a clear Late Fusion output prominently labeled as an "Experimental Classification" rather than a lie detector.
3. **Trial History** (`/history`): Searchable, filterable log of past trials with an expandable row design, avoiding full page reloads.
4. **Trial Detail** (`/history/[id]`): Deep dive into a specific trial, showing multimodal feature summaries and granular probabilities.
5. **Analytics** (`/analytics`): Display of Phase 3-5 results, utilizing `recharts` for Modality Comparisons and Performance Radar charts.
6. **Diagnostics** (`/diagnostics`): Engineering-specific view detailing COM ports, I2C addresses, dropped frames, and component health.

## Design System & Branding
- **Color Palette**: Deep slate/navy background (`#020617`, `#0f172a`) with restrained teal/blue accents.
- **Typography**: Inter font family, utilizing strict hierarchy and monospace fonts for technical data.
- **Micro-animations**: Subtle `animate-fade-in-up` applied on page loads to feel dynamic yet highly professional.
- **No False Claims**: All classification outputs explicitly state they are experimental and do not establish deception truth.

## Testing & Simulation Mode
The application implements a robust **Software Validation Mode**. This allows the entire pipeline UI to be demonstrated using pre-recorded dataset simulations without requiring the physical ESP32 or MAX30102 to be connected. Fallbacks and "UNAVAILABLE" error states have been tested and implemented gracefully (no silent failures or blank screens).

## Commands to Run
```bash
cd frontend
npm install
npm run dev
```
