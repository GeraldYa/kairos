# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2026-05-17

### Added
- `docs/case-niuxue-bots.md` — Technical implementation notes from the first real-world Kairos deployment (6-agent household at [niuxue.org](https://niuxue.org)).
- README "Real-World Adoption" section linking the user-facing case study and the implementation notes.
- `CHANGELOG.md` (this file).

### Notes
- No template or runtime change in this release — additions are documentation only.
- The 6-agent deployment validates the per-project memory isolation pattern: personalities never bleed because Claude Code already scopes auto-memory to the project directory.

## [0.1.0] - 2026-02-13

### Added
- Initial public release of Kairos.
- Core templates: `IDENTITY.md`, `SOUL.md`, `BOOT.md`, `baseline.md`, `style-profile.md`, `signals.jsonl`, `daily-reflection.md`, `soul-changelog.md`.
- Documentation: `architecture.md`, `signal-capture.md`, `persona-drift.md`, `daily-reflection.md`.
- 5-layer architecture diagram (`docs/architecture.png`).
- Demo reflection script (`scripts/reflect.py`).
- 30-day worked example with signal samples and before/after souls (`examples/`).
- MIT License.

[0.1.1]: https://github.com/GeraldYa/kairos/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/GeraldYa/kairos/releases/tag/v0.1.0
