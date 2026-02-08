# Codebase Summary

**Generated:** 2026-02-07
**Repository:** https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
**Total Files:** 111
**Total Tokens:** 279,500
**Size:** ~1.1MB

---

## 1. Directory Structure

```
ui-ux-pro-max-skill/
├── src/ui-ux-pro-max/                 # Source of Truth
│   ├── data/                          # Canonical CSV databases
│   │   ├── *.csv                      # 12 core domain databases
│   │   └── stacks/                    # 13 stack-specific guidelines
│   ├── scripts/                       # Python search engine
│   │   ├── search.py                  # CLI entry point (115 LOC)
│   │   ├── core.py                    # BM25 search engine (254 LOC)
│   │   └── design_system.py           # Design system generator (1,068 LOC)
│   └── templates/                     # Platform configs & templates
│       ├── base/                      # Shared templates
│       └── platforms/                 # 15 platform-specific configs
│
├── cli/                               # TypeScript CLI installer
│   ├── src/                           # TypeScript source
│   │   ├── index.ts                   # CLI entry point
│   │   ├── commands/                  # Command handlers (init, update, versions)
│   │   ├── types/                     # TypeScript type definitions
│   │   └── utils/                     # Helper utilities
│   ├── assets/                        # Bundled data (synced from src/)
│   │   ├── data/                      # CSV copy
│   │   ├── scripts/                   # Python script copy
│   │   └── templates/                 # Template copy
│   ├── package.json                   # npm metadata (v2.2.3)
│   └── tsconfig.json                  # TypeScript configuration
│
├── .claude-plugin/                    # Claude Marketplace plugin
│   ├── plugin.json                    # Plugin metadata (v2.0.1 - OUTDATED)
│   └── marketplace.json               # Marketplace publishing (v2.2.1)
│
├── .claude/skills/                    # Claude Code skill (symlink)
│   └── ui-ux-pro-max/                 # → ../src/ui-ux-pro-max/
│
├── .shared/                           # Shared reference (symlink)
│   └── ui-ux-pro-max/                 # → ../src/ui-ux-pro-max/
│
├── screenshots/                       # Marketing screenshots
├── README.md                          # Main documentation (496 lines)
├── LICENSE                            # MIT License
└── CLAUDE.md                          # Development guidelines
```

---

## 2. Data Layer (src/ui-ux-pro-max/data/)

### 2.1 Core Databases (12)

| Database | File | Records | Key Columns | Purpose |
|----------|------|---------|------------|---------|
| **Styles** | styles.csv | 67 | Style Category, Keywords, Best For, CSS Keywords | UI style definitions |
| **Colors** | colors.csv | 96 | Product Type, Primary/Secondary/CTA/BG/Text (Hex) | Color palettes by industry |
| **Typography** | typography.csv | 57 | Font Pairing Name, Category, Heading/Body Font | Font pairings + Google Fonts |
| **Products** | products.csv | 100+ | Product Type, Keywords, Primary/Secondary Styles | Product → style mapping |
| **Charts** | charts.csv | 25 | Data Type, Best Chart Type, Library, Color Guidance | Data visualization recommendations |
| **Landing** | landing.csv | 24 | Pattern Name, Keywords, Conversion Strategy, Sections | Landing page patterns |
| **UI Reasoning** | ui-reasoning.csv | 100 | UI_Category, Recommended Pattern, Style Priority, Rules | Industry-specific reasoning rules |
| **UX Guidelines** | ux-guidelines.csv | 99 | Category, Issue, Description, Do/Don't, Code Examples | UX best practices |
| **Web Interface** | web-interface.csv | - | Category, Issue, Description, Platform | Web-specific guidelines |
| **React Performance** | react-performance.csv | - | Category, Issue, Keywords, Performance Concern | React optimization patterns |
| **Icons** | icons.csv | - | Category, Icon Name, Library, Best For | Icon library recommendations |
| **Form Patterns** | (embedded in stack CSVs) | - | Category, Guideline, Code Samples | Form validation & handling |

### 2.2 Stack-Specific Databases (13)

