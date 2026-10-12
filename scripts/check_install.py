"""Install the checkout in a temporary project; compare both complete packages."""

import subprocess
import tempfile
from pathlib import Path


def check_copy(source, destination):
    expected = {p.relative_to(source): p.read_bytes() for p in source.rglob("*") if p.is_file()}
    actual = {
        p.relative_to(destination): p.read_bytes() for p in destination.rglob("*") if p.is_file()
    }
    if expected != actual:
        missing = sorted(str(p) for p in expected.keys() - actual.keys())
        extra = sorted(str(p) for p in actual.keys() - expected.keys())
        changed = sorted(
            str(p) for p in expected.keys() & actual.keys() if expected[p] != actual[p]
        )
        raise AssertionError(f"{destination}: missing={missing}, extra={extra}, changed={changed}")
    return len(expected)


def main():
    repo = Path(__file__).resolve().parents[1]
    with tempfile.TemporaryDirectory(prefix="product-team-ci-") as directory:
        target = Path(directory)
        subprocess.run(["git", "init", "--quiet", str(target)], check=True, timeout=30)
        subprocess.run(
            [
                str(repo / "node_modules/.bin/skills"),
                "add",
                str(repo),
                "--agent",
                "codex",
                "claude-code",
                "--copy",
                "--yes",
            ],
            cwd=target,
            check=True,
            timeout=240,
        )
        for skill in sorted((repo / "skills").iterdir()):
            if not (skill / "SKILL.md").is_file():
                continue
            for agent_dir in (".agents", ".claude"):
                count = check_copy(skill, target / agent_dir / "skills" / skill.name)
                print(f"{agent_dir}: {skill.name}: {count} files match")


if __name__ == "__main__":
    main()
