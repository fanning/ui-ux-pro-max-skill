# System Architecture

**Version:** 2.2.3
**Last Updated:** 2026-02-07
**Architecture Type:** Multi-layer search + generation engine

---

## 1. Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     PRESENTATION LAYER                          │
│  (User Interfaces: Claude Code, Cursor, Windsurf, CLI, etc.)   │
└─────────────────────────────┬───────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────┐
│                  ORCHESTRATION LAYER                            │
│  (CLI Installer + Skill Activation Framework)                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ uipro-cli (TypeScript)                                  │   │
│  │ - Platform detection (Claude, Cursor, Windsurf, etc.)   │   │
│  │ - Template rendering (17 platform configs)             │   │
│  │ - File generation (.claude/, .cursor/, .windsurf/)     │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────┬───────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────┐
│                   PROCESSING LAYER                              │
│  (Python Search Engine + Design System Generator)              │
│  ┌──────────────────┐  ┌──────────────────────────────────┐   │
│  │ search.py        │  │ design_system.py                 │   │
│  │ (CLI entry)      │  │ (Design system reasoning)        │   │
│  └────────┬─────────┘  └────────┬─────────────────────────┘   │
│           │                     │                              │
│           └─────┬───────────────┘                              │
│                 │                                              │
│           ┌─────▼───────────────┐                              │
│           │ core.py             │                              │
│           │ - BM25 search       │                              │
│           │ - Domain detection  │                              │
│           │ - Result ranking    │                              │
│           └─────┬───────────────┘                              │
└────────────────┼──────────────────────────────────────────────┘
                 │
┌────────────────▼──────────────────────────────────────────────┐
│                    DATA LAYER                                 │
│  (CSV-based Knowledge Base)                                   │
│  ┌────────────────────────────────────────────────────────┐   │
│  │ Core Databases (12)                                    │   │
│  │ ┌──────────┬──────────┬────────────┬─────────────┐    │   │
│  │ │ styles   │ colors   │ typography │ products    │    │   │
│  │ │ (67)     │ (96)     │ (57)       │ (100+)      │    │   │
│  │ └──────────┴──────────┴────────────┴─────────────┘    │   │
│  │ ┌──────────┬──────────┬────────────┬─────────────┐    │   │
│  │ │ landing  │ charts   │ ux-guide   │ ui-reasoning│   │   │
│  │ │ (24)     │ (25)     │ (99)       │ (100)       │    │   │
│  │ └──────────┴──────────┴────────────┴─────────────┘    │   │
│  ├────────────────────────────────────────────────────────┤   │
│  │ Stack-Specific Guidelines (13)                         │   │
│  │ React, Next.js, Vue, Nuxt, Svelte, SwiftUI, etc.      │   │
│  └────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────┘
```

---

## 2. Layer Responsibilities

### 2.1 Data Layer

**Responsibility:** Store and provide access to design knowledge

**Components:**
- 12 core CSV databases
- 13 stack-specific CSV databases
- Metadata files (categories, relationships)

**Characteristics:**
- **Immutable at runtime** (no updates via API)
- **Versioned in git** (changes tracked)
- **Replicated** (source in src/, copy in cli/assets/)
- **Format:** UTF-8 CSV, comma-separated

**Data Flow Out:**
```
CSV files → DictReader → Python lists → BM25 ranking
```

**Design Principles:**
- Single source of truth: `src/ui-ux-pro-max/data/`
- Zero external dependencies (no database, no API)
- Offline-first (works without internet)

### 2.2 Search & Processing Layer

**Responsibility:** Query data and generate intelligent recommendations

**Components:**
- **core.py** - BM25 search algorithm
- **design_system.py** - Reasoning engine
- **search.py** - CLI entry point

**Execution Model:**
```
Input (query) → Auto-detect domain → BM25 search → Results
Input (query) → Multi-domain search → Reasoning rules → Design system
```

**Key Algorithms:**

#### BM25 Ranking
```
score(doc, query) = Σ IDF(term) * (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * |doc| / avgdl))

Parameters:
- k1 = 1.5 (term frequency saturation)
- b = 0.75 (document length normalization)
- IDF = log((N - df + 0.5) / (df + 0.5) + 1)

Why BM25:
- Proven ranking algorithm for text search
- Fast (linear time complexity O(n))
- Requires no external dependencies
- Works well for short documents (CSV rows)
```

#### Domain Detection
```
query = "glassmorphism and minimalism"

Domain scores:
  style: 2 (matches "glassmorphism", "minimalism")
  product: 0
  color: 0
  landing: 0