**Web Stacks:**
- `html-tailwind.csv` - HTML + Tailwind CSS (default)
- `react.csv` - React-specific patterns
- `nextjs.csv` - Next.js framework guidelines
- `astro.csv` - Astro framework patterns
- `vue.csv` - Vue 3 guidelines
- `nuxtjs.csv` - Nuxt.js patterns
- `nuxt-ui.csv` - Nuxt UI component library
- `svelte.csv` - Svelte framework

**Mobile Stacks:**
- `swiftui.csv` - iOS SwiftUI patterns
- `react-native.csv` - React Native guidelines
- `flutter.csv` - Flutter framework
- `jetpack-compose.csv` - Android Jetpack Compose

**Component Libraries:**
- `shadcn.csv` - shadcn/ui component patterns

**Common Stack Columns:**
- Category, Guideline, Description, Do, Don't, Code Good, Code Bad, Severity, Docs URL

### 2.3 Data Characteristics

- **Format:** CSV (UTF-8 encoding)
- **Size:** Largest file = styles.csv (24,653 tokens, 94KB)
- **No dependencies:** Plain text, no external data fetches
- **Versioning:** Embedded in each record via timestamp/version fields
- **Search columns:** Subset of all columns for BM25 optimization
- **Output columns:** Custom per-domain for user-facing results

---

## 3. Search Engine (src/ui-ux-pro-max/scripts/)

### 3.1 search.py (115 LOC)

**Purpose:** CLI entry point & argument parser

**Key Functions:**
- `format_output(result)` - Format results for Claude consumption (token-optimized)
- Argument parsing for 8 command modes:
  - Domain search (default)
  - Stack search (`--stack`)
  - Design system generation (`--design-system`)
  - Persistence (`--persist`)
  - Format selection (`-f ascii|markdown`)

**Windows Fix:** UTF-8 encoding override for emoji output (cp1252 → UTF-8)

**Exit Points:**
- JSON output (`--json`)
- ASCII design system
- Markdown design system
- Persistence confirmation

### 3.2 core.py (254 LOC)

**Purpose:** BM25 search implementation & CSV loading

**Key Classes:**
- `BM25` - Ranking algorithm (k1=1.5, b=0.75)
  - `tokenize()` - Lowercase, punctuation removal, >2 char words
  - `fit()` - Build index from documents
  - `score()` - Calculate BM25 scores for all docs

**Key Functions:**
- `_load_csv()` - Load CSV with DictReader
- `_search_csv()` - Core search using BM25
- `detect_domain()` - Auto-detect search domain from query (10 domain keywords)
- `search()` - Main search function with auto-detection
- `search_stack()` - Stack-specific search

**Configuration:**
- `CSV_CONFIG` - 9 domains (style, color, chart, landing, product, ux, typography, icons, react, web)
- `STACK_CONFIG` - 13 stacks
- `DATA_DIR` - Points to `../data/` from script location
- `MAX_RESULTS` - Default 3 results

**Algorithm:**
```
1. Load CSV & extract search columns
2. Tokenize each row into documents
3. Build BM25 index (IDF calculation)
4. Score query against all documents
5. Return top K results with output columns
```

### 3.3 design_system.py (1,068 LOC) - MODULARIZATION NEEDED

**Purpose:** Design system generation & reasoning

**Key Classes:**
- `DesignSystemGenerator` - Main generator class
  - `_load_reasoning()` - Load ui-reasoning.csv
  - `_multi_domain_search()` - Execute 5 parallel searches
  - `_find_reasoning_rule()` - Match category to reasoning rule
  - `_apply_reasoning()` - Apply rules to search results
  - `_format_output_ascii()` - Generate ASCII design system
  - `_format_output_markdown()` - Generate Markdown design system
  - `_generate_pre_delivery_checklist()` - Quality checklist

**Key Functions:**
- `generate_design_system()` - Main entry point
- `persist_design_system()` - Save to disk (Master + Overrides pattern)

