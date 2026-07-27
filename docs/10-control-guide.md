# ISO/IEC 42001 Control Guidance

ISO/IEC 42001 gives an organization the management-system scaffolding for AI: policy, accountability, resourcing, impact assessment, lifecycle discipline, data governance, transparency, responsible use, and third-party management. What it does not give you is the wiring between a control and the specific technical weakness that control is supposed to close. That wiring is what this file adds.

Each entry below restates the control's objective, description, and implementation guidance from the standard in plain language, then links it forward to the specific vulnerability IDs in `docs/07-vulnerability-guide.md` that the control most directly addresses. Use it in three ways: to answer "which ISO 42001 clause covers this gap" when you are writing Section 5 (Existing Control Mapping) of `docs/09-threat-model-report-template.md`; to answer "which vulnerabilities does this control actually reduce" when you are building an audit or certification narrative; and to spot a vulnerability with no corresponding control listed here, which is itself a finding worth raising.

**A note on numbering.** Control IDs (A.2.2, A.3.2, and so on) follow ISO/IEC 42001:2023 Annex A exactly. This file paraphrases the standard's language for readability and does not reproduce it verbatim; treat this as a working companion to the standard, not a substitute for reading the published text, particularly for certification or audit purposes where the exact wording matters.

## How to read each entry

- **Objective** — the outcome the control area exists to achieve, as stated in Annex A.
- **Control description** — what the standard requires the organization to do, restated plainly.
- **Implementation guidance** — the practical steps Annex A points to, condensed to what a team actually needs to act on.
- **Linked vulnerabilities** — the ids from `data/vulnerabilities.yaml` and `docs/07-vulnerability-guide.md` this control most directly mitigates when implemented well, and most directly exposes the organization to when missing or weak.

---

## Area A.2: Policies related to AI

**Objective:** provide management direction and support for AI systems according to business requirements.

### A.2.2 AI policy

**Control description:** the organization must document a policy for the development or use of AI systems.

**Implementation guidance:** build the policy on the organization's actual business strategy, its risk appetite, and the legal requirements it operates under, not on a generic industry template. State the principles that will guide every AI-related activity across the organization, including how deviations and exceptions to the policy get handled, since a policy with no exception process tends to get quietly ignored the first time it is inconvenient. Where a topic needs more depth than the policy itself can carry, cross-reference a topic-specific policy rather than trying to fit everything into one document; common examples are AI resources and assets, impact assessments, and system development practices. The policy should guide every stage where AI touches the organization: development, purchase, operation, and use, not only in-house builds.

**Linked vulnerabilities:** V035 Missing AI Policies, V040 Weak Intended Use Controls, V041 Weak Requirements Definition, V043 Misaligned Business Objectives.

### A.2.3 Alignment with other organizational policies

**Control description:** the organization must determine where other existing policies are affected by, or apply to, its AI objectives.

**Implementation guidance:** AI cuts across domains the organization already has policy for, most obviously quality, security, safety, and privacy. Run a deliberate analysis of where those existing policies intersect with AI-specific risk, then either update the existing policy to cover the AI-specific case or add a provision to the AI policy itself, whichever keeps the two consistent. The governing body's own policies should inform the AI policy, not sit alongside it as a disconnected parallel structure; ISO/IEC 38507 gives governing-body-level guidance on this if your organization needs it.

**Linked vulnerabilities:** V035 Missing AI Policies, V015 Weak Data Governance, V064 Weak Vendor Due Diligence.

### A.2.4 Review of the AI policy

**Control description:** the AI policy must be reviewed at planned intervals, and additionally whenever needed, to confirm it is still suitable, adequate, and effective.

**Implementation guidance:** assign a management-approved role to own the policy's development, review, and evaluation, so the review is not left to whoever happens to remember. Reviews should specifically look for improvement opportunities driven by a changed organizational environment, new business circumstances, a legal change, or a shift in the technical landscape, and should incorporate whatever management review already surfaced rather than duplicating that work separately.

**Linked vulnerabilities:** V035 Missing AI Policies, V042 Weak Planning Discipline, V031 Weak Performance Auditing.

---

## Area A.3: Internal organization

**Objective:** establish accountability within the organization to uphold its responsible approach to the implementation, operation, and management of AI systems.

