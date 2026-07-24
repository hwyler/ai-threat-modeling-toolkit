# Source Alignment

This catalog is meant to sit alongside the maintained frameworks below, not replace them. Where this toolkit references a framework by name in `data/threat_vectors.yaml`, treat that as a pointer to check the source directly; version numbers and specific technique identifiers in this space change frequently enough that hardcoding them here would go stale. This page was checked against current public sources as of mid-2026 and should be re-verified periodically, since every framework listed here is under active revision.

## MITRE ATLAS

MITRE ATLAS (Adversarial Threat Landscape for Artificial-Intelligence Systems) is a living, community-maintained knowledge base of adversary tactics and techniques against AI and machine learning systems, structured the same way as MITRE ATT&CK: tactics, techniques and sub-techniques, mitigations, and real-world case studies. As of the early-2026 releases it documents roughly sixteen tactics and in the range of eighty or more techniques, a figure that has grown substantially over the past year as the framework added dedicated coverage for agentic AI attack patterns, including context and memory poisoning, agent configuration tampering, and tool-invocation abuse. Because the exact counts shift release to release, cite the ATLAS site directly (atlas.mitre.org) rather than a fixed number when precision matters. This toolkit uses ATLAS primarily for tactic-level grounding of the vulnerability and threat vector categories, particularly Spoofing, Tampering, and the credential and exfiltration-adjacent threat vectors.

## OWASP Top 10 for LLM Applications

Maintained by the OWASP GenAI Security Project, the current edition (2025) lists ten risks numbered LLM01 through LLM10, covering prompt injection, sensitive information disclosure, supply chain, data and model poisoning, improper output handling, excessive agency, system prompt leakage, vector and embedding weaknesses, misinformation, and unbounded consumption. This toolkit's generative-AI priority list draws directly from this ordering, and the cross-reference field in `data/threat_vectors.yaml` cites the relevant LLM0x number where the mapping is direct.

## OWASP Top 10 for Agentic Applications

Released in December 2025 by the same project, this is a separate, newer list (ASI01 through ASI10) purpose-built for autonomous, tool-using agents rather than single-turn LLM applications. It covers agent goal hijacking, tool misuse, identity and privilege abuse, agentic supply chain compromise, unexpected code execution, and memory and context poisoning, among others. This toolkit's agentic-AI priority list and the multi-agent vulnerability category are aligned to this framework. Teams assessing an agentic system should treat the LLM Top 10 as a floor and this list as the layer specific to autonomy.

## NIST AI 100-2

NIST's taxonomy of adversarial machine learning attacks, organized by lifecycle stage (training-time, deployment-time) and by attacker objective (availability, integrity, privacy). This toolkit's predictive-AI priority list, and the data-poisoning, evasion, and privacy-attack entries in `data/threat_vectors.yaml`, are grounded in this taxonomy's structure.

## NIST AI Risk Management Framework

A voluntary framework organized around four functions: Govern, Map, Measure, and Manage. The six-phase methodology in `docs/01-methodology.md` follows this structure loosely, with Phase 1 and Phase 6 corresponding to Govern, Phase 2 and Phase 3 to Map, Phase 4 to Measure, and Phase 5 and Phase 6 to Manage.

## ISO/IEC 42001

The international standard for AI management systems, used here as the basis for treating an AI security assessment as a recurring, governed process rather than a one-time test, and for the governance and accountability vulnerability category.

## How to keep this page current

- Re-check the ATLAS technique count and the current OWASP list numbering at least twice a year; both frameworks have shipped major updates within months of each other recently.
- When a cross-reference in `data/threat_vectors.yaml` cites a specific numbered item (an LLMxx or ASIxx code), verify the number against the current published list before publishing a new release of this toolkit, since numbering has changed between editions.
- Log any correction as a pull request against this file and the corresponding YAML entry together, so the narrative and machine-readable versions never drift apart.
