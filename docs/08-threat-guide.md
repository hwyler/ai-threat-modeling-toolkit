# AI Threat Vector Guide

This is the full-detail companion to `data/threat_vectors.yaml`. Where the YAML file gives you one filterable sentence per item for scripting, this guide gives you the complete picture for each of the 49 cataloged threat vectors: what the attack path is, why it is distinct from a conventional application attack, which layer of the AI stack it moves through, which stage of the AI project lifecycle it is most likely to be introduced or executed at, which cataloged vulnerability (see `docs/07-vulnerability-guide.md`) it depends on, which AI system types it matters most for, how it aligns with maintained external frameworks, what to actually test, and the controls that address it. Nothing here is condensed from the source catalog; every entry is written out in full.

Use this file in Phase 3 of an assessment (see `docs/01-methodology.md`) once assets are inventoried, to turn a general awareness of "prompt injection is a risk" into a specific, testable statement about your system.

## How to read each entry

- **Category** — the grouping used across this toolkit, matching `data/threat_vectors.yaml`.
- **Stack layer** — where in the AI system the attack actually executes: Interface and API, Data Pipeline, Training Pipeline, Model and Inference, Orchestration and Agent Layer, Infrastructure, Tooling and Supply Chain, Human and Organizational, or Physical and Hardware. A threat vector can touch more than one layer; the layer listed is where the attack surface is most concentrated.
- **Lifecycle stage(s)** — the AI project lifecycle stage(s) where this vector is most likely to be introduced, exploited, or both: Design and Requirements, Data Collection and Preparation, Training and Fine-Tuning, Validation and Testing, Deployment and Integration, Runtime and Inference, Monitoring and Maintenance, or Retirement and Decommission. Some vectors are introduced at one stage and exploited at another; both are noted where relevant.
- **Applies to** — which AI system type (predictive, generative, agentic) the vector is most consequential for.
- **Exploits vulnerability** — the id and name of the cataloged vulnerability or vulnerabilities from `docs/07-vulnerability-guide.md` and `data/vulnerabilities.yaml` that make this attack path feasible. A threat vector without a matching vulnerability present in your environment is a lower assessment priority.
- **External alignment** — the maintained framework this threat vector maps to. See `docs/06-source-alignment.md` for how to keep these current.
- **What to test** — the specific assessment activity, restated from practitioner guidance as a testable action.
- **Primary controls** — the controls that hold up in practice.

---

## Category 1: Prompt and Instruction Manipulation

Attacks that target the boundary between trusted instructions and untrusted content inside a model's context window.

### T001. Prompt Injection

| Field | Value |
|---|---|
| Stack layer | Interface and API, Model and Inference |
| Lifecycle stage(s) | Runtime and Inference |
| Applies to | Generative, Agentic |
| Exploits vulnerability | V004 Weak Prompt Isolation, V002 Insecure API Exposure |
| External alignment | OWASP Top 10 for LLM Applications (LLM01); MITRE ATLAS, Initial Access |

An attacker supplies malicious instructions through user input, retrieved content, uploaded documents, webpages, messages, or tool output in order to alter the model's intended behavior. This is one of the most consequential threats for generative and agentic AI because a successful injection can override the system's intended instructions, expose information the system was designed to withhold, bypass safety controls built into the prompt, and induce actions the user never authorized. The vector is not limited to typed user input: any channel the model reads from during a session, including a file, a search result, or a prior turn in a conversation, is a potential injection surface if the architecture does not separate it from trusted instructions.

**What to test:** whether the system can be manipulated through direct instruction injection typed by the user, indirect injection embedded in retrieved or uploaded content, and multimodal injection embedded in an image, audio clip, or document the model processes; and whether untrusted content of any of these kinds can influence the model's decisions, outputs, or tool invocations.

**Primary controls:** structural separation between system instructions and any user-supplied or retrieved content, enforced outside the model; output-side filtering for signs of instruction override; least-privilege tool access so a successful injection has limited downstream reach.

### T002. Indirect Prompt Injection

| Field | Value |
|---|---|
| Stack layer | Data Pipeline, Model and Inference |
| Lifecycle stage(s) | Data Collection and Preparation, Runtime and Inference |
| Applies to | Generative, Agentic |
| Exploits vulnerability | V004 Weak Prompt Isolation, V020 Uncontrolled Data Ingestion, V021 Untrusted External Data Sources |
| External alignment | OWASP Top 10 for LLM Applications (LLM01); MITRE ATLAS |

Malicious instructions are embedded in external content that the model reads later as part of retrieval, browsing, search, email processing, document parsing, or task execution, rather than being typed directly by an attacker in the session. This allows an attacker to influence model behavior without any direct interaction with the user's session or the API, which makes the vector harder to attribute and easier to deliver at scale, since a single poisoned document can affect every user session that later retrieves it. It is a distinct entry from direct prompt injection because the delivery mechanism, and therefore the defense, is different: the content entering the model's context was not supplied by the current user and was not necessarily under the organization's control when it was created.

**What to test:** whether hostile content placed in documents, support tickets, code comments, internal wikis, or external websites can alter model behavior, exfiltrate data, or trigger an unauthorized action once that content is retrieved into a session.

**Primary controls:** treat every document in a retrieval corpus as untrusted regardless of its original source, since a document trustworthy at creation can be altered later; sanitize and validate content at the retrieval boundary before it reaches the model's context; monitor for anomalous retrieval patterns that could indicate a poisoned document is being served repeatedly.

### T048. Context Window Flooding

| Field | Value |
|---|---|
| Stack layer | Model and Inference |
| Lifecycle stage(s) | Runtime and Inference |
| Applies to | Generative, Agentic |
| Exploits vulnerability | V004 Weak Prompt Isolation |
| External alignment | OWASP Top 10 for LLM Applications |

An attacker overloads the model's context with large, distracting, conflicting, or adversarially ordered content in order to suppress trusted instructions or increase the model's confusion about what to prioritize. This can reduce reliability, increase inference cost, and improve the success rate of an injection or evasion attack by pushing the system's own safety instructions out of the portion of context the model weighs most heavily. It is distinct from ordinary prompt injection because the attack does not necessarily need to contain a coherent malicious instruction; volume and placement alone can degrade the model's adherence to its original instructions.

**What to test:** context prioritization behavior, truncation rules, token budgeting, and whether trusted system instructions remain dominant when the model is presented with an adversarially large or adversarially ordered input load.

**Primary controls:** enforce context size limits with trusted instructions placed and re-asserted in a position the architecture protects from truncation; monitor for unusually large inputs relative to the task; token budgeting per session tied to expected task complexity.

---

## Category 2: Data and Training Integrity

Attacks that corrupt what a model learns, or what it treats as ground truth at retrieval time, rather than attacking the model directly at inference.

### T003. Data Poisoning

| Field | Value |
|---|---|
| Stack layer | Data Pipeline, Training Pipeline |
| Lifecycle stage(s) | Data Collection and Preparation, Training and Fine-Tuning |
| Applies to | Predictive, Generative |
| Exploits vulnerability | V014 Data Poisoning Susceptibility, V016 Weak Data Quality Controls, V020 Uncontrolled Data Ingestion |
| External alignment | NIST AI 100-2; OWASP Top 10 for LLM Applications (LLM04) |

Data poisoning is the deliberate insertion, modification, or curation of training, fine-tuning, feedback, or retrieval data intended to influence future model behavior. This threat vector is especially important in predictive AI and in any learning-enabled pipeline, because poisoned samples can either degrade performance broadly across the whole model or create a targeted backdoor that activates only under specific, attacker-chosen conditions, making it far harder to detect through ordinary performance monitoring. Assessment needs to cover poisoning across the full range of places training-relevant data originates: pre-training data, fine-tuning corpora, labels, retraining feedback loops, and retrieval-augmented generation knowledge bases, with particular attention wherever data is sourced externally or validated weakly before it enters the pipeline.

**What to test:** whether crafted samples can enter pre-training data, fine-tuning corpora, labels, retraining feedback loops, or a RAG knowledge base without triggering validation, and whether such samples measurably shift model behavior once incorporated.

**Primary controls:** anomaly detection on incoming training and feedback data; a held-out, provenance-verified evaluation set used to catch a performance shift after any retraining event; staged human review for externally sourced data before it reaches a training run.

### T004. Label Poisoning

| Field | Value |
|---|---|
| Stack layer | Data Pipeline |
| Lifecycle stage(s) | Data Collection and Preparation |
| Applies to | Predictive |
| Exploits vulnerability | V014 Data Poisoning Susceptibility, V016 Weak Data Quality Controls |
| External alignment | NIST AI 100-2 |

Label poisoning is a threat vector in which labels in a supervised learning dataset are manipulated, corrupted, or systematically skewed to alter the model's decision boundary and degrade its reliability. This vector can be used to reduce overall performance across the board, to create a targeted blind spot for a specific class or condition, or to make the model favor an attacker-selected outcome while leaving the underlying raw feature data completely unchanged, which is what makes it difficult to catch through feature-level data quality checks alone. Because the manipulation lives in the labels rather than the features, standard data validation focused on feature distributions will not catch it; the check has to specifically examine labeling consistency and the annotation process itself.