Best domain: style (highest score)
```

#### Multi-Domain Search
```
User query: "beauty spa wellness"

Parallel searches (5 domains):
1. products.csv → "Beauty/Spa" (1 result)
   ↓ Extract UI_Category
2. ui-reasoning.csv → Match rules for Beauty/Spa
3. styles.csv → Search "beauty spa" (3 results)
4. colors.csv → Search "beauty" (2 results)
5. landing.csv → Search "spa" (2 results)
6. typography.csv → Search "elegant" (2 results)

Combine results → Apply reasoning → Output design system
```

**Characteristics:**
- **Stateless** - No memory between requests
- **Deterministic** - Same query = same results
- **Fast** - <2 seconds for design system generation
- **Portable** - Pure Python, no external deps

### 2.3 Orchestration Layer

**Responsibility:** Install skill, activate for AI assistants, manage configuration

**Components:**
- **uipro-cli** (TypeScript/Node.js)
- **Template system** (17 platform-specific configs)
- **Platform detection** (OS, AI assistant, file structure)

**Installation Flow:**
```
User: npm install -g uipro-cli && uipro init --ai claude

┌─────────────────────────────────┐
│ 1. Detect Platform              │
│ - OS (Windows/Mac/Linux)        │
│ - Project structure             │
│ - Existing .claude/ directory   │
└──────────────┬──────────────────┘
               │
┌──────────────▼──────────────────┐
│ 2. Load Template                │
│ - skill-content.md (base)       │
│ - claude.json (config)          │
└──────────────┬──────────────────┘
               │
┌──────────────▼──────────────────┐
│ 3. Render Template              │
│ - Substitute variables          │
│ - Format for platform           │
└──────────────┬──────────────────┘
               │
┌──────────────▼──────────────────┐
│ 4. Generate Files               │
│ - .claude/skills/...            │
│ - Copy data & scripts           │
│ - Create config files           │
└──────────────┬──────────────────┘
               │
┌──────────────▼──────────────────┐
│ 5. Activate & Verify            │
│ - Test execution                │
│ - Provide instructions          │
└─────────────────────────────────┘
```

**Key Features:**
- **Platform-agnostic** - Works for 15 different AI assistants
- **Template-based** - Easy to add new platforms
- **Offline-capable** - Bundled assets (no GitHub download needed with `--offline`)
- **Backward-compatible** - New platforms don't affect existing installations

### 2.4 Presentation Layer

**Responsibility:** Deliver results to users in appropriate format

**User Interfaces:**

| Interface | Format | Activation |
|-----------|--------|-----------|
| **Claude Code** | Markdown in chat | Auto-skill activation |
| **Cursor** | Same as Claude | Auto-skill activation |
| **Windsurf** | Same as Claude | Auto-skill activation |
| **GitHub Copilot** | Markdown output | Slash command `/ui-ux-pro-max` |
| **Kiro** | Markdown output | Slash command `/ui-ux-pro-max` |
| **CLI Direct** | ASCII/Markdown | `python search.py "query"` |
| **Design System** | ASCII/Markdown | `python search.py "query" --design-system` |

**Output Formats:**

```
ASCII (Terminal-friendly):
+────────────────────────────────────┐
│ TARGET: Serenity Spa               │
│ RECOMMENDED DESIGN SYSTEM          │
│ PATTERN: Hero-Centric + Social ... │
│ STYLE: Soft UI Evolution           │
│ COLORS:                            │
│   Primary: #E8B4B8                 │
│   Secondary: #A8D5BA               │
└────────────────────────────────────┘

