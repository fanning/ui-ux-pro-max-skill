# Deployment & Release Guide

**Version:** 2.2.3
**Last Updated:** 2026-02-07
**Audience:** Maintainers, DevOps, Release Managers

---

## 1. Pre-Release Checklist

### 1.1 Code Verification

Before any release, verify:

```bash
# 1. Check git status (clean working directory)
git status
# Expected: On branch main, nothing to commit

# 2. Update version numbers in all files
# - cli/package.json
# - .claude-plugin/plugin.json
# - .claude-plugin/marketplace.json
# - CHANGELOG.md (create if needed)
VERSION="2.2.3"

# 3. Verify all tests pass
cd src/ui-ux-pro-max && pytest tests/  # When added in v2.3
cd ../../cli && npm test

# 4. Run linting
npm run lint
python -m flake8 src/ui-ux-pro-max/scripts/
python -m mypy src/ui-ux-pro-max/scripts/

# 5. Run CLI build
npm run build

# 6. Test installation in temporary directory
mkdir /tmp/test-uipro
cd /tmp/test-uipro
node /path/to/cli/dist/index.js init --ai claude --offline
# Verify files generated correctly
```

### 1.2 Documentation Verification

```bash
# Check that docs are updated
grep -r "2.2.3" docs/
# Should find version in multiple places

# Verify all links work
grep -r "\[.*\](.*\.md)" docs/
# Should find internal links pointing to existing files

# Check for broken references
grep -r "TODO\|FIXME\|XXX" docs/
# Should be minimal (only intentional notes)
```

### 1.3 Platform Testing

Test the full installation flow for each platform:

```bash
# Test Claude Code (macOS/Linux/Windows)
uipro init --ai claude --offline

# Test Cursor
uipro init --ai cursor --offline

# Test Windsurf
uipro init --ai windsurf --offline

# Test GitHub Copilot
uipro init --ai copilot --offline

# Test offline mode (no GitHub download)
uipro init --ai claude --offline
# Should succeed without network call
```

---

## 2. Release Process

### 2.1 Create Release Branch

```bash
# Create release branch
git checkout -b release/v2.2.3

# Update version numbers
sed -i 's/"version": "2.2.2"/"version": "2.2.3"/' cli/package.json
sed -i 's/"version": "2.2.1"/"version": "2.2.3"/' .claude-plugin/marketplace.json
sed -i 's/"version": "2.0.1"/"version": "2.2.3"/' .claude-plugin/plugin.json

# Create CHANGELOG entry
cat >> CHANGELOG.md << 'EOF'
## [2.2.3] - 2026-02-07

### Added
- Droid (Factory) platform support
- Improved error messages for edge cases

### Fixed
- Version alignment (2.0.1 → 2.2.3 in plugin.json)
- Windows emoji encoding in design system output

### Changed
- Updated CLI assets synchronization

### Security
- No security issues reported
EOF

# Commit
git add .
git commit -m "chore: release v2.2.3

- Update version numbers across all files
- Add Droid platform support
- Align plugin.json with current version"
```

### 2.2 Sync CLI Assets

**Critical:** Must sync before npm publish

```bash
# Copy data files
cp -r src/ui-ux-pro-max/data/* cli/assets/data/

# Copy scripts
cp -r src/ui-ux-pro-max/scripts/* cli/assets/scripts/

# Copy templates
cp -r src/ui-ux-pro-max/templates/* cli/assets/templates/

# Verify sync
ls -la cli/assets/data/ | wc -l
ls -la cli/assets/scripts/ | wc -l
ls -la cli/assets/templates/ | wc -l

# Should match src/ structure

# Commit sync
git add cli/assets/
git commit -m "chore: sync CLI assets from src/"
```

### 2.3 Build & Test

```bash
# Build CLI
cd cli
npm run build

# Verify build output
ls -la dist/
# Should contain: index.js, index.js.map, package.json

# Test build output
node dist/index.js --help
# Should display help menu

# Test init command
mkdir /tmp/release-test
cd /tmp/release-test
node /path/to/cli/dist/index.js init --ai claude --offline
# Verify installation succeeds

cd - # Return to project root
```

