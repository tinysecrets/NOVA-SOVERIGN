# Release Checklist

## Required local checks

Run the local policy test before a release:

```bash
cd backend
python -m pytest tests/test_local_policy.py
```

For backend integration tests, install `requirements-dev.txt` and run only against a disposable local deployment. The documented HTTP suite requires `NOVA_TEST_API_URL`, `NOVA_TEST_ALLOW_MUTATIONS=1`, and synthetic `NOVA_TEST_EMAIL` / `NOVA_TEST_PASSWORD`; do not configure it to use a production API. If a non-default model is under test, set the documented expected-model environment variables.

## Deployment and privacy

1. Confirm service binds remain loopback/private Tailscale and reject wildcard/LAN binds.
2. Verify no `.env`, credentials, sessions, Mongo data, prompts, or uploaded documents enter Git/build artifacts.
3. Test authentication and policy enforcement before any API route changes; keep cloud inference opt-in.
4. Run `git diff --check`, review the staged diff and exact commit, then verify health from an approved local/private device.
5. Preserve a known-good revision and document how to stop every process if startup or model routing fails.
