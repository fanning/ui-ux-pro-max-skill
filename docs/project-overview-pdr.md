# UI/UX Pro Max Skill - Project Overview & PDR

**Version:** 2.2.3 (CLI) / 2.2.1 (Marketplace)
**License:** MIT
**Repository:** https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
**Website:** https://uupm.cc
**Published:** https://www.npmjs.com/package/uipro-cli

---

## 1. Executive Summary

**UI/UX Pro Max** is an AI-powered design intelligence toolkit that provides searchable databases of UI styles, color palettes, font pairings, chart types, and UX guidelines. It enables developers and designers to rapidly generate complete design systems for any product type or framework.

The project is implemented as:
- **CLI Tool** (npm: `uipro-cli`) - Installation & configuration
- **Skill/Plugin** - AI assistant integration (Claude, Cursor, Windsurf, Copilot, etc.)
- **Python Search Engine** - BM25 hybrid search + design system reasoning

---

## 2. Project Vision & Objectives

### Vision
Bridge the gap between designers and developers by enabling designers-turned-developers and developers to ship beautiful, professional UI/UX designs without design expertise.

### Primary Objectives
1. **Reduce Time-to-Beautiful-UI** - From weeks to minutes
2. **Democratize Design Knowledge** - Make professional design patterns accessible to all developers
3. **Support Multiple Frameworks** - Work with 13+ tech stacks
4. **Generate Complete Design Systems** - Not just recommendations, but complete, reasoned systems
5. **Support 15+ AI Coding Assistants** - Claude, Cursor, Windsurf, Copilot, Kiro, Trae, Gemini, etc.

---

## 3. Target Users

| User Type | Primary Use Case |
|-----------|-----------------|
| **Developers** | Build professional UIs without design skills |
| **Designers** | Code their own designs faster (designer-developers) |
| **AI Assistants** | Provide better design guidance in code generation |
| **Design Teams** | Enforce design system consistency across teams |
| **Startups** | Ship MVPs with professional design at low cost |

---

## 4. Key Features (v2.0)

### 4.1 Design System Generation
**Flagship Feature:** AI-powered reasoning engine that generates complete design systems in seconds.

**Inputs:**
- Project description/query (e.g., "beauty spa website")
- Optional project name & target page

**Outputs:**
```
Pattern + Style + Colors + Typography + Effects + Anti-patterns
+ Pre-delivery Checklist
```

Example: Query "beauty spa" → generates Serenity Spa design system with Soft UI style, soft pinks/greens, elegant typography, and pre-delivery quality checks.

### 4.2 Content Databases

| Database | Count | Content |
|----------|-------|---------|
| **UI Styles** | 67 | Glassmorphism, Claymorphism, Minimalism, Brutalism, Y2K, Cyberpunk, AI-Native, etc. |
| **Color Palettes** | 96 | Industry-specific palettes (SaaS, E-commerce, Healthcare, Fintech, Beauty, etc.) |
| **Typography** | 57 | Font pairings with Google Fonts, mood classifications |
| **Chart Types** | 25 | Dashboard recommendations by data type |
| **Products** | 100+ | Product categories with style/pattern recommendations |
| **UI Reasoning** | 100 | Industry-specific decision rules (v2.0 flagship) |
| **UX Guidelines** | 99 | Best practices, anti-patterns, accessibility rules |
| **Landing Patterns** | 24 | Page structure & CTA strategies |
| **Icon Guidelines** | - | SVG icon library recommendations |
| **Stack Guidelines** | 13 | Framework-specific implementation patterns |

### 4.3 Supported Platforms (15 AI Assistants)

| Platform | Support Type | Status |
|----------|-------------|--------|
| **Claude Code** | Skill + Marketplace | Active |
| **Cursor** | Skill | Active |
| **Windsurf** | Skill | Active |
| **GitHub Copilot** | Workflow | Active |
| **Copilot (VS Code)** | Extension | Active |
| **Antigravity** | Skill | Active |
| **Droid** | Skill | Active (v2.2.3) |
| **Kiro** | Workflow | Active |
| **Trae** | Skill | Active |
| **Roo Code** | Workflow | Active |
| **Codex CLI** | Workflow | Active |
| **Gemini CLI** | Skill | Active |
| **Continue** | Skill | Active |
| **OpenCode** | Skill | Active |
| **CodeBuddy** | Skill | Active |
| **Qoder** | Workflow | Active |

### 4.4 Supported Tech Stacks (13)

**Web:**
- HTML + Tailwind CSS (default)
- React & React ecosystem (Next.js, shadcn/ui)
- Vue & Vue ecosystem (Nuxt.js, Nuxt UI)
- Astro, Svelte

