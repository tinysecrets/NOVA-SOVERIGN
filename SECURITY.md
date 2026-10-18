# Security Policy

NOVA is a private, single-user assistant. The backend uses MongoDB and JWT/session secrets, and cloud LLM use is an explicit opt-in. Protect `ADMIN_EMAIL`, `ADMIN_PASSWORD`, `JWT_SECRET`, MongoDB URLs, provider keys, conversations, notes, and uploaded documents. Keep `.env` files, local database volumes, exported user data, and logs out of Git.

Default to loopback binding. Do not expose the API or frontend to a LAN or public network; use a narrow, approved Tailscale address and tailnet ACLs when remote device access is needed. The single-owner design is not a substitute for general multi-user authorization. Keep cloud inference opt-in and do not send sensitive content to a provider without operator consent.

Tests that mutate sessions or call inference must use a disposable local deployment, synthetic account, and explicit opt-in environment variables. Report vulnerabilities privately and remove credentials or user content from evidence before sharing.
