# Subagent Test Suite

Tests for verifying subagent functionality in OpenClaw, with focus on Kimi-related auth/model issues.

## References

- GitHub Issue #20359: Subagent model override fails with 401 while main session works
- GitHub Issue #29965: Kimi Tool Binding Failures (tools intermittently fail after first call)

## Detecting Failures

Each test reports:
- **Result**: PASS / FAIL / ERROR
- **Expected vs Actual**: What was supposed to happen vs what did
- **Subagent model**: Which model the subagent actually used (may differ from requested)
- **Error details**: Any error messages, auth failures, tool failures
- **Latency**: How long the subagent took

## Tests

| Test | Description | Detects |
|------|-------------|---------|
| 01-basic-spawn | Simple task with no model override | Can subagents spawn at all? |
| 02-model-override | Explicit model override (K2.5, K2.6, K2.7) | 401 auth errors on specific models |
| 03-tool-access | Subagent trying to use tools | "Tool not found" / sandbox unavailable |
| 04-auth-token | Same provider/token as main | Auth token inheritance issues |
| 05-parallel | Multiple simultaneous subagents | Race conditions, rate limits |
| 06-context-fork | fork vs isolated context | Context-dependent failures |
| 07-fallback-detection | Verify actual model used | Silent fallback to different model |

## Running

```bash
# Run all tests
bash run-all.sh

# Run specific test
bash test-01-basic-spawn.sh

# View results
cat results/results.json
```
