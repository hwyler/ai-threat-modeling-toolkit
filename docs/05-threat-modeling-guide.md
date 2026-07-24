# Building a Threat Model From This Catalog

This guide walks through turning the vulnerability and threat vector catalogs into an actual threat model for a specific system. It assumes you have completed Phase 1 (classification) and Phase 2 (asset inventory) from `docs/01-methodology.md`.

## Step 1: Confirm the system type per component, not per product

A single product often mixes types. A customer support platform might use a predictive model to route tickets, a generative model to draft replies, and an agentic layer to actually update the customer's account. Classify each component separately and run the matching priority list against each one; do not run the agentic checklist against the routing model just because it lives in the same product.

## Step 2: Walk the asset inventory against the STRIDE-AI categories

For each asset in your Phase 2 inventory, ask the six STRIDE-AI questions from `docs/02-stride-ai.md`: can this asset be spoofed, tampered with, repudiated, made to disclose information, denied service, or used to escalate privilege. Record which STRIDE categories apply to which assets before moving to specific threat vectors; this catches architectural gaps that a threat-vector checklist alone can miss, because it forces you to look at every asset rather than only the ones a known vector happens to name.

## Step 3: Pull the scoped threat vector list

Use `tools/generate_checklist.py` or filter `data/threat_vectors.yaml` directly by the `applies_to` field and the relevant priority list. For each vector, note which asset from your inventory it targets and which vulnerability from `data/vulnerabilities.yaml` would need to be present for the attack to succeed. A threat vector without a corresponding vulnerability in your environment is a lower priority; a threat vector matched to a confirmed vulnerability is a finding.

## Step 4: Write scenario-based descriptions for the highest-impact matches

Do not attempt equal-depth narrative for all 49 threat vectors against every asset; that produces a long document nobody reads. Instead, write a two-to-three sentence scenario for the combinations with the highest plausible business impact: what the attacker does, what vulnerability they exploit, and what the consequence is. This is the input to Phase 4 testing.

## Step 5: Score and log

Move each scenario into `templates/risk_register.csv` with a likelihood and impact score. Log the mapped vulnerability id and threat vector id so the register stays traceable back to the catalog.

## Worked example: a retrieval-augmented customer support agent

**System**: A generative model with a retrieval-augmented knowledge base, wrapped in an agent that can look up order status and issue refunds under a defined dollar threshold. Built in-house on a licensed foundation model, fine-tuned on internal support tickets.

**Classification**: Generative (drafting) and agentic (refund action) components, sourced as a hybrid: foundation model procured, fine-tuning and orchestration built in-house.

**Asset inventory highlights**: the fine-tuning dataset (internal tickets), the vector database (product and policy documents), the prompt template, the refund tool integration, and the orchestration layer that decides when to call the refund tool.

**STRIDE-AI walk**: Tampering and Spoofing are both live against the vector database, since anyone who can add or edit a policy document can influence what the model treats as authoritative. Elevation of Privilege is live against the refund tool integration, since a successful manipulation converts a chat message into a financial transaction.

**Matched threat vectors**: RAG corpus poisoning against the vector database, matched to weak data governance and uncontrolled data ingestion if the document repository accepts updates without review. Indirect prompt injection against the same asset, since a manipulated policy document is a delivery mechanism for hidden instructions. Excessive agency abuse and unauthorized tool use against the refund integration, matched to excessive tool permissions if the agent's refund authority is not capped or independently authorized.

**Scenario**: An attacker who can influence one product FAQ document (through a support ticket that gets copied into the knowledge base, for example) embeds an instruction that reframes the agent's refund policy. On a subsequent customer session, the agent retrieves that document, treats the embedded instruction as legitimate policy, and issues a refund outside its intended threshold. This scenario depends on two conditions holding at once: weak data governance over what enters the vector database, and a refund tool with no independent authorization check beyond the model's own decision. Testing and mitigation should target both, not just one.

This is the level of specificity to aim for in Phase 3 and Phase 4: named assets, named vulnerabilities, a plausible attacker action, and a concrete consequence, rather than a restated definition from the catalog.
