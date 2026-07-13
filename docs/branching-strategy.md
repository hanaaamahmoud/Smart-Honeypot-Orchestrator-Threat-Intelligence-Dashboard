# Git Branching Strategy

## Overview

This document defines the Git branching strategy and workflow used by our team during the development of the Smart Honeypot Orchestrator & Threat Intelligence Dashboard project.

The goal is to keep the repository organized, reduce merge conflicts, and ensure that all team members follow the same development process.

Team members are encouraged to work locally using Git whenever possible instead of editing files directly on GitHub.

## Branch Structure

| Branch | Purpose |
|--------|---------|
| `main` | Contains the stable and production-ready version of the project. No direct commits or pushes are allowed. |
| `develop` | Main integration branch where approved changes from feature branches are merged. |
| `feature/*` | Used for developing a single feature or task. Created from `develop` and merged back into `develop`. |
| `bugfix/*` | Used for fixing bugs found during development. |
| `docs/*` | Used for documentation updates. |
| `research/*` | Used for research, experiments, and technical investigations. |

## Branch Naming Convention

Branch names should be clear, descriptive, and use lowercase letters with hyphens (`-`) to separate words.

Examples:
- `feature/cowrie-setup`
- `feature/dashboard-websocket`
- `bugfix/docker-network`
- `docs/branching-strategy`
- `research/mitre-attack-mapping`

## Team Workflow

1. Switch to the `develop` branch.
2. Pull the latest changes from GitHub.
3. Create a new feature branch from `develop`.
4. Complete the assigned task.
5. Stage and commit your changes using a clear commit message.
6. Push the feature branch to GitHub.
7. Create a Pull Request targeting the `develop` branch.
8. Team members review the Pull Request and provide feedback if needed.
9. After approval, the repository administrator merges the Pull Request into `develop`.
10. Delete the feature branch after a successful merge.

## Commit Message Convention

Use clear and meaningful commit messages.

Examples:
- feat: add Cowrie deployment
- fix: resolve Docker networking issue
- docs: update branching strategy

## Pull Request Process

- Open a Pull Request to the `develop` branch.
- Team members review the changes.
- After team approval, the repository administrator merges the Pull Request.
- Delete the feature branch after merging.