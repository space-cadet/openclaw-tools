# Technical Context: openclaw-tools

## Tech Stack
- **GitHub**: Public repo, `main` branch
- **Languages**: Python 3, Bash, JavaScript (for tests/benchmarks)
- **Skill Format**: SKILL.md + optional scripts/ directory
- **Memory Bank**: v6.12 text workflow (manual markdown editing)
- **CI**: None yet (GitHub Actions optional)

## Directory Structure
```
openclaw-tools/
├── skills/              # Each skill is a directory with SKILL.md
│   ├── token-usage/
│   │   ├── SKILL.md
│   │   └── scripts/
│   │       ├── parse.py
│   │       └── pricing.json
│   └── ...
├── scripts/             # Generic scripts, each with header docs
│   ├── git-guardian.sh
│   ├── daily-backup.sh
│   └── ...
├── tests/               # Benchmarks and test harnesses
│   ├── kimi-benchmarks/
│   └── subagent-tests/
├── docs/
│   ├── CONTRIBUTING.md
│   └── skill-template.md
├── memory-bank/         # Project tracking (v6.12)
└── README.md
```

## Skill Template
```
skills/<skill-name>/
├── SKILL.md          # Required: description, usage, triggers
├── skill-card.md     # Optional: quick reference card
└── scripts/          # Optional: supporting scripts
    └── ...
```

## Script Standards
- Header comment with: purpose, usage, dependencies, author
- No hardcoded personal paths (use `$HOME` or environment variables)
- No secrets or API keys
- Exit codes: 0 = success, 1 = error, 2 = warning
- Prefer `#!/usr/bin/env bash` or `#!/usr/bin/env python3`

## Git Workflow
- `main` branch for stable releases
- Feature branches for new skills/scripts
- Squash merge for clean history
- Semantic versioning for skills (e.g., `v1.0.0` in SKILL.md)