**What to test:** annotation workflows, reviewer independence, class distribution anomalies, suspicious relabeling events, and whether label quality is monitored throughout retraining rather than only at the initial labeling pass.

**Primary controls:** reviewer independence in the annotation process, with disagreement tracked rather than silently resolved; class distribution monitoring across retraining cycles; spot audits of labels against source ground truth on a recurring schedule.

### T005. Backdoor Injection

| Field | Value |
|---|---|
| Stack layer | Training Pipeline, Model and Inference |
| Lifecycle stage(s) | Training and Fine-Tuning, Validation and Testing |
| Applies to | Predictive, Generative |
| Exploits vulnerability | V014 Data Poisoning Susceptibility, V065 Unverified Third-Party Models, V010 Complex Model Loading |
| External alignment | MITRE ATLAS; NIST AI 100-2 |

Backdoor injection is a threat vector in which hidden triggers are embedded into training data or model behavior so that the system acts normally under nearly all conditions but fails or behaves maliciously the moment a specific trigger condition appears. This vector is especially dangerous because the model can pass standard validation and benchmark testing while still containing latent malicious behavior, since standard test sets are extremely unlikely to happen to include the exact trigger condition an attacker chose. Practitioners need to specifically evaluate outsourced training arrangements, third-party model imports, suspicious trigger-response patterns discovered through targeted probing, and whether purpose-built test cases can surface hidden conditional behavior that ordinary evaluation would miss entirely.

**What to test:** outsourced training relationships and third-party model imports for trigger-response patterns; targeted test cases specifically designed to surface conditional behavior rather than relying on standard benchmark evaluation alone.

**Primary controls:** independent security testing for any model that was trained outside the organization's direct control; trigger-pattern scanning where tooling exists for the model architecture in use; treating any third-party or outsourced training relationship as a trust decision requiring its own validation, not a routine procurement step.

### T006. RAG Corpus Poisoning

| Field | Value |
|---|---|
| Stack layer | Data Pipeline, Model and Inference |
| Lifecycle stage(s) | Data Collection and Preparation, Runtime and Inference |
| Applies to | Generative |
| Exploits vulnerability | V020 Uncontrolled Data Ingestion, V021 Untrusted External Data Sources, V013 Insufficient Provenance Controls |
| External alignment | OWASP Top 10 for LLM Applications (LLM04, LLM08) |

RAG corpus poisoning is a threat vector in which malicious or misleading content is inserted into a document repository, vector database, or enterprise knowledge source that a model later retrieves and treats as authoritative. This is especially important in enterprise generative AI because an attacker may not need to attack the model directly at all if they can influence the retrieval layer instead, embedding hidden instructions, false facts, or operationally harmful content into a source the model has been configured to trust by default. The attack is often cheaper and less detectable than a direct model-level attack, because it exploits the system's own design assumption that retrieved content is reliable simply because it came from an internal or previously-vetted source.

**What to test:** whether a poisoned document can alter output behavior, suppress correct information the model would otherwise surface, induce a prompt injection through embedded instructions, or cause disclosure of confidential data the poisoned document was never meant to have access to.

**Primary controls:** content sanitization and provenance checks at the point of ingestion into the retrieval corpus; ongoing review of who can add or edit content in the knowledge base; anomaly detection on retrieval results that could indicate a poisoned document is being surfaced unusually often.

### T029. Data Provenance Falsification

| Field | Value |
|---|---|
| Stack layer | Data Pipeline |
| Lifecycle stage(s) | Data Collection and Preparation |
| Applies to | Predictive, Generative, Agentic |
| Exploits vulnerability | V013 Insufficient Provenance Controls |
| External alignment | NIST AI 100-2 |

Data provenance falsification is a threat vector in which metadata, lineage records, ownership fields, timestamps, source identifiers, or chain-of-custody records are altered to disguise the true origin or integrity of AI data. This enables poisoned, biased, stolen, or noncompliant data to enter the training or retrieval pipeline under the appearance of legitimacy, which is what makes it a distinct and more insidious vector than data poisoning on its own: it specifically attacks the trust mechanism the organization relies on to decide which data is safe to use, rather than the data itself. Practitioners need to assess whether source records can be forged, silently overwritten, or detached from the actual datasets they claim to describe, and whether data trust decisions in the organization rely too heavily on metadata that is itself editable by the same actors who could benefit from falsifying it.

**What to test:** whether provenance and lineage records can be forged or overwritten without detection, and whether the organization's data trust decisions depend on metadata fields that are not independently verified against the data they describe.

**Primary controls:** cryptographic signing of provenance records at the point of data creation or ingestion, separate from the editable metadata fields; independent verification of lineage claims rather than trusting self-reported metadata; audit trails on any change to provenance fields themselves.

### V014-adjacent note

Bias Exploitation Through Imbalanced Data is catalogued separately below under Privacy and Fairness Exploitation, since its primary harm is discriminatory outcome rather than data integrity, though it shares data-layer root causes with this category.

---

## Category 3: Model Extraction and Inference Attacks

Attacks that target the model's learned behavior directly, either to steal it or to force it into an incorrect decision.

### T008. Model Extraction via Queries

| Field | Value |
|---|---|
| Stack layer | Interface and API, Model and Inference |
| Lifecycle stage(s) | Runtime and Inference |
| Applies to | Predictive, Generative |
| Exploits vulnerability | V003 Unrestricted Query Access, V002 Insecure API Exposure |
| External alignment | MITRE ATLAS, Exfiltration; OWASP Top 10 for LLM Applications (LLM10) |

Model extraction via queries is a threat vector in which an attacker systematically interacts with a model API or inference service in order to learn its behavior closely enough to reproduce a functional copy offline. This threatens both intellectual property and security simultaneously, because the extracted model can then be studied offline to map its decision boundaries, design evasion strategies against the original system, or bypass licensing and usage restrictions the organization intended to enforce. Assessment should specifically examine whether repeated querying at scale, detailed confidence outputs, verbose responses, or weak abuse monitoring make extraction feasible at a cost an attacker would consider reasonable relative to the value of the model.

**What to test:** whether repeated, systematic querying, exposed confidence scores, overly detailed responses, or the absence of abuse monitoring make it practical to reconstruct a functional copy of the model at a realistic cost.

**Primary controls:** rate limiting and per-key quotas tuned to detect extraction-pattern querying specifically, not just high volume; minimization of confidence scores and other detail in production responses; monitoring for query patterns consistent with systematic boundary-mapping.

### T009. Functional Extraction

| Field | Value |
|---|---|
| Stack layer | Interface and API, Model and Inference |
| Lifecycle stage(s) | Runtime and Inference |
| Applies to | Predictive, Generative |
| Exploits vulnerability | V003 Unrestricted Query Access |
| External alignment | MITRE ATLAS |

Functional extraction is a threat vector in which attackers create an offline model that behaves similarly enough to the target system to support attack development, policy evasion, or competitive substitution, without necessarily obtaining the model's exact weights or a full-fidelity copy of its architecture. While closely related to model extraction via queries, this vector specifically emphasizes reproducing operational behavior rather than exact replication, which means it can succeed even against a system with some anti-extraction controls in place, as long as those controls do not also obscure the model's functional decision patterns. Practitioners should assess whether the system reveals enough output structure, determinism, and behavioral consistency across queries for an attacker to clone its practical utility for downstream offensive use, even without a bit-for-bit copy.

**What to test:** whether the system's output structure, determinism, and behavioral consistency across repeated similar queries are sufficient for an attacker to build a usable functional substitute without full weight access.

**Primary controls:** introducing controlled variability in non-safety-relevant output where feasible; monitoring for the specific query diversity pattern consistent with functional cloning rather than normal use; treating this as a distinct risk from full-weight extraction when designing anti-abuse controls.

### T007. Adversarial Evasion

| Field | Value |
|---|---|
| Stack layer | Model and Inference |
| Lifecycle stage(s) | Runtime and Inference |
| Applies to | Predictive |
| Exploits vulnerability | V025 Insufficient Model Validation |
| External alignment | NIST AI 100-2; MITRE ATLAS |

Adversarial evasion is a threat vector in which attackers craft inputs specifically designed to cause the model to misclassify, mis-rank, or generate an unsafe result during inference. This is highly relevant to predictive AI used in fraud detection, computer vision, malware detection, and general classification systems, where an attacker directly benefits from being misclassified as legitimate. Analogous forms exist in generative AI as well, where prompts are designed to induce a policy bypass or an unsafe completion, though the underlying mechanism differs from classic adversarial perturbation. Assessment should include both targeted evasion, aimed at a specific misclassification, and untargeted evasion, aimed at any misclassification; semantic manipulation; obfuscation techniques; environmental perturbation for systems that process real-world sensor input; and sensitivity testing against minor but adversarially chosen input changes that a human would not consider meaningfully different.

**What to test:** targeted and untargeted evasion scenarios, semantic manipulation, obfuscation, environmental perturbation for sensor-driven systems, and the model's sensitivity to minor but adversarially chosen input changes.

**Primary controls:** adversarial robustness testing as a standing part of the validation process, not a one-time check; ensemble or confidence-threshold defenses for high-stakes classification decisions; human review triggered for decisions near the model's confidence threshold.

