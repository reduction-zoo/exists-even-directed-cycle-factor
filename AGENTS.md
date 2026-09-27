# Research instructions

Read the [fixed question](campaigns/exists-even-directed-cycle-factor/question.md), [prior state](campaigns/exists-even-directed-cycle-factor/state.md) and [preparation notes](campaigns/exists-even-directed-cycle-factor/work/preparation.md). The fixed [test corpus](campaigns/exists-even-directed-cycle-factor/work/cases.json) and [verifier](campaigns/exists-even-directed-cycle-factor/work/check.py) are the starting evidence; the preparation notes state their coverage and any pending checks.

Run `uv sync --locked`, then `uv run --locked python campaigns/exists-even-directed-cycle-factor/work/check.py --self-test` before relying on that evidence. Follow the current user's AutoResearch pipeline. Scope and budgets in the state describe earlier work and do not limit a new campaign. Preserve prior evidence, commit new work incrementally and make only evidence-backed claims.