**Mobile:**
- iOS: SwiftUI
- Android: Jetpack Compose
- Cross-platform: React Native, Flutter

---

## 5. Technical Architecture

### 5.1 Components

```
┌─────────────────────────────────────────┐
│  CLI (TypeScript/Bun)                   │
│  - uipro init --ai claude               │
│  - Platform detection & installation    │
└─────────────────────────────────────────┘
            ↓
┌─────────────────────────────────────────┐
│  Source of Truth: src/ui-ux-pro-max/    │
│  - data/*.csv (canonical databases)     │
│  - scripts/*.py (search + generation)   │
│  - templates/* (platform configs)       │
└─────────────────────────────────────────┘
            ↓
┌─────────────────────────────────────────┐
│  Search Engine (Python)                 │
│  - BM25 ranking (k1=1.5, b=0.75)       │
│  - Regex hybrid matching                │
│  - Auto-domain detection                │
└─────────────────────────────────────────┘
            ↓
┌─────────────────────────────────────────┐
│  Design System Generator                │
│  - Multi-domain search (5 parallel)    │
│  - Reasoning rule application           │
│  - Anti-pattern filtering               │
│  - ASCII/Markdown output                │
└─────────────────────────────────────────┘
```

### 5.2 Data Flow

```
User Query
    ↓
Auto-Domain Detection (10 domain keywords)
    ↓
BM25 Search (7 search domains)
    ↓
Parallel Searches:
  • products.csv (1 result)
  • styles.csv (3 results)
  • colors.csv (2 results)
  • landing.csv (2 results)
  • typography.csv (2 results)
    ↓
UI Reasoning Rules (100 industry-specific rules)
    ↓
Design System Generation
    ↓
Output (ASCII/Markdown/Persisted)
```

### 5.3 Synchronization Rules

**Source of Truth:** `src/ui-ux-pro-max/` (all changes here first)

**Sync Targets:**
1. `.shared/ui-ux-pro-max/` → Symlink to src/
2. `.claude/skills/ui-ux-pro-max/` → Symlink to src/
3. `cli/assets/` → Copy before npm publish

**Sync Protocol:**
- Data & scripts: Always edit in src/, changes auto-available via symlinks
- CLI: Manual sync required before `npm publish`
- Marketplace: Automatic via GitHub integration

---

## 6. Success Metrics & KPIs

### User-Facing Metrics
- **Time to First Design System:** < 30 seconds
- **Design System Completeness:** ≥ 90% coverage (pattern, style, colors, typography, effects)
- **User Satisfaction:** ≥ 4.5/5 (from GitHub issues/feedback)
- **Adoption Rate:** ≥ 50% of users use design system generation feature

### Technical Metrics
- **Search Performance:** ≤ 500ms per query
- **Design System Generation:** ≤ 2 seconds end-to-end
- **CLI Installation:** ≤ 5 seconds (with bundled assets)
- **Code Coverage:** ≥ 70% (Python & TypeScript)
- **Platform Support:** ≥ 15 AI assistants

### Community Metrics
- **GitHub Stars:** 11K+ (current)
- **npm Downloads:** ≥ 1K/month
- **GitHub Issues:** ≤ 5% outstanding
- **Community Contributions:** ≥ 10 PRs/quarter

---

## 7. Functional Requirements

### 7.1 Core Features
1. **Design System Generation** - Complete system from single query
2. **Domain-Specific Search** - Filter by style, color, typography, etc.
3. **Stack-Specific Guidelines** - Framework-optimized recommendations
4. **Master + Overrides Pattern** - Hierarchical design system persistence
5. **Platform Auto-Detection** - Detect AI assistant & install correctly
6. **Template Generation** - Create platform-specific files from templates

### 7.2 Design System Components
1. **Recommended Pattern** - Landing page structure & section order
2. **Style Recommendation** - Best matching UI style + keywords
3. **Color Palette** - Primary, secondary, CTA, background, text colors
4. **Typography Pairing** - Heading & body fonts with Google Fonts URL
5. **Key Effects** - Animations, hover states, transitions
6. **Anti-Patterns** - What NOT to do for this industry
7. **Pre-Delivery Checklist** - Accessibility, responsive, performance items

### 7.3 User Workflows
1. **Installation:** `npm install -g uipro-cli && uipro init --ai claude`
2. **Skill Mode:** Request UI/UX work naturally in chat
3. **Design System:** Query design system generation directly
4. **Persistence:** Save to `design-system/MASTER.md` for reuse
5. **Stack Search:** `--stack react` for framework-specific guidelines

---

## 8. Non-Functional Requirements

