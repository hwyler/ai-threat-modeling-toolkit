Assessment Methodology
This toolkit follows a six-phase process aligned with the NIST AI Risk Management Framework (Govern, Map, Measure, Manage) and ISO/IEC 42001's requirements for an AI management system. The phases are sequential the first time you run an assessment and cyclical after that; Phase 6 findings feed back into Phase 3 on a regular cadence.
Phase 1: Define scope and classification
Before touching a checklist, answer two questions:
System type: predictive (classification, scoring, forecasting), generative (produces text, images, code, or other content), or agentic (plans, calls tools, and takes action with limited human review). A single product can combine more than one type; assess each component separately.
Sourcing model: built in-house, procured as a vendor product, or a hybrid such as a fine-tuned foundation model. Sourcing changes which controls you can inspect directly and which you must obtain through vendor due diligence.
Write measurable success criteria at this stage. "No personally identifiable information in outputs" and "prompt injection bypass rate under a defined threshold" can be tested. "Make the system secure" cannot. Document risk tolerance and who signs off on residual risk.
Phase 2: Inventory assets and data flows
Catalog every component that touches AI data or artifacts: models, datasets, feature pipelines, training and inference infrastructure, prompt templates, retrieval corpora, tool integrations, and third-party APIs. Record metadata for each: data lineage, model version, training configuration, deployment endpoint, and access controls.
This is the phase where most assessments fall short. Teams commonly inventory the model and the API endpoint, then miss the feature store, the retrieval corpus, the prompt templates, the tool configurations, and the monitoring stack. Each of these is a distinct asset with its own threat profile. Use `templates/asset_inventory.md` and trace every data flow from source through processing, training, deployment, inference, and monitoring. If you cannot draw the complete data flow diagram, the assessment is not ready for Phase 3.
Phase 3: Threat mapping and vulnerability analysis
Apply the STRIDE-AI mapping in `docs/02-stride-ai.md` to each asset from Phase 2. Cross-reference against MITRE ATLAS for attack patterns specific to your system type, and pull the relevant priority list from `data/threat_vectors.yaml` (filter by `applies_to: predictive | generative | agentic`). Build scenario-based descriptions for the threats with the highest plausible business impact rather than trying to narrate all of them in equal depth.
Phase 4: Testing and validation
Test against the specific threats identified in Phase 3, not against a generic list. Typical test categories:
Adversarial and evasion testing for predictive systems
Prompt injection and jailbreak testing for generative and agentic systems
Data integrity and provenance checks across the pipeline
Privacy leakage testing (membership inference, model inversion, training data extraction)
Agent behavior testing: tool misuse, goal drift, memory poisoning, multi-step action chains
Abuse and rate-limit resistance testing
Combine automated tooling with manual testing. Automated scanners catch known patterns; manual testing catches the business-logic failures that are specific to your use case.
Phase 5: Risk scoring and prioritization
Score each finding on likelihood and impact using `templates/risk_register.csv`, and adjust for AI-specific factors: how easily the flaw can be triggered by an unauthenticated user, whether it requires a single query or a sustained campaign, and what downstream action or disclosure results. Teams with a more mature program should consider the OWASP AI Vulnerability Scoring System, which was designed specifically for AI risk including agentic systems, in place of the simplified matrix included here.
Phase 6: Mitigation and continuous monitoring
Implement layered controls matched to the finding: access control, input validation, rate limiting, adversarial training, differential privacy, output filtering, structured logging, and human approval gates for high-risk actions. Set up ongoing monitoring for performance drift, anomalous behavior, and security signals, and route findings from monitoring back into Phase 3 on a defined schedule rather than waiting for the next full assessment cycle.
Built versus bought: what changes
	Built in-house	Procured or fine-tuned
Training data inspection	Direct access, full lineage tracing possible	Limited to vendor disclosures and model cards
Testing depth	Full adversarial and data-level testing	API-level and output-level testing only, unless the vendor provides a sandbox
Change control	Enforced internally	Dependent on vendor's release process and notice period
Primary controls	Data governance, training pipeline security, model validation	Vendor due diligence, contract terms, output filtering, monitoring
Procured systems shift the assessment's center of gravity from Phase 2 and Phase 4 toward vendor due diligence and contractual controls. See the third-party vulnerability category in `data/vulnerabilities.yaml` for the specific items to check.
