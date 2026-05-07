from pathlib import Path
import tempfile
import unittest

from landfall_forge.cli import choose_landfall, landfall_files, repo_root, scalar_values_for_key


class LandfallCliTests(unittest.TestCase):
    def test_repo_root_finds_git_parent(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".git").mkdir()
            child = root / "a" / "b"
            child.mkdir(parents=True)
            self.assertEqual(repo_root(child), root.resolve())

    def test_landfall_files_are_repo_local_yaml(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            directory = root / "landfalls"
            directory.mkdir()
            (directory / "one.yaml").write_text("name: one\n", encoding="utf-8")
            (directory / "README.md").write_text("# docs\n", encoding="utf-8")
            self.assertEqual([p.name for p in landfall_files(root)], ["one.yaml"])

    def test_choose_landfall_weights_identity_over_incidental_mentions(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            directory = root / "landfalls"
            directory.mkdir()
            closing = directory / "closing-landfall.yaml"
            heather = directory / "heather-landfall.yaml"
            closing.write_text(
                "name: closing-landfall\nsize: broad\npurpose: >\n  Mentions Heather readiness.\n",
                encoding="utf-8",
            )
            heather.write_text(
                "name: heather-landfall\nsize: focused\npurpose: >\n  Refresh Heather messages.\n",
                encoding="utf-8",
            )
            self.assertEqual(choose_landfall([closing, heather], "get Heather ready"), heather)

    def test_scalar_values_for_key_unescapes_quoted_values(self):
        text = 'commands:\n  - "reeves-messages ask \\"What is due?\\""\n'
        self.assertEqual(scalar_values_for_key('prompt: "What next?"', "prompt"), ["What next?"])
        from landfall_forge.cli import list_values_for_key

        self.assertEqual(list_values_for_key(text, "commands"), ['reeves-messages ask "What is due?"'])


if __name__ == "__main__":
    unittest.main()