### T036. Black-Box Manipulation

| Field | Value |
|---|---|
| Stack layer | Model and Inference |
| Lifecycle stage(s) | Runtime and Inference |
| Applies to | Predictive, Generative |
| Exploits vulnerability | V038 Weak Explainability Controls |
| External alignment | MITRE ATLAS |

Black-box manipulation is a threat vector in which attackers exploit the inherent opacity of a model to probe its behavior, infer weaknesses, and craft attacks without needing any internal access to the model's architecture or weights. This is especially relevant to deep learning systems, where the lack of interpretability makes it genuinely difficult for defenders to notice subtle manipulation occurring or to understand why the model failed under a particular adversarial condition after the fact. Assessment should test whether an attacker, working purely through trial-and-error interaction with the exposed interface, can systematically identify blind spots, unstable decision regions, or policy inconsistencies without ever needing privileged access to the model itself.

**What to test:** whether systematic, purely external trial-and-error interaction can identify blind spots, unstable regions, or policy inconsistencies in the model's decision behavior.

**Primary controls:** monitoring for the query patterns consistent with systematic probing rather than normal use; explainability tooling sufficient to let defenders diagnose a suspected manipulation after the fact, even if full interpretability is not achievable; rate limiting on interactive probing.

### T037. Model Drift Exploitation

| Field | Value |
|---|---|
| Stack layer | Model and Inference |
| Lifecycle stage(s) | Monitoring and Maintenance |
| Applies to | Predictive, Generative |
| Exploits vulnerability | V027 Missing Drift Controls |
| External alignment | NIST AI RMF, Measure function |

Model drift exploitation is a threat vector in which attackers take advantage of the fact that a model has become misaligned with current data, behavior, or environmental conditions, causing degraded performance or incorrect decisions the organization has not yet noticed. Drift itself may occur naturally as the world changes around a static model, but an adversary can intentionally time or steer an attack specifically to exploit periods when the model is least calibrated to current conditions, since a drifted model's error patterns are often more predictable and more exploitable than a well-calibrated one's. Assessment should determine whether the organization can detect drift quickly enough to matter, isolate its effects to the specific decisions it has already influenced, and prevent an attacker from exploiting known stale behavior once drift has been identified but not yet corrected.

**What to test:** the organization's actual time-to-detect for drift, whether drift effects can be isolated to specific affected decisions, and whether known drift is corrected before it becomes exploitable in practice.

**Primary controls:** statistical drift monitoring with a defined action threshold, not just an alert; a documented, rehearsed process to isolate and correct drift once detected; scheduled re-validation independent of drift alerts, since gradual drift can stay under alerting thresholds for extended periods.

### T038. Generalization Failure Exploitation

| Field | Value |
|---|---|
| Stack layer | Model and Inference |
| Lifecycle stage(s) | Validation and Testing, Runtime and Inference |
| Applies to | Predictive |
| Exploits vulnerability | V025 Insufficient Model Validation |
| External alignment | NIST AI 100-2 |

Generalization failure exploitation is a threat vector in which attackers capitalize on overfitting, underfitting, brittle decision boundaries, or narrow training coverage to force incorrect model behavior on inputs that are novel but entirely realistic. Some practitioners classify this as a model limitation rather than a threat vector in the traditional sense, but from a red-teaming perspective it is a genuine attack path whenever an adversary deliberately searches for out-of-distribution or weakly represented conditions the model was never adequately trained or tested against. Assessment should include deliberate edge-case exploration, subgroup testing across demographic or use-case segments, out-of-domain input testing, and evaluation of whether an attacker can reliably trigger failure using data that falls outside the standard evaluation set the model was originally validated against.

**What to test:** edge-case exploration, subgroup testing, out-of-domain input testing, and whether failure can be triggered reliably using inputs outside the model's original evaluation set.

**Primary controls:** validation coverage deliberately extended beyond the standard benchmark to include edge cases and underrepresented subgroups; ongoing collection of production failure cases fed back into evaluation; confidence-based fallback to human review for inputs the model flags as unfamiliar.

---

## Category 4: Privacy and Fairness Exploitation

Attacks that extract information the model was never meant to disclose, or that exploit imbalance in the data the model learned from.

### T013. Sensitive Data Extraction

| Field | Value |
|---|---|
| Stack layer | Model and Inference, Data Pipeline |
| Lifecycle stage(s) | Runtime and Inference |
| Applies to | Predictive, Generative, Agentic |
| Exploits vulnerability | V022 Weak De-Identification, V023 Training Data Memorization, V061 Weak Metadata Scrubbing |
| External alignment | OWASP Top 10 for LLM Applications (LLM02) |

Sensitive data extraction is a threat vector in which attackers recover confidential training data, personal data, secrets, business records, or proprietary knowledge from the model itself, its outputs, associated storage, or surrounding components. This is a broad category that includes behaviors more specifically described elsewhere in this guide as data leakage, exfiltration, membership inference, or privacy extraction, depending on the exact technical path the attacker takes; this entry covers the general case where the specific mechanism may not be immediately clear. Assessment should focus on whether an adversary can obtain sensitive information through ordinary interaction with the system, through API abuse, through abuse of the retrieval layer, through exposed debugging interfaces, through prompt replay of prior sessions, or through model-assisted reconstruction of partial information the attacker already holds.

**What to test:** whether sensitive information can be obtained through ordinary interaction, API abuse, retrieval abuse, exposed debugging interfaces, prompt replay, or model-assisted reconstruction from partial attacker-held information.

**Primary controls:** output filtering and redaction layered on top of training-time minimization; active adversarial testing specifically designed to elicit leakage, not just functional testing; segmented access so a single compromised credential cannot reach the full range of sensitive data paths.

### T010. Model Inversion

| Field | Value |
|---|---|
| Stack layer | Model and Inference |
| Lifecycle stage(s) | Runtime and Inference |
| Applies to | Predictive |
| Exploits vulnerability | V022 Weak De-Identification, V023 Training Data Memorization |
| External alignment | NIST AI 100-2 |

Model inversion is a threat vector in which an attacker analyzes model responses in order to reconstruct sensitive attributes, representative records, or close approximations of the data used to train the model. This is particularly relevant where models are trained on healthcare, biometric, financial, or otherwise sensitive data and where the model exposes rich responses or detailed confidence information that gives an attacker more to work with than a simple pass or fail output would. Practitioners should assess whether outputs, gradients, embedding access, or repeated targeted queries against the same decision boundary enable meaningful inference of private records or sensitive attributes that were never meant to be recoverable from the deployed model.

**What to test:** whether outputs, gradients, embedding access, or repeated targeted querying allow reconstruction of private records or sensitive attributes from the training data.

**Primary controls:** minimizing response detail and confidence information in production; differential privacy applied during training where the sensitivity of the underlying data warrants the accuracy tradeoff; restricting or monitoring embedding and gradient access where those interfaces are exposed.

### T011. Membership Inference

| Field | Value |
|---|---|
| Stack layer | Model and Inference |
| Lifecycle stage(s) | Runtime and Inference |
| Applies to | Predictive, Generative |
| Exploits vulnerability | V023 Training Data Memorization |
| External alignment | NIST AI 100-2 |

Membership inference is a threat vector in which an attacker determines whether a specific individual, record, or item was included in a model's training data. This may seem like a narrow or low-impact capability at first glance, but it can create serious privacy and legal exposure whenever mere participation in a dataset is itself sensitive information, such as in healthcare, law enforcement, employment, or intelligence contexts, where confirming someone was part of a particular dataset can itself reveal something the individual never consented to disclose. Assessment should examine whether output confidence patterns, signs of overfitting, differential behavior between training and non-training inputs, or unusually verbose responses allow an adversary to infer dataset membership with accuracy meaningful enough to matter.

**What to test:** whether output confidence, overfitting signals, differential behavior between seen and unseen inputs, or response verbosity allow an adversary to infer training-set membership with meaningful accuracy.

**Primary controls:** overfitting reduction during training, since overfitting is a primary enabler of successful membership inference; differential privacy where the dataset's sensitivity warrants it; testing membership inference susceptibility as a standing part of pre-release validation for sensitive-domain models.

### T012. Gradient Leakage

| Field | Value |
|---|---|
| Stack layer | Training Pipeline |
| Lifecycle stage(s) | Training and Fine-Tuning |
| Applies to | Predictive |
| Exploits vulnerability | V060 Exposed Gradient Information |
| External alignment | NIST AI 100-2 |

Gradient leakage is a threat vector in which an attacker reconstructs training examples or infers sensitive information from gradient updates or model parameter changes shared during distributed or federated learning. This vector is well established in the technical literature and is especially important wherever an organization uses collaborative learning methods under the working assumption that sharing gradients, rather than raw data, is inherently privacy-preserving; that assumption does not hold without additional protection layered on top. Assessment should evaluate whether secure aggregation is in place, whether differential privacy is applied to shared updates, whether gradient clipping limits the information any single update can carry, who has access to the update stream, and whether the shared training signals could plausibly reveal individual data points to a participant or observer.