**Multi-Domain Search (parallel):**
1. Product search (1 result) - Identify product type
2. Style search (3 results) - Best matching styles
3. Color search (2 results) - Industry color palettes
4. Landing search (2 results) - Page patterns
5. Typography search (2 results) - Font pairings

**Reasoning Application:**
1. Find matching rule by UI_Category
2. Apply style priority weights
3. Filter anti-patterns for industry
4. Apply decision rules (JSON conditions)
5. Generate output with sections

**Output Sections:**
- Target & recommended system
- Pattern (structure)
- Style (keywords, best for, effects)
- Colors (hex palette with mood notes)
- Typography (fonts, mood, Google Fonts URL)
- Key effects (animations, transitions)
- Anti-patterns (what to avoid)
- Pre-delivery checklist (14 items)

**Persistence Pattern:**
```
design-system/
├── {project-slug}/
│   ├── MASTER.md              # Global source of truth
│   └── pages/
│       └── {page-name}.md     # Page-specific overrides
```

**Issues:**
- Exceeds 200-line modularization guideline (1,068 LOC)
- Reasoning rules parsed but not fully applied
- Output formatting logic mixed with generation logic
- No caching for repeated queries

---

## 4. CLI (cli/src/)

### 4.1 File Structure

```
cli/src/
├── index.ts                    # Entry point (command dispatcher)
├── commands/
│   ├── init.ts                 # uipro init --ai <platform>
│   ├── update.ts               # uipro update
│   └── versions.ts             # uipro versions
├── types/
│   └── index.ts                # TypeScript interfaces
└── utils/
    ├── detect.ts               # Detect OS & AI assistant
    ├── extract.ts              # Extract ZIP from GitHub
    ├── github.ts               # GitHub API calls
    ├── logger.ts               # Logging utilities
    └── template.ts             # Template rendering
```

### 4.2 Key Commands

| Command | Purpose | Key Functions |
|---------|---------|---------------|
| **init** | Install skill for AI assistant | Platform detection, template rendering, file generation |
| **update** | Check & update to latest version | npm registry query, version comparison |
| **versions** | List available versions | GitHub releases API query |

### 4.3 Platform Support

**Skill Mode (Auto-activate):**
- Claude Code, Cursor, Windsurf, Antigravity, Codex CLI, Continue, Gemini CLI, OpenCode, CodeBuddy

**Workflow Mode (Slash command):**
- Kiro, GitHub Copilot, Roo Code

**Factory Mode (New):**
- Droid (v2.2.3)

**Legacy Mode:**
- Trae (SOLO mode first)

### 4.4 Installation Flow

```
1. uipro init --ai claude
2. Detect platform/OS
3. Download/extract assets
4. Render templates (base + platform-specific)
5. Generate SKILL.md/.claude/skills/ files
6. Provide activation instructions
7. Verify installation
```

### 4.5 Bundled Assets

Location: `cli/assets/`

**Contents:**
- Data: 25 CSV files (copied from src/ui-ux-pro-max/data/)
- Scripts: 3 Python files (copied from src/ui-ux-pro-max/scripts/)
- Templates: 2 base + 15 platform configs (copied from src/ui-ux-pro-max/templates/)

**Size:** 564KB (includes all 25 CSVs + 3 Python scripts + 17 templates)

**Sync Required:** Before `npm publish`, manually run:
```bash
cp -r src/ui-ux-pro-max/data/* cli/assets/data/
cp -r src/ui-ux-pro-max/scripts/* cli/assets/scripts/
cp -r src/ui-ux-pro-max/templates/* cli/assets/templates/
```

---

## 5. Templates (src/ui-ux-pro-max/templates/)

### 5.1 Base Templates

| Template | Purpose | Size |
|----------|---------|------|
| **skill-content.md** | Common SKILL.md for all platforms | ~5KB |
| **quick-reference.md** | Quick reference (Claude only) | ~2KB |

### 5.2 Platform Configs (15)

Each platform has a `.json` template with:
- Platform name
- File paths (where to create .claude/, .cursor/, etc.)
- Environment variables
- Activation instructions
- Specific commands

