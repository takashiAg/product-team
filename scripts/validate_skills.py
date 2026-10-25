"""Validate portable skill metadata, local links, and the role catalog."""

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml


def outside_code(text):
    """Ignore examples in fenced code when checking Markdown links."""
    fence = None
    for line in text.splitlines():
        match = re.match(r"^\s*(`{3,}|~{3,})", line)
        if match:
            marker = match.group(1)
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence):
                fence = None
            continue
        if fence is None:
            yield line


def local_targets(path):
    text = "\n".join(outside_code(path.read_text(encoding="utf-8")))
    inline = re.findall(r"!?\[[^\]\n]*\]\(([^)\n]+)\)", text)
    references = re.findall(r"^\s{0,3}\[[^\]]+\]:\s*(.+)$", text, re.MULTILINE)
    for raw in inline + references:
        raw = raw.strip()
        target = raw[1 : raw.index(">")] if raw.startswith("<") and ">" in raw else raw.split()[0]
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        yield unquote(parsed.path)


def validate(root):
    root = root.resolve()
    errors = []
    skills = sorted((root / "skills").glob("*/SKILL.md"))
    if not skills:
        errors.append("No skills/*/SKILL.md found")

    for entry in skills:
        skill = entry.parent
        text = entry.read_text(encoding="utf-8")
        match = re.match(r"\A---\n(.*?)\n---(?:\n|$)", text, re.DOTALL)
        if not match:
            errors.append(f"{entry.relative_to(root)}: missing YAML frontmatter")
            continue
        try:
            meta = yaml.safe_load(match.group(1))
        except yaml.YAMLError as exc:
            errors.append(f"{entry.relative_to(root)}: invalid YAML: {exc}")
            continue
        if not isinstance(meta, dict):
            errors.append(f"{entry.relative_to(root)}: frontmatter must be a mapping")
            continue
        allowed = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
        unknown = set(meta) - allowed
        if unknown:
            errors.append(f"{skill.name}: unknown frontmatter fields: {sorted(map(str, unknown))}")
        for optional in ("license", "compatibility", "allowed-tools"):
            if optional in meta and not isinstance(meta[optional], str):
                errors.append(f"{skill.name}: {optional} must be a string")
        if isinstance(meta.get("compatibility"), str) and len(meta["compatibility"]) > 500:
            errors.append(f"{skill.name}: compatibility exceeds 500 characters")
        if "metadata" in meta and (
            not isinstance(meta["metadata"], dict)
            or not all(
                isinstance(k, str) and isinstance(v, str) for k, v in meta["metadata"].items()
            )
        ):
            errors.append(f"{skill.name}: metadata must map strings to strings")
        name = meta.get("name")
        if (
            not isinstance(name, str)
            or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name)
            or len(name) > 64
        ):
            errors.append(f"{skill.name}: invalid skill name")
        elif name != skill.name:
            errors.append(f"{skill.name}: name must match directory")
        description = meta.get("description")
        if not isinstance(description, str) or not description.strip() or len(description) > 1024:
            errors.append(f"{skill.name}: invalid description")
        if not text[match.end() :].strip():
            errors.append(f"{skill.name}: empty instructions")

        interface_file = skill / "agents/openai.yaml"
        if interface_file.exists():
            try:
                config = yaml.safe_load(interface_file.read_text(encoding="utf-8"))
                interface = config.get("interface") if isinstance(config, dict) else None
                if not isinstance(interface, dict):
                    errors.append(f"{skill.name}: missing interface mapping")
                else:
                    for key in ("display_name", "short_description", "default_prompt"):
                        if not isinstance(interface.get(key), str) or not interface[key].strip():
                            errors.append(f"{skill.name}: invalid interface.{key}")
                    prompt = interface.get("default_prompt")
                    if isinstance(prompt, str) and f"${skill.name}" not in prompt:
                        errors.append(f"{skill.name}: default_prompt must reference the skill")
            except yaml.YAMLError as exc:
                errors.append(f"{skill.name}: invalid openai.yaml: {exc}")

    docs = sorted((root / "skills").rglob("*.md"))
    docs.extend(sorted((root / "docs").rglob("*.md")))
    if (root / "README.md").exists():
        docs.append(root / "README.md")
    for doc in docs:
        for target in local_targets(doc):
            resolved = (doc.parent / target).resolve()
            scope = next(
                (entry.parent for entry in skills if doc.is_relative_to(entry.parent)), root
            )
            if not resolved.is_relative_to(scope):
                errors.append(f"{doc.relative_to(root)}: reference escapes package: {target}")
            elif not resolved.is_file():
                errors.append(f"{doc.relative_to(root)}: missing file: {target}")

    for entry in skills:
        catalog = entry.parent / "references/catalog.md"
        roles = entry.parent / "references/roles"
        if roles.exists():
            if not catalog.is_file():
                errors.append(f"{entry.parent.name}: missing role catalog")
                continue
            linked = {(catalog.parent / target).resolve() for target in local_targets(catalog)}
            for role in roles.glob("*.md"):
                if role.resolve() not in linked:
                    errors.append(f"{role.relative_to(root)}: role is missing from catalog")
                if not role.read_text(encoding="utf-8").strip():
                    errors.append(f"{role.relative_to(root)}: empty role")
    return errors


if __name__ == "__main__":
    repository = Path(__file__).resolve().parents[1]
    problems = validate(repository)
    for problem in problems:
        print(problem, file=sys.stderr)
    if problems:
        sys.exit(1)
    print("Skill metadata, local file links, and role catalogs are valid.")
