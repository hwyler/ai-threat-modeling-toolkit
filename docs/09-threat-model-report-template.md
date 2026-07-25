# AI Threat Model Report Template

This is the document a red team actually fills out and hands to an architect, a developer, and a CISO, each of whom needs something different from it. It is built to be used alongside the rest of this toolkit: the STRIDE-AI mapping in `docs/02-stride-ai.md`, the full vulnerability catalog in `docs/07-vulnerability-guide.md`, and the full threat vector catalog in `docs/08-threat-guide.md`. Where earlier templates in this repository (`templates/asset_inventory.md`, `templates/risk_register.csv`, `templates/assessment_report.md`) cover the workflow end to end, this file is the working document a red team produces during Phase 3 and Phase 4 of an assessment (see `docs/01-methodology.md`).

Treat it as a living document. The first version gets written during the architecture design phase, before a line of production code exists, so the team can act on findings while the cost of a fix is still a design conversation rather than a re-engineering effort. It then gets revisited every time the system changes meaningfully: a new data source, a new tool integration, a new model version, a new deployment region. A threat model that was accurate at launch and has not been touched since is a historical document, not a working control.

## How to use this template

- Copy this file per system under assessment. Do not try to run one shared threat model across multiple products; a threat model is only as good as the specificity of the scenarios in it.
- Fill Section 1 and Section 2 before the threat identification session, not during it. A red team that spends its working session reconstructing the architecture instead of hunting threats has wasted its most expensive resource, the time everyone is in the room together.
- Sections 3 through 6 are the working core. Expect to revise Section 3 as Section 6 surfaces gaps that suggest a threat you had not scoped.
- Section 7 through 9 turn the threat model into something that survives past the workshop: an action plan with owners, a test plan that proves the fix worked, and a monitoring plan that catches the next one.
- Every table in this template is intentionally sparse in its header row and detailed in its guidance. Delete the guidance text once your team is fluent with the format; keep it for the first few assessments.

---

## Section 1: AI System Identification

The point of this section is to force a decision the team is often tempted to skip: what, precisely, are we threat modeling, and what would "done" look like. A vague scope produces a vague assessment. Everything downstream depends on getting this section specific.

| Field | Entry |
|---|---|
| Project name | |
| AI system description | |
| Document version | |
| Red team lead | |
| Red team members | |
| Stakeholders | |
| Assessment date | |
| Compliance requirements | |
| Environments | |
| Known limitations of this assessment | |

**Guidance for each field:**

- **AI system description** — write this as if explaining the system to a smart colleague who has never seen it: its business purpose, what it actually does at inference time, and who uses it. A description that only a person who already knows the system could understand is a sign the scope is not yet clear enough to threat model.
- **Stakeholders** — list every function that will need to act on this document, not just the people who commissioned it. A finding that affects a vendor relationship needs procurement in the loop; a finding that touches personal data needs privacy or legal.
- **Assessment date** — schedule this before development starts, during architecture design, if you want the findings to change the design rather than justify a rewrite. A threat model run for the first time after launch still has value, but it is a different exercise: you are now assessing residual risk in a system you cannot easily redesign.
- **Compliance requirements** — list the specific clauses, standards, or internal policies that apply, not a generic reference to "applicable regulations." Cite ISO/IEC 42001, the NIST AI Risk Management Framework, sector-specific rules, or contractual security clauses by name.
- **Environments** — note where each stage of the pipeline runs (cloud, on-premises, hybrid, edge) since the environment materially changes which vulnerabilities in `docs/07-vulnerability-guide.md` apply; a fully cloud-hosted system does not need the physical and hardware category, an edge deployment does.
- **Known limitations** — say plainly what this assessment did not cover: time constraints, a vendor that would not grant testing access, incomplete architecture documentation. An unstated limitation gets treated by the reader as a clean bill of health for that area; a stated one keeps everyone honest about residual risk.

**Classification for downstream use.** Complete this now; every later section filters against it.

| Field | Entry |
|---|---|
| AI system type(s) in scope | predictive / generative / agentic / mixed — list each component separately if mixed |
| Sourcing model per component | built in-house / procured / hybrid |

