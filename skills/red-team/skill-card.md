# red-team — Skill Card

| Field | Value |
|-------|-------|
| **Name** | red-team |
| **Version** | — |
| **One-liner** | Validate numerical claims through 5 gates before promoting to findings. |

## Trigger
- Any claim with numerical results, comparisons, predictions, trends
- "The result is...", "on average...", "increases with..."
- Before committing, dashboarding, or reporting results

## The 5 Gates

| Gate | Question | Required |
|------|----------|----------|
| 1 | Literature baseline — what does the literature say? | Cite a source |
| 2 | Observable audit — what did I actually compute? | Method, params, N, error bars |
| 3 | Claim taxonomy — what kind of claim is this? | Classify: point estimate, trend, bound, etc. |
| 4 | Falsification — what would prove this wrong? | 2-3 sentences on error sources |
| 5 | Peer-check — weakest point for Reviewer 2? | 1-2 sentences + review-readiness |

## Key Commands

No CLI — this is a mental protocol. Write answers out explicitly.

## Dependencies
- Access to literature (papers, arXiv, books)
- Honest self-assessment

## Quick Example

```
Claim: "Ground state energy is 0.34"

Gate 1: Literature says 0.35 ± 0.02 (Smith et al. 2024) → AGREES
Gate 2: DMRG, L=12, bond dim=512, converged to 1e-6 → CHECKED
Gate 3: Point estimate → convergence plot attached
Gate 4: If finite-size scaling wrong, artifact. Check ξ vs L. → NOTED
Gate 5: Weakest: only L=12. Reviewer 2 wants L=16, 20. → CLOSE

Verdict: TENTATIVE (pending larger system sizes)
```

> If any gate is "I don't know" or "I assume" → claim stays TENTATIVE. No exceptions.