| Requirement | Target |
|------------|--------|
| **Performance** | Design system generation ≤ 2s, search ≤ 500ms |
| **Reliability** | 99.9% uptime, graceful degradation (offline mode) |
| **Maintainability** | Modular architecture, clear separation of concerns |
| **Scalability** | Support unlimited databases (CSV-based) |
| **Security** | No external dependencies for search, local-first |
| **Accessibility** | WCAG AA compliance in generated designs |
| **Compatibility** | Python 3.x, TypeScript 4.x+, Bun/Node 18+ |

---

## 9. Known Issues & Technical Debt

### Version Mismatches
- `plugin.json`: v2.0.1 (outdated)
- `marketplace.json`: v2.2.1 (current)
- `cli/package.json`: v2.2.3 (latest)

**Action:** Align all versions to 2.2.3

### Code Size
- `design_system.py`: 1,068 LOC (exceeds 200-line guideline)

**Action:** Modularize reasoning engine (separate rule application, output formatting)

### Missing Features
- Decision rules parsed but not fully applied in generation
- No caching layer for repeated queries
- Limited error messages for CSV parsing failures

---

## 10. Roadmap

### v2.3 (Next)
- [ ] Align version numbers (→ 2.2.3)
- [ ] Modularize design_system.py
- [ ] Add caching for search results
- [ ] Improve error messages
- [ ] Add unit tests for design system generation

### v2.4
- [ ] Support CSS variable generation
- [ ] Add theme builder UI
- [ ] Implement design token export (JSON)
- [ ] Add accessibility audit tools

### v3.0
- [ ] AI-powered design refinement
- [ ] Collaborative design system editor
- [ ] Real-time component preview
- [ ] Integration with Figma/Adobe XD

---

## 11. Dependencies

### Core Dependencies
- Python 3.x (no external packages for search engine)
- Node.js 18+ (for CLI)
- Bun (build tool for CLI)

### External Services (Optional)
- GitHub (ZIP download fallback)
- Claude Marketplace (distribution)

### Development Dependencies
See `cli/package.json` and Python environment setup

---

## 12. Project Constraints

| Constraint | Impact | Mitigation |
|-----------|--------|-----------|
| **CSV-Based Data** | Limited to tabular data, no nested objects | Use composite columns for complex data |
| **Offline Installation** | Must bundle all assets | Keep assets under 1MB (currently 564KB) |
| **BM25 Algorithm** | No semantic understanding | Combine with regex matching & auto-domain detection |
| **15 Platforms** | High maintenance burden | Template-based generation reduces overhead |

---

## 13. Acceptance Criteria

### Feature Acceptance
- [ ] Design system generation produces valid output for all 100+ product types
- [ ] All 15 platforms generate correct files without errors
- [ ] BM25 search returns relevant results (precision > 80%)
- [ ] Master + Overrides pattern correctly persists and retrieves data
- [ ] CLI < 5s installation time with bundled assets
- [ ] No external network calls required for core functionality

### Quality Acceptance
- [ ] No critical security vulnerabilities (npm audit clean)
- [ ] ≥ 70% test coverage
- [ ] All code passes linting (Python & TypeScript)
- [ ] Documentation is up-to-date and >80% coverage of features
- [ ] README < 300 lines with clear quick-start

### Platform Support Acceptance
- [ ] Claude Code: Auto-activate on UI/UX requests
- [ ] Cursor, Windsurf, Copilot: Consistent experience
- [ ] All 15 platforms: Correct file generation & activation

---

## 14. Stakeholders

| Role | Responsibility |
|------|-----------------|
| **Product Owner** | Define features, roadmap, success metrics |
| **Lead Developer** | Architecture, code quality, releases |
| **Designers** | Design database content (styles, colors, typography) |
| **QA** | Test all platforms, design system quality |
| **Community** | Contribute data, report bugs, feature requests |

---

## 15. Glossary

| Term | Definition |
|------|-----------|
| **Design System** | Complete set of patterns, styles, colors, typography, effects for a product |
| **Reasoning Rule** | Industry-specific decision rule matching product type → design system |
| **Master + Overrides** | Hierarchical pattern: check page-specific file first, fallback to MASTER.md |
| **BM25** | Ranking function used in search (Okapi BM25) |
| **Stack** | Technology framework (React, Vue, Svelte, etc.) |
| **Domain** | Search category (style, color, typography, etc.) |
| **Anti-Pattern** | Design practice to avoid for specific industry |

---

## Unresolved Questions

1. **Version Alignment:** Should we immediately bump all versions to 2.2.3 or maintain separate versions?
2. **Design System Caching:** Should generated design systems be cached to improve repeated query performance?
3. **CSS Variables:** Should we auto-generate CSS custom properties from color palettes?
4. **Analytics:** Should we track which design systems are most popular?
5. **Marketplace Sustainability:** How to keep marketplace data current as design trends evolve?