**What to test:** whether secure aggregation, differential privacy, and gradient clipping are actually applied to shared training signals, and whether an observer with access to the update stream could reconstruct individual data points from it.

**Primary controls:** secure aggregation protocols so no single party can observe raw gradient updates; gradient clipping and differential privacy applied before sharing; restricted access to the update stream itself, treated with the same sensitivity as the underlying data.

### T014. Bias Exploitation Through Imbalanced Data

| Field | Value |
|---|---|
| Stack layer | Data Pipeline, Model and Inference |
| Lifecycle stage(s) | Data Collection and Preparation, Runtime and Inference |
| Applies to | Predictive |
| Exploits vulnerability | V016 Weak Data Quality Controls, V044 Weak Human Rights Assessment |
| External alignment | NIST AI 100-2 |

Bias exploitation through imbalanced data is a threat vector in which attackers, or in some cases negligent internal processes, take advantage of underrepresented groups, skewed classes, or socially biased data distributions to produce discriminatory or otherwise harmful outcomes. While this is not always the result of an intentional attack, it becomes a genuine threat vector the moment a bad actor knowingly manipulates or deliberately leverages an existing imbalance to steer outcomes in high-stakes domains such as hiring, lending, fraud screening, identity verification, or other public-facing services. Assessment should cover the representativeness of the underlying data, subgroup error rates measured separately rather than only in aggregate, the data collection process itself for embedded bias, and whether an adversary could plausibly steer outcomes further by deliberately amplifying an existing imbalance rather than needing to introduce a new one.

**What to test:** representativeness of the training data, subgroup error rates measured independently rather than in aggregate, the data collection process for embedded bias, and whether an adversary could amplify existing imbalance to steer outcomes.

**Primary controls:** subgroup-level fairness evaluation as a required release gate, not an optional analysis; corrective sampling or reweighting where representativeness gaps are identified; ongoing monitoring for outcome disparities in production, not only at initial validation.

### T030. Eavesdropping on Inputs

| Field | Value |
|---|---|
| Stack layer | Interface and API, Infrastructure |
| Lifecycle stage(s) | Runtime and Inference |
| Applies to | Predictive, Generative, Agentic |
| Exploits vulnerability | V002 Insecure API Exposure |
| External alignment | NIST AI RMF, Manage function |

Eavesdropping on inputs is a threat vector in which attackers intercept user prompts, uploaded files, sensor streams, or transaction data before that data is processed by the AI system. This can expose highly sensitive business or personal information at the point of transmission, and it may also provide an attacker with the raw material needed to conduct a secondary attack, such as crafting a targeted prompt injection, harvesting credentials that appeared incidentally in the intercepted content, or gathering competitive intelligence about how the organization actually uses the system. Assessment should cover network encryption end to end, the possibility of endpoint compromise on either side of the exchange, exposure through browser or proxy layers the input passes through, and whether every model input channel is genuinely protected both in transit and at the point of collection.

**What to test:** network encryption coverage end to end, endpoint compromise scenarios, browser and proxy exposure, and whether every input channel is protected both in transit and at the point of collection.

**Primary controls:** encryption in transit for every input channel without exception; endpoint hardening on client-side components that collect input before submission; monitoring for interception attempts at network chokepoints.

### T031. Eavesdropping on Outputs

| Field | Value |
|---|---|
| Stack layer | Interface and API, Infrastructure |
| Lifecycle stage(s) | Runtime and Inference |
| Applies to | Predictive, Generative, Agentic |
| Exploits vulnerability | V028 Insufficient Logging, V061 Weak Metadata Scrubbing |
| External alignment | NIST AI RMF, Manage function |

Eavesdropping on outputs is a threat vector in which attackers intercept model responses, decision results, generated content, confidence values, or tool results as they leave the AI system on their way back to the user or to a downstream consumer. This can expose confidential business logic, personal data, training artifacts, or operational instructions that the response was never meant to reveal outside its intended recipient, and it can also support a subsequent model inversion or functional extraction attempt by giving the attacker a larger sample of the model's actual output behavior to analyze. Practitioners should assess the output channels themselves, the logging systems that may retain a copy of the output longer than intended, browser rendering paths for web-based interfaces, inter-service messaging between components of a larger pipeline, and whether outputs are genuinely protected both in transit and at rest wherever they are stored.

**What to test:** output channel protection, logging retention of output content, browser rendering exposure, inter-service messaging security, and whether outputs are protected both in transit and at rest.

**Primary controls:** encryption in transit and at rest for output data, including in logs; retention limits on logged output content, scoped to what is actually needed for the purposes logging serves; access controls on inter-service messaging carrying model output.

---

## Category 5: Content and Trust Exploitation

Attacks and misuse patterns that exploit what a generative model produces, or how much a human trusts it, rather than the model's internal mechanics.

### T015. Hallucination Exploitation

| Field | Value |
|---|---|
| Stack layer | Model and Inference |
| Lifecycle stage(s) | Runtime and Inference |
| Applies to | Generative, Agentic |
| Exploits vulnerability | V038 Weak Explainability Controls, V047 Over-Automation Dependence |
| External alignment | OWASP Top 10 for LLM Applications |

Hallucination exploitation is a threat vector in which attackers intentionally cause a generative model to produce false, fabricated, or misleading content that can then be used to deceive users, justify an unwarranted action, or contaminate a downstream workflow that consumes the model's output as if it were reliable. This is particularly relevant in high-trust business settings where plausible-sounding but incorrect outputs may be accepted as valid by operators, customers, or automated downstream systems without independent verification, precisely because the output reads as confident and coherent. Practitioners should assess whether the model can be deliberately induced to invent facts, credentials, citations, procedures, or policy interpretations in ways that would materially affect a real operational or business decision if accepted at face value.

**What to test:** whether the model can be deliberately induced to invent facts, credentials, citations, procedures, or policy interpretations that would materially affect a real decision if accepted without verification.

**Primary controls:** grounding mechanisms that tie output to verifiable source material wherever the use case allows it; verification checks or confidence indicators surfaced to the user rather than hidden; restrictions on fully automated use of unverifiable output in consequential decisions.

### T016. Toxicity Induction

| Field | Value |
|---|---|
| Stack layer | Model and Inference |
| Lifecycle stage(s) | Runtime and Inference |
| Applies to | Generative |
| Exploits vulnerability | V004 Weak Prompt Isolation |
| External alignment | OWASP Top 10 for LLM Applications |

Toxicity induction is a threat vector in which attackers deliberately provoke a model into generating hateful, abusive, sexually explicit, extremist, or otherwise harmful content. This is especially important for public-facing generative AI because harmful output alone can create immediate legal, reputational, and trust consequences even in the complete absence of any broader system compromise; the model does not need to be "hacked" in a technical sense for this to be a serious incident. Assessment should test whether adversaries can elicit toxic output across multiple languages, across different conversational contexts, and through obfuscation methods including role-play framing, paraphrase, and coded or indirect language designed to evade keyword-based filtering.

**What to test:** whether toxic output can be elicited across languages, contexts, and obfuscation methods, including role-play framing, paraphrase, and coded language designed to evade filtering.

**Primary controls:** content filtering that evaluates semantic intent rather than relying solely on keyword matching; testing across languages and obfuscation techniques as a standing part of red-teaming, not a one-time check; a defined incident response path specifically for public-facing toxic output events.

### T017. Dual-Use or Malicious Repurposing

| Field | Value |
|---|---|
| Stack layer | Model and Inference, Human and Organizational |
| Lifecycle stage(s) | Runtime and Inference |
| Applies to | Generative, Agentic |
| Exploits vulnerability | V040 Weak Intended Use Controls, V047 Over-Automation Dependence |
| External alignment | OWASP Top 10 for LLM Applications |

Dual-use or malicious repurposing is a threat vector in which a model designed for benign enterprise use is repurposed, stolen, or adapted for fraud, misinformation, surveillance, phishing, deepfake production, or other harmful purposes. This vector matters both internally and externally, because misuse may originate from authorized employees who exceed the system's intended purpose, from malicious customers using a legitimately granted access level, or from external actors who obtain model access or a derivative artifact through some other compromise. Assessment should cover observed abuse patterns, the strength of policy restrictions on use, monitoring of both customer and employee behavior for signs of repurposing, and whether the model's actual capabilities create foreseeable misuse channels that were not considered during the original design review.

**What to test:** observed abuse patterns, enforcement of use-policy restrictions, customer and employee behavioral monitoring, and whether the model's capabilities create foreseeable misuse channels not addressed in the original design review.

**Primary controls:** use-policy enforcement built into the system, not documented only in a terms-of-service agreement; monitoring calibrated to detect repurposing patterns specifically, separate from general abuse monitoring; periodic review of the model's actual capabilities against foreseeable misuse, repeated as capabilities expand.

### T018. Unsafe Content Repurposing

| Field | Value |
|---|---|
| Stack layer | Model and Inference |
| Lifecycle stage(s) | Runtime and Inference |
| Applies to | Generative |
| Exploits vulnerability | V040 Weak Intended Use Controls |
| External alignment | OWASP Top 10 for LLM Applications |

