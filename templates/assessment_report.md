# AI Security Assessment Report: [System Name]

**Assessment date**:
**Assessors**:
**System classification**: predictive / generative / agentic / mixed
**Sourcing model**: built in-house / procured / hybrid

## 1. Scope and objectives

State what was in scope, what was explicitly out of scope, and the measurable success criteria agreed in Phase 1.

## 2. Asset inventory summary

Reference the completed `asset_inventory.md` for this system. Summarize the components in scope and flag any component the team could not fully inventory.

## 3. Threat model summary

Summarize the STRIDE-AI walk and the matched threat vectors from `data/threat_vectors.yaml`. List the highest-impact scenarios in full; reference the risk register for the complete list.

## 4. Testing performed

List the specific tests run against each high-impact scenario: adversarial testing, prompt injection testing, data integrity checks, privacy leakage testing, agent behavior testing, abuse resistance testing. Note tooling used and whether testing was automated, manual, or both.

## 5. Findings

| Finding | Threat vector | Vulnerability | Likelihood | Impact | Risk score | Status |
|---|---|---|---|---|---|---|
| | | | | | | |

See `risk_register.csv` for the full, working register.

## 6. Recommended mitigations

List mitigations by finding, referencing the control suggestions in `docs/02-stride-ai.md` and `docs/03-vulnerability-catalog.md` where relevant. Distinguish mitigations that are immediately actionable from those that require a longer-term architectural change.

## 7. Residual risk and sign-off

State the residual risk after recommended mitigations and who is accepting it. This should tie back to the risk tolerance defined in Phase 1.

## 8. Next review

State the date or trigger condition (a material architecture change, a new model version, a vendor update) for the next assessment cycle.
