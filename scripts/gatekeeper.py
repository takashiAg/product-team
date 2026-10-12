"""Fail closed unless every expected prerequisite completed successfully."""

import json
import os
import sys

REQUIRED_JOBS = frozenset({"lint", "skill-validation", "security", "eval-smoke"})


def failures(needs):
    if not isinstance(needs, dict):
        return ["needs must be an object"]
    problems = []
    if set(needs) != REQUIRED_JOBS:
        problems.append(f"Unexpected dependency set: {sorted(needs)}")
    for name in sorted(REQUIRED_JOBS):
        job = needs.get(name)
        if not isinstance(job, dict) or job.get("result") != "success":
            problems.append(f"{name}: {job!r}")
    return problems


if __name__ == "__main__":
    try:
        errors = failures(json.loads(os.environ["NEEDS_JSON"]))
    except (KeyError, ValueError) as exc:
        errors = [f"Missing or invalid dependency results: {exc}"]
    if errors:
        print("Gatekeeper rejected:\n" + "\n".join(errors), file=sys.stderr)
        sys.exit(1)
    print("Gatekeeper: all required checks succeeded.")