Unsafe content repurposing is a threat vector in which a model is used to generate phishing messages, malware-adjacent scripts, disinformation, fraudulent documents, social engineering content, or deepfake support materials. This is a significant risk for enterprise AI because the system itself can become a force multiplier for internal misuse, for external abuse by a malicious user of the product, or for policy-violating customer behavior that the organization is then implicated in facilitating, even unintentionally. Practitioners should assess whether misuse patterns of this kind can actually be detected once they begin, whether stated use restrictions are technically enforced rather than merely documented, and whether the model can be steered into providing harmful assistance despite policy controls that were designed to prevent exactly that outcome.

**What to test:** whether misuse patterns can be detected in practice, whether use restrictions are technically enforced, and whether the model can be steered into harmful assistance despite existing policy controls.

**Primary controls:** technical enforcement of content restrictions layered with, not substituted for, policy documentation; abuse pattern detection tuned to the specific misuse categories relevant to the deployment; rapid response process for confirmed misuse, including account-level action where appropriate.

### T019. Synthetic Identity and Deepfake Enablement

| Field | Value |
|---|---|
| Stack layer | Model and Inference |
| Lifecycle stage(s) | Runtime and Inference |
| Applies to | Generative |
| Exploits vulnerability | V040 Weak Intended Use Controls |
| External alignment | OWASP Top 10 for LLM Applications |

Synthetic identity and deepfake enablement is a threat vector in which AI systems are used to create realistic fake personas, voice clones, forged images, or impersonation content that supports fraud or disinformation efforts. This vector is most relevant to generative models with image, audio, or text synthesis capability, and it can materially increase the effectiveness of social engineering attacks by giving the attacker a far more convincing artifact than earlier-generation forgery techniques could produce. Assessment should consider how easily the model can be used to generate impersonation content in the first place, what safeguards exist to limit or watermark that capability, and how the organization actually monitors for abuse of these capabilities once they are made available.

**What to test:** how easily impersonation content can be generated, what safeguards or watermarking exist, and how abuse of these specific capabilities is monitored once deployed.

**Primary controls:** watermarking or provenance signals embedded in synthetic content where the underlying technology supports it; restrictions or additional verification steps on identity-adjacent generation capabilities; monitoring specifically calibrated to detect impersonation-content generation patterns.

### T020. Overreliance / Automation Bias

| Field | Value |
|---|---|
| Stack layer | Human and Organizational |
| Lifecycle stage(s) | Deployment and Integration, Runtime and Inference |
| Applies to | Predictive, Generative, Agentic |
| Exploits vulnerability | V047 Over-Automation Dependence, V039 Poor User Guidance |
| External alignment | OWASP Top 10 for LLM Applications; OWASP Top 10 for Agentic Applications |

Overreliance is a threat vector in which humans accept AI outputs or recommendations with insufficient scrutiny, leading to poor decisions, unsafe approvals, or the unchecked propagation of a model's error into a real-world outcome. This is a major cross-cutting threat because even a technically accurate system can cause real harm if users trust it in contexts where uncertainty, bias, or adversarial manipulation are not visible to the person relying on the output, and no amount of model-level robustness fixes a process that removed the human check that was supposed to catch the remaining failure cases. Practitioners should assess whether users are likely to defer to the model specifically in high-stakes decisions, and whether the surrounding process actually forces independent verification where the risk of the decision warrants it, rather than assuming users will apply appropriate skepticism on their own.

**What to test:** whether users defer to model output in high-stakes decisions without independent verification, and whether process controls actually force that verification where the risk warrants it.

**Primary controls:** mandatory independent verification for decisions above a defined risk threshold, enforced by process rather than left to individual judgment; user guidance that explicitly states the system's known limitations rather than implying general reliability; periodic audit of decisions actually made against model recommendations to check for unchecked deference.

### T039. Transparency Deficit Exploitation

| Field | Value |
|---|---|
| Stack layer | Model and Inference, Human and Organizational |
| Lifecycle stage(s) | Monitoring and Maintenance |
| Applies to | Predictive, Generative, Agentic |
| Exploits vulnerability | V038 Weak Explainability Controls, V030 Weak Event Traceability |
| External alignment | NIST AI RMF, Govern function |

Transparency deficit exploitation is a threat vector in which attackers, or in some cases negligent internal actors, benefit from the organization's inability to explain, justify, or audit its own model's decisions. This can hide biased outcomes that would otherwise be caught by review, obscure a manipulation that has already occurred, delay incident response because investigators cannot reconstruct what happened, and reduce the organization's ability to prove compliance to a regulator or to investigate a harmful result after the fact with any confidence in the conclusion. Practitioners should assess whether the lack of explainability creates operational blind spots that an attacker could specifically exploit, or that simply prevent the organization's own teams from recognizing when the AI system has already been manipulated.

**What to test:** whether the current level of explainability would actually allow the organization to detect and investigate a manipulation that had already occurred, rather than only explain a normal decision.

**Primary controls:** explainability and traceability sufficient to support a real post-incident investigation, tested against a simulated scenario rather than assumed adequate; periodic review of whether opacity has been a contributing factor in any past incident or near-miss; escalation of transparency gaps as a governance finding, not only a technical one.

---

## Category 6: Access, API, and Credential Attacks

Attacks that target the interface layer common to nearly every AI deployment, regardless of system type.

### T022. API Abuse

| Field | Value |
|---|---|
| Stack layer | Interface and API |
| Lifecycle stage(s) | Runtime and Inference |
| Applies to | Predictive, Generative, Agentic |
| Exploits vulnerability | V002 Insecure API Exposure, V003 Unrestricted Query Access |
| External alignment | OWASP Top 10 for LLM Applications (LLM10) |

API abuse is a threat vector in which attackers exploit exposed AI interfaces to manipulate model behavior, extract data, steal the model itself, or degrade the service for legitimate users. This is a high-frequency vector across predictive, generative, and agentic systems alike, because application programming interfaces often provide the most direct and scalable path into both the model and the orchestration environment surrounding it, compared to any other component in the stack. Practitioners should assess for weak authentication, broken authorization that permits access beyond a caller's intended scope, missing rate limits, evidence of query automation, ease of endpoint discovery for undocumented paths, replay abuse of previously captured requests, and insecure handling of request parameters that could allow unexpected behavior.

**What to test:** authentication strength, authorization boundaries, rate limit enforcement, evidence of automated querying, undocumented endpoint discoverability, replay abuse, and parameter handling.

**Primary controls:** strong authentication and fine-grained authorization on every endpoint, including undocumented or internal ones; comprehensive rate limiting tuned per endpoint sensitivity; regular API discovery scanning from an attacker's perspective to catch undocumented exposure.

### T023. API Token Compromise

| Field | Value |
|---|---|
| Stack layer | Infrastructure, Tooling and Supply Chain |
| Lifecycle stage(s) | Deployment and Integration, Runtime and Inference |
| Applies to | Predictive, Generative, Agentic |
| Exploits vulnerability | V001 Weak Access Control, V009 Weak Artifact Protection |
| External alignment | MITRE ATLAS, Credential Access |

API token compromise is a threat vector in which attackers steal, leak, reuse, or misuse credentials that grant access to AI models, tools, data stores, orchestration services, or cloud resources. This vector is operationally significant because many AI environments rely heavily on service tokens, integration keys, notebook secrets, and automation credentials, and these credentials are frequently overprivileged relative to what any single automated task actually requires, and poorly rotated compared to standard credential hygiene practices for human user accounts. Assessment should include a review of secret exposure in prompts, in logs, in code repositories, in continuous integration and deployment pipelines, in browser storage for web-based tools, and across any third-party integrations the system depends on, since a leaked credential in any one of these locations grants the same access as one leaked anywhere else.

**What to test:** secret exposure across prompts, logs, code repositories, CI/CD pipelines, browser storage, and third-party integrations, and whether exposed credentials would grant access disproportionate to their intended purpose.

**Primary controls:** credential scanning across code repositories, logs, and CI/CD pipelines as a standing automated check; scoped, short-lived credentials for automated tasks rather than long-lived broad-access tokens; regular rotation enforced by policy rather than left to individual teams.

### T021. Shadow AI Use

| Field | Value |
|---|---|
| Stack layer | Human and Organizational |
| Lifecycle stage(s) | Design and Requirements, Runtime and Inference |
| Applies to | Generative |
| Exploits vulnerability | V040 Weak Intended Use Controls, V035 Missing AI Policies |
| External alignment | NIST AI RMF, Govern function |

Shadow AI use is a threat vector in which employees or business units introduce unapproved AI tools, models, or services outside the organization's security, compliance, and architecture review process. This exposes the organization to uncontrolled data transfer into systems it does not govern, insecure prompting practices that were never reviewed, vendor risk that procurement never assessed, poor retention practices for sensitive data submitted to the unapproved tool, and unmonitored decision-making that may be influencing real business outcomes without any oversight at all. Assessment should determine whether staff are actually using external copilots, browser plugins, software-as-a-service models, or local agents without authorization, and specifically whether sensitive business data is being routed to these unsanctioned systems as part of ordinary work.

**What to test:** whether staff are using unapproved external copilots, browser plugins, SaaS models, or local agents, and whether sensitive business data is flowing to any of them.

