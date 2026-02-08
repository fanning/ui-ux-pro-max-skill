# Code Standards & Development Guidelines

---

## 1. Python Code Standards (Search Engine & Design System)

### 1.1 General Style

**Compliance:** PEP 8 with pragmatism
**Tools:** Black (code formatter), flake8 (linter), mypy (type checking)
**Min Python:** 3.8+

### 1.2 File Structure

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module docstring (purpose, usage, examples)
"""

import <stdlib>
from <stdlib> import <specific>
import <third-party>
from <third-party> import <specific>

# ============ CONFIGURATION ============
CONSTANT_NAME = value
DICT_CONFIG = {...}

# ============ CLASS DEFINITIONS ============
class ClassName:
    """Class docstring"""

    def __init__(self):
        """Initialize"""
        pass

    def method_name(self):
        """Method docstring"""
        pass

# ============ FUNCTION DEFINITIONS ============
def function_name(param1, param2):
    """Function docstring with Args, Returns, Raises"""
    pass

# ============ MAIN ENTRY ============
if __name__ == "__main__":
    main()
```

### 1.3 Naming Conventions

| Type | Format | Example |
|------|--------|---------|
| **Constants** | UPPER_SNAKE_CASE | `MAX_RESULTS = 3` |
| **Functions** | snake_case | `def _load_csv():` |
| **Classes** | PascalCase | `class BM25:` |
| **Private** | _snake_case prefix | `def _internal_function():` |
| **Dunder** | __name__ (avoid custom) | `__init__, __str__` |
| **Variables** | snake_case | `query_result = []` |

### 1.4 Docstring Format

```python
def search(query, domain=None, max_results=MAX_RESULTS):
    """
    Main search function with auto-domain detection.

    Args:
        query (str): Search query string
        domain (str, optional): Specific domain to search. If None, auto-detect.
        max_results (int): Maximum number of results (default: 3)

    Returns:
        dict: Result dictionary with keys: domain, query, file, count, results

    Raises:
        FileNotFoundError: If CSV file not found
        ValueError: If domain is invalid

    Example:
        >>> result = search("minimalism", "style", 5)
        >>> print(result['count'])  # 3
    """
    pass
```

### 1.5 Imports & Dependencies

**Rule:** Minimize external dependencies for portability

```python
# Good
import csv
from pathlib import Path
from math import log

# Avoid
import numpy  # Not in stdlib, adds weight
import requests  # Use only if absolutely necessary
```

**Organization:**
1. Stdlib imports first
2. Third-party imports next (none for search engine)
3. Local imports last
4. Blank line between groups

### 1.6 Error Handling

```python
# Good
try:
    result = _search_csv(filepath, columns, query, max_results)
except FileNotFoundError:
    return {"error": f"File not found: {filepath}", "domain": domain}
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise

# Avoid
try:
    # code
except:
    pass  # Silent failures are bad
```

### 1.7 Type Hints

**Required for:**
- Public function signatures
- Class methods with complex logic
- Design system generator (all methods)

**Format:**
```python
def _search_csv(
    filepath: Path,
    search_cols: list[str],
    output_cols: list[str],
    query: str,
    max_results: int
) -> list[dict]:
    """Search CSV and return results."""
    pass

# Return types
def get_results(self) -> dict[str, any]:
    pass
```

### 1.8 Code Comments

**Good comments explain WHY, not WHAT:**

```python
# Good
# BM25 uses k1=1.5 and b=0.75 (standard tuning for document length normalization)
idf = log((self.N - freq + 0.5) / (freq + 0.5) + 1)

# Avoid
# Calculate log
idf = log((self.N - freq + 0.5) / (freq + 0.5) + 1)

# Good
# Exclude words < 3 chars to reduce noise (and, the, a, etc.)
return [w for w in text.split() if len(w) > 2]

# Avoid
# Filter words
return [w for w in text.split() if len(w) > 2]
```

### 1.9 Line Length

- **Maximum:** 100 characters (flexible for URLs/strings)
- **Readability:** Break long lines at logical operators

```python
# Good
if (config_exists and
    permission_granted and
    not already_installed):
    proceed()

# Avoid
if config_exists and permission_granted and not already_installed and something_else: proceed()
```

### 1.10 CSV Handling

**Rules:**
1. Always use UTF-8 encoding
2. Handle missing fields gracefully
3. Preserve field order for consistency
4. Use DictReader/DictWriter for clarity

```python
# Good
with open(filepath, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    data = list(reader)

# Handle missing
value = row.get('Column', 'default_value')

# Avoid
open(filepath)  # No encoding specified
row['Column']  # KeyError if missing
```

### 1.11 Windows Compatibility

```python
# Good - UTF-8 for emoji/special chars on Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Good - Use pathlib for cross-platform paths
from pathlib import Path
filepath = Path(__file__).parent / "data" / "styles.csv"

# Avoid
filepath = f"{os.getcwd()}\\data\\styles.csv"  # Windows-specific
```

---

## 2. TypeScript Code Standards (CLI)

### 2.1 General Style

**Compliance:** ESLint (airbnb config) + Prettier
**Min TypeScript:** 4.8+
**Target:** Node 18+

### 2.2 File Structure

```typescript
/**
 * Module purpose and usage
 */

import type { TypeName } from './types/index';
import { functionName } from './utils/logger';

// ============ TYPES ============
interface ConfigOptions {
  platform: string;
  offline?: boolean;
}

// ============ CONSTANTS ============
const PLATFORMS = ['claude', 'cursor', 'windsurf'] as const;
const DEFAULT_TIMEOUT = 30000;

// ============ EXPORTED FUNCTIONS ============
export async function initCommand(options: ConfigOptions): Promise<void> {
  // implementation
}

// ============ PRIVATE FUNCTIONS ============
function detectPlatform(): string {
  // implementation
}

// ============ MAIN ENTRY ============
export default function main() {
  // entry point
}
```

### 2.3 Naming Conventions

| Type | Format | Example |
|------|--------|---------|
| **Constants** | UPPER_SNAKE_CASE | `const MAX_RETRIES = 3` |
| **Functions** | camelCase | `function detectPlatform()` |
| **Classes** | PascalCase | `class TemplateRenderer` |
| **Interfaces** | PascalCase | `interface ConfigOptions` |
| **Types** | PascalCase | `type Platform = 'claude' \| 'cursor'` |
| **Variables** | camelCase | `let platformName = 'claude'` |
| **Private** | leadingUnderscore | `_internalFunction()` |
| **Files** | kebab-case | `template-renderer.ts`, `detect.ts` |

### 2.4 Type Definitions

**Rules:**
1. Always export types from `types/index.ts`
2. Use `type` for unions/aliases, `interface` for objects
3. Strict null checking enabled

```typescript
// types/index.ts
export interface InitOptions {
  platform: 'claude' | 'cursor' | 'windsurf';
  offline?: boolean;
  outputDir?: string;
}

export type Platform = InitOptions['platform'];

// Usage
export async function init(options: InitOptions): Promise<void> {
  const platform: Platform = options.platform;
}
```

### 2.5 Async/Await

```typescript
// Good
async function downloadAssets(): Promise<void> {
  try {
    const data = await fetchFromGitHub(url);
    await writeFiles(data);
  } catch (error) {
    logger.error(`Download failed: ${error.message}`);
    throw new Error('Failed to download assets');
  }
}

// Avoid
function downloadAssets() {
  return new Promise((resolve, reject) => {
    // callback hell
  });
}
```

### 2.6 Error Handling

```typescript
// Good - Custom error types
class InstallerError extends Error {
  constructor(message: string, public platform?: string) {
    super(message);
    this.name = 'InstallerError';
  }
}

// Usage
try {
  await installSkill(platform);
} catch (error) {
  if (error instanceof InstallerError) {
    logger.error(`Installation failed for ${error.platform}: ${error.message}`);
  } else {
    throw error;
  }
}
```

### 2.7 Comments & Documentation

```typescript
/**
 * Detects the current AI coding assistant platform.
 *
 * @returns The detected platform name, or 'unknown' if not detected
 *
 * @example
 * const platform = detectPlatform();
 * console.log(platform); // 'claude'
 */
function detectPlatform(): string {
  // implementation
}
```

### 2.8 Module Exports

```typescript
// Good - Named exports for tree-shaking
export { initCommand } from './commands/init';
export { updateCommand } from './commands/update';
export type { ConfigOptions } from './types/index';

// Avoid
export default { initCommand, updateCommand };  // Default export
export * from './types';  // Wildcard exports (less clear)
```

---

## 3. CSV Data Format Standards

### 3.1 Structure Requirements

**Rules:**
1. UTF-8 encoding (no BOM)
2. Unix line endings (LF, not CRLF)
3. Comma-separated values
4. Header row with descriptive names
5. Consistent data types per column

### 3.2 CSV Header Naming

```csv
# Good - Clear, no special chars
Style Category,Type,Keywords,Best For,Performance,Accessibility

# Avoid
StyleCat,T,KW,BF,Perf,A11y  # Unclear abbreviations
style_category,type,keywords  # snake_case in CSV (use PascalCase)
```

### 3.3 Field Requirements

**All Fields:**
- Non-empty unless explicitly optional
- Properly escaped if containing quotes/commas
- Consistent data type per column

```csv
Style Category,Keywords,Best For
"Glassmorphism","glass, frosted, transparency, modern",SaaS apps
"Claymorphism","clay, soft, rounded, tactile",Educational apps
```

### 3.4 Data Consistency

| Domain | Requirement | Example |
|--------|------------|---------|
| **Styles** | Consistent capitalization | "Glassmorphism" not "glassmorphism" |
| **Colors** | Valid hex format | #E8B4B8 not E8B4B8 or #e8b4b8 (case-insensitive OK) |
| **Products** | Consistent categories | "SaaS" not "saas" or "SAAS" |
| **URLs** | Absolute, http/https | https://fonts.google.com/... |
| **Lists** | Comma-separated, consistent | "item1, item2, item3" |

### 3.5 Search Column Selection

**Rules:**
1. Include searchable columns in config
2. Exclude very long text (use truncation in output)
3. Prioritize frequently-searched fields

```python
# In core.py CSV_CONFIG
"style": {
    "file": "styles.csv",
    "search_cols": ["Style Category", "Keywords", "Best For", "Type", "AI Prompt Keywords"],
    "output_cols": ["Style Category", "Type", "Keywords", ..., "Design System Variables"]
}
```

### 3.6 Size Guidelines

| File | Max Rows | Max Size | Rationale |
|------|----------|----------|-----------|
| styles.csv | 100 | 100KB | Most important, larger acceptable |
| typography.csv | 100 | 50KB | Detailed font information |
| products.csv | 150 | 50KB | Comprehensive product coverage |
| colors.csv | 150 | 50KB | Industry-specific palettes |
| Others | 50 | 20KB | Specialized domains |

---

## 4. Git & Version Control

### 4.1 Branching Strategy

**Pattern:** `<type>/<description>`

```bash
# Feature development
git checkout -b feat/add-design-system-caching
git checkout -b feat/support-droid-platform

# Bug fixes
git checkout -b fix/windows-unicode-emoji
git checkout -b fix/version-mismatch-plugin

# Documentation
git checkout -b docs/update-codebase-summary

# Refactoring
git checkout -b refactor/modularize-design-system

# Never commit directly to main
```

### 4.2 Commit Message Format

**Standard:** Conventional Commits

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `refactor:` - Code restructuring
- `perf:` - Performance improvement
- `test:` - Test additions
- `chore:` - Build, CI, dependencies

**Examples:**
```bash
git commit -m "feat(design-system): add caching for repeated queries"
git commit -m "fix(cli): resolve Windows emoji encoding issue"
git commit -m "docs(readme): update installation instructions"
git commit -m "refactor(search): extract reasoning rules to separate module"
```

### 4.3 Code Review Checklist

Before pushing, verify:
- [ ] Code follows style standards (Python PEP 8, TypeScript ESLint)
- [ ] No hardcoded values or secrets
- [ ] Tests pass (if applicable)
- [ ] Linting passes
- [ ] Documentation updated
- [ ] Version numbers correct
- [ ] Commit message is descriptive
- [ ] No unnecessary files committed

### 4.4 Release Process

```bash
# 1. Update version numbers
# - cli/package.json
# - .claude-plugin/marketplace.json
# - .claude-plugin/plugin.json

# 2. Update CHANGELOG
# - Note what changed, list new features/fixes

# 3. Sync CLI assets
cp -r src/ui-ux-pro-max/data/* cli/assets/data/
cp -r src/ui-ux-pro-max/scripts/* cli/assets/scripts/
cp -r src/ui-ux-pro-max/templates/* cli/assets/templates/

# 4. Build and test
cd cli && bun run build
node dist/index.js init --ai claude --offline

# 5. Publish
npm publish

# 6. Tag release
git tag -a v2.2.3 -m "Release v2.2.3"
git push origin v2.2.3
```

---

## 5. Testing Standards

### 5.1 Python Tests (pytest)

**Location:** `tests/test_*.py`
**Target Coverage:** ≥ 70%

```python
# tests/test_core.py
import pytest
from core import BM25, search

class TestBM25:
    """Test BM25 ranking algorithm"""

    def test_tokenize_removes_short_words(self):
        bm25 = BM25()
        tokens = bm25.tokenize("the quick brown fox jumps")
        assert "the" not in tokens
        assert "quick" in tokens

    def test_search_returns_top_results(self):
        result = search("minimalism", "style", max_results=3)
        assert result['count'] <= 3
        assert 'Minimalism' in [r.get('Style Category') for r in result['results']]

@pytest.mark.skip(reason="Requires CSV files")
def test_design_system_generation():
    """Design system generation test"""
    pass
```

### 5.2 TypeScript Tests (vitest)

**Location:** `cli/src/__tests__/test_*.ts`
**Target Coverage:** ≥ 70%

```typescript
import { describe, it, expect, beforeEach } from 'vitest';
import { detectPlatform } from '../utils/detect';

describe('Platform Detection', () => {
  it('should detect Claude Code', () => {
    process.env.CLAUDE_CODE = 'true';
    const platform = detectPlatform();
    expect(platform).toBe('claude');
  });

  it('should return unknown for undetected platform', () => {
    delete process.env.CLAUDE_CODE;
    const platform = detectPlatform();
    expect(platform).toMatch(/unknown|fallback/);
  });
});
```

### 5.3 Integration Tests

```python
# Integration test: Full design system generation
def test_design_system_beauty_spa():
    """Test design system generation for beauty spa"""
    result = generate_design_system(
        "beauty spa wellness",
        "Serenity Spa",
        format="ascii"
    )

    # Assertions
    assert "Serenity Spa" in result
    assert "STYLE:" in result
    assert "COLORS:" in result
    assert "TYPOGRAPHY:" in result
    assert "ANTI-PATTERNS:" in result
```

### 5.4 Linting & Formatting

**Python:**
```bash
# Install
pip install black flake8 mypy

# Format
black src/ui-ux-pro-max/scripts/

# Lint
flake8 src/ui-ux-pro-max/scripts/

# Type check
mypy src/ui-ux-pro-max/scripts/
```

**TypeScript:**
```bash
# Install
npm install --save-dev eslint prettier @typescript-eslint/parser

# Format
prettier --write cli/src/

# Lint
eslint cli/src/

# Type check
tsc --noEmit
```

---

## 6. Documentation Standards

### 6.1 Markdown Style

**File Structure:**
```markdown
# Main Title (H1)

Brief intro (1-2 sentences)

## Section (H2)

Content with `code inline`

### Subsection (H3)

- Bullet point
- Another point

| Column 1 | Column 2 |
|----------|----------|
| Data | More data |

## Code Blocks

\`\`\`python
# Language-specified
def example():
    pass
\`\`\`

## Links

[Text](relative/path.md) or [Text](https://example.com)
```

### 6.2 README Requirements

- [ ] One-sentence project description
- [ ] Installation instructions (quick start)
- [ ] Basic usage examples
- [ ] Supported platforms/stacks
- [ ] Contributing guidelines
- [ ] License information
- [ ] Links to detailed docs in `docs/`

**Max Length:** 300 lines (link to docs/ for details)

### 6.3 Code Example Standards

**All examples must:**
1. Be runnable (copy-paste and work)
2. Show expected output
3. Include comments explaining WHY
4. Use realistic data

```python
# Good example with explanation
def example_search():
    """Example: Search for minimalism style"""
    result = search("minimalism", "style", max_results=3)

    # Result contains metadata + top matches
    print(f"Domain: {result['domain']}")  # 'style'
    print(f"Found: {result['count']} results")  # 3
    print(result['results'][0]['Style Category'])  # 'Minimalism & Swiss Style'
```

---

## 7. Accessibility Standards

### 7.1 Design System Accessibility

**All generated designs must:**
1. WCAG AA compliance minimum
2. Text contrast ≥ 4.5:1 (normal text)
3. Focus states visible for keyboard nav
4. Respect `prefers-reduced-motion`
5. No information conveyed by color alone

### 7.2 UI Component Accessibility

```html
<!-- Good -->
<button class="cta" aria-label="Subscribe to newsletter">
  Subscribe
</button>

<!-- Avoid -->
<div class="button" onclick="...">Subscribe</div>
```

### 7.3 Color Palette Guidelines

**Rules:**
1. Check contrast ratios (WebAIM Contrast Checker)
2. Include colorblind-safe palettes
3. Don't rely on color alone for meaning
4. Test with Lighthouse/axe DevTools

---

## 8. Performance Standards

### 8.1 Python Performance

| Operation | Target | Limit |
|-----------|--------|-------|
| CSV load | < 50ms | 100ms |
| BM25 index | < 100ms | 200ms |
| Single search | < 200ms | 500ms |
| Design system | < 2s | 3s |

**Optimization Strategies:**
- Load CSVs once, cache in memory
- Use generators for large datasets
- Profile with `cProfile` before optimizing

### 8.2 CLI Performance

| Operation | Target | Limit |
|-----------|--------|-------|
| Platform detection | < 100ms | 200ms |
| Template rendering | < 50ms | 100ms |
| File generation | < 1s | 2s |
| Full installation | < 5s | 10s |

---

## 9. Security Standards

### 9.1 Code Security

**Rules:**
1. No hardcoded API keys/secrets
2. No eval() or dynamic code execution
3. Sanitize user input (file paths, queries)
4. Validate CSV data before use

```python
# Good
filepath = Path(__file__).parent / "data" / filename
if not filepath.is_file():
    raise ValueError(f"File not found: {filename}")

# Avoid
filepath = f"./data/{user_input}"  # Path traversal vulnerability
exec(user_query)  # Code injection
```

### 9.2 Dependency Security

```bash
# Regular audits
npm audit
pip audit

# Only add necessary dependencies
# No "just in case" packages
```

### 9.3 Data Privacy

- No telemetry without consent
- Generated design systems stay local
- No tracking of user queries

---

## 10. File Organization Best Practices

### 10.1 Project Structure Enforcement

**Rule:** Always edit in `src/ui-ux-pro-max/`, sync to CLI/skill

```
CORRECT:
  1. Edit src/ui-ux-pro-max/data/styles.csv
  2. Run sync: cp -r src/ui-ux-pro-max/data/* cli/assets/data/
  3. Test in CLI
  4. Commit both src/ and cli/assets/

WRONG:
  1. Edit cli/assets/data/styles.csv directly
  2. Changes lost on next sync
```

### 10.2 CSV File Organization

```
data/
├── styles.csv              # Must exist
├── colors.csv              # Must exist
├── typography.csv          # Must exist
├── products.csv            # Must exist
├── charts.csv              # Must exist
├── landing.csv             # Must exist
├── ui-reasoning.csv        # Must exist (v2.0+)
├── ux-guidelines.csv       # Required
├── icons.csv               # Optional
├── react-performance.csv   # Optional
├── web-interface.csv       # Optional
└── stacks/                 # 13 stack CSVs
    ├── html-tailwind.csv
    ├── react.csv
    └── ... (11 more)
```

---

## 11. Unresolved Questions

1. **Test Framework:** Should we use pytest + vitest, or add coverage tools like coverage.py?
2. **CI/CD:** Should we add GitHub Actions for linting/testing on PR?
3. **Python Version:** Drop support for Python 3.8 and require 3.9+ for better type hints?
4. **Linting Config:** Should we enforce strict mypy mode or keep pragmatic?
5. **API Stability:** How to version the Python API (core.py/design_system.py) for external users?
