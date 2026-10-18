"""Offline checks for safe defaults; no MongoDB or model provider is contacted."""
from __future__ import annotations

import ast
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BACKEND = ROOT / "backend"


class LocalPolicyTests(unittest.TestCase):
    def test_backend_defaults_to_local_ollama(self):
        source = (BACKEND / "server.py").read_text(encoding="utf-8")
        tree = ast.parse(source, filename="backend/server.py")
        assignments = []
        for node in tree.body:
            if isinstance(node, ast.Assign) and any(
                isinstance(target, ast.Name) and target.id == "LLM_BACKEND"
                for target in node.targets
            ):
                assignments.append(ast.unparse(node.value))
        self.assertTrue(assignments)
        self.assertIn("LLM_BACKEND", assignments[0])
        self.assertIn("'ollama'", assignments[0])
        self.assertIn("LLM_BACKEND not in", source)

    def test_cors_has_explicit_local_origins_and_rejects_wildcard(self):
        source = (BACKEND / "server.py").read_text(encoding="utf-8")
        compose = (ROOT / "docker-compose.yml").read_text(encoding="utf-8")
        self.assertIn("_DEFAULT_CORS_ORIGINS", source)
        self.assertIn('if "*" in CORS_ORIGINS:', source)
        self.assertNotIn('allow_origins=CORS_ORIGINS or ["*"]', source)
        self.assertIn("${CORS_ORIGINS:-http://127.0.0.1:3000,http://localhost:3000}", compose)
        self.assertNotIn('CORS_ORIGINS: "*"', compose)

    def test_authentication_secrets_fail_closed(self):
        source = (BACKEND / "server.py").read_text(encoding="utf-8")
        self.assertIn("len(JWT_SECRET) < 32", source)
        self.assertIn("Set a real ADMIN_EMAIL and ADMIN_PASSWORD", source)

    def test_http_integration_suite_cannot_target_live_api_by_default(self):
        source = (BACKEND / "tests" / "backend_test.py").read_text(encoding="utf-8")
        for required in (
            "NOVA_TEST_API_URL",
            "NOVA_TEST_ALLOW_MUTATIONS",
            "NOVA_TEST_EMAIL",
            "NOVA_TEST_PASSWORD",
            "pytest.mark.skipif",
        ):
            self.assertIn(required, source)
        self.assertNotRegex(source, r"(?m)^\s*PASSWORD\s*=\s*['\"]")
        self.assertNotIn("REACT_APP_BACKEND_URL", source)
        self.assertNotIn("/app/frontend/.env", source)

    def test_checked_in_env_templates_are_local_first_and_placeholder_only(self):
        root_env = (ROOT / ".env.example").read_text(encoding="utf-8")
        backend_env = (BACKEND / ".env.example").read_text(encoding="utf-8")
        for template in (root_env, backend_env):
            self.assertIn("LLM_BACKEND=ollama", template)
            self.assertIn("EMERGENT_LLM_KEY=", template)
            self.assertIn("JWT_SECRET=replace-", template)
            self.assertNotIn("CORS_ORIGINS=*", template)


if __name__ == "__main__":
    unittest.main()
