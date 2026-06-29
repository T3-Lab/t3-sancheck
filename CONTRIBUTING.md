# Contributing to SanCheck

Thanks for your interest in contributing! SanCheck originated from concerns regarding repetitive, routine data analysis tasks; contributions are welcome from anyone wishing to help develop SanCheck further in its mission to assist others.

---

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run SanCheck:
   ```bash
   python -m src.sancheck
   ```

For full usage, see [README.md](README.md).

---

## Reporting Bugs & Suggesting Features

Please **open an Issue first** before submitting a PR — this keeps things transparent and avoids duplicate work.

When opening an Issue, include:
- What you expected to happen
- What actually happened
- Steps to reproduce (if applicable)

---

## Submitting a Pull Request

1. Fork the repository
2. Create a branch for your change
3. Submit a PR referencing the related Issue

PRs without a linked Issue may be closed without review.

---

## Hard Rule — Keep the Simplicity

> **The tool's core logic must remain lightweight and produce output interpretations that are easy to understand..**

This is SanCheck project's philosophy, not a suggestion. Contributions that entail a significant increase in complexity and poor interpretability of results will not be accepted regardless of quality.

---

(PAS)
## Contribution Spirit

SanCheck is a lightweight helper tool, not an all-in-one EDA checker. Experiments are welcome — as long as they come with an explanation of *why*. A good PR doesn't just change code, it documents the reasoning behind the change.

When in doubt, ask in an Issue first.