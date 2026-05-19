# VCDDD

[中文说明](./README.zh-CN.md)

VCDDD (Vibe Coding Domain-Driven Design) is a skill and methodology for AI-assisted software design. It carries two layers of meaning that are complementary, not alternative.

> **New here?** → [Quick Start Guide](./QUICKSTART.md) — no DDD knowledge needed, just follow the steps.

This repository is published as a single-skill repository. The repository root is the skill root.

## What Is Included

- `SKILL.md`: main entry — theory foundation + controller agent + step navigation
- `steps/{STEP}/SKILL.md`: modular step skills, each self-contained for sub-agent dispatch
- `reference/theory/`: whitepaper, methodology guides, and implementation mapping
- `reference/guides/`: requirement clarification and domain design workflow
- `reference/engine/`: implementation engine reference (orchestration, review, TDD bridge, etc.)
- `reference/templates/`: document templates for input, facts, boundary, business, etc.

## Repository Structure

```text
vcddd/                     ← repository / skill root
├── SKILL.md               ← Main entry (theory + controller + navigation)
├── steps/
│   ├── BROWNFIELD/        ← Analyze existing code into LLM-readable docs
│   ├── VISION/            ← Capture user intent
│   ├── CONTEXT/           ← Clarify into business facts
│   ├── DOMAIN-DESIGN/     ← Derive boundaries and invariants
│   ├── DEVSETUP/          ← Determine tech stack
│   ├── FRONTEND-DESIGN/   ← Complete frontend design standards with google-design-md
│   ├── TDD-BRIDGE/        ← Derive black-box test specs (+ prompt files)
│   ├── IMPLEMENT-DOMAIN/  ← Code + white-box + black-box tests (+ prompt files)
│   ├── REVIEW-DOMAIN/     ← Three-layer adversarial review (+ prompt files)
│   ├── INTEGRATE/         ← Cross-domain integration verification
│   ├── REPORT/            ← Final completion report
│   └── EVENT-LOG/         ← Domain-level progress log specification
└── reference/
    ├── theory/            ← vcddd-methodology, whitepaper, design-guide, implementation
    ├── guides/            ← requirements.md, design.md
    ├── engine/            ← automated-execution, fallback-execution, tdd-bridge,
    │   │                     review-loop, subagent-orchestration, integration-verification,
    │   │                     tech-setup, implementation, brownfield-init
    │   └── examples/      ← Full code examples (TS, Python, Java, Serverless)
    └── templates/         ← Document templates for all VCDDD outputs
```

## Two Layers of VCDDD

```
┌─────────────────────────────────────────────────────┐
│         Layer 2: Five-Step Working Methodology       │
│   V → C → D¹ → D² → D³                             │
│   Vision · Context · Domain · Dev Setup · Develop   │
│                                                      │
│   ┌─ Automated Execution Layer (D²→D³) ─────────┐   │
│   │  SuperPower engine (preferred)               │   │
│   │  └─ TDD bridge → writing plans → subagent    │   │
│   │     dispatch → two-stage review → verify     │   │
│   │                                               │   │
│   │  Builtin engine (fallback)                    │   │
│   │  └─ Manual subagent orchestration + review   │   │
│   └───────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────┤
│         Layer 1: Theoretical Foundation              │
│   Vibe Coding × Domain-Driven Design                │
│   A redefinition of DDD for the AI era              │
└─────────────────────────────────────────────────────┘
```

### Layer 1 — Theoretical Foundation

VCDDD is not a lighter DDD or an AI-wrapped DDD. It is a redefinition of what DDD is fundamentally about.

In the AI era, code is no longer the scarcest asset — it can be regenerated frequently. What must be protected instead is:

- **Business truth** — the facts the system commits to
- **Semantic boundaries** — where concepts hold and where they stop
- **Decision ownership** — who has the final say on what judgment
- **Process state** — where a long-running flow is at any moment
- **Collaboration contracts** — stable agreements across boundaries
- **Validation barriers** — mechanisms that prevent implementation from drifting away from the above

> Code can change frequently. The system's expression of the business world must not drift.

"Vibe Coding" acknowledges the high changeability of AI-generated code while insisting that the business model remains the stable anchor. The two are not in conflict: precisely because code can always be rewritten, business truth must be established first, independently, and protected throughout.

### Layer 2 — Five-Step Working Methodology

| Step | Full Name | Core Task | Key Output |
|---|---|---|---|
| **V** | Vision | Capture and structure user intent — no analysis yet | `input.md` |
| **C** | Context | Clarify intent into user-confirmed business facts | `facts.md` + ubiquitous language |
| **D¹** | Domain Design | Derive boundaries, decision ownership, invariants, events, and contracts from facts alone | `boundary.md` + `business.md` per domain |
| **D²** | Dev Setup | Formalize tech choices as written architectural conventions | `tech-stack.md` |
| **D²·⁶** | Frontend Design | For user-interface projects, use `google-design-md` to complete unified frontend design standards | `docs/vcddd/frontend/*` |
| **D³** | Develop | Generate code governed by D¹ design and D² conventions | Working codebase + `implementation.md` |

Each step has a hard prerequisite gate. No step may begin until its predecessor output has been confirmed. This sequencing is not ceremony — it prevents building correct-looking code on top of unconfirmed business assumptions.

## Recommended Reading Order

### Foundation

1. `SKILL.md` — operating rules, theory base, and automation layer
2. `reference/methodology/vcddd-methodology.md` — the five-step method in full
3. `reference/thinking/requirements.md` — how to run V and C
4. `reference/thinking/design.md` — how to run D¹

### Brownfield (for existing projects without VCDDD docs)

5. `reference/coding/brownfield-init.md` — analyze existing code into an LLM-readable architecture knowledge base (entry points, business logic, data flows)

### Execution (choose a path after D¹)

**Automated path (recommended):**
5. `reference/coding/automated-execution.md` — master orchestration (auto-detects SuperPower, delegates or falls back)
6. `reference/coding/tdd-bridge.md` — mechanical test derivation from business.md
7. `reference/coding/subagent-orchestration.md` — domain→task decomposition
8. `reference/coding/review-loop.md` — spec compliance + code quality checklists
9. `reference/coding/integration-verification.md` — cross-domain contract testing

**Manual path:**
5. `reference/coding/tech-setup.md` — how to run D²
6. `reference/coding/implementation.md` — how to run D³

### Theory (deeper dives)

- `reference/methodology/vcddd-whitepaper.md`
- `reference/methodology/vcddd-design-guide.md`
- `reference/methodology/vcddd-implementation.md`

## How To Use

This repository follows the shared `SKILL.md` convention used by multiple coding-agent ecosystems.

For Codex-style local skills, place this repository directory under your local skills path so that the root `SKILL.md` remains intact, for example:

```text
~/.claude/skills/vcddd/
```

Then use the skill when the task is about:

- clarifying business requirements into confirmed facts
- deriving domain boundaries from business truth
- designing invariants, states, events, and contracts
- keeping implementation aligned to a documented business model

### Optional: SuperPower Engine

VCDDD can delegate D²→D³ execution to SuperPower for automated subagent dispatch, TDD cycle, and code review. Install SuperPower separately:

```bash
npm install -g @superpowers/skills
```

When SuperPower is detected, VCDDD automatically uses it as the execution engine. When not available, VCDDD falls back to its built-in engine.

## Workflow Summary

### Phase 1: Human-Confirmed Business Truth (V → C → D¹)

These three steps always require user confirmation at each gate. They establish the business truth that all later work depends on.

1. **V — Vision**: Capture the user's intent faithfully, without analysis or architecture.
2. **C — Context**: Clarify intent into user-confirmed business facts, state machines, and a shared ubiquitous language.
3. **D¹ — Domain Design**: From confirmed facts only, derive bounded contexts, decision boundaries, invariants, events, and collaboration contracts.

### Phase 2: Automated Execution (D² → D³)

After D¹ is confirmed, the system can execute the remaining steps automatically:

4. **D²-auto**: Scan project config files to detect tech stack (or research options for new projects). Only ask the user about items that can't be inferred from code.
5. **Frontend Design (if applicable)**: For user-interface projects, use the local `google-design-md` skill to complete unified design standards and write them into `docs/vcddd/frontend/`.
6. **TDD Bridge**: Mechanically derive test specifications from the domain's `business.md` — each invariant, state transition, command path, and failure branch maps to specific test cases.
7. **Task Decomposition**: Split each domain into independent 2-5 minute subagent tasks with exact file paths and test IDs.
8. **Subagent Execution**: Dispatch each task to a fresh subagent following TDD (RED-GREEN-REFACTOR). Two-stage review (spec compliance vs business.md, code quality vs tech-stack.md) gates each task.
9. **Integration Verification**: After all domains complete, verify cross-domain contracts, E2E workflows, idempotency, and event ordering.
10. **Final Report**: Present a summary of domain status, test counts, and verification results.

### What the User Sees

During automated execution, the user sees only progress updates and is interrupted only when:

- Tech stack has unresolvable ambiguous items
- A `business.md` rule is internally contradictory
- A subagent reports BLOCKED requiring a business-level decision

## License

This repository is released under the Creative Commons Attribution 4.0
International license (`CC BY 4.0`).