### 2.4 Create GitHub Release

```bash
# Create git tag
git tag -a v2.2.3 -m "Release v2.2.3

- Droid platform support
- Version alignment
- CLI asset synchronization
- Bug fixes and improvements"

# Push to remote
git push origin release/v2.2.3
git push origin v2.2.3

# Create GitHub release via gh CLI
gh release create v2.2.3 \
  --title "UI/UX Pro Max v2.2.3" \
  --notes "## Features
- Droid (Factory) platform support
- Improved error messages

## Fixes
- Version alignment (plugin.json)
- Windows emoji encoding

## Installation
\`\`\`bash
npm install -g uipro-cli@2.2.3
uipro init --ai claude
\`\`\`"
```

---

## 3. npm Package Publishing

### 3.1 npm Authentication

```bash
# Login to npm (one-time)
npm login
# Prompts for username, password, 2FA code

# Verify login
npm whoami
# Should show your npm username

# Set up credentials for CI (optional)
npm token create --read-only
# For GitHub Actions, add as NPM_TOKEN secret
```

### 3.2 Publish to npm

```bash
# From cli/ directory
cd cli

# Verify package.json is correct
cat package.json | grep version
# Should show 2.2.3

# Do a dry run first (recommended)
npm publish --dry-run
# Shows what would be published without doing it

# Publish for real
npm publish

# Verify on npm registry
npm info uipro-cli
# Should show version 2.2.3 in "dist-tags"
```

### 3.3 Post-Publish Verification

```bash
# Install from npm (tests installation)
npm install -g uipro-cli@2.2.3

# Verify it works
uipro --version
# Should output: 2.2.3

# Test init command with installed version
mkdir /tmp/final-test
cd /tmp/final-test
uipro init --ai claude --offline

# Check file structure
ls -la .claude/skills/ui-ux-pro-max/
# Should contain SKILL.md, data/, scripts/, templates/
```

---

## 4. Claude Marketplace Publishing

### 4.1 Marketplace Submission

**Requirements:**
- GitHub repository must be public
- plugin.json or marketplace.json in root
- All versions aligned
- Feature descriptions accurate

### 4.2 Update Marketplace Metadata

```json
{
  ".claude-plugin/marketplace.json": {
    "name": "ui-ux-pro-max-skill",
    "id": "ui-ux-pro-max-skill",
    "metadata": {
      "description": "UI/UX design intelligence skill with 67 styles, 96 palettes, 57 font pairings, 25 charts, and 13 stack guidelines",
      "version": "2.2.3"
    },
    "plugins": [
      {
        "name": "ui-ux-pro-max",
        "version": "2.2.3",
        "description": "Professional UI/UX design intelligence for AI coding assistants..."
      }
    ]
  }
}
```

### 4.3 Submit to Marketplace

```bash
# Automatic via GitHub integration
# Marketplace watches for:
# - marketplace.json in root
# - Version tag matches marketplace version
# - Automatic sync on push to main

# Manual submission (if needed)
# Go to: https://marketplace.claude.ai/
# Click "Submit Plugin"
# Select repository: nextlevelbuilder/ui-ux-pro-max-skill
# Review metadata
# Click "Publish"
```

---

## 5. Continuous Integration / CD

### 5.1 GitHub Actions Workflow

Create `.github/workflows/release.yml`:

```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: 18
          registry-url: https://registry.npmjs.org/

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Run tests
        run: |
          cd cli && npm test
          python -m pytest src/ui-ux-pro-max/tests/

      - name: Run linting
        run: |
          npm run lint
          python -m flake8 src/ui-ux-pro-max/scripts/

      - name: Sync CLI assets
        run: |
          cp -r src/ui-ux-pro-max/data/* cli/assets/data/
          cp -r src/ui-ux-pro-max/scripts/* cli/assets/scripts/
          cp -r src/ui-ux-pro-max/templates/* cli/assets/templates/

      - name: Build CLI
        run: cd cli && npm run build

      - name: Publish to npm
        run: cd cli && npm publish
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}

      - name: Create GitHub Release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ github.ref }}
          release_name: Release ${{ github.ref }}
          body: |
            Release notes here
            ## Installation
            ```bash
            npm install -g uipro-cli@${{ github.ref }}
            uipro init --ai claude
            ```
          draft: false
          prerelease: false
```