**Primary controls:** a clear, low-friction approval path for new AI tools so shadow adoption is less attractive than the sanctioned alternative; network and endpoint monitoring for known unapproved AI service patterns; regular staff communication clarifying which tools are approved and why the distinction matters.

### T040. Homogenization Risk Exploitation

| Field | Value |
|---|---|
| Stack layer | Tooling and Supply Chain |
| Lifecycle stage(s) | Design and Requirements, Deployment and Integration |
| Applies to | Predictive, Generative, Agentic |
| Exploits vulnerability | V063 Black-Box Dependency Reliance, V066 Outdated Third-Party Components |
| External alignment | OWASP Top 10 for LLM Applications (LLM03) |

Homogenization risk exploitation is a threat vector in which attackers target a widely adopted model, dependency, or architectural pattern, knowing that a single successful exploit path may affect many systems simultaneously rather than just one. This creates systemic risk because AI monocultures concentrate failure: when a large share of an industry, or even a single large organization's own product portfolio, relies on the same foundation model or the same shared component, one attack technique can scale across vendors, business units, or an entire sector at once. Assessment should review the organization's dependence on common models, shared third-party services, uniform prompt frameworks used across multiple products, and whether a single compromise anywhere in that shared dependency could propagate broadly through the environment before it is contained.

**What to test:** the extent of dependence on common models or shared third-party services across multiple products, and whether a compromise in one could propagate broadly before containment.

**Primary controls:** diversification of critical dependencies where feasible, weighed against the operational cost of maintaining multiple integrations; blast-radius analysis specifically for shared components during architecture review; incident response planning that accounts for a shared-dependency compromise affecting multiple systems at once.

---

## Category 7: Agentic-Specific Threat Vectors

Attacks unique to systems that plan, call tools, retain memory across turns, and act with limited human review. Every vector in this category assumes the system has moved from producing output to taking action.

### T041. Unauthorized Tool Use

| Field | Value |
|---|---|
| Stack layer | Orchestration and Agent Layer |
| Lifecycle stage(s) | Runtime and Inference |
| Applies to | Agentic |
| Exploits vulnerability | V005 Excessive Tool Permissions, V006 Weak Runtime Authorization |
| External alignment | OWASP Top 10 for Agentic Applications (ASI02) |

Unauthorized tool use is a threat vector in which a model or agent is induced to call plugins, application programming interfaces, scripts, databases, or enterprise systems in ways that violate its intended authority or the organization's business policy. This is a primary concern for agentic AI specifically because the impact of a successful attack moves from an unsafe output that a human might catch before acting on it, to an unsafe action that has already happened, including account modification, data exfiltration, workflow corruption, or the execution of a real transaction. Practitioners should assess whether a model can be induced to trigger sensitive tools through direct prompt manipulation, through manipulated tool output that misleads the agent's planning, through hidden argument injection into an otherwise legitimate-looking tool call, or through multi-step planning abuse that arrives at an unauthorized tool call indirectly.

**What to test:** whether sensitive tools can be triggered through prompt manipulation, manipulated tool output, hidden argument injection, or multi-step planning that indirectly arrives at an unauthorized call.

**Primary controls:** independent authorization for any sensitive tool call, not granted by the model's own decision alone; scoped, task-specific tool credentials rather than broad standing access; logging and review of every tool invocation, with alerting on calls outside expected patterns.

### T042. Tool Output Manipulation

| Field | Value |
|---|---|
| Stack layer | Orchestration and Agent Layer, Infrastructure |
| Lifecycle stage(s) | Runtime and Inference |
| Applies to | Agentic |
| Exploits vulnerability | V004 Weak Prompt Isolation |
| External alignment | OWASP Top 10 for Agentic Applications; MITRE ATLAS |

Tool output manipulation is a threat vector in which attackers poison, spoof, or compromise the outputs returned from application programming interfaces, web retrieval, databases, or other enterprise tools that an AI system relies on to inform its decisions. In agentic systems specifically, malicious tool output can mislead the agent's planning process, alter what the agent believes is true and writes into memory, trigger a dangerous downstream call the attacker never had to request directly, or create an entirely false operational picture that the model then trusts as if it were ground truth. Practitioners should assess whether the system authenticates tool responses before acting on them, validates the schema of returned data, scores the trustworthiness of the source a given response came from, and structurally separates data returned by a tool from anything the system would treat as an instruction.

**What to test:** whether tool responses are authenticated, whether their schema is validated, whether source trust is scored, and whether data returned by a tool is kept structurally separate from instructions the agent might act on.

**Primary controls:** authentication and integrity checking on tool responses before they inform agent planning; schema validation rejecting malformed or unexpected tool output; structural separation between tool-returned data and anything the agent treats as an instruction.

### T043. Memory Poisoning

| Field | Value |
|---|---|
| Stack layer | Orchestration and Agent Layer |
| Lifecycle stage(s) | Runtime and Inference, Monitoring and Maintenance |
| Applies to | Agentic |
| Exploits vulnerability | V006 Weak Runtime Authorization, V004 Weak Prompt Isolation |
| External alignment | OWASP Top 10 for Agentic Applications (ASI06); MITRE ATLAS |

Memory poisoning is a threat vector in which attackers insert malicious instructions, false facts, hidden goals, or misleading context into an agent's persistent or semi-persistent memory. This is particularly dangerous compared to a single-turn prompt injection because the compromise can persist across sessions and continue to influence future actions long after the original malicious input that caused it has disappeared from the visible conversation entirely, making the root cause much harder to trace once the effect finally surfaces. Assessment should examine exactly what content can be written to memory and under what conditions, how that memory is reviewed before being trusted in a future session, how long written memory persists before expiring or being reviewed, and whether durable memory content can override policy constraints or otherwise-trusted context in a later session.

**What to test:** what can be written to memory and under what conditions, how memory content is reviewed, how long it persists, and whether durable memory can override policy or trusted context in a later session.

**Primary controls:** validation of content before it is committed to persistent memory, not only at the point it is later retrieved; expiration or periodic review of stored memory rather than indefinite retention; explicit precedence rules ensuring memory content cannot silently override system policy.

### T044. Goal Hijacking

| Field | Value |
|---|---|
| Stack layer | Orchestration and Agent Layer, Model and Inference |
| Lifecycle stage(s) | Runtime and Inference |
| Applies to | Agentic |
| Exploits vulnerability | V004 Weak Prompt Isolation, V006 Weak Runtime Authorization |
| External alignment | OWASP Top 10 for Agentic Applications (ASI01) |

Goal hijacking is a threat vector in which an attacker causes an agent to reinterpret its own objective, optimize for an attacker-favored outcome instead of its intended one, or deprioritize safety and policy constraints that were meant to bound its behavior. This can happen through direct prompt manipulation, through malicious context introduced into the agent's working environment, through shaping the environment the agent perceives so a harmful action appears operationally reasonable, or through task reframing that makes a restricted action look instrumental to accomplishing whatever broader task the agent believes it has been assigned. Assessment should test whether the system can be induced to redefine what counts as success, to pursue side effects the original task never called for, or to treat an explicitly restricted action as merely a necessary step toward a legitimate-sounding broader goal.

**What to test:** whether the system can be induced to redefine success criteria, pursue unintended side effects, or treat a restricted action as instrumentally necessary for a broader, legitimate-sounding task.

**Primary controls:** the agent's core objective and constraints enforced outside the model, in a layer the model cannot redefine through its own reasoning; independent review of any action the agent flags as instrumentally necessary but outside its normal pattern; monitoring for goal drift across a session, not only at the start of a task.

### T045. Excessive Agency Abuse

| Field | Value |
|---|---|
| Stack layer | Orchestration and Agent Layer |
| Lifecycle stage(s) | Runtime and Inference |
| Applies to | Agentic |
| Exploits vulnerability | V005 Excessive Tool Permissions, V047 Over-Automation Dependence |
| External alignment | OWASP Top 10 for LLM Applications (LLM06); OWASP Top 10 for Agentic Applications |

Excessive agency abuse is a threat vector in which a model or agent that has been granted excessive permissions or autonomy is induced to perform an action beyond its intended scope. This is a defining threat of agentic AI specifically, because the combination of autonomous planning, direct tool access, and permissive system integration together turns what would otherwise be a contained prompt-level manipulation into a real, business-impacting action path with consequences that extend well past the conversation itself. Assessment should cover whether the agent can write, delete, transact, send a message, escalate a permission, or reconfigure a system without an independent authorization or human review step standing between the model's decision and the action actually being carried out.

**What to test:** whether the agent can write, delete, transact, message, escalate permissions, or reconfigure systems without independent authorization or human review.

**Primary controls:** independent authorization required for any action in the high-impact category (financial, data-deletion, external-communication, permission-escalation); explicit action-scope definition per agent role, reviewed as part of deployment; regular audit of actions actually taken against the scope the agent was designed for.

### T046. Autonomous Action Chaining Abuse

| Field | Value |
|---|---|
| Stack layer | Orchestration and Agent Layer |
| Lifecycle stage(s) | Runtime and Inference |
| Applies to | Agentic |
| Exploits vulnerability | V005 Excessive Tool Permissions, V006 Weak Runtime Authorization |
| External alignment | OWASP Top 10 for Agentic Applications |

