# STRIDE Adapted for AI Systems

Classic STRIDE was built for deterministic software with fixed logic and fully inspectable source code. AI systems break several of the assumptions STRIDE relies on: behavior is learned from data rather than coded, outputs are probabilistic, decision boundaries are often opaque even to the system's own developers, and the supply chain includes datasets, pre-trained models, fine-tuning data, and retrieval corpora, each with its own vulnerability class. Applying STRIDE without adapting it produces an assessment that looks complete but misses the attack surface that actually matters in an AI system.

Below, each STRIDE category is restated for AI assets, with the controls that hold up in practice and the primary threat vectors it maps to in `data/threat_vectors.yaml`.

## Spoofing: faking anything the model trusts

In an AI system, spoofing is not limited to impersonating a user. It extends to faking training data sources, distributing trojanized models through public model hubs, spoofing service identities that call model APIs, and spoofing tools or plugins in agent-based systems. A distinct and frequently missed variant is prompt identity manipulation, where an attacker reframes the model's role through crafted input and changes its behavior without touching any system component.

**Controls**: strong identity and access management across users, services, and pipelines; mutual authentication between internal components; cryptographic signing of datasets and model artifacts with verification before use; provenance validation for any public or third-party model; explicit allowlists for external tools and plugins.

**Related threat vectors**: prompt injection, backdoor injection, third-party component compromise, tool output manipulation.

## Tampering: changing the system without touching the code

Tampering in AI systems rarely resembles a traditional code change. It targets what the model learns or how it interprets input: training data poisoning that introduces backdoors, label manipulation that corrupts ground truth, feature pipeline tampering that shifts inputs undetected, direct modification of model weights, prompt template changes, retrieval corpus poisoning in retrieval-augmented systems, and long-term agent memory corruption.

**Controls**: full data lineage tracing from ingestion to training; signing and versioning of datasets, features, and models; artifact hashing with integrity verification before deployment; strict change control with separation of duties; immutable logs for all modifications; drift and anomaly monitoring after deployment.

**Related threat vectors**: data poisoning, label poisoning, backdoor injection, parameter tampering, RAG corpus poisoning, memory poisoning.

## Repudiation: when you cannot prove what happened

Repudiation risk becomes material the moment an AI system affects real people or regulated decisions. It appears as missing records of who modified a dataset or model, no version history for prompts or system instructions, and no way to reconstruct why a specific output occurred.

**Controls**: end-to-end audit logging across data, training, and inference; version control for prompts, models, datasets, and configurations; traceability linking each output to a model version and input context; signed approvals for training runs and deployments; tamper-evident log storage.

**Related threat vectors**: data provenance falsification, weak event traceability (see vulnerability catalog), insider sabotage.

## Information Disclosure: when the model reveals too much

AI systems create leakage paths that have no equivalent in traditional software. Models can memorize and reproduce training data, expose system prompts through carefully crafted queries, and generate personal data even when that was never the intent. Membership inference and model inversion attacks can reveal whether a specific record was used in training or reconstruct sensitive attributes. In agent systems, secrets can leak through retrieval or tool interactions.

**Controls**: minimize sensitive data in training and retrieval pipelines; output filtering and redaction; active adversarial testing for leakage; privacy-preserving training techniques such as differential privacy where warranted; segmented access to data, models, and tools; encryption at rest and in transit; data loss prevention applied to outputs, not only to storage.

**Related threat vectors**: sensitive data extraction, model inversion, membership inference, gradient leakage, model extraction via queries.

## Denial of Service: when usage becomes the attack

AI systems change the economics of denial of service. The goal is often not to take the system offline but to make it expensive or unstable. Attackers can flood APIs, exploit token limits, craft prompts that maximize compute usage, or trigger long or infinite tool-calling loops in agent workflows. In practice, this often surfaces first as a cost spike rather than an outage.

**Controls**: rate limits and per-user quotas; input size and context length restrictions; cost-aware request validation; circuit breakers for runaway processes; resource isolation across tenants and workloads; defined fallback behavior when limits are reached.

**Related threat vectors**: denial of service / denial of wallet, context window flooding, autonomous action chaining abuse.

## Elevation of Privilege: from unsafe output to unsafe action

STRIDE's original Elevation of Privilege category maps most directly onto agentic AI, where a model's output can trigger a real-world action. An agent or tool integration with excessive permissions turns a successful prompt manipulation into a business-impacting action: unauthorized transactions, data exfiltration, workflow corruption, or system reconfiguration.

**Controls**: least-privilege tool access; approval gates for sensitive or irreversible actions; action sandboxing; short-lived credentials scoped to the task; step-level logging of agent actions; explicit budget, time, and action-count limits.

**Related threat vectors**: excessive agency abuse, unauthorized tool use, goal hijacking, agent collusion.

## Threats STRIDE does not capture on its own

Several AI-specific risk categories do not map cleanly onto any single STRIDE letter and deserve independent attention during Phase 3: data poisoning as a lifecycle-spanning risk rather than a single tampering event, adversarial evasion at inference time, hallucination and fabrication as a source of exploitable business risk even without malicious intent, and the full set of agentic risks (goal hijacking, tool abuse, memory poisoning, cross-system lateral movement through authorized tools). These are addressed directly in `data/threat_vectors.yaml` and should be walked as a supplementary checklist alongside the STRIDE-AI pass, not folded into it.
