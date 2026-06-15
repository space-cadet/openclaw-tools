#!/usr/bin/env python3
"""
Subagent Test Runner
Executes test definitions and records results.

Usage:
    python3 run_test.py test-01-basic-spawn.json
    python3 run_all.py
"""

import json
import sys
import time
import subprocess
from pathlib import Path
from typing import Dict, Any, List

RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(exist_ok=True)

class SubagentTest:
    def __init__(self, config_path: str):
        with open(config_path) as f:
            self.config = json.load(f)
        
        self.test_id = self.config["test_id"]
        self.test_name = self.config["test_name"]
        self.result = {
            "test_id": self.test_id,
            "test_name": self.test_name,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "status": "PENDING",
            "spawn_config": self.config.get("spawn_config", {}),
            "expected": self.config.get("expected", {}),
            "actual": {},
            "errors": [],
            "warnings": [],
            "latency_ms": 0,
            "failure_patterns_found": []
        }
    
    def detect_failures(self, output: str) -> List[str]:
        """Check output against known failure patterns."""
        found = []
        patterns = self.config.get("failure_patterns", [])
        
        for pattern in patterns:
            if pattern.lower() in output.lower():
                found.append(pattern)
                self.error(f"Failure pattern detected: {pattern}")
        
        return found
    
    def error(self, message: str):
        self.result["errors"].append(message)
        self.result["status"] = "FAIL"
    
    def warning(self, message: str):
        self.result["warnings"].append(message)
    
    def record(self, key: str, value: Any):
        self.result["actual"][key] = value
    
    def save(self):
        output_path = RESULTS_DIR / f"{self.test_id}.json"
        with open(output_path, "w") as f:
            json.dump(self.result, f, indent=2)
        print(f"Result saved: {output_path}")
    
    def print_summary(self):
        print(f"\n{'='*50}")
        print(f"Test: {self.test_id} - {self.test_name}")
        print(f"Status: {self.result['status']}")
        print(f"Latency: {self.result['latency_ms']}ms")
        
        if self.result["errors"]:
            print(f"\n❌ Errors ({len(self.result['errors'])}):")
            for e in self.result["errors"]:
                print(f"  - {e}")
        
        if self.result["warnings"]:
            print(f"\n⚠️ Warnings ({len(self.result['warnings'])}):")
            for w in self.result["warnings"]:
                print(f"  - {w}")
        
        if self.result["failure_patterns_found"]:
            print(f"\n🔍 Failure patterns detected: {', '.join(self.result['failure_patterns_found'])}")
        
        if self.result["status"] == "PASS":
            print(f"\n✅ Test passed")
        elif self.result["status"] == "PENDING":
            print(f"\n⏳ Test pending - awaiting manual execution")
        
        print(f"{'='*50}\n")


def print_all_results():
    """Print summary of all test results."""
    print(f"\n{'='*60}")
    print("         SUBAGENT TEST SUITE - FULL SUMMARY")
    print(f"{'='*60}\n")
    
    passed = failed = pending = 0
    
    for result_file in sorted(RESULTS_DIR.glob("test-*.json")):
        with open(result_file) as f:
            result = json.load(f)
        
        status = result["status"]
        test_id = result["test_id"]
        test_name = result["test_name"]
        errors = len(result.get("errors", []))
        
        if status == "PASS":
            passed += 1
            print(f"✅ {test_id}: {test_name}")
        elif status == "FAIL":
            failed += 1
            print(f"❌ {test_id}: {test_name} ({errors} errors)")
            for e in result.get("errors", []):
                print(f"   → {e}")
        else:
            pending += 1
            print(f"⏳ {test_id}: {test_name} ({status})")
    
    total = passed + failed + pending
    print(f"\n{'='*60}")
    print(f"  Total: {total} | ✅ Passed: {passed} | ❌ Failed: {failed} | ⏳ Pending: {pending}")
    print(f"{'='*60}\n")
    
    if failed > 0:
        print("⚠️  Some tests failed. Check individual result files for details.")
        print(f"   Results directory: {RESULTS_DIR.absolute()}\n")
        return 1
    return 0


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--summary":
        sys.exit(print_all_results())
    
    if len(sys.argv) < 2:
        print("Usage: python3 run_test.py <test-config.json>")
        print("       python3 run_test.py --summary")
        sys.exit(1)
    
    test = SubagentTest(sys.argv[1])
    test.print_summary()