**Platforms:**
claude, cursor, windsurf, copilot, copilot-vscode, kiro, trae, roocode, codex, qoder, gemini, continue, opencode, codebuddy, droid, agent

---

## 6. Marketplace Plugin (.claude-plugin/)

### 6.1 plugin.json (v2.0.1 - OUTDATED)

```json
{
  "name": "ui-ux-pro-max",
  "version": "2.0.1",
  "description": "50 styles, 21 palettes, 50 font pairings...",
  "skills": ["./.claude/skills/ui-ux-pro-max"]
}
```

**Issues:**
- Version number outdated (should be 2.2.3)
- Feature counts outdated (50 styles → 67 styles, etc.)

### 6.2 marketplace.json (v2.2.1)

```json
{
  "name": "ui-ux-pro-max-skill",
  "version": "2.2.1",
  "metadata": {
    "description": "67 styles, 96 palettes, 57 font pairings, 25 charts, 13 stacks",
    "version": "2.2.1"
  },
  "plugins": [
    {
      "name": "ui-ux-pro-max",
      "version": "2.2.1",
      "description": "Professional UI/UX design intelligence..."
    }
  ]
}
```

**Status:** Current but should be aligned with CLI (v2.2.3)

---

## 7. File Statistics

### 7.1 Top 5 Largest Files

| File | Type | Size | Tokens |
|------|------|------|--------|
| styles.csv | CSV | 94.9KB | 24,653 |
| typography.csv | CSV | 31.9KB | 9,114 |
| ui-reasoning.csv | CSV | ~20KB | ~5,000 |
| products.csv | CSV | ~15KB | ~4,000 |
| design_system.py | Python | 43.6KB | 10,158 |

### 7.2 Codebase Composition

| Language | Files | LOC | Purpose |
|----------|-------|-----|---------|
| **Python** | 3 | 1,437 | Search engine, design system |
| **TypeScript** | 8 | ~1,200 | CLI installer |
| **CSV** | 25 | ~500K | Design databases |
| **Markdown** | 3 | 500+ | Documentation |
| **JSON** | 18 | ~300 | Configs, package info |
| **Shell/Other** | 48 | - | Binary files, configs |

### 7.3 Dependencies

**Python:** None (pure Python 3.x)
**Node/TypeScript:**
- commander (CLI framework)
- chalk (colored output)
- ora (spinners)
- prompts (interactive prompts)

**Build Tools:**
- Bun (build, package manager)
- TypeScript (compilation)

---

## 8. Execution Flow

### 8.1 User Request → Design System

```
User: "Build a landing page for my beauty spa"
  ↓
Claude Code (skill auto-activates)
  ↓
Query → search.py --design-system "beauty spa"
  ↓
Python core.py:
  • Auto-detect domain (product)
  • Perform multi-domain search
  ↓
design_system.py:
  • Find UI_Category match (Wellness/Beauty)
  • Apply reasoning rules
  • Select pattern, style, colors, typography
  • Generate anti-patterns
  • Create pre-delivery checklist
  ↓
Output (ASCII or Markdown):
  TARGET: Beauty Spa
  PATTERN: Hero-Centric + Social Proof
  STYLE: Soft UI Evolution
  COLORS: Soft Pink, Sage Green, Gold
  TYPOGRAPHY: Cormorant Garamond / Montserrat
  KEY EFFECTS: Soft shadows, smooth transitions
  ANTI-PATTERNS: Bright neon colors, harsh animations
  CHECKLIST: [...14 items...]
  ↓
Claude generates HTML/React/etc. with design system applied
```

### 8.2 CLI Installation Flow

```
User: npm install -g uipro-cli && uipro init --ai claude
  ↓
CLI index.ts (command dispatcher)
  ↓
init command:
  • Detect OS (Windows/Mac/Linux)
  • Detect project structure
  • Prompt for AI assistant
  ↓
template.ts (template rendering):
  • Load skill-content.md (base template)
  • Load claude.json (platform config)
  • Substitute variables (${AI_NAME}, ${SKILL_PATH}, etc.)
  ↓
File generation:
  • Create .claude/skills/ui-ux-pro-max/ directory
  • Copy SKILL.md with rendered template
  • Copy assets (data, scripts, templates)
  ↓
Output:
  ✓ Installed UI/UX Pro Max for Claude Code
  📖 Usage: Request UI/UX work naturally in chat
  🔧 Advanced: python .claude/skills/ui-ux-pro-max/scripts/search.py "query"
```

