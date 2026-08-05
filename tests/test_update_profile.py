import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "update_profile.py"
SPEC = importlib.util.spec_from_file_location("update_profile", SCRIPT)
assert SPEC and SPEC.loader
update_profile = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(update_profile)


class UpdateProfileTests(unittest.TestCase):
    def test_selection_filters_and_orders_projects(self):
        repositories = [
            {"name": "HarshSaand", "description": "Profile", "pushed_at": "2026-08-05T00:00:00Z"},
            {"name": "blank", "description": None, "pushed_at": "2026-08-04T00:00:00Z"},
            {"name": "forked", "description": "Fork", "fork": True, "pushed_at": "2026-08-03T00:00:00Z"},
            {"name": "new-system", "description": "Newest work", "pushed_at": "2026-08-02T00:00:00Z"},
            {"name": "older-system", "description": "Older work", "pushed_at": "2026-07-02T00:00:00Z"},
        ]
        selected = update_profile.select_repositories(repositories)
        self.assertEqual([repo["name"] for repo in selected], ["new-system", "older-system"])

    def test_rendered_feed_contains_evidence_not_badges(self):
        repositories = [{
            "name": "signal-lab",
            "html_url": "https://github.com/HarshSaand/signal-lab",
            "description": "An inspectable signal pipeline.",
            "language": "Python",
            "topics": ["machine-learning", "evaluation"],
            "pushed_at": "2026-08-02T00:00:00Z",
        }]
        feed = update_profile.render_feed(repositories)
        self.assertIn("Signal Lab", feed)
        self.assertIn("<br>", feed)
        self.assertIn("Python / machine learning / evaluation / Aug 2026", feed)

    def test_marker_replacement_preserves_surrounding_copy(self):
        readme = "Before\n<!-- RECENT_WORK:START -->\nOld\n<!-- RECENT_WORK:END -->\nAfter\n"
        updated = update_profile.replace_feed(readme, "New")
        self.assertEqual(
            updated,
            "Before\n<!-- RECENT_WORK:START -->\nNew\n<!-- RECENT_WORK:END -->\nAfter\n",
        )


if __name__ == "__main__":
    unittest.main()
