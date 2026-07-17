#!/bin/bash
# Test 01: Basic Spawn Test
# Can subagents spawn at all and complete a simple task?

source "$(dirname "$0")/harness.sh"

TEST_ID="test-01-basic-spawn"
TEST_NAME="Basic Spawn Test"

init_test "$TEST_ID" "$TEST_NAME"
expect "$TEST_ID" "behavior" "Subagent spawns, completes task, returns result"
expect "$TEST_ID" "auth_errors" "none"
expect "$TEST_ID" "model_fallback" "none"

echo "========================================"
echo "TEST 01: Basic Spawn Test"
echo "========================================"
echo ""
echo "Objective: Verify subagents can spawn and complete simple tasks"
echo ""
echo "STEPS TO RUN:"
echo "1. Call sessions_spawn with a simple task (e.g., calculate 2+2)"
echo "2. Wait for completion with sessions_yield"
echo "3. Check result"
echo ""
echo "EXPECTED: Subagent completes successfully, returns correct answer (4)"
echo ""
echo "FAILURE INDICATORS:"
echo "- 401 / Invalid Authentication errors"
echo "- Timeout without completion"
echo "- Wrong or no result returned"
echo "- Model fallback to different provider"
echo ""
echo "To run: Call sessions_spawn with task='What is 2+2?'"
echo ""
echo "Run this test? (y/n)"
read -r response

if [ "$response" = "y" ] || [ "$response" = "Y" ]; then
    echo ""
    echo "Please run the subagent and paste the result here."
    echo "(Or use Ctrl+D if you already ran it)"
    echo ""
    
    result=""
    while IFS= read -r line; do
        result="$result$line\n"
    done
    
    record "$TEST_ID" "raw_output" "$result"
    
    # Check for failures
    if is_auth_error "$result"; then
        error "$TEST_ID" "401/Authentication error detected"
    fi
    
    if echo "$result" | grep -qi "timeout\|timed out"; then
        error "$TEST_ID" "Timeout detected"
    fi
    
    if echo "$result" | grep -q "4"; then
        record "$TEST_ID" "answer" "4 (correct)"
        if ! is_auth_error "$result" && ! echo "$result" | grep -qi "timeout"; then
            finalize "$TEST_ID" "PASS" "Subagent completed and returned correct answer"
        else
            finalize "$TEST_ID" "FAIL" "Partial success but with errors"
        fi
    else
        error "$TEST_ID" "Incorrect or missing answer"
        finalize "$TEST_ID" "FAIL" "Subagent did not return expected result"
    fi
else
    finalize "$TEST_ID" "SKIPPED" "User skipped manual execution"
fi