---

## Section 2: AI Pipeline Components

This section decomposes the system into the units a threat actually attacks. A threat model organized around business features ("the chatbot," "the recommendation engine") instead of pipeline components will systematically miss the training pipeline, the feature store, and the monitoring stack, which is exactly the failure pattern described in `docs/01-methodology.md`, Phase 2. If you cannot fill every row below with something concrete, the asset inventory is not ready and neither is the threat model.

| Pipeline stage | Component(s) | Functionality | Dependencies | Applicable vulnerability categories (see `docs/07-vulnerability-guide.md`) |
|---|---|---|---|---|
| Data collection | | | | Data Governance and Quality; Access and Exposure |
| Data cleaning and processing | | | | Data Governance and Quality |
| Model training | | | | Model Lifecycle; Change and Artifact Integrity |
| Model deployment | | | | Access and Exposure; Resilience and Infrastructure |
| Monitoring and maintenance | | | | Observability and Response |
| Retrieval / knowledge base (if generative) | | | | Data Governance and Quality; Access and Exposure |
| Tool and orchestration layer (if agentic) | | | | Access and Exposure; Multi-Agent |

**Guidance for each column:**

- **Component(s)** — name the actual systems, not a category. "PostgreSQL customer database, ingested through a nightly Airflow job" tells a red teamer something to attack; "database" does not. Note whether each component is internal or third-party, and name the vendor where it is not internal, since that determines whether Section 4's controls come from your own environment or from a vendor's attestation.
- **Functionality** — describe what the component actually does to the data or the model that passes through it: what comes in, what transformation happens, what goes out, and which libraries or frameworks are doing the work.
- **Dependencies** — list what this component cannot function without: external APIs, certificate authorities, cloud provider services, GPU allocation, a specific third-party library version. A dependency you cannot name is a dependency you cannot assess, and it will surface later as a gap in Section 4.
- **Applicable vulnerability categories** — the pre-filled suggestions are a starting point, not a ceiling. Cross-check each component against the full list in `docs/07-vulnerability-guide.md` and adjust; a training pipeline that uses a proprietary hardware accelerator should also pull in Hardware and Side Channel.

### Architecture and data flow diagrams

Attach both. A threat model without these two artifacts is describing a system nobody can independently verify.

- **System architecture diagram.** Show every major component, how it connects to the others, and how it connects to anything outside the organization's direct control. Use a notation your engineering team already reads comfortably (UML, C4, or an informal box-and-arrow diagram is fine as long as it is precise) rather than introducing a new notation just for this document.
- **Data flow diagram.** Trace every path data takes: external entities (users, sensors, other systems) that data enters from or exits to, the processes performed on it (cleaning, feature extraction, training, inference), where it is stored, and the flows between all of the above. Mark every **trust boundary** explicitly — every point where the system crosses from an environment you control into one you do not, such as the public internet, a third-party API, or a vendor's infrastructure. Trust boundaries are where Section 3's threat identification should concentrate first; nearly every threat vector in `docs/08-threat-guide.md` becomes more severe at a boundary than inside a fully trusted zone.

---

## Section 3: Threat Identification

This is where the red team does its actual work: turning a general awareness that "prompt injection is a risk" into a specific, falsifiable statement about this system. Do this systematically, component by component, rather than only brainstorming the threats that come to mind first; the threats that come to mind first are usually the ones the team is already defending against, and the ones you miss are the ones worth finding.

### Frameworks in use

Cite whichever of these your team is actually applying for this assessment, and note the version:

