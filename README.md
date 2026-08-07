# RepoIntel

# RepoIntel

<div align="center">

### Engineering Intelligence for GitHub Repositories

Analyze any public GitHub repository and generate a comprehensive engineering report covering documentation quality, architecture, code health, dependencies, security, project maturity, and portfolio readiness.

Built with **FastAPI**, **Next.js**, **TypeScript**, **Python**, and **Google Gemini**.

---

![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi)
![Next.js](https://img.shields.io/badge/Next.js-Frontend-black?style=for-the-badge&logo=next.js)
![TypeScript](https://img.shields.io/badge/TypeScript-React-3178C6?style=for-the-badge&logo=typescript)
![Gemini](https://img.shields.io/badge/Google-Gemini-4285F4?style=for-the-badge&logo=google)

</div>

---

## Overview

RepoIntel is an engineering intelligence platform that evaluates GitHub repositories beyond simple code metrics.

Instead of only counting files or lines of code, RepoIntel combines deterministic static analysis with LLM-powered project classification to generate a detailed engineering assessment.

The platform inspects repository structure, documentation quality, source code, dependencies, security practices, and overall project health before producing explainable engineering scores and actionable recommendations.

---

## Features

### Repository Analysis

- Clone and inspect any public GitHub repository
- Automatic language detection
- Technology stack detection
- Repository structure visualization

### Documentation Intelligence

- README quality analysis
- Section detection
- Documentation completeness
- License detection
- Contribution guide detection
- Documentation scoring

### Code Engineering

- Source file statistics
- Code/comment ratio
- Function & class metrics
- TODO / FIXME detection
- Duplicate filename detection

### Dependency Analysis

- Detect package managers
- Count production/development dependencies
- Lock file detection
- Dependency quality metrics

### Security Checks

- Secret detection
- API key detection
- Private key detection
- Dangerous code pattern detection
- Security policy checks

### Project Health

- Test detection
- CI/CD detection
- GitHub Actions detection
- Changelog detection
- Code of Conduct detection

### AI Classification

Powered by Google Gemini

Automatically predicts

- Repository category
- Repository purpose
- Project maturity
- Classification confidence

---

# Architecture

```text
                GitHub Repository URL
                        │
                        ▼
            Repository Collector
                        │
        ┌───────────────┴───────────────┐
        ▼                               ▼
 Repository Scanner              Metadata Extraction
        │
        ▼
 Feature Extractors
 ├── Documentation
 ├── Structure
 ├── Code
 ├── Dependencies
 ├── Security
 └── Project Health
        │
        ▼
 Rule Engine
        │
        ▼
 Gemini Project Classification
        │
        ▼
 Scoring Engine
        │
        ▼
 FastAPI
        │
        ▼
 Next.js Dashboard
```

---

# Tech Stack

## Backend

- Python
- FastAPI
- GitPython
- Google Gemini
- Pydantic

## Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS
- Framer Motion
- Lucide Icons

---

# Project Structure

```text
RepoIntel
│
├── backend
│   ├── api
│   ├── core
│   │   ├── collector
│   │   ├── extractor
│   │   ├── llm
│   │   ├── rules
│   │   └── scoring
│   ├── models
│   ├── temp
│   └── requirements.txt
│
├── frontend
│   ├── src
│   ├── public
│   └── package.json
│
└── README.md
```

---

# Engineering Pipeline

```text
Repository URL
      │
      ▼
Clone Repository
      │
      ▼
Extract Repository Metrics
      │
      ▼
Run Engineering Rules
      │
      ▼
LLM Classification
      │
      ▼
Calculate Domain Scores
      │
      ▼
Generate Final Report
      │
      ▼
Interactive Dashboard
```

---

# Scoring System

The overall engineering score is computed across six independent domains.

| Domain | Weight |
|---------|--------|
| Documentation | 20 |
| Code Quality | 25 |
| Structure | 15 |
| Dependencies | 10 |
| Security | 20 |
| Project Health | 10 |

Overall Score = **100**

Every deduction is fully explainable and linked directly to a repository finding.

---

# API

### Analyze Repository

```
POST /analyze
```

Request

```json
{
  "url": "https://github.com/owner/repository"
}
```

Returns

- Repository metadata
- Engineering findings
- Project classification
- Domain scores
- Overall engineering score

---

# Running Locally

## Backend

```bash
cd backend

pip install -r requirements.txt

uvicorn api.main:app --reload
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

---

# Environment Variables

Backend

```
GEMINI_API_KEY=your_api_key
```

Frontend

```
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

---

# Screenshots

- Landing Page
- Dashboard
- Findings Panel
- Metrics Explorer

---

# Future Improvements

- Repository history
- PDF report export
- Repository comparison
- User authentication
- Background analysis queue
- Repository caching

---

# License

This project is licensed under the MIT License.

---

<div align="center">

Built using FastAPI, Next.js and Google Gemini.

</div>
