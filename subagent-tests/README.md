# Subagent Test Suite

Tests for verifying subagent functionality in OpenClaw, with focus on Kimi-related issues.

## References

- GitHub Issue #20359: Subagent model override fails with 401 while main session works
- GitHub Issue #29965: Kimi Tool Binding Failures (tools intermittently fail after first call)

## Key Findings

### ❌ K2.6 Subagent Bug Confirmed
Subagent failures are **specific to Kimi K2.6**, not infrastructure:

| Test | Provider | Task | Result | Duration |
|------|----------|------|--------|----------|
| test-06 | Kimi K2.6 | Count 50,000 | ❌ **FAIL** | 20s + timeout |
| test-07 | OpenRouter | Count 50,000 | ✅ **PASS** | 18s |
| test-08 | **Kimi K2.7** | Count 50,000 | ✅ **PASS** | 36s |

**Conclusion**: Upgrade to **K2.7** for subagent workloads. The bug is fixed in newer models.

### Failure Patterns Detected

| Pattern | Meaning | Fix |
|---------|---------|-----|
| `CommandLaneTaskTimeoutError` | Task completes but command lane crashes | Use K2.7 or OpenRouter |
| `session completed before registry settled` | Session infrastructure crash | Reduce task complexity |
| `401 Invalid Authentication` | Auth key rejected | Check API key validity |
| `Unknown model` | Invalid model ID | Check model name format |

## Tests

| Test | Description | Detects |
|------|-------------|---------|
| 01-basic-spawn | Simple task (2+2) | Can subagents spawn at all? |
| 02-model-override | Explicit model override | 401 auth errors on specific models |
| 03-tool-access | Subagent reading files | "Tool not found" / sandbox issues |
| 04-parallel | 3 simultaneous subagents | Race conditions, rate limits |
| 05-numerics | QHE-BHE resonance graph | Complex task failures |
| 06-timeout-stress | Varying timeouts (15s-120s) | Crash threshold |
| 07-openrouter | OpenRouter comparison | Provider-specific issues |
| 08-k2.7 | K2.7 model test | K2.6 vs K2.7 comparison |

## Running Tests

```bash
# View all results
python3 run_test.py --summary

# Results are auto-recorded in results/test-NN.json
```

## Repo
https://github.com/space-cadet/openclaw-tests