Autonomous action chaining abuse is a threat vector in which attackers exploit a system's ability to plan and execute a sequence of steps that are individually permitted but collectively harmful when combined. This is especially relevant in agentic AI because a multi-step plan may cross a trust boundary partway through, combine several individually benign tools into a harmful outcome none of them would produce on its own, or evade a simplistic guardrail that only inspects single actions in isolation rather than the plan as a whole. Assessment should evaluate whether the system actually reasons over the cumulative impact of a planned sequence of actions, whether business constraints are enforced across the full sequence rather than only at each individual step, and whether the system can detect an action sequence that is suspicious in aggregate even though no single step in it would have triggered a guardrail on its own.

**What to test:** whether the system reasons over cumulative impact across a planned action sequence, whether constraints are enforced across the whole sequence rather than per step, and whether a suspicious sequence can be detected even when no individual step would trigger a guardrail alone.

**Primary controls:** guardrails evaluated against the cumulative plan, not only against each individual action in isolation; a defined limit on the number and type of chained actions an agent can execute without a checkpoint; logging that preserves the full action sequence for later review, not just individual action records.

### T047. Agent Collusion

| Field | Value |
|---|---|
| Stack layer | Orchestration and Agent Layer |
| Lifecycle stage(s) | Design and Requirements, Runtime and Inference |
| Applies to | Agentic |
| Exploits vulnerability | V076 Agent Coordination Weakness |
| External alignment | OWASP Top 10 for Agentic Applications |

Agent collusion is a threat vector in which multiple AI agents coordinate, either intentionally through a deliberate attack or emergently through the normal course of their design, to manipulate decisions, bypass controls, or amplify a harmful outcome beyond what any single agent could achieve alone. This vector is especially relevant in multi-agent environments where agents can share memory, negotiate plans with one another, or delegate tasks between themselves without strong identity separation and policy enforcement governing those interactions. Practitioners should assess whether a compromised or maliciously manipulated agent can influence other agents in the system, whether the architecture allows a harmful feedback loop to form between agents, and whether unsafe actions can be distributed across multiple actors specifically to evade a detection mechanism designed around monitoring a single agent's behavior.

**What to test:** whether a compromised agent can influence other agents in the system, whether harmful feedback loops can form between agents, and whether unsafe actions can be distributed across agents to evade single-agent detection.

**Primary controls:** authenticated identity and defined trust boundaries between every agent in a multi-agent system, not implicit cooperative trust; monitoring designed at the multi-agent level, not only per individual agent; a defined containment procedure that can isolate one agent without halting the entire system.

---

## Category 8: Insider and Physical Threat Vectors

Attacks that depend on organizational access or physical proximity rather than a purely remote technical exploit.

### T026. Insider Sabotage

| Field | Value |
|---|---|
| Stack layer | Human and Organizational |
| Lifecycle stage(s) | Data Collection and Preparation, Training and Fine-Tuning, Deployment and Integration |
| Applies to | Predictive, Generative, Agentic |
| Exploits vulnerability | V001 Weak Access Control, V008 Weak Change Management |
| External alignment | NIST AI RMF, Govern function |

Insider sabotage is a threat vector in which authorized personnel intentionally degrade, corrupt, or weaponize the AI system, often by introducing dormant logic, malicious code, bad data, or a harmful operational change that is not immediately obvious as such. This vector is especially important in AI environments because developers, data scientists, and machine learning operations personnel typically have broad, legitimate access to models, datasets, prompts, and deployment pipelines as a routine part of their job, which is exactly the access an insider would need to cause deliberate harm without raising an immediate alarm. Practitioners should assess whether insider actions could implant a delayed failure that activates later, poison training data in a way that looks like an ordinary data update, change prompts in a way that is not caught by review, weaken monitoring, or suppress alerts, all without timely detection by the organization's existing controls.

**What to test:** whether an insider with normal access could implant a delayed failure, poison data under the guise of a routine update, alter prompts without triggering review, or suppress alerts without timely detection.

**Primary controls:** separation of duties so no single individual can both make a change and approve it; anomaly detection tuned to insider behavior patterns, not only external attack patterns; periodic access review that specifically questions whether current access still matches current role.

### T027. Insider Subversion

| Field | Value |
|---|---|
| Stack layer | Human and Organizational |
| Lifecycle stage(s) | Data Collection and Preparation, Training and Fine-Tuning, Deployment and Integration |
| Applies to | Predictive, Generative, Agentic |
| Exploits vulnerability | V001 Weak Access Control, V009 Weak Artifact Protection |
| External alignment | NIST AI RMF, Govern function |

Insider subversion is a threat vector in which internal personnel are bribed, coerced, recruited, or otherwise influenced to steal AI assets, leak data, or manipulate system behavior for the benefit of an external actor such as a competitor or a criminal group. This differs from general insider sabotage because the objective typically includes espionage, theft of competitive advantage, or a strategic compromise benefiting a specific external party, rather than disruption for its own sake, which changes both the likely behavior pattern to look for and the appropriate response once detected. Assessment should examine privileged access levels across the organization, the strength of separation of duties, any observed behavioral anomalies among staff with sensitive access, unusual patterns of artifact access that do not match a person's normal work, and whether sensitive model assets could realistically be exported or altered by a small number of insiders acting alone.

**What to test:** privileged access distribution, separation of duties, behavioral anomalies among staff with sensitive access, unusual artifact access patterns, and whether sensitive assets could be exported or altered by a small number of insiders.

**Primary controls:** the same access and separation-of-duties controls as insider sabotage, paired with behavioral monitoring specifically tuned for exfiltration patterns; export controls on high-value model and data artifacts requiring more than one person's approval; a confidential reporting channel for colleagues who notice concerning behavior.

### T028. Espionage Against AI Assets

| Field | Value |
|---|---|
| Stack layer | Human and Organizational, Tooling and Supply Chain |
| Lifecycle stage(s) | Training and Fine-Tuning, Validation and Testing, Deployment and Integration |
| Applies to | Predictive, Generative, Agentic |
| Exploits vulnerability | V009 Weak Artifact Protection, V064 Weak Vendor Due Diligence |
| External alignment | MITRE ATLAS, Exfiltration |

Espionage against AI assets is a threat vector in which attackers infiltrate the organization or its suppliers with the specific goal of stealing training data, model artifacts, fine-tuning sets, prompts, evaluation results, or strategic AI plans. This vector is especially important in industries where AI models provide meaningful competitive differentiation, carry national security value, or grant access to proprietary data that would be valuable to a competitor or a foreign intelligence service, since the model itself becomes as valuable a target as any traditional trade secret. Assessment should examine insider access patterns that could support quiet exfiltration over time, the range of exfiltration paths actually available from artifact repositories, exposure of data lakes to broader access than necessary, and whether an attacker could realistically study or remove high-value AI assets gradually enough to avoid detection under current monitoring.

**What to test:** exfiltration paths from artifact repositories and data lakes, and whether an attacker could gradually study or remove high-value assets without triggering current detection thresholds.

**Primary controls:** artifact access logging sensitive enough to detect gradual, low-and-slow exfiltration patterns, not only bulk transfers; classification of AI assets by competitive or strategic value to prioritize protection accordingly; supplier-side due diligence extended to cover this specific risk, not only conventional vendor security.

### T032. Physical Tampering

| Field | Value |
|---|---|
| Stack layer | Physical and Hardware |
| Lifecycle stage(s) | Deployment and Integration, Runtime and Inference |
| Applies to | Predictive |
| Exploits vulnerability | V057 Poor Hardware Assurance, V058 Weak Hardware Protection |
| External alignment | NIST AI 100-2 |

Physical tampering is a threat vector in which attackers manipulate hardware, storage media, networking equipment, edge devices, or hosting infrastructure to alter, disable, or exfiltrate an AI system component. This vector is more likely wherever the deployment model involves physical exposure: edge deployments, industrial environments, robotics, Internet of Things systems, and poorly secured data center or office environments where an unauthorized person could plausibly gain hands-on access to a device. Assessment should include hardware access controls at the physical location, exposure through removable media ports, protection of local consoles that could grant privileged access, general environmental security of the deployment site, and whether physical interference of any kind could change model behavior or reveal sensitive data stored on the device.

**What to test:** hardware access controls, removable media exposure, local console protection, environmental security, and whether physical interference could change model behavior or reveal sensitive data.

**Primary controls:** physical access controls proportional to the device's exposure and value; disabled or restricted removable media ports on deployed edge devices; environmental monitoring at deployment sites, particularly unattended ones.

### T033. Hardware Trojan Insertion

| Field | Value |
|---|---|
| Stack layer | Physical and Hardware, Tooling and Supply Chain |
| Lifecycle stage(s) | Design and Requirements, Deployment and Integration |
| Applies to | Predictive |
| Exploits vulnerability | V057 Poor Hardware Assurance |
| External alignment | NIST AI 100-2 |

