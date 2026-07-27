# Engineering workflow

## Delivery rule

Each phase is completed and verified before work begins on the next. A phase must include its implementation, tests appropriate to its risk, documentation changes, and a short acceptance record.

## Standards

- Keep business rules in services rather than route handlers or browser code.
- Validate at trust boundaries and return stable, versioned error shapes.
- Prefer dependency injection for provider adapters and time-sensitive services.
- Keep modules cohesive; shared code must represent a genuinely shared concept.
- Add migrations for every schema change and make destructive changes explicitly staged.
- Never commit secrets, real customer data, or production payment credentials.
- Meet WCAG 2.2 AA and support keyboard and reduced-motion use from the first component.

## Branch and review checks

Before merging, run formatting, linting, unit tests, integration tests, security checks, and the production frontend build. Later phases will add exact executable commands as their toolchains are installed.

## Phase 1 acceptance

- repository boundaries and ownership are explicit
- local secrets have a documented environment contract
- frontend and backend runtime requirements are pinned
- security, performance, accessibility, and future-extension principles are documented
- no later-phase mock functionality is presented as complete