Markdown (AI-friendly):
## Design System: Serenity Spa
### Pattern
Hero-Centric + Social Proof
### Style
Soft UI Evolution
...
```

---

## 3. Data Flow Architecture

### 3.1 Complete User Journey

```
┌──────────────────────────────────────────────────┐
│ User Action                                      │
│ "Build a landing page for my beauty spa"        │
└──────────────────────┬───────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────┐
│ Claude Code (Skill activation)                   │
│ - Activates UI/UX Pro Max skill                  │
│ - Routes to search.py                            │
└──────────────────────┬───────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────┐
│ search.py (CLI entry point)                      │
│ - Parse arguments: "beauty spa" --design-system  │
│ - Call design_system.generate_design_system()    │
└──────────────────────┬───────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────┐
│ design_system.py (Multi-domain search)           │
│ 1. Multi-domain search (5 parallel):             │
│    - products.csv → "Beauty/Spa"                 │
│    - styles.csv → ["Soft UI", "Claymorphism"]   │
│    - colors.csv → [soft palette #1, #2]         │
│    - landing.csv → ["Hero + Social Proof"]      │
│    - typography.csv → ["Cormorant + Montserrat"]│
│                                                  │
│ 2. Find reasoning rule → "Wellness/Beauty"      │
│    - Recommended pattern                         │
│    - Style priorities                            │
│    - Color mood                                  │
│    - Anti-patterns                               │
│                                                  │
│ 3. Apply reasoning rules to results              │
│    - Filter conflicting styles                   │
│    - Weight by industry relevance                │
│    - Generate complete design system             │
└──────────────────────┬───────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────┐
│ core.py (BM25 search engine)                     │
│ - For each search domain:                        │
│   1. Load CSV                                    │
│   2. Build BM25 index                            │
│   3. Score query against documents              │
│   4. Return top K results                        │
└──────────────────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────┐
│ Output Generation                                │
│ - Format as ASCII/Markdown                       │
│ - Include pre-delivery checklist                 │
│ - Return to Claude Code                          │
└──────────────────────┬───────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────┐
│ Claude generates HTML/React with design system   │
│ - Applies colors, typography, effects           │
│ - Follows pattern structure                      │
│ - Respects anti-patterns                         │
│ - Passes pre-delivery checklist                  │
└──────────────────────────────────────────────────┘
```

### 3.2 CLI Installation Flow

```
npm install -g uipro-cli
         │
         ▼
uipro init --ai claude
         │
         ▼
┌──────────────────────────────────────────────────┐
│ Detect Platform (detect.ts)                      │
│ - Check environment variables                    │
│ - Check file system (.claude/, .cursor/, etc.)   │
│ - Detect OS (Windows/Mac/Linux)                  │
└──────────────┬───────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────┐
│ Load Templates (template.ts)                     │
│ - Load skill-content.md (base)                   │
│ - Load claude.json (config)                      │
│ - Load 25 CSV files from assets/data/            │
│ - Load 3 Python scripts from assets/scripts/     │
└──────────────┬───────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────┐
│ Render Templates                                 │
│ - Substitute ${SKILL_PATH}, ${AI_NAME}, etc.     │
│ - Format for platform conventions                │
└──────────────┬───────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────┐
│ Generate Files                                   │
│ - Create .claude/skills/ui-ux-pro-max/           │
│ - Generate SKILL.md                              │
│ - Copy data/ & scripts/                          │
│ - Write .claude-plugin/plugin.json               │
└──────────────┬───────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────┐
│ Verify & Activate                                │
│ - Test Python environment                        │
│ - Run first test search                          │
│ - Display activation instructions                │
└──────────────────────────────────────────────────┘
```

---

## 4. Component Interactions

### 4.1 Search Engine Components

```
Query String
    │
    ▼
┌─────────────────────┐
│ detect_domain()     │ (core.py)
│ Auto-detect domain  │
│ from keywords       │
└────────┬────────────┘
         │
         ▼
┌──────────────────────────────────────────┐
│ search(query, domain)                     │ (core.py)
│ 1. Load CSV (data_dir/domain.csv)        │
│ 2. Call _search_csv()                    │
└────────┬─────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────┐
│ _search_csv()                             │ (core.py)
│ 1. Extract search columns from CSV       │
│ 2. Build BM25 index                      │
│ 3. Score query against all documents    │
└────────┬─────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────┐
│ BM25.score(query)                         │ (core.py)
│ 1. Tokenize query                         │
│ 2. For each document:                     │
│    - Calculate TF for each token          │
│    - Look up IDF for each token           │
│    - Sum BM25 scores                      │
│ 3. Return ranked list [(idx, score), ...] │
└────────┬─────────────────────────────────┘
         │
         ▼
Results (top K with output columns)
```

### 4.2 Design System Generator Components

```
Query String
    │
    ▼
┌──────────────────────────────────────────────────┐
│ generate_design_system(query, project_name)      │ (design_system.py)
│ 1. Initialize DesignSystemGenerator              │
│ 2. Call _multi_domain_search()                   │
│ 3. Call _find_reasoning_rule()                   │
│ 4. Call _apply_reasoning()                       │
│ 5. Format output (ASCII or Markdown)             │
│ 6. Persist to disk (optional)                    │
└───┬──────────────────────────────────────────────┘
    │
    ├─────────────────────┬─────────────────────┐
    │                     │                     │
    ▼                     ▼                     ▼
┌──────────┐    ┌──────────────┐    ┌──────────────┐
│ Search   │    │ Find Rule    │    │ Apply        │
│ Products │    │ by Category  │    │ Reasoning    │
│ (1 res)  │    │ → UI_Reasoning│    │ & Generate  │
│          │    │ .csv match   │    │ Output      │
└──────────┘    └──────────────┘    └──────────────┘
    │                     │                     │
    └─────────────────────┴─────────────────────┘
                          │
                          ▼
                ┌──────────────────┐
                │ Parallel Search  │
                │ - Styles (3)     │
                │ - Colors (2)     │
                │ - Landing (2)    │
                │ - Typography (2) │
                └────────┬─────────┘
                         │
                         ▼
              Design System Output
              + Pre-delivery checklist
```

---

## 5. Database Schema

### 5.1 Core Database Relationships

```
products.csv
├─ Product Type (e.g., "Beauty/Spa")
├─ Primary Style Recommendation (→ ui-reasoning.csv)
├─ Secondary Styles (→ styles.csv)
├─ Landing Page Pattern (→ landing.csv)
├─ Color Palette Focus (→ colors.csv)
└─ Dashboard Style (optional)
        │
        ▼
ui-reasoning.csv
├─ UI_Category = Product Type
├─ Recommended Pattern (→ landing.csv)
├─ Style Priority (→ styles.csv)
├─ Color Mood (→ colors.csv)
├─ Typography Mood (→ typography.csv)
├─ Anti-patterns (text)
└─ Decision Rules (JSON conditions)
        │
        ├─────────────┬─────────────┬─────────────┐
        ▼             ▼             ▼             ▼
    styles.csv   colors.csv   typography.csv  landing.csv
    (67 rows)    (96 rows)    (57 rows)       (24 rows)
```

### 5.2 Search Column Mapping

| CSV File | Search Columns | Indexed For | Purpose |
|----------|-----------------|------------|---------|
| styles.csv | Style Category, Keywords, Best For, Type, AI Prompt Keywords | Full-text BM25 | Find matching styles |
| colors.csv | Product Type, Notes | BM25 | Find industry color palettes |
| typography.csv | Font Pairing Name, Category, Mood Keywords, Best For, Heading/Body Font | BM25 | Find font pairings |
| landing.csv | Pattern Name, Keywords, Conversion Optimization, Section Order | BM25 | Find page patterns |
| products.csv | Product Type, Keywords, Primary Style, Key Considerations | BM25 | Identify product category |

---

## 6. Caching & Optimization

### 6.1 Current State (No Caching)

**Characteristics:**
- CSV loaded fresh on each query
- BM25 index built each time
- No in-memory caching

**Performance Impact:**
- First query: ~1.5-2s (includes CSV load + indexing)
- Repeated queries: Same time (no cache benefit)

### 6.2 Future Optimization (v2.3+)

**Proposed Caching Strategy:**
```
Cache Layer (Memory):
├─ Loaded CSVs (25 files, ~5MB)
├─ BM25 indexes (per domain)
├─ Last 10 queries + results
└─ TTL: 1 hour (user session)

Trigger: First search per session
Benefit: 2nd+ queries → ~200ms (skip CSV load)
```

---

## 7. Scalability Considerations

### 7.1 Current Limits

| Constraint | Current | Limit | Reached? |
|-----------|---------|-------|----------|
| CSV files | 25 | 50 | No |
| Rows per CSV | 100 | 1,000 | No |
| Total data size | 1.1MB | 10MB | No |
| Search domains | 9 | 20 | No |
| Platforms | 15 | 30 | No |

### 7.2 Scaling Strategy

**If data grows 10x:**
- Add pagination to CSV results
- Implement incremental BM25 indexing
- Move to SQLite database (optional)
- Add caching layer

**If platforms grow 2x:**
- Use platform family templates (reduces duplication)
- Parameterize platform detection
- Auto-generate platform configs

---

## 8. Error Handling & Resilience

### 8.1 Graceful Degradation

```
Scenario: CSV file missing
  → Return {"error": "File not found", "domain": "style"}
  → User sees helpful message
  → No crash

Scenario: Query matches nothing
  → Return empty results list
  → User gets message "No results found"
  → Suggest alternative search

Scenario: Python script not found
  → CLI fails with clear message
  → Suggests reinstalling uipro-cli
  → Provides troubleshooting URL
```

### 8.2 Validation Layers

```
Input Validation:
  query string → length check → tokenization → BM25 scoring

CSV Validation:
  read file → encoding check → header validation → type inference

Output Validation:
  results → truncate long values → format → return
```

---

## 9. Deployment Architecture

### 9.1 Distribution Channels

```
Source of Truth: src/ui-ux-pro-max/
         │
         ├─ Symlink → .shared/ui-ux-pro-max/
         ├─ Symlink → .claude/skills/ui-ux-pro-max/
         │
         └─ Copy → cli/assets/
                │
                └─ npm publish uipro-cli
                        │
                        └─ Users: npm install -g uipro-cli
                              │
                              └─ uipro init --ai claude
                                    │
                                    └─ Generates .claude/skills/
```

### 9.2 Version Synchronization

**Current Issues:**
- CLI: v2.2.3
- Marketplace: v2.2.1
- Plugin: v2.0.1 (outdated)

**Solution:**
1. Update plugin.json → v2.2.3
2. Update marketplace.json → v2.2.3
3. Tag release: v2.2.3
4. Sync CLI assets before publish

---

## 10. Security Architecture

### 10.1 Threat Model

| Threat | Impact | Mitigation |
|--------|--------|-----------|
| **Code injection via query** | Moderate | Tokenization & regex (no eval) |
| **CSV injection via data** | Low | Data validation on load |
| **Path traversal** | Low | Use pathlib, whitelist directories |
| **Secrets in code** | High | Pre-commit hook scanning |
| **Dependency vulnerabilities** | Moderate | npm audit, minimal deps |

### 10.2 Security Best Practices

```python
# Good: Safe path handling
from pathlib import Path
data_dir = Path(__file__).parent / "data"
filepath = data_dir / filename
if not filepath.is_relative_to(data_dir):
    raise ValueError("Path traversal detected")

# Good: Input validation
def tokenize(text):
    """Tokenize with safety checks"""
    if not isinstance(text, str):
        raise TypeError("Query must be string")
    if len(text) > 1000:
        text = text[:1000]  # Truncate
    return [w for w in text.lower().split() if len(w) > 2]

# Avoid
def search(query):
    # Code injection risk!
    exec(f"find_in_database({query})")
```

---

## 11. Monitoring & Observability

### 11.1 Metrics to Track

```
Search Engine:
- Query count (per domain)
- Average search time
- Cache hit rate (future)
- Top 10 queries

Design System Generation:
- Query count
- Average generation time
- Most popular product types
- Most selected styles

CLI Installation:
- Total installs
- Platform distribution
- Installation success rate
- Common errors
```

### 11.2 Logging Strategy

```python
# Verbose logging (enabled with --verbose)
logger.debug(f"Loading CSV: {filepath}")
logger.debug(f"BM25 index built: {len(self.corpus)} docs")
logger.debug(f"Query tokens: {query_tokens}")
logger.info(f"Search completed in {elapsed_ms}ms")

# Error logging
logger.error(f"CSV load failed: {error}")
logger.warning(f"Query returned 0 results")
```

---

## 12. Technology Stack

| Layer | Technology | Why Chosen |
|-------|-----------|-----------|
| **Search Engine** | Python 3.x (pure stdlib) | Zero dependencies, portable |
| **CLI** | TypeScript + Bun | Fast compilation, clear types |
| **Data** | CSV (UTF-8) | Simple, version-controllable |
| **Ranking** | BM25 algorithm | Proven, efficient, no ML needed |
| **Distribution** | npm + GitHub | Reach JavaScript/Node users |
| **Platforms** | 15 AI assistants | Maximum user coverage |

---

## 13. Future Architecture Considerations

### 13.1 v3.0 Vision

```
Current (v2.2):
  CSV → BM25 → Design System (rule-based)

Future (v3.0):
  CSV → Embeddings → Semantic search → LLM-enhanced → Design System
  (Better semantic understanding, LLM-powered reasoning)

Benefits:
- More natural language queries
- Semantic similarity matching
- Adaptive recommendations
- Real-time learning
```

### 13.2 Potential Enhancements

1. **Design Token Export** - Generate CSS variables from palettes
2. **Figma Integration** - Auto-create design systems in Figma
3. **Component Preview** - Real-time UI component rendering
4. **Accessibility Audit** - Auto-check contrast ratios, WCAG compliance
5. **A/B Testing** - Compare design systems, track performance
6. **Collaborative Editor** - Team-based design system refinement

---

## Unresolved Questions

1. **Semantic Search:** Should we add embedding-based search (OpenAI API) for v3.0?
2. **Real-time Analytics:** How to track design system popularity without telemetry?
3. **Caching Layer:** Memory or disk? TTL? Shared across sessions?
4. **Multi-language:** Should we support design systems in non-English languages?
5. **API Stability:** How to version Python modules for external users?
