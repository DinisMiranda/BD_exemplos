# Security

## Reporting a vulnerability

If you believe you have found a security vulnerability in this project, please report it responsibly:

1. **Do not** open a public issue.
2. Email the maintainers (see [CODEOWNERS](.github/CODEOWNERS) or repository contacts) with:
   - A description of the vulnerability
   - Steps to reproduce
   - Possible impact
   - Suggested fix (if any)

We will acknowledge your report and work on a fix. We ask that you give us reasonable time to address the issue before any public disclosure.

## Configuration and secrets

- **Never** commit `config.toml` or any file containing MySQL credentials. Use `config.toml.example` as a template and keep your real config local (it is in `.gitignore`).
- Do not log or print passwords or connection strings.
