# Asset Inventory: [System Name]

Complete this before starting Phase 3. If any row cannot be filled in, that gap is itself a finding, most likely under Lack of Design Documentation (V037) or Insufficient Provenance Controls (V013).

## System classification

- **AI system type**: predictive / generative / agentic / mixed (list components separately below if mixed)
- **Sourcing model**: built in-house / procured / hybrid (fine-tuned foundation model)
- **Business owner**:
- **Technical owner**:
- **Risk tolerance and success criteria**: (measurable, e.g. "prompt injection bypass rate below defined threshold")

## Data assets

| Asset | Description | Source and lineage | Owner | Sensitivity | Access controls |
|---|---|---|---|---|---|
| Training data | | | | | |
| Fine-tuning data | | | | | |
| Feedback / RLHF data | | | | | |
| Retrieval corpus / vector store | | | | | |
| Evaluation and holdout sets | | | | | |

## Model assets

| Asset | Version | Base model / provenance | Deployment endpoint | Validation status |
|---|---|---|---|---|
| Production model | | | | |
| Fallback / prior version | | | | |

## Pipeline and infrastructure assets

| Asset | Description | Owner | Change control process |
|---|---|---|---|
| Training pipeline | | | |
| Feature store | | | |
| Model registry | | | |
| Inference infrastructure | | | |
| Monitoring and logging stack | | | |

## Interface and orchestration assets (generative and agentic systems)

| Asset | Description | Trust boundary crossed | Access controls |
|---|---|---|---|
| System prompt / instructions | | | |
| Retrieval integration | | | |
| Tool / plugin integrations | | | |
| Agent memory store | | | |
| Multi-agent communication channel | | | |

## External dependencies

| Dependency | Vendor | What it provides | Contract terms covering security | Last due diligence review |
|---|---|---|---|---|
| | | | | |

## Data flow diagram

Attach or link a diagram tracing every data flow from source through processing, training, deployment, inference, and monitoring. Mark every trust boundary explicitly; the STRIDE-AI walk in the next phase is applied at trust boundaries.
