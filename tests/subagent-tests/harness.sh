#!/bin/bash
# Test harness for subagent testing
# Source this in test scripts

RESULTS_DIR="${RESULTS_DIR:-results}"
mkdir -p "$RESULTS_DIR"

# Initialize result file for this test
init_test() {
    local test_id="$1"
    local test_name="$2"
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    
    cat > "$RESULTS_DIR/${test_id}.json" <<EOF
{
  "test_id": "$test_id",
  "test_name": "$test_name",
  "timestamp": "$timestamp",
  "status": "RUNNING",
  "expected": {},
  "actual": {},
  "errors": [],
  "latency_ms": 0
}
EOF
}

# Record expected behavior
expect() {
    local test_id="$1"
    local key="$2"
    local value="$3"
    
    # Read current file, update expected
    python3 -c "
import json
with open('$RESULTS_DIR/${test_id}.json') as f:
    d = json.load(f)
d['expected']['$key'] = '$value'
with open('$RESULTS_DIR/${test_id}.json', 'w') as f:
    json.dump(d, f, indent=2)
"
}

# Record actual result
record() {
    local test_id="$1"
    local key="$2"
    local value="$3"
    
    python3 -c "
import json
with open('$RESULTS_DIR/${test_id}.json') as f:
    d = json.load(f)
d['actual']['$key'] = '$value'
with open('$RESULTS_DIR/${test_id}.json', 'w') as f:
    json.dump(d, f, indent=2)
"
}

# Record error
error() {
    local test_id="$1"
    local message="$2"
    
    python3 -c "
import json
with open('$RESULTS_DIR/${test_id}.json') as f:
    d = json.load(f)
d['errors'].append('$message')
with open('$RESULTS_DIR/${test_id}.json', 'w') as f:
    json.dump(d, f, indent=2)
"
}

# Mark test as passed/failed
finalize() {
    local test_id="$1"
    local status="$2"  # PASS or FAIL
    local notes="$3"
    
    python3 -c "
import json
with open('$RESULTS_DIR/${test_id}.json') as f:
    d = json.load(f)
d['status'] = '$status'
if '$notes':
    d['notes'] = '$notes'
with open('$RESULTS_DIR/${test_id}.json', 'w') as f:
    json.dump(d, f, indent=2)
"
}

# Check if error contains 401/auth pattern
is_auth_error() {
    local output="$1"
    if echo "$output" | grep -qi "401\|Invalid Authentication\|Unauthorized"; then
        return 0
    fi
    return 1
}

# Check if error contains tool failure pattern
is_tool_failure() {
    local output="$1"
    if echo "$output" | grep -qi "Tool not found\|sandbox unavailable\|tool.*not.*found"; then
        return 0
    fi
    return 1
}

# Check if output indicates model fallback
is_fallback() {
    local output="$1"
    local expected_model="$2"
    if echo "$output" | grep -qi "fallback\|MiniMax\|glm-5\|using.*instead"; then
        return 0
    fi
    # Check if model in output doesn't match expected
    if echo "$output" | grep -q "model.*k2p" && ! echo "$output" | grep -q "model.*$expected_model"; then
        return 0
    fi
    return 1
}

# Print summary of all results
print_summary() {
    echo ""
    echo "========================================"
    echo "           SUBAGENT TEST SUMMARY"
    echo "========================================"
    echo ""
    
    local passed=0
    local failed=0
    local total=0
    
    for f in "$RESULTS_DIR"/test-*.json; do
        if [ -f "$f" ]; then
            total=$((total + 1))
            local id=$(basename "$f" .json)
            local status=$(python3 -c "import json; d=json.load(open('$f')); print(d.get('status','UNKNOWN'))")
            local name=$(python3 -c "import json; d=json.load(open('$f')); print(d.get('test_name','?'))")
            local errors=$(python3 -c "import json; d=json.load(open('$f')); print(len(d.get('errors',[])))")
            
            if [ "$status" = "PASS" ]; then
                passed=$((passed + 1))
                echo "✅ $id: $name"
            else
                failed=$((failed + 1))
                echo "❌ $id: $name ($errors errors)"
                python3 -c "import json; d=json.load(open('$f')); 
for e in d.get('errors',[]): print(f'   → {e}')
for k,v in d.get('actual',{}).items(): print(f'   → $k: {v}')
"
            fi
        fi
    done
    
    echo ""
    echo "========================================"
    echo "  Total: $total | Passed: $passed | Failed: $failed"
    echo "========================================"
    
    if [ $failed -gt 0 ]; then
        return 1
    fi
    return 0
}
