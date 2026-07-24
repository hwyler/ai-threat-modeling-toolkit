# Threat Vector Catalog: Narrative Summary

This is the readable companion to `data/threat_vectors.yaml`. It groups the 49 cataloged threat vectors by the AI system type they matter most for. A threat vector marked for more than one type applies to both; assess it once per system, scoped to that system's actual architecture.

## Highest priority for generative AI

Prompt injection and its indirect variant (malicious instructions arriving through a retrieved document, a webpage, or an email rather than typed directly) are the two vectors that show up first in almost every generative AI assessment. Behind them: hallucination exploitation and toxicity induction, both of which can cause real business harm even without a determined attacker; sensitive data extraction and RAG corpus poisoning, which target the retrieval layer specifically; API abuse and model extraction via queries, which target the interface; unsafe content repurposing, which turns the model into a tool for downstream fraud or social engineering; and overreliance, which is less a technical flaw than a business process weakness that determined attackers routinely exploit.

## Highest priority for agentic AI

Agentic systems inherit every generative AI vector and add a layer specific to autonomy: unauthorized tool use and excessive agency abuse, where a successful manipulation stops being a bad answer and becomes a real action; goal hijacking, where the agent's objective itself is redefined; memory poisoning, which can persist a compromise across sessions long after the original malicious input is gone; tool output manipulation, which misleads an agent's planning through a poisoned API or database response rather than through the model directly; autonomous action chaining abuse, where individually permitted steps combine into a harmful sequence; agent collusion in multi-agent environments; API token compromise, which is especially damaging when the compromised credential belongs to an agent with broad tool access; and denial of service through resource or budget exhaustion, which is cheaper to trigger in an agent that can be induced into long tool-calling loops.

## Highest priority for predictive AI

Predictive systems, the classification, scoring, and forecasting models most organizations have run for years, face a different set of priorities: data poisoning and label poisoning at the training stage; backdoor injection, which can pass standard validation while containing latent malicious behavior; adversarial evasion at inference time, common in fraud detection, vision, and malware classification; model inversion and membership inference, both privacy attacks that reconstruct or confirm sensitive training data; gradient leakage in federated or distributed training; bias exploitation through imbalanced data; and two vectors that concern reliability under changing conditions, model drift exploitation and generalization failure exploitation, which take advantage of periods when the model is poorly calibrated to current data.

## Cross-cutting vectors

Several vectors are not specific to one AI type and deserve attention regardless of system classification: third-party component compromise and neglected patching exploitation, both supply-chain risks; API abuse and API token compromise, which target the interface layer common to every deployment; sensitive data extraction, which applies wherever the system handles regulated or proprietary data; insider sabotage and insider subversion, which depend on organizational access controls rather than model architecture; espionage against AI assets and physical tampering, most relevant to high-value models and edge deployments; and shadow AI use, an organizational risk that predates any specific technical vulnerability.

## Using the priority lists

`data/threat_vectors.yaml` includes machine-readable priority lists (`predictive_priority`, `generative_priority`, `agentic_priority`, `cross_cutting_priority`) that mirror the groupings above. Run `tools/generate_checklist.py --system-type <type>` to pull the matching subset into a checklist rather than copying ids by hand.