- **STRIDE-AI** — this toolkit's adaptation of STRIDE for AI trust boundaries; see `docs/02-stride-ai.md`. Use this as the first pass across every asset in Section 2.
- **MITRE ATLAS** — tactic and technique coverage for adversarial attacks specific to AI and machine learning systems. See `docs/06-source-alignment.md` for how this toolkit cross-references it.
- **OWASP Top 10 for LLM Applications** and **OWASP Top 10 for Agentic Applications** — prioritized risk lists for generative and agentic systems respectively; both are cited throughout `docs/08-threat-guide.md`.
- **CAPEC** (Common Attack Pattern Enumeration and Classification) — a dictionary of known attack patterns, useful when a red teamer needs to go one level more granular than a threat vector into the specific technique an attacker would use.
- **This toolkit's own catalog** — `data/threat_vectors.yaml` and `data/vulnerabilities.yaml`, already cross-referenced to the frameworks above. Use `tools/generate_checklist.py --system-type <type>` to generate a starting list scoped to your system before the brainstorming session, so the team's time goes to scenario-writing, not to remembering what to check.

### Brainstorming questionnaire

Run this as a facilitated session with the red team and, ideally, someone who owns the business process the AI system supports. Work through both angles below for each component in Section 2; a threat that only emerges from one angle is a threat you would have missed using the other alone.

**Goal-oriented prompts** (start from what an attacker wants):

- If someone wanted to make this system produce a wrong answer without anyone noticing, which component would they target first, and why?
- If someone wanted to extract the training data or the retrieval corpus this system relies on, what is the cheapest path to try first?
- If someone wanted this system to take an action it should never take on its own, what is the shortest chain of steps that gets them there?
- If someone wanted to make this system expensive to run rather than take it offline, what would they do?
- If someone wanted to plant something now that pays off later, undetected, where would they hide it?

**Actor-centric prompts** (start from who might attack, and what they already have):

- What could a disgruntled current employee with normal access do that a security control outside the access system would not catch?
- What could a competitor accomplish with nothing more than the API access any paying customer already has?
- What could a well-resourced external attacker accomplish if they compromised one upstream vendor this system depends on?
- What could happen with no malicious actor at all — through negligence, misconfiguration, or a natural failure like a hardware fault or a regional outage?
- Whose incentives are misaligned with this system's security today, and what would they do if given a strong enough reason?

### Threat register

Log every scenario the brainstorming session produces here. One row per distinct scenario; do not collapse multiple attack paths into a single row just because they target the same component.

| Threat ID | Type | Affected component(s) | Threat vector | Exploited vulnerability | STRIDE-AI category | AI system type | Scenario description |
|---|---|---|---|---|---|---|---|
| 1 | Adversarial | | (id from `data/threat_vectors.yaml`, e.g. T003 Data Poisoning) | (id from `data/vulnerabilities.yaml`, e.g. V014 Data Poisoning Susceptibility) | | | |
| 2 | Negligence | | | | | | |
| 3 | Natural forces | | | | | | |

**Guidance on threat type:**

- **Adversarial** — a deliberate attacker with intent, whether external or an insider. Write the scenario as a full attack path: what the attacker does, what they exploit, and what the consequence is, at the level of specificity in the worked example in `docs/05-threat-modeling-guide.md`. "Adversary poisons training data to bias model outputs" is a category, not a scenario; "an external contributor submits crafted support tickets that get copied into the RAG knowledge base, embedding an instruction that reframes the refund policy" is a scenario.
- **Negligence** — no attacker required, just a control that was never built or was built wrong: a misconfigured access boundary, inadequate de-identification, a missing approval gate. These threats are often higher likelihood than adversarial ones and deserve equal attention, not a lower priority by default.
- **Natural forces** — environmental disruption, hardware failure, a regional outage, a natural disaster affecting a data center. Lower frequency in most environments, but often higher blast radius, and frequently the scenario that exposes a single point of failure (V049) the team did not know it had.

---

## Section 4: Risk Scoring

Score each threat in your register using the rubric below, adapted from the DREAD approach for AI-specific impact. The scoring is deliberately subjective — no formula here removes the need for judgment — but a shared 1-to-5 scale keeps that judgment comparable across threats and across the people applying it, which is the entire point of scoring in the first place.

### Scoring rubric

Score each of the five dimensions from 1 (lowest) to 5 (highest), then sum for a total out of 25.