### 5.2 Pre-commit Hooks

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash

# Check that versions are aligned
VERSION_CLI=$(grep '"version"' cli/package.json | head -1 | grep -o '"[^"]*"' | tail -1 | tr -d '"')
VERSION_MARKETPLACE=$(grep '"version"' .claude-plugin/marketplace.json | head -1 | grep -o '"[^"]*"' | tail -1 | tr -d '"')
VERSION_PLUGIN=$(grep '"version"' .claude-plugin/plugin.json | head -1 | grep -o '"[^"]*"' | tail -1 | tr -d '"')

if [ "$VERSION_CLI" != "$VERSION_MARKETPLACE" ] || [ "$VERSION_CLI" != "$VERSION_PLUGIN" ]; then
    echo "❌ Version mismatch!"
    echo "  CLI: $VERSION_CLI"
    echo "  Marketplace: $VERSION_MARKETPLACE"
    echo "  Plugin: $VERSION_PLUGIN"
    exit 1
fi

echo "✓ Versions aligned: $VERSION_CLI"
```

---

## 6. Rollback Procedures

### 6.1 npm Rollback

```bash
# If something went wrong after publishing

# Option 1: Deprecate version
npm deprecate uipro-cli@2.2.3 "Broken release, use 2.2.2"

# Option 2: Publish patch immediately
# Fix bug
git checkout -b hotfix/v2.2.4
# ... make fixes ...
# Follow release process for v2.2.4

# Option 3: Unpublish (not recommended, breaks caching)
npm unpublish uipro-cli@2.2.3
```

### 6.2 Git Rollback

```bash
# If tag was created in error
git tag -d v2.2.3  # Delete local tag
git push origin :refs/tags/v2.2.3  # Delete remote tag

# If branch was merged
git revert -m 1 <commit-hash>
git push origin main
```

### 6.3 Marketplace Rollback

```bash
# Marketplace sync is automatic
# To fix:
1. Fix plugin.json/marketplace.json
2. Push to main
3. Marketplace auto-syncs within 5 minutes
4. Broken version remains available (manual cleanup via marketplace UI)
```

---

## 7. Release Documentation

### 7.1 CHANGELOG Format

```markdown
# Changelog

All notable changes to this project will be documented in this file.

## [2.2.3] - 2026-02-07

### Added
- Droid (Factory) platform support
- Caching layer for repeated queries (v2.3 target)

### Fixed
- Version alignment: plugin.json updated from v2.0.1 to v2.2.3
- Windows emoji encoding in design system output

### Changed
- CLI assets synchronization before publish
- Improved error messages for missing CSVs

### Security
- No security vulnerabilities reported

### Deprecated
- Legacy plugin format (v2.0.1) - use v2.2.3+

## [2.2.1] - 2026-01-15

### Added
- Marketplace integration
- v2.0 design system generation
```

### 7.2 Release Notes Template

```markdown
## UI/UX Pro Max v2.2.3

Professional UI/UX design intelligence for 15 AI coding assistants.

### What's New

#### Droid Platform Support
UI/UX Pro Max now works with Droid (Factory mode)! Install with:
```bash
uipro init --ai droid
```

#### Bug Fixes
- Fixed version mismatch in plugin.json (was v2.0.1, now v2.2.3)
- Fixed Windows emoji encoding in design system output

#### Improved Installation
- Faster offline installation (uses bundled assets)
- Better error messages for troubleshooting

### Installation

```bash
npm install -g uipro-cli@2.2.3
uipro init --ai claude      # Claude Code
uipro init --ai cursor      # Cursor
uipro init --ai windsurf    # Windsurf
uipro init --ai copilot     # GitHub Copilot
# ... and 10+ other platforms
```