### A.3.2 AI roles and responsibilities

**Control description:** roles and responsibilities for AI must be defined and allocated according to the organization's needs.

**Implementation guidance:** derive the role assignments from the AI policy, the organization's AI objectives, and its already-identified risks, so coverage actually maps to where risk concentrates rather than to whoever happened to be available. Prioritize assigning ownership for risk management, impact assessments, asset and resource management, security, safety, privacy, development, performance, human oversight, supplier relationships, legal compliance capability, and data quality management across the full lifecycle. Define each role's responsibilities to the depth the person holding it actually needs to do the job, not at a level so abstract it cannot guide a real decision.

**Linked vulnerabilities:** V036 Undefined AI Roles, V001 Weak Access Control, V026 Weak Feedback Loops.

### A.3.3 Reporting of concerns

**Control description:** the organization must define and operate a process for reporting concerns about its role with respect to an AI system throughout its life cycle.

**Implementation guidance:** the reporting mechanism needs to offer confidentiality or anonymity, be actively promoted to every employee and contractor rather than merely existing, be staffed by people with real investigation and resolution authority, provide an escalation path to management with a defined timeliness expectation, and protect reporters from reprisal. Existing reporting mechanisms elsewhere in the organization can be extended to cover AI concerns rather than building a parallel channel from scratch. ISO 37002 offers further guidance on whistleblowing management systems if the organization wants to go deeper here.

**Linked vulnerabilities:** V034 Missing Reporting Channels, V046 Unknown Customer Expectations.

---

## Area A.4: Resources for AI systems

**Objective:** ensure the organization accounts for the resources of the AI system, including its components and assets, so it can fully understand and address risks and impacts.

### A.4.2 Resource documentation

**Control description:** the organization must identify and document the resources required for each relevant AI system life cycle stage and for other AI-related activities.

**Implementation guidance:** document resources across every category that matters: AI system components, data resources, tooling resources, system and computing resources, and human resources, regardless of whether the organization provides those resources itself or receives them from a customer or a third party. Data flow diagrams and system architecture diagrams are useful documentation formats here, and this documentation is exactly what later feeds the impact assessment work in Area A.5. If documenting resources reveals a resource genuinely is not available, treat that as a signal to revise the system's design specification or its deployment requirements, not as something to work around silently.

**Linked vulnerabilities:** V037 Lack of Design Documentation, V074 Poor Resource Documentation, V075 Poor Tooling Documentation, V048 Complex Architecture Sprawl.

### A.4.3 Data resources

**Control description:** as part of resource identification, the organization must document information about the data resources used for the AI system.

**Implementation guidance:** cover provenance, the date data was last updated, the category of data (training, validation, test, production), the labeling process, the data's intended use, its quality, applicable retention and disposal policies, and any known or potential bias issues, along with how the data was prepared before use. Treat this documentation as a living record that gets updated as data resources change, not a one-time exercise completed at project kickoff.

**Linked vulnerabilities:** V013 Insufficient Provenance Controls, V016 Weak Data Quality Controls, V022 Weak De-Identification, V014 Data Poisoning Susceptibility.

### A.4.4 Tooling resources

**Control description:** as part of resource identification, the organization must document information about the tooling resources used for the AI system.

**Implementation guidance:** cover the algorithm types and machine learning models in use, data conditioning tools and processes, optimization methods, evaluation methods, provisioning tools, model development aids, and the software and hardware used across design, development, and deployment. ISO/IEC 23053 has detailed guidance on the specific types and methods of machine learning tooling if a deeper reference is needed.

**Linked vulnerabilities:** V075 Poor Tooling Documentation, V063 Black-Box Dependency Reliance, V010 Complex Model Loading.

### A.4.5 System and computing resources

**Control description:** as part of resource identification, the organization must document information about the system and computing resources used for the AI system.

**Implementation guidance:** document the AI system's actual resource requirements, where its system and computing resources are located (on-premises, cloud, or edge), the processing resources involved including network and storage, and the environmental impact of the hardware the workload runs on. Recognize explicitly that development, deployment, and operation can each demand different resources, and document each stage's needs rather than assuming a single resource profile covers the whole lifecycle. ISO/IEC 25029 covers system resource considerations in more depth.