| Score | Damage | Reproducibility | Exploitability | Affected scope | Discoverability |
|---|---|---|---|---|---|
| 1 | Under $10,000 in loss or harm; minor operational disruption | Requires a highly specialized skillset, rare access, or an undisclosed flaw to reproduce at all | Requires advanced technical skill, custom tooling, and privileged access | A single individual account or record is affected | Requires deep, specialized analysis to find; effectively hidden |
| 2 | $10,000 to $50,000; moderate impact, small-scale data exposure | Reproducible only under specific, uncommon circumstances | Requires available tooling and real technical knowledge, plus network or system access | A small handful of users or records are affected | Findable with specific tools or techniques, not casual inspection |
| 3 | $50,000 to $250,000; significant financial or reputational impact | Reproducible with moderate skill and moderate effort | Exploitable with readily available tools or scripts and moderate technical knowledge | A department, team, or defined user segment is affected | Findable through standard security testing or a routine review |
| 4 | $250,000 to $1,000,000; major financial loss, regulatory exposure, or significant disruption | Easily reproducible by any authenticated user or with commonly available tools | Exploitable with basic technical skill after a focused, short effort | Privileged or administrative accounts and records are affected | Publicly known or easily found through common knowledge |
| 5 | Over $1,000,000, or harm that cannot be reduced to a dollar figure: safety impact, irreversible privacy harm, or catastrophic reputational damage | Reproducible by anyone, with no authentication and no special access, on the first attempt | Exploitable with minimal effort, no special skill, and no custom tooling | Every user, every record, or the entire system is affected | Trivially discoverable through normal, unprivileged use of the system |

**A note on using this rubric for AI-specific harm.** Traditional DREAD scoring was built around financial and operational damage. For AI systems, extend the Damage column explicitly to cover harm that a dollar figure understates: a biased hiring decision, a fabricated medical recommendation acted on by a clinician, a privacy violation that discloses someone's health status. Score these at whatever level of the 1-to-5 scale the harm actually warrants, and note in the scenario description why a dollar-only reading would understate it. This is also where the vulnerability guide's Governance and Accountability category, particularly the human rights assessment weakness (V044), earns its place in a scoring conversation that would otherwise stay purely financial.

### Scored threat register

| Threat ID | Damage | Reproducibility | Exploitability | Affected scope | Discoverability | Total score | Priority |
|---|---|---|---|---|---|---|---|
| 1 | | | | | | | |
| 2 | | | | | | | |
| 3 | | | | | | | |

Set priority thresholds explicitly for your organization rather than assuming a universal cutoff; a reasonable starting point is Critical at 20 to 25, High at 15 to 19, Medium at 10 to 14, and Low at 5 to 9, adjusted for your own risk appetite as documented in Section 1.

---

## Section 5: Existing Control Mapping

For every threat scored above, document what is actually in place today, not what the team intends to build. A control that exists on a roadmap is not a control; it belongs in Section 6 and Section 7, not here.

| Threat ID | Control ID | Control description | Type | Effectiveness | Last tested or attested |
|---|---|---|---|---|---|
| 1 | (cross-reference to NIST AI RMF, ISO/IEC 42001, ISO/IEC 27001, or an internal control ID) | | preventative / detective / corrective / contingency | | |

**Guidance:**

- **Control ID** — cross-reference an external standard where one applies, so the mapping is auditable by someone outside the red team. Internal-only controls are fine; give them a stable internal ID so they can be tracked across assessment cycles.
- **Type** — a preventative control stops the threat from occurring; a detective control notices it happened; a corrective control limits the damage after detection; a contingency control keeps the business running if the threat succeeds despite everything else. A threat with only detective controls and no preventative ones is a materially different risk conversation than one with strong prevention, even at the same likelihood score.
- **Effectiveness** — state this from evidence: the result of the last test, audit, or self-attestation, not from confidence in the control's design. "Believed effective, not independently tested since design" is an honest and useful answer; do not round it up to "effective."

---

## Section 6: AI Control Gaps

This is the section each audience actually reads first. Write it so an architect, a developer, and a security tester can each find what they need without reading the whole document.

| Gap ID | Affected component | Related threat ID(s) | Gap description | Criticality | Recommended remediation | Primary audience |
|---|---|---|---|---|---|---|
| 1 | | | | | | AI Architect / AI Developer / Security Testing Team |

