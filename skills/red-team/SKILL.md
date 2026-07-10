---
name: "red-team"
description: "Red-team protocol for validating numerical claims before promoting them from tentative to real. 5 gates: literature baseline, observable audit, claim taxonomy,"
---

# Red-Team Protocol

## Purpose

Before promoting *any* numerical claim from "tentative observation" to "finding worth reporting, committing, or dashboarding," run this protocol. No exceptions. The red team is a skeptical colleague who will tear your claim apart if you let them.

## Trigger

Any claim involving:
- Numerical results from computation or simulation
- Comparisons to literature values
- Physical predictions or bounds
- Trend identification ("increases with", "decreases with")
- Statistical summaries ("on average", "typical value")

## The 5 Gates

Answer each gate explicitly, in writing, before calling the claim a "result."

### Gate 1: Literature Baseline

**Question:** What does the literature say? What's the accepted value or range?

**Required:**
- Cite at least one source (paper, book, arXiv, review)
- State the accepted value with uncertainty if available
- Note if your result contradicts, agrees with, or extends known results

**If no literature exists:** State explicitly that this is a *prediction* with no known comparison.

**If you cannot find a source:** The claim stays **tentative** until you do.

### Gate 2: Observable Audit

**Question:** What did I actually compute? Method, parameters, sample size, error bars.

**Required:**
- Exact method name (algorithm, solver, approximation scheme)
- All parameters used (no defaults assumed without checking)
- Sample size / number of data points / convergence level
- Statistical uncertainty or error estimate
- If the computation was interrupted or resumed, say so

**No hand-waving.** "The usual parameters" or "standard settings" are not acceptable. Write the numbers down.

### Gate 3: Claim Taxonomy

**Question:** What *kind* of claim is this?

**Classify exactly one:**

| Type | Example | Required Evidence |
|------|---------|-----------------|
| Point estimate | "The ground state energy is 0.34" | Convergence plot, error bars |
| Trend | "Energy increases with g" | Multiple data points, monotonicity check |
| Existence proof | "A phase transition exists" | Finite-size scaling, multiple L values |
| Bound | "The error is less than 0.01" | Upper bound derivation, checked numerically |
| Null result | "No phase transition found" | Scan of parameter space, finite-size analysis |
| Comparison | "Our result agrees with X" | Quantitative difference, error propagation |

**If you cannot classify the claim:** It is not a result. It is an observation. Go back to work.

### Gate 4: Falsification Paragraph

**Question:** What would prove this wrong? What could I check that I'm not checking?

**Required:** Write 2-3 sentences describing:
- A plausible error source that would invalidate the claim
- A check you haven't done but could do
- A limit or caveat that makes the claim provisional

**Example:** *"If the finite-size scaling is wrong because the correlation length exceeds L=12, the trend in g_c(L) would be an artifact. I should check ξ vs L before claiming convergence."*

**If you cannot identify a falsification path:** You are not thinking hard enough. Try again.

### Gate 5: Peer-Check Gate

**Question:** If I had to explain this to a skeptical colleague, what's the weakest point?

**Required:** State the weakest point in 1-2 sentences. Then ask:
- Would this pass a peer review? (yes/no/close)
- What would Reviewer 2 complain about?

**If the weakest point is the entire claim:** The claim is not ready. Back to Gate 1.

## Enforcement

1. **Write the answers out.** Do not run the protocol mentally. Write it in the same file, message, or note where you are reporting the result.
2. **If any gate is missing or answered with "I don't know" or "I assume" — the claim stays TENTATIVE.** No exceptions.
3. **No promotion without all 5 gates.** A result without a red-team pass is a rumor, not science.
4. **When reporting to the user:** Use language that reflects the gate status:
   - All gates passed: "The result is..." (confident)
   - Some gates partial: "The tentative result is..." (cautious)
   - No gates run: "I observed..." (descriptive only)

## Red-Team Log

When a claim is promoted from tentative to confirmed, append a brief record to the red-team log (can be in the same memory file or a separate note):

```
[DATE] Claim: [one-line summary]
- Gate 1: [status] [source]
- Gate 2: [status] [method, params, N]
- Gate 3: [type]
- Gate 4: [falsification risk]
- Gate 5: [weakest point] [review-readiness]
- Verdict: CONFIRMED / TENTATIVE / REJECTED
```

## Failure Modes

These are the ways this protocol has failed in the past. Watch for them:

- **Gate 1 skipped:** "I didn't look it up because I know the answer." → You don't. Look it up.
- **Gate 2 hand-waved:** "The usual parameters." → Write them down.
- **Gate 3 misclassified:** Calling a trend a point estimate because you like the middle value. → Classify honestly.
- **Gate 4 weak:** "Maybe I made a mistake." → Be specific. What mistake? How would you detect it?
- **Gate 5 optimistic:** "I'm sure this is right." → Find the weakest point. It's there.

## Related

- `self-improving-agent` skill: Log red-team failures as learnings
- `spike` skill: Run throwaway tests to validate claims before red-teaming