---

## 9. Key Dependencies & Integrations

### 9.1 Internal Dependencies

- **search.py** → imports core.py, design_system.py
- **design_system.py** → imports core.py (search function)
- **core.py** → standalone (no local imports)
- **CLI** → reads bundled assets (data/, scripts/, templates/)

### 9.2 External Dependencies

- **Python Search:** csv, pathlib, math, re (all stdlib)
- **CLI:** commander, chalk, ora, prompts (npm)
- **Marketplace:** GitHub integration (releases, publishing)

### 9.3 Data Integrations

- **Product-to-Style Mapping:** products.csv → ui-reasoning.csv
- **Style-to-Colors:** styles.csv + colors.csv (joined in generation)
- **Typography-to-Fonts:** typography.csv + Google Fonts API

---

## 10. Entry Points

| Entry Point | Type | Location | Command |
|------------|------|----------|---------|
| **Design System Query** | Python | `scripts/search.py` | `python search.py "query" --design-system` |
| **Domain Search** | Python | `scripts/search.py` | `python search.py "query" --domain style` |
| **Stack Search** | Python | `scripts/search.py` | `python search.py "query" --stack react` |
| **CLI Installation** | Node | `cli/src/index.ts` | `uipro init --ai claude` |
| **Skill Activation** | Markdown | `SKILL.md` | Auto-activates in Claude Code |

---

## 11. Configuration Management

| Config File | Purpose | Scope |
|-------------|---------|-------|
| **core.py lines 13-92** | CSV_CONFIG, STACK_CONFIG | Search domains & stacks |
| **design_system.py lines 25-33** | SEARCH_CONFIG | Multi-domain result counts |
| **cli/package.json** | npm metadata, version | CLI distribution |
| **marketplace.json** | Plugin metadata | Claude Marketplace |
| **plugin.json** | Plugin definition | Local skill reference |
| **src/ui-ux-pro-max/templates/platforms/*.json** | Platform templates | Installation files |

---

## 12. Known Issues & TODOs

| Issue | Severity | File | Fix |
|-------|----------|------|-----|
| Version mismatch (v2.0.1 vs v2.2.1 vs v2.2.3) | High | plugin.json, marketplace.json | Update to 2.2.3 |
| design_system.py exceeds 200 LOC | Medium | design_system.py (1,068) | Modularize into 3-4 modules |
| CLI assets sync required before publish | Medium | cli/assets/ | Automate pre-publish sync |
| No error handling for CSV parse errors | Low | core.py | Add try-catch for DictReader |
| Decision rules parsed but not applied | Medium | design_system.py | Complete rule application logic |
| No test coverage | High | All | Add unit tests (target 70%+) |
| README exceeds 300 lines | Low | README.md (496) | Split into docs/ with links |

---

## 13. Performance Characteristics

| Operation | Time | Bottleneck |
|-----------|------|-----------|
| CSV loading | ~50ms | File I/O (all 25 CSVs) |
| BM25 indexing | ~100ms | Tokenization + IDF calculation |
| Single search | ~200ms | Document scoring |
| Multi-domain search | ~1s | 5 parallel searches |
| Design system generation | ~2s | Reasoning rule lookup + output formatting |
| CLI installation | ~3-5s | File copying + template rendering |

---

## 14. Unresolved Questions

1. **Version Sync:** Should we maintain separate versions for CLI, Marketplace, and Plugin?
2. **Design System Modularization:** How to split design_system.py without breaking reasoning logic?
3. **Caching:** Should search results be cached for identical queries?
4. **Testing:** What framework to use for Python (pytest) and TypeScript (vitest)?
5. **Data Freshness:** How often should design trend data be updated?
6. **Analytics:** Track which design systems users generate?