Hardware Trojan insertion is a threat vector in which malicious logic or a hidden backdoor is introduced into a graphics processing unit, an accelerator, a sensor, firmware, or another hardware component used by an AI system. This vector is difficult to detect using standard security tooling and can bypass many software-layer controls entirely, since the compromise sits beneath the layer most security review actually examines, which makes it particularly concerning in high-assurance environments and in any deployment relying on a complex, global hardware supply chain the organization cannot fully audit itself. Practitioners should assess trusted hardware sourcing practices, firmware integrity verification, manufacturing provenance documentation where it is available, hardware attestation capability if the platform supports it, and any anomalous low-level behavior that might indicate an embedded compromise even without direct evidence of one.

**What to test:** hardware sourcing trust, firmware integrity verification, manufacturing provenance, hardware attestation availability, and any anomalous low-level behavior suggesting embedded compromise.

**Primary controls:** trusted, verifiable sourcing for critical AI hardware; firmware integrity verification at deployment and on a recurring schedule afterward; hardware attestation where the platform supports it, treated as a standing control rather than a one-time check at procurement.

### T034. Fault Injection

| Field | Value |
|---|---|
| Stack layer | Physical and Hardware |
| Lifecycle stage(s) | Runtime and Inference |
| Applies to | Predictive |
| Exploits vulnerability | V054 Limited Fault Tolerance, V058 Weak Hardware Protection |
| External alignment | NIST AI 100-2 |

Fault injection is a threat vector in which attackers induce errors through voltage changes, heat, clock manipulation, sensor interference, malformed inputs, or other environmental manipulation in order to cause an AI system to malfunction. This is especially relevant in embedded, edge, robotics, automotive, and industrial AI deployments, where the system depends directly on real-time sensor input or physical-state information that an attacker with local access or proximity could plausibly interfere with. Assessment should test the system's resilience to corrupted inputs of this kind, its behavior under abnormal operating conditions generally, whether a genuine fail-safe mode actually activates when it should, and specifically whether an induced fault can cause a silent misclassification rather than a visible shutdown that would at least alert an operator that something had gone wrong.

**What to test:** resilience to corrupted inputs and abnormal operating conditions, whether fail-safe behavior actually activates as designed, and whether an induced fault can cause silent misclassification rather than a visible failure.

**Primary controls:** fail-safe behavior specifically designed to surface a detectable failure rather than a silent misclassification; environmental hardening appropriate to the deployment context; fault injection testing as part of pre-deployment validation for physically exposed systems.

---

## Category 9: Supply Chain and Component Threat Vectors

Attacks that target what the organization did not build itself, or the discipline around what runs in production.

### T024. Third-Party Component Compromise

| Field | Value |
|---|---|
| Stack layer | Tooling and Supply Chain |
| Lifecycle stage(s) | Design and Requirements, Deployment and Integration, Monitoring and Maintenance |
| Applies to | Predictive, Generative, Agentic |
| Exploits vulnerability | V065 Unverified Third-Party Models, V066 Outdated Third-Party Components, V063 Black-Box Dependency Reliance |
| External alignment | OWASP Top 10 for LLM Applications (LLM03) |

Third-party component compromise is a threat vector in which attackers exploit or subvert external models, libraries, prompt frameworks, package dependencies, application programming interfaces, development tools, or model-serving components used by the AI system. This is a major vector in modern AI because most organizations assemble their systems from open-source and vendor-supplied parts rather than building every component internally, which means the organization's actual security posture depends on the security practices of every one of those upstream parts, most of which the organization has limited visibility into. Practitioners should assess whether imported models, packages, and services could introduce malware, hidden behaviors, unsafe defaults left in place from the original development, poisoned dependencies inserted somewhere upstream in the supply chain, or undisclosed data flows the organization never authorized.

**What to test:** whether imported models, packages, and services could introduce malware, hidden behaviors, unsafe defaults, poisoned dependencies, or undisclosed data flows.

**Primary controls:** dependency review and scanning as a standing part of the build process, not a one-time check at initial adoption; a software bill of materials maintained for the AI stack specifically, not just conventional application dependencies; monitoring for anomalous behavior from third-party components after they are already in production.

### T025. Parameter Tampering

| Field | Value |
|---|---|
| Stack layer | Model and Inference, Infrastructure |
| Lifecycle stage(s) | Deployment and Integration, Runtime and Inference |
| Applies to | Predictive, Generative, Agentic |
| Exploits vulnerability | V011 Unauthorized Parameter Changes, V008 Weak Change Management |
| External alignment | MITRE ATLAS |

Parameter tampering is a threat vector in which an attacker or an unauthorized insider modifies model weights, prompts, hyperparameters, temperature settings, routing logic, safety thresholds, or other decision parameters in order to alter system behavior. This vector can quietly weaken safety controls, degrade predictive accuracy, implant a hidden instruction into the system prompt, or shift model behavior in ways that are genuinely difficult to detect through ordinary operational monitoring, since a small parameter change rarely produces an obvious, single-event signal the way a code deployment failure typically does. Assessment should examine every access path to model configuration, the parameter update workflow itself, whether approval controls actually govern changes to safety-relevant parameters specifically, and whether small changes can produce a disproportionate security impact that the review process does not weight appropriately.

**What to test:** access paths to model configuration, the parameter update workflow, whether approval controls cover safety-relevant parameters specifically, and whether small changes can produce disproportionate security impact.

**Primary controls:** the same change management rigor for parameters and prompts as for code, treating both as production configuration; monitoring specifically for parameter drift, not only for output-quality drift; a documented list of safety-relevant parameters requiring elevated approval before any change.

### T035. Neglected Patching Exploitation

| Field | Value |
|---|---|
| Stack layer | Infrastructure, Tooling and Supply Chain |
| Lifecycle stage(s) | Monitoring and Maintenance |
| Applies to | Predictive, Generative, Agentic |
| Exploits vulnerability | V066 Outdated Third-Party Components |
| External alignment | Common Vulnerabilities and Exposures program; OWASP Top 10 for LLM Applications (LLM03) |

Neglected patching exploitation is a threat vector in which attackers take advantage of unpatched frameworks, runtimes, libraries, model-serving components, notebooks, operating systems, and other infrastructure supporting AI workflows. This is a standard cybersecurity vector in general, but it carries particular weight in AI specifically because AI ecosystems often depend on fast-moving open-source packages and complex graphics processing unit or container stacks with dependency chains deeper and more tangled than a typical application stack, which makes tracking and applying patches materially harder. Assessment should include measuring patch latency against known release timelines, identifying unsupported components still in use, checking for exposed known vulnerabilities in machine learning tooling specifically, evaluating upgrade discipline across teams, and determining whether security updates are being blocked by concerns about breaking a fragile model pipeline that nobody wants to risk destabilizing.

**What to test:** patch latency, unsupported components still in use, exposed known vulnerabilities in machine learning tooling specifically, and whether security updates are being deferred out of concern for breaking a fragile pipeline.

**Primary controls:** dependency scanning integrated into the AI-specific build process, separate from general application scanning that may miss ML-specific tooling; a defined patch cadence with an explicit, time-boxed exception process rather than indefinite deferral; regression testing robust enough that patching is not perceived as a high-risk activity.

---

## Category 10: Availability Threat Vectors

Attacks that target uptime or operating cost rather than confidentiality or integrity.

### T049. Denial of Service / Denial of Wallet

| Field | Value |
|---|---|
| Stack layer | Infrastructure, Model and Inference |
| Lifecycle stage(s) | Runtime and Inference |
| Applies to | Predictive, Generative, Agentic |
| Exploits vulnerability | V003 Unrestricted Query Access, V032 Insufficient Resource Monitoring, V055 Excessive Compute Demand |
| External alignment | OWASP Top 10 for LLM Applications (LLM10) |

Denial of service is a threat vector in which attackers exhaust the compute, token, memory, concurrency, storage, or budget resources of an AI system, reducing its availability or sharply increasing its operating cost without necessarily taking it fully offline. This vector is increasingly important in generative and agentic systems specifically, because attackers can craft inputs that maximize token generation, trigger long tool-calling chains in an agent, or force worst-case inference behavior without needing a very high volume of traffic; a small number of well-crafted requests can be far more damaging than a large volume of ordinary ones. Assessment should evaluate flood resistance under realistic attack traffic, concurrency control across sessions, whether token budgets are enforced per session, whether tool-calling loops have a defined limit, whether spend alerts fire in time to matter, and whether the system degrades gracefully rather than catastrophically under genuinely abusive demand.

**What to test:** flood resistance, concurrency control, per-session token budget enforcement, tool-calling loop limits, spend alert timeliness, and graceful degradation under abusive demand.

**Primary controls:** per-session token and tool-call budgets enforced at the orchestration layer, not only at the API gateway; circuit breakers for runaway agent loops specifically, since these are the costliest failure mode in agentic systems; cost-spike alerting independent of and faster than standard infrastructure alerting.

---

## Cross-reference

Every entry in this guide corresponds to an id in `data/threat_vectors.yaml`, which remains the source to use for filtering, scripting, and generating a scoped checklist with `tools/generate_checklist.py`. Update both files, and `docs/07-vulnerability-guide.md` where the vulnerability mapping changes, together; see `CONTRIBUTING.md`.