**Guidance:**

- **Gap description** — explain specifically why the existing control (or its absence) fails to address the threat: wrong layer, wrong trigger condition, wrong scope, or simply never built. "Insufficient" without a reason is not actionable; "the refund tool's authorization check validates the requester's identity but not the requested amount against the agent's configured ceiling" is.
- **Criticality** — base this on the threat's score from Section 4, adjusted for how directly this specific gap contributes to that score; a gap that closes most of a Critical threat's exposure outranks one that only marginally reduces a Medium threat.
- **Recommended remediation** — write this at the level of specificity the primary audience needs. For an AI Architect, that is a design change and its rationale. For an AI Developer, that is an implementable specification: what to build, where, and against what acceptance criteria. For the Security Testing Team, that is a description of the test that would prove the gap is closed, feeding directly into Section 8.
- **Primary audience** — pick the one function that owns closing this gap, even if others will be consulted. A gap with three co-owners is a gap that tends not to get closed.

---

## Section 7: Action Plan

Turn Section 6 into commitments with dates.

| Recommendation ID | Description | Responsible party | Timeline | Status |
|---|---|---|---|---|
| 1 | | | | Not Started / In Progress / Completed / Deferred |

If a recommendation is marked Deferred, record why and who accepted the residual risk; an undocumented deferral is functionally identical to a forgotten finding.

---

## Section 8: Validation and Testing

Prove the remediation actually closed the gap. Design each test directly against the threat vector it is meant to defeat, using the "what to test" guidance already written out per threat vector in `docs/08-threat-guide.md`, rather than inventing test criteria from scratch.

| Test ID | Related threat ID | Test scenario | Testing method | Result | Remediation status |
|---|---|---|---|---|---|
| 1 | | | Adversarial testing / Prompt injection testing / Data integrity testing / Privacy leakage testing / Agent behavior testing / Abuse resistance testing | Pass / Fail | Remediated / In Progress / Not Remediated |

**Guidance:** a test that passes once is evidence, not proof of a durable fix. For any Critical or High priority threat, plan to re-run the corresponding test after the next material change to the affected component, not only once at remediation time. This is the practical link between Section 8 and Section 9: a test plan with no repeat cadence quietly becomes a one-time exercise.

---

## Section 9: Continuous Monitoring and Improvement

A threat model that is not revisited decays the moment the system it describes changes. Define how this one stays current.

| Monitoring activity | Frequency | Responsible party | Output |
|---|---|---|---|
| Review threat intelligence relevant to this system's stack and dependencies | | | Updated entries in the threat register |
| Re-run Section 8 tests for Critical and High threats | | | Updated remediation status |
| Re-score threats against Section 4 rubric after a material change | | | Updated priority ranking |
| Full threat model refresh | | | New document version |

**Guidance on triggering an out-of-cycle update**, beyond the scheduled cadence above: a new data source enters the pipeline, a new tool or plugin is granted to an agent, the system is deployed to a new region with different jurisdictional requirements, a foundation model dependency ships a material update, or an incident anywhere in the organization reveals a threat vector this document did not previously consider. Any one of these is a reason to open this document again before the next scheduled review, not wait for it.

---

## Appendix: Quick reference to this toolkit

| If you need... | Go to |
|---|---|
| The six-phase assessment process this template fits into | `docs/01-methodology.md` |
| The STRIDE-AI category definitions used in Section 3 | `docs/02-stride-ai.md` |
| A worked, narrative example of building a threat model | `docs/05-threat-modeling-guide.md` |
| Full detail on any vulnerability referenced in Section 3 or 6 | `docs/07-vulnerability-guide.md` |
| Full detail on any threat vector referenced in Section 3 or 8 | `docs/08-threat-guide.md` |
| A scoped starting checklist before your brainstorming session | `tools/generate_checklist.py` |
| The asset inventory to complete before Section 2 | `templates/asset_inventory.md` |
| Where scored findings ultimately get tracked long-term | `templates/risk_register.csv` |
