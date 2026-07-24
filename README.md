AI Threat Modeling and Vulnerability Assessment Toolkit
An open-source, framework-aligned toolkit for assessing security vulnerabilities and mapping threat vectors across predictive, generative, and agentic AI systems. Built for AI architects, security engineers, risk managers, and chief AI officers who need a repeatable way to move from a generic security checklist to a threat model that matches the actual system in front of them.
Traditional application security controls cover the software wrapper around an AI system: the API, the infrastructure, the identity layer. They do not cover the parts that make AI systems different: training data, learned parameters, retrieval corpora, prompts, and, in agentic systems, autonomous planning and tool use. This toolkit closes that gap with a structured catalog of vulnerabilities and threat vectors, a STRIDE adaptation for AI, and templates you can use in an actual assessment.

Why this exists
Most AI security assessments still run on general-purpose checklists borrowed from traditional application security. That approach misses the attack surface that is unique to machine learning: poisoned training data, prompt injection through retrieved content, model extraction through API queries, and tool misuse in autonomous agents. This toolkit gives teams a single, versioned reference that:
Classifies vulnerabilities and threat vectors by AI system type (predictive, generative, agentic), because a fraud model, a RAG chatbot, and an autonomous agent do not share the same risk profile.
Maps each item to public, maintained frameworks (MITRE ATLAS, the OWASP Top 10 for LLM Applications, the OWASP Top 10 for Agentic Applications, NIST AI 100-2, and the NIST AI Risk Management Framework) so the catalog stays anchored to community consensus rather than one team's opinion.
Ships as structured data (YAML), not just prose, so it can be filtered, scored, and dropped into a risk register or a red-team test plan.

Repository structure
```
ai-threat-modeling-toolkit/
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── docs/
│   ├── 01-methodology.md          Six-phase assessment process
│   ├── 02-stride-ai.md            STRIDE adapted for AI trust boundaries
│   ├── 03-vulnerability-catalog.md  Narrative version of the vulnerability catalog
│   ├── 04-threat-vector-catalog.md  Narrative version of the threat vector catalog
│   ├── 05-threat-modeling-guide.md  How to build a model per AI system type, with a worked example
│   └── 06-source-alignment.md     Cross-reference table to MITRE ATLAS, OWASP, NIST, ISO
├── data/
│   ├── vulnerabilities.yaml       Machine-readable vulnerability catalog
│   ├── threat_vectors.yaml        Machine-readable threat vector catalog
│   └── stride_ai_mapping.yaml     STRIDE category to threat vector mapping
├── templates/
│   ├── asset_inventory.md
│   ├── risk_register.csv
│   └── assessment_report.md
└── tools/
    └── generate_checklist.py      Command-line filter: system type in, scoped checklist out

```
Quick start
Classify your system. Every assessment starts by answering two questions: what type of AI system is this (predictive, generative, or agentic), and was it built in-house or procured from a vendor. See `docs/01-methodology.md`, Phase 1.
Build the asset inventory using `templates/asset_inventory.md`. Most assessments fail here, not in the testing phase, because teams catalog the model and the endpoint and miss the training pipeline, the retrieval corpus, the prompt templates, and the tool permissions.
Generate a scoped checklist:
```bash
   python tools/generate_checklist.py --system-type agentic --sourcing built
   ```

This filters `data/vulnerabilities.yaml` and `data/threat_vectors.yaml` down to the items relevant to your system type and prints a markdown checklist you can paste into your assessment report.
Walk the STRIDE-AI mapping in `docs/02-stride-ai.md` against your architecture diagram, asset by asset.
Score findings and log them in `templates/risk_register.csv`.
Write up the assessment using `templates/assessment_report.md`.
Scope: what this toolkit covers
60-plus AI-specific vulnerabilities (control weaknesses), grouped into technical, data, model, operational, third-party, governance, resilience, and physical categories.
45-plus AI-specific threat vectors (attack paths), each tagged with which AI system type it applies to most.
A STRIDE-AI mapping that shows how classic Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, and Elevation of Privilege categories translate into AI-specific failure modes.
Priority lists for predictive, generative, and agentic systems, so a team assessing a fraud model is not handed the same checklist as a team assessing a customer support agent.
What this toolkit does not do
It does not replace a penetration test, a red-team engagement, or legal review. It is a structured starting point for scoping and prioritizing that work. Risk scoring in `templates/risk_register.csv` uses a simple likelihood-impact model; teams with more mature programs should substitute the OWASP AI Vulnerability Scoring System or an internal equivalent.

Framework alignment
This catalog is cross-referenced, not duplicated, against the following maintained sources. Always check the source for the current version; frameworks in this space change often.

Framework	Maintainer	What it contributes here
MITRE ATLAS	MITRE Corporation	Tactic and technique taxonomy for adversarial attacks on AI and ML systems
OWASP Top 10 for LLM Applications	OWASP GenAI Security Project	Prioritized risk list for generative AI applications
OWASP Top 10 for Agentic Applications	OWASP GenAI Security Project	Prioritized risk list for autonomous, tool-using agents
NIST AI 100-2	NIST	Taxonomy of adversarial machine learning attacks by lifecycle stage
NIST AI Risk Management Framework	NIST	Lifecycle governance structure (Govern, Map, Measure, Manage)
ISO/IEC 42001	ISO/IEC	AI management system requirements used for the six-phase process
See `docs/06-source-alignment.md` for the full cross-reference table with specific mappings.
Contributing
Threat vectors and vulnerabilities in AI systems change faster than most catalogs can track. See `CONTRIBUTING.md` for how to propose a new entry, update a mapping, or correct a citation. Every new entry needs at minimum a plain-language description and a mapped AI system type; a citation to a maintained framework is strongly preferred over an uncited addition.

Disclaimer
This catalog is a starting framework for structuring an AI security assessment. It is not a substitute for a full assessment performed by qualified security and AI governance professionals, and it carries no warranty of completeness or fitness for a specific regulatory requirement. New AI attack techniques are documented on a rolling basis. Treat this repository as a living document and revalidate it against current sources on the cadence described in CONTRIBUTING.md.

About
Maintained by Hernan Huwyler, Senior Manager of AI Governance and Digital Compliance and Executive Professor of AI governance and quantitative risk management. Built for the AI architects, data scientists, and risk professionals who need a practical bridge between an AI vulnerability and an auditable control, not another slide deck.

License
Code is released under the MIT License. Catalog content and documentation are released under CC BY 4.0. See LICENSE for both.
