from pathlib import Path
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from check_install import check_copy
from validate_skills import validate


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.workspace = tempfile.TemporaryDirectory()
        self.addCleanup(self.workspace.cleanup)
        self.root = Path(self.workspace.name)
        source = Path(__file__).resolve().parents[1]
        shutil.copytree(source / "skills", self.root / "skills")
        self.skill = self.root / "skills/product-team"

    def test_valid_package(self):
        self.assertEqual(validate(self.root), [])

    def test_rejects_invalid_frontmatter(self):
        entry = self.skill / "SKILL.md"
        entry.write_text("---\nname: [\n---\nInstructions\n")
        self.assertTrue(any("invalid YAML" in error for error in validate(self.root)))

    def test_rejects_missing_role(self):
        (self.skill / "references/roles/technical-writer.md").unlink()
        self.assertTrue(any("missing file" in error for error in validate(self.root)))

    def test_rejects_undiscoverable_role(self):
        (self.skill / "references/roles/new-role.md").write_text("# New role\n")
        self.assertTrue(any("missing from catalog" in error for error in validate(self.root)))

    def test_rejects_reference_outside_installable_package(self):
        (self.root / "private.md").write_text("Not installed\n")
        with (self.skill / "SKILL.md").open("a") as handle:
            handle.write("\n[external dependency](../../private.md)\n")
        self.assertTrue(any("escapes package" in error for error in validate(self.root)))

    def test_detects_incomplete_or_modified_installation(self):
        destination = self.root / "installed"
        shutil.copytree(self.skill, destination)
        self.assertGreater(check_copy(self.skill, destination), 0)
        (destination / "references/roles/manager.md").unlink()
        with self.assertRaises(AssertionError):
            check_copy(self.skill, destination)
        shutil.copyfile(self.skill / "references/roles/manager.md", destination / "references/roles/manager.md")
        (destination / "SKILL.md").write_text("changed\n")
        with self.assertRaises(AssertionError):
            check_copy(self.skill, destination)


if __name__ == "__main__":
    unittest.main()