**Linked vulnerabilities:** V048 Complex Architecture Sprawl, V055 Excessive Compute Demand, V056 Edge Capacity Weakness, V049 Single Point of Failure.

### A.4.6 Human resources

**Control description:** as part of resource identification, the organization must document information about the human resources and their competencies needed for developing, deploying, operating, changing, maintaining, transferring, decommissioning, verifying, and integrating the AI system.

**Implementation guidance:** think explicitly about the diversity of expertise a given system needs, not just headcount: data scientists, human-oversight roles, trustworthiness specialists covering safety, security, and privacy, and domain experts relevant to the specific AI application. Different life cycle stages will require different resources; a system in active development needs a different mix of people than the same system three years into stable operation.

**Linked vulnerabilities:** V036 Undefined AI Roles, V001 Weak Access Control, V027 Missing Drift Controls (through inadequate operational staffing).

---

## Area A.5: Assessing impacts of AI systems

**Objective:** assess the impacts an AI system can have on individuals, groups of individuals, and societies throughout its life cycle.

### A.5.2 AI system impact assessment process

**Control description:** the organization must establish a process to assess the potential consequences for individuals, groups of individuals, and societies that can result from the AI system throughout its life cycle.

**Implementation guidance:** define what triggers an impact assessment (the criticality of the system's intended purpose, the complexity of the AI technology and its level of automation, and the sensitivity of the data types involved, or a significant change to any of these), and build the process around identification, analysis, evaluation, treatment, and documentation of the consequences you find. Decide explicitly who performs the assessment and how its results actually get used, whether that is informing system design, triggering a review, or requiring an approval before proceeding. ISO/IEC 23894 describes how to fold this kind of impact analysis into a broader organizational risk management process rather than running it as an isolated exercise.

**Linked vulnerabilities:** V044 Weak Human Rights Assessment, V038 Weak Explainability Controls, V043 Misaligned Business Objectives.

### A.5.3 Documentation of AI system impact assessments

**Control description:** the organization must document the results of AI system impact assessments and retain them for a defined period.

**Implementation guidance:** capture the system's intended use and any reasonably foreseeable misuse, the positive and negative impacts on affected individuals and societies, predictable failure modes and the measures taken to mitigate them, the demographic groups the system applies to, the system's complexity, and the role humans play in overseeing it. Set a retention period informed by the organization's own retention schedule or by applicable legal requirements, and keep the documentation current as the system or its context changes rather than treating it as a point-in-time artifact.

**Linked vulnerabilities:** V037 Lack of Design Documentation, V044 Weak Human Rights Assessment, V030 Weak Event Traceability.

### A.5.4 Assessing AI system impact on individuals or groups of individuals

**Control description:** the organization must assess and document the AI system's potential impacts on individuals or groups of individuals throughout its life cycle.

**Implementation guidance:** ground this assessment in the organization's governance principles, its AI policy, and its objectives, and pay specific attention to groups with distinct protection needs, such as children, people with disabilities, older adults, and workers. Cover fairness, accountability, transparency and explainability, security and privacy, safety and health, financial consequences, accessibility, and human rights as the areas of impact to evaluate, and bring in outside expertise, researchers, subject matter specialists, or actual users, when the internal team cannot fully characterize a potential impact on its own.

**Linked vulnerabilities:** V044 Weak Human Rights Assessment, V016 Weak Data Quality Controls (as a driver of unfair outcomes), V038 Weak Explainability Controls.

### A.5.5 Assessing societal impacts of AI systems

**Control description:** the organization must assess and document the AI system's potential societal impacts throughout its life cycle.

**Implementation guidance:** consider environmental sustainability, economic effects (access to financial services, employment, trade), effects on government processes and national security, health and safety, and effects on norms, traditions, culture, and values, both the harms an AI system can create and the harms it can help address. Give explicit thought to how the system could be misused and whether it risks reinforcing a historical societal harm rather than assuming good intent at design time guarantees a good outcome in deployment. ISO/IEC TR 24368 gives a useful high-level overview of the ethical and societal concerns at play here.

**Linked vulnerabilities:** V044 Weak Human Rights Assessment, V017 Distributed Data Inconsistency (as a driver of inconsistent societal outcomes across regions), V043 Misaligned Business Objectives.

---

## Area A.6: AI system life cycle

**Objective:** ensure the organization identifies and documents objectives and implements processes for the responsible design and development of AI systems, and defines criteria and requirements for each life cycle stage.

### A.6.1.2 Objectives for responsible development of AI system

**Control description:** the organization must identify and document objectives to guide the responsible development of AI systems and integrate measures to achieve those objectives throughout the development life cycle.

**Implementation guidance:** decide what "responsible development" concretely means for this system before development starts, then build measures into the life cycle that actually pursue those objectives rather than treating them as a preamble nobody revisits. Consider explicitly how AI techniques can be used to reinforce the security of the AI system itself and of the conventional software around it, since this is one area where AI capability and AI risk management genuinely reinforce each other rather than trading off.

**Linked vulnerabilities:** V041 Weak Requirements Definition, V025 Insufficient Model Validation, V008 Weak Change Management.

### A.6.1.3 Processes for responsible AI system design and development

**Control description:** the organization must define and document the specific processes for the responsible design and development of the AI system.

**Implementation guidance:** cover life cycle stages, testing requirements and how testing will actually be performed, human oversight requirements especially where the system can affect people directly, the points at which an impact assessment should run, expectations and rules for training data including which sources are approved, the expertise developers need or should be trained in, release criteria, required approvals and sign-offs, change control, usability and controllability, and how interested parties get engaged. Tailor the specific process to the actual technology and functionality in play; a generic process written for one AI technique will not fit every system the organization builds.

**Linked vulnerabilities:** V008 Weak Change Management, V025 Insufficient Model Validation, V042 Weak Planning Discipline.

### A.6.2.2 AI system requirements and specification

**Control description:** the organization must specify and document requirements for new AI systems or material enhancements to existing ones.

**Implementation guidance:** document why the system is being built at all, whether that is a business case, a customer request, or a policy driver, and how the model will be trained and what data requirements that implies. Requirements need to span the entire life cycle, not just the initial build, and should be revisited whenever the system cannot operate as intended or new information changes what is feasible, including the possibility that continuing development stops making financial sense.

**Linked vulnerabilities:** V041 Weak Requirements Definition, V043 Misaligned Business Objectives.

### A.6.2.3 Documentation of AI system design and development

**Control description:** the organization must document the AI system's design and development based on its organizational objectives, documented requirements, and specification criteria.

**Implementation guidance:** capture the machine learning approach, the learning algorithm and model type, how the model is trained and to what data quality standard, how the model is evaluated and refined, the hardware and software components involved, the security threats considered throughout the life cycle (data poisoning, model stealing, and model inversion are the ones the standard names explicitly), the interface and output presentation, how humans interact with the system, and interoperability and portability considerations. Design and development typically iterate several times; maintain documentation through those iterations and ensure a final, accurate system architecture document exists once the design stabilizes.

**Linked vulnerabilities:** V037 Lack of Design Documentation, V009 Weak Artifact Protection, V014 Data Poisoning Susceptibility, V008 Weak Change Management.

### A.6.2.4 AI system verification and validation

**Control description:** the organization must define and document verification and validation measures for the AI system and specify the criteria for their use.

**Implementation guidance:** define the testing methodologies and tools, how test data is selected and how representative it is of the real domain of use, and the release criteria the system must pass. Build an evaluation plan around reliability and safety requirements including acceptable error rates, the responsible-AI objectives set earlier in Area A.6, operational factors like data quality and intended use, and the methods used to judge whether the people relying on the system's output can actually interpret it. Document what happens when the system cannot meet its evaluation criteria, especially against responsible-AI objectives, rather than only documenting the plan for when it does.

**Linked vulnerabilities:** V025 Insufficient Model Validation, V024 Weak Transfer Validation, V007 (from the threat guide, Adversarial Evasion, tested here at validation time).

### A.6.2.5 AI system deployment

**Control description:** the organization must document a deployment plan and confirm that appropriate requirements are met before deployment.

**Implementation guidance:** account for the possibility that a system is developed in one environment and deployed in another, and that components (software and model, for instance) may deploy independently of each other. Define release criteria that must be satisfied before release: verification and validation results, performance metrics, completed user testing, and the management approvals required. Build the deployment plan around the perspectives and impacts of the interested parties affected by the deployment, not only around technical readiness.

**Linked vulnerabilities:** V008 Weak Change Management, V010 Complex Model Loading, V009 Weak Artifact Protection.

### A.6.2.6 AI system operation and monitoring

**Control description:** the organization must define and document what is needed for the AI system's ongoing operation, covering at minimum system and performance monitoring, repairs, updates, and support.

**Implementation guidance:** monitor for general errors and failures and for whether the system performs as expected against real production data, using technical performance criteria appropriate to the task (classification, regression, ranking, and so on). Where the system continues to learn from production data, monitor specifically to confirm it still meets its original design goals; where it does not continuously learn, monitor for concept or data drift that can still degrade performance over time. Maintain defined processes for repairing and updating the system, including how updates are communicated to users, and for supporting it, whether that support is internal, external, or both. Identify AI-specific security threats relevant to the system explicitly, with data poisoning, model stealing, and model inversion named by the standard as baseline examples to consider.

**Linked vulnerabilities:** V027 Missing Drift Controls, V029 Inadequate Monitoring, V031 Weak Performance Auditing, V026 Weak Feedback Loops, V014 Data Poisoning Susceptibility.

### A.6.2.7 AI system technical documentation

**Control description:** the organization must determine what technical documentation each relevant category of interested party (users, partners, supervisory authorities) needs and provide it in an appropriate form.

**Implementation guidance:** cover a general description of the system and its intended purpose, usage instructions, technical assumptions about its deployment and operation, technical limitations such as acceptable error rates, monitoring capabilities available to users and operators, design and architecture specifications, the design choices and quality measures applied during development, information about the data used, verification and validation records, and the impact assessment documentation from Area A.5. Separately document a failure management plan (including a rollback approach and customer notification process), how the system's health is monitored, standard operating procedures including how event logs are prioritized and reviewed, and who is accountable for operating the system and responding to its failures. Keep this documentation current and have it approved by relevant management, not just by the team that produced it.

**Linked vulnerabilities:** V037 Lack of Design Documentation, V039 Poor User Guidance, V038 Weak Explainability Controls.

### A.6.2.8 AI system recording of event logs

**Control description:** the organization must determine at which life cycle phases event log recording should be enabled, at minimum while the AI system is in use.

**Implementation guidance:** log enough to trace whether the system's functionality is operating as intended and to detect when its performance falls outside its intended operating conditions in a way that could harm interested parties. Capture the time and date of use, the production data the system operated on, and any output that fell outside the system's intended operating range. Retain logs as long as the intended use and the organization's data retention policy require, and be aware that some system categories, biometric identification systems are the example the standard calls out, can carry additional jurisdiction-specific logging requirements.

**Linked vulnerabilities:** V028 Insufficient Logging, V030 Weak Event Traceability, V032 Insufficient Resource Monitoring.

---

## Area A.7: Data for AI systems

**Objective:** ensure the organization understands the role and impacts of data in AI systems across the application, development, provision, or use of AI systems throughout their life cycles.

### A.7.2 Data for development and enhancement of AI system

**Control description:** the organization must define, document, and implement data management processes related to the development of AI systems.

**Implementation guidance:** address the privacy and security implications of the data in use, the security and safety threats that data-dependent development can introduce, transparency and explainability considerations including data provenance and the ability to explain how data drove a given output, the representativeness of training data against the real operational domain, and the accuracy and integrity of the data itself. ISO/IEC 22989 has more detailed guidance on life cycle and data management concepts if the team needs a deeper reference.

**Linked vulnerabilities:** V015 Weak Data Governance, V014 Data Poisoning Susceptibility, V016 Weak Data Quality Controls.

### A.7.3 Acquisition of data

**Control description:** the organization must determine and document details about the acquisition and selection of data used in AI systems.

**Implementation guidance:** document the categories and quantity of data needed, the sources it comes from (internal, purchased, shared, open, or synthetic), the characteristics of each source (static, streamed, gathered, or machine generated), the demographics and characteristics of the data subjects including known or potential bias, how the data was previously handled and whether that handling was privacy- and security-compliant, applicable data rights, associated metadata such as labeling details, and the data's provenance. ISO/IEC 19944-1 offers a data category structure that can be adapted for this documentation.

**Linked vulnerabilities:** V020 Uncontrolled Data Ingestion, V021 Untrusted External Data Sources, V013 Insufficient Provenance Controls.

### A.7.4 Quality of data for AI systems

**Control description:** the organization must define and document data quality requirements and ensure the data used to develop and operate the AI system meets them.

**Implementation guidance:** treat data quality as the degree to which the data's characteristics satisfy stated and implied needs under the specific conditions the system will actually run in, per the definition in ISO/IEC 25024. For supervised or semi-supervised learning, define, measure, and improve the quality of training, validation, test, and production data specifically, and consider the impact of bias on both system performance and fairness, adjusting the model and the data as needed to bring the result to an acceptable level for the use case. The ISO/IEC 5259 series and ISO/IEC TR 24027 give additional depth on data quality and bias respectively.

**Linked vulnerabilities:** V016 Weak Data Quality Controls, V017 Distributed Data Inconsistency, V018 Complex Data Transformations.

### A.7.5 Data provenance

**Control description:** the organization must define and document a process for recording the provenance of data used in its AI systems across the life cycles of both the data and the AI system.

**Implementation guidance:** a provenance record, per ISO 8000-2, can include information about the data's creation, updates, transcription, abstraction, validation, and any transfer of control, as well as sharing without transfer of control and any transformations applied. Decide, based on the data's source, content, and context of use, whether the organization needs active measures to verify that provenance rather than accepting it on the strength of the record alone.

**Linked vulnerabilities:** V013 Insufficient Provenance Controls, V015 Weak Data Governance.

### A.7.6 Data preparation

**Control description:** the organization must define and document its criteria for selecting data preparation methods, and the specific methods used.

**Implementation guidance:** cover the common preparation needs: statistical exploration of the data, cleaning, imputation for missing entries, normalization, scaling, target variable labeling, and encoding of categorical variables into a usable form. For each AI task, document both the criteria used to choose a given preparation method and the specific methods and transforms actually applied, since undocumented preparation logic is one of the harder gaps to reconstruct later when something goes wrong. The ISO/IEC 5259 series and ISO/IEC 23053 provide additional detail specific to machine learning data preparation.

**Linked vulnerabilities:** V018 Complex Data Transformations, V019 Schema Incompatibility, V016 Weak Data Quality Controls.

---

## Area A.8: Information for interested parties of AI systems

**Objective:** ensure relevant interested parties have the information they need to understand and assess the risks and impacts, both positive and negative, of the AI system.

### A.8.2 System documentation and information for users

**Control description:** the organization must determine and provide the necessary information to users of the AI system.

**Implementation guidance:** give users both technical detail where they need it and a plain notification that they are interacting with an AI system where that is the more relevant fact, since the right level of detail depends heavily on who the user actually is. Cover the system's purpose, the fact that the user is interacting with an AI system, how to interact with it and how to override it, the technical requirements and limitations of operation, the human oversight the system relies on, accuracy and performance information, relevant findings from the impact assessment particularly where they affect specific demographic groups, revisions to any claims made about the system's benefits, and how to get support. Document the criteria the organization uses to decide what information gets shared, and validate that users can actually find the information once it exists, since information that is technically available but practically undiscoverable does not satisfy this control.

**Linked vulnerabilities:** V039 Poor User Guidance, V046 Unknown Customer Expectations, V038 Weak Explainability Controls.

### A.8.3 External reporting

**Control description:** the organization must provide a way for interested parties to report adverse impacts of the AI system.

**Implementation guidance:** monitoring the system for failures internally is necessary but not sufficient; give users and other external parties an explicit channel to report an adverse impact, such as an unfair outcome, that internal monitoring might never surface on its own.

**Linked vulnerabilities:** V034 Missing Reporting Channels, V044 Weak Human Rights Assessment.

### A.8.4 Communication of incidents

**Control description:** the organization must determine and document a plan for communicating AI system incidents to users.

**Implementation guidance:** understand the organization's actual notification obligations, which can vary sharply depending on context, a safety-relevant AI component in a physical product can carry very different notification requirements than an internal analytics tool. Where legal or contractual requirements apply, they typically specify the notification timeline, which authorities must be told, and exactly what details must be communicated. AI incident response can be integrated into the organization's broader incident management program, but the team running it needs to know where AI-specific requirements diverge, such as different reporting obligations for a personal-data breach in training data compared to an equivalent breach elsewhere. ISO/IEC 27001 and ISO/IEC 27701 give further detail on security and privacy incident management respectively.

**Linked vulnerabilities:** V033 Weak Incident Coordination, V030 Weak Event Traceability.

### A.8.5 Information for interested parties

**Control description:** the organization must determine and document its obligations to report information about the AI system to interested parties.

**Implementation guidance:** some jurisdictions require sharing system information with regulators or other authorities within a defined timeframe; the information involved can include technical system documentation such as training, validation, and test datasets, algorithmic choice justifications, verification and validation records, identified risks, impact assessment results, and system logs. Confirm the organization understands both its general reporting obligations and any jurisdiction-specific requirements for sharing information with law enforcement.

**Linked vulnerabilities:** V045 Jurisdictional Control Gaps, V068 Weak Contract Governance.

---

## Area A.9: Use of AI systems

**Objective:** ensure the organization uses AI systems responsibly and in accordance with its own policies.

### A.9.2 Processes for responsible use of AI systems

**Control description:** the organization must define and document the processes for the responsible use of AI systems.

**Implementation guidance:** whether an AI system is built in-house or sourced from a third party, be explicit about the considerations that determine whether to use it at all: cost including the ongoing cost of monitoring and maintenance, approved sourcing requirements, and the legal requirements the organization has to meet. Where the organization already has accepted policies for using other systems and assets, incorporate them here rather than building a parallel policy structure from nothing.

**Linked vulnerabilities:** V040 Weak Intended Use Controls, V064 Weak Vendor Due Diligence.

### A.9.3 Objectives for responsible use of AI system

**Control description:** the organization must identify and document objectives to guide the responsible use of AI systems.

**Implementation guidance:** define what fairness, accountability, transparency, explainability, reliability, safety, robustness and redundancy, privacy and security, and accessibility mean for this specific use case, then determine at which life cycle stages meaningful human oversight needs to be built in. That oversight can include human reviewers checking system outputs with real authority to override them, ensuring oversight is present wherever the intended deployment instructions call for it, monitoring performance and accuracy, reporting concerns about outputs and their impact, and deciding deliberately whether fully automated decision-making is even appropriate for this use case. Base the depth of oversight on the findings of the impact assessment in Area A.5, and make sure the people doing the oversight are actually trained on what they are overseeing.

**Linked vulnerabilities:** V047 Over-Automation Dependence, V038 Weak Explainability Controls, V025 Insufficient Model Validation.

### A.9.4 Intended use of the AI system

**Control description:** the organization must ensure the AI system is used according to its intended uses and accompanying documentation.

**Implementation guidance:** deploy the system with the resources and human oversight its documentation calls for, and confirm the data it operates on in practice actually matches what its documentation describes, since performance guarantees do not transfer to data the system was never validated against. Monitor operation continuously, and where correct deployment per the documented instructions still raises a concern about impact to interested parties or legal exposure, escalate that concern internally and to any third-party supplier involved rather than treating "we followed the instructions" as a closed question. Keep event logs and other documentation that can demonstrate the system was used as intended, retained per the organization's data retention policy and any applicable legal requirement.

**Linked vulnerabilities:** V040 Weak Intended Use Controls, V028 Insufficient Logging.

---

## Area A.10: Third-party and customer relationships

**Objective:** ensure the organization understands its responsibilities, remains accountable, and apportions risk appropriately when third parties are involved at any stage of the AI system life cycle.

### A.10.2 Allocating responsibilities

**Control description:** the organization must ensure responsibilities across its AI system life cycle are allocated between itself, its partners, suppliers, customers, and other third parties.

**Implementation guidance:** document every party involved in the life cycle, whether they supply data, algorithms and models, or development and use of the system itself, and be explicit about who is accountable to which interested parties for what. Where the organization supplies an AI system to a third party, it still needs to take a responsible approach to developing that system and be able to hand over the necessary documentation to both the interested parties and the receiving third party. Where personal data is processed, responsibilities typically split between data controllers and processors per ISO/IEC 29100, and privacy-preserving controls such as those in ISO/IEC 27701 should be considered based on the organization's actual role.

**Linked vulnerabilities:** V036 Undefined AI Roles, V068 Weak Contract Governance, V073 Vendor Data Siloing.

### A.10.3 Suppliers

**Control description:** the organization must establish a process ensuring that services, products, or materials from suppliers align with its approach to responsible AI development and use.

**Implementation guidance:** recognize the range of things a supplier might provide, datasets, algorithms or models, software components, or an entire AI system, and calibrate selection requirements and ongoing monitoring to the level of risk each type of supply actually carries. Document how supplier-provided components get integrated into the systems the organization builds or uses, and where a supplier's component underperforms or creates an impact inconsistent with the organization's responsible-AI approach, require the supplier to take corrective action rather than absorbing the gap silently. Confirm the supplier actually delivers adequate documentation for its AI system or component, since a supplier relationship without documentation transfers risk to the organization without transferring the information needed to manage it.

**Linked vulnerabilities:** V064 Weak Vendor Due Diligence, V065 Unverified Third-Party Models, V066 Outdated Third-Party Components, V067 Weak Supplier Oversight, V072 Conflicting Vendor Objectives.

### A.10.4 Customers

**Control description:** the organization must ensure its responsible approach to developing and using AI systems accounts for its customers' expectations and needs.

**Implementation guidance:** recognize that a single organization can hold many different customer relationships with different expectations, formal contractual requirements, general usage agreements, or a design-phase request, and that these will not all look alike. Be explicit about where responsibility sits between the organization as provider and the customer, and where the organization identifies a risk in how a customer might use its AI product or service, decide deliberately whether to communicate that risk to the customer so the customer can manage it on their end, for example by clearly communicating the boundaries of a system's validated domain of use.

**Linked vulnerabilities:** V046 Unknown Customer Expectations, V040 Weak Intended Use Controls.

---

## Reverse index: vulnerability category to primary control areas

Use this when you are starting from a finding in `docs/07-vulnerability-guide.md` and need the fastest path back to the relevant ISO/IEC 42001 controls, rather than starting from the standard and working forward.

| Vulnerability category | Primary control areas |
|---|---|
| Access and Exposure | A.3.2, A.9.3 |
| Change and Artifact Integrity | A.6.2.3, A.6.2.5 |
| Data Governance and Quality | A.7.2, A.7.3, A.7.4, A.7.5, A.7.6 |
| Model Lifecycle | A.6.1.2, A.6.1.3, A.6.2.4 |
| Observability and Response | A.6.2.6, A.6.2.8, A.8.4 |
| Governance and Accountability | A.2.2, A.2.3, A.2.4, A.3.2, A.5.2, A.5.3, A.5.4, A.5.5, A.9.2, A.9.3, A.9.4 |
| Resilience and Infrastructure | A.4.5 |
| Hardware and Side Channel | A.4.5 (this file's source list does not include a dedicated hardware-security control; treat this as a gap to raise, not an omission to ignore) |
| Third-Party and Supply Chain | A.10.2, A.10.3, A.10.4 |
| Documentation | A.4.2, A.4.3, A.4.4, A.6.2.7 |
| Multi-Agent | A.3.2, A.6.1.3 (this file's source list has no agent-specific control; treat this the same way as the hardware gap above) |

The two callouts above are deliberate: ISO/IEC 42001's Annex A, as scoped in this file, does not have a control purpose-built for physical hardware assurance or for multi-agent coordination risk. That is a genuine gap between the standard and the current threat landscape for agentic AI, not an error in this mapping. Where your assessment surfaces a finding in either category, cite the closest general control above and note the gap explicitly in Section 6 (AI Control Gaps) of `docs/09-threat-model-report-template.md`, rather than forcing a fit that overstates the standard's coverage.

## Cross-reference

Pair this file with `docs/07-vulnerability-guide.md` for the full technical detail behind each linked vulnerability, and with `docs/09-threat-model-report-template.md` Section 5 (Existing Control Mapping) and Section 6 (AI Control Gaps) when running an actual assessment. When citing a control in a report, cite the ISO/IEC 42001 clause number exactly as listed here so the citation is independently checkable against the published standard.