### Documentation

- [Quick Start](README.md)
- [Design System Generation](docs/system-architecture.md)
- [Platform Guides](docs/)
- [Contributing](CONTRIBUTING.md)

### Downloads

- npm: `npm install -g uipro-cli@2.2.3`
- GitHub: [Download Release](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/releases/tag/v2.2.3)

### Credits

Thank you to all contributors and the community! 🎉

---

**Previous Releases:** [Changelog](CHANGELOG.md) | [Releases](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/releases)
```

---

## 8. Deployment Checklist

### 8.1 Before Release

- [ ] All tests pass locally
- [ ] Linting passes (Python & TypeScript)
- [ ] Version numbers aligned (2.2.3)
- [ ] CHANGELOG updated
- [ ] CLI assets synced
- [ ] README reviewed and updated
- [ ] Documentation links verified
- [ ] No console.log or debug statements
- [ ] No hardcoded secrets or API keys

### 8.2 During Release

- [ ] Create release branch: `release/v2.2.3`
- [ ] Update version numbers in all files
- [ ] Commit changes with descriptive message
- [ ] Build CLI: `npm run build`
- [ ] Test installation in temp directory
- [ ] Create GitHub tag: `git tag -a v2.2.3`
- [ ] Push branch and tag to GitHub
- [ ] Publish to npm: `npm publish`
- [ ] Verify npm package page
- [ ] Create GitHub release with notes
- [ ] Update marketplace.json

### 8.3 After Release

- [ ] Announce on social media (@nextlevelbuilder)
- [ ] Post to GitHub Discussions
- [ ] Update website homepage (if applicable)
- [ ] Send email to newsletter subscribers
- [ ] Monitor GitHub issues for bugs
- [ ] Respond to user questions
- [ ] Update installed version info in docs

---

## 9. Monitoring & Analytics

### 9.1 npm Package Metrics

```bash
# View downloads
npm view uipro-cli downloads

# View version distribution
npm view uipro-cli versions

# View weekly downloads
curl -s 'https://api.npmjs.org/downloads/point/last-week/uipro-cli'
```

### 9.2 GitHub Metrics

```bash
# Clone stats
git clone https://github.com/nextlevelbuilder/ui-ux-pro-max-skill.git
cd ui-ux-pro-max-skill
git log --oneline | wc -l  # Total commits

# Star history
# View at: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/stargazers
```

### 9.3 User Feedback

- Monitor GitHub issues
- Review npm package reviews
- Check marketplace ratings
- Respond to GitHub Discussions
- Analyze error reports

---

## 10. Troubleshooting Deployment Issues

### 10.1 npm Publish Fails

```bash
# Issue: "npm ERR! 403 Forbidden"
# Solution: Check npm credentials
npm login
npm whoami

# Issue: "npm ERR! 404 Not Found"
# Solution: Check package.json name and files
cat cli/package.json | grep -E '"name"|"files"'

# Issue: "npm ERR! version conflicts"
# Solution: Increment version
npm version patch  # Bumps version automatically
```

### 10.2 GitHub Release Fails

```bash
# Issue: "fatal: tag 'v2.2.3' already exists"
# Solution: Delete existing tag
git tag -d v2.2.3
git push origin :refs/tags/v2.2.3

# Issue: "Permission denied"
# Solution: Check GitHub token
gh auth login
gh auth status
```

### 10.3 Platform Installation Fails

```bash
# Issue: ".claude directory not found"
# Solution: Create manually or use --create flag
mkdir -p ~/.claude/skills
uipro init --ai claude

# Issue: "Python not found"
# Solution: Ensure Python 3 installed
python3 --version
which python3
```

---

## 11. Unresolved Questions

1. **Automated Testing:** Should we add nightly tests for all 15 platforms?
2. **Analytics:** How to track which platforms are most popular?
3. **Deprecation Policy:** When to remove support for old platforms?
4. **Semantic Versioning:** Should design system changes trigger minor version bumps?
5. **Security Updates:** Process for immediate security patches?
