<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/signal-system-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/signal-system-light.svg">
  <img alt="Signal to System: silicon, speech, vision, and trust connected through an evaluated AI systems pipeline" src="assets/signal-system-light.svg">
</picture>

# Harsh Saand

**AI engineer · MSc Artificial Intelligence candidate at NTU Singapore**

I build evaluation-minded AI systems across semiconductor intelligence, multilingual speech, computer vision, and trustworthy multimodal analysis. I am most interested in the point where a strong model becomes an inspectable system another person can actually use.

[Email](mailto:harshsaand@yahoo.com) · [LinkedIn](https://www.linkedin.com/in/harsh-saand-961228230) · [Ask a technical question](https://github.com/HarshSaand/HarshSaand/issues/new?title=Technical%20question%3A%20&body=Hi%20Harsh%2C%0A%0AI%20was%20looking%20at%20%E2%80%A6)

### Pick your lens

[Hiring teams → selected systems](#selected-systems) · [Researchers → questions and boundaries](#questions-i-am-carrying-forward) · [Engineers → how I build](#how-i-build)

---

## Selected systems

Four projects, ordered by the technical thread I want to keep developing: understand the mechanism, expose the evidence, and state the boundary.

<a id="processtwin"></a>

### 01 · [ProcessTwin AI TCAD](https://github.com/HarshSaand/processtwin-ai-tcad)

**Question.** Can reduced-order silicon process physics and a learned surrogate support fast recipe exploration without hiding what the model approximates?

**Built.** Deal–Grove oxidation, 1D dopant diffusion, a deterministic 6,000-recipe simulated DOE, PCA profile compression, residual MLP ensembles, OOD warnings, and simulator-verified inverse design.

**Evidence.** Held-out simulator fidelity reached R² 0.9968 for oxide thickness and 0.9985 for junction depth. These are simulator-backed results, not fab calibration.

<details>
<summary><b>Open technical brief</b> — architecture, evidence, and limits</summary>

#### System path

`recipe → reduced-order physics → simulated DOE → PCA + residual ensemble → prediction / disagreement / inverse search → solver verification`

#### Inspect

- [Physics and model source](https://github.com/HarshSaand/processtwin-ai-tcad/tree/main/src/processtwin)
- [Saved evaluation metrics](https://github.com/HarshSaand/processtwin-ai-tcad/blob/main/outputs/metrics.json)
- [Tests](https://github.com/HarshSaand/processtwin-ai-tcad/tree/main/tests)
- [Technical report](https://github.com/HarshSaand/processtwin-ai-tcad/blob/main/outputs/processtwin_report.pdf)

#### Boundary

The simulator omits geometry effects, segregation, clustering, implant damage, stress, equipment variation, and fab calibration. The ensemble bands are uncalibrated model-disagreement signals, not calibrated predictive intervals. The saved interpolation test also shows that this deliberately simple physics solver can be faster than the surrogate.

</details>

<a id="wafer-triage"></a>

### 02 · [Wafer Process Signature Triage](https://github.com/HarshSaand/wafer-process-signature-triage)

**Question.** Can wafer-map geometry be converted into a useful review signal while keeping spatial structure visible to an engineer?

**Built.** Cartesian and polar CNN views fused with a 17-value spatial signature, grouped splitting, temperature calibration, uncertainty routing, and similar-case retrieval.

**Evidence.** The saved seed-42 run reached 0.812 macro-F1 on an untouched 138-image grouped test split across nine classes.

<details>
<summary><b>Open technical brief</b> — data audit, evaluation, and limits</summary>

#### System path

`wafer image → audit + grouped split → Cartesian / polar views + spatial descriptors → calibrated ranking → review route + similar cases`

#### Inspect

- [Data provenance](https://github.com/HarshSaand/wafer-process-signature-triage/blob/main/DATA_PROVENANCE.md)
- [Model and feature source](https://github.com/HarshSaand/wafer-process-signature-triage/tree/main/src/wafer_tcad)
- [Saved evaluation metrics](https://github.com/HarshSaand/wafer-process-signature-triage/blob/main/outputs/metrics.json)
- [Tests](https://github.com/HarshSaand/wafer-process-signature-triage/tree/main/tests)

#### Boundary

This is pattern triage, not causal root-cause diagnosis. The result comes from one seed and a curated 902-image JPEG derivative with 15–16 test examples per class. Multiple-seed intervals, stronger ablations, and a global cross-label near-duplicate audit remain follow-up work.

</details>

<a id="deepshield"></a>

### 03 · [DeepShield ApprovalGuard](https://github.com/HarshSaand/deepshield-approvalguard)

**Question.** Before a sensitive financial instruction moves forward, can local AI surface media-integrity evidence that deserves human review?

**Built.** Separate synthetic-voice, face-manipulation, visual-continuity, media-quality, and audio–video timing branches with timestamped evidence, abstention, and structured review routing.

**Evidence.** The AASIST audio branch reached ROC-AUC 0.9078 on a balanced 570-file ASVspoof subset; the other branches are demonstrated with functional fixtures rather than presented as validated detectors.

<details>
<summary><b>Open technical brief</b> — evidence branches, governance, and limits</summary>

#### System path

`recording → quality checks → independent evidence branches → timestamped timeline → STANDARD / REVIEW / ESCALATE / INSUFFICIENT EVIDENCE`

#### Inspect

- [Evidence pipeline](https://github.com/HarshSaand/deepshield-approvalguard/tree/main/approvalguard)
- [Evaluation artifacts](https://github.com/HarshSaand/deepshield-approvalguard/tree/main/evaluation)
- [Dataset card](https://github.com/HarshSaand/deepshield-approvalguard/blob/main/DATASET_CARD.md)
- [Third-party model provenance](https://github.com/HarshSaand/deepshield-approvalguard/blob/main/THIRD_PARTY_MODELS.md)

#### Boundary

The system supports review; it does not establish identity, intent, or fraud. Scores are evidence scales rather than calibrated fraud probabilities. The quantitative result covers the audio branch only, and the showcase threshold was selected and measured on the same subset.

</details>

<a id="speech"></a>

### 04 · [Local Multilingual Speech Intelligence](https://github.com/HarshSaand/local-multilingual-speech-intelligence)

**Question.** How can multilingual recordings be transcribed, translated, speaker-labelled, and reviewed while keeping audio processing local?

**Built.** A compact `faster-whisper` pipeline with optional `pyannote.audio` diarization, temporal-overlap speaker assignment, and accessible TXT, JSON, and HTML exports.

**Evidence.** The public repository includes synthetic data and deterministic tests for timestamps, speaker overlap, JSON preservation, and HTML escaping. It is a reference pipeline, not a claimed speech-quality benchmark.

<details>
<summary><b>Open technical brief</b> — local pipeline, privacy, and limits</summary>

#### System path

`local media → VAD + faster-whisper → optional diarization → overlap assignment → TXT / JSON / HTML`

#### Inspect

- [Pipeline source](https://github.com/HarshSaand/local-multilingual-speech-intelligence/blob/main/local_speech_intelligence.py)
- [Synthetic output](https://github.com/HarshSaand/local-multilingual-speech-intelligence/blob/main/examples/synthetic-transcript.json)
- [Tests](https://github.com/HarshSaand/local-multilingual-speech-intelligence/tree/main/tests)

#### Boundary

The public reference contains no employer source, recordings, customer transcripts, identifiers, private vocabulary, or production configuration. Model setup may download weights, but audio inference is local. WER, translation quality, diarization error, and runtime are not yet benchmarked here.

</details>

---

## How I build

```text
define the failure mode
        ↓
build the smallest measurable system
        ↓
inspect errors and distribution shifts
        ↓
document what the result does not prove
        ↓
design the path to use
```

- **Mechanism before mystique.** I want to know what produces the output and where the abstraction breaks.
- **Evaluation before adjectives.** A metric needs a dataset, protocol, baseline, and boundary around it.
- **Privacy is architecture.** Data handling and deployment constraints shape the system from the beginning.
- **Interfaces are part of the model.** Evidence is only useful if another person can inspect and act on it.

## Questions I am carrying forward

- How can mechanistic models and learned surrogates work together with uncertainty that is actually calibrated?
- How should multimodal integrity systems behave under distribution shift, missing evidence, and deliberate attack?
- How can multilingual speech systems remain private, inspectable, and useful on constrained hardware?

## Technical working set

```text
Learning systems   PyTorch · Transformers · RAG · LoRA/PEFT · model evaluation
Speech & language  faster-whisper · WhisperX · pyannote · multilingual translation
Vision             CNNs · diffusion models · geometric vision · 3D reconstruction
Engineering        Python · Java · REST APIs · Docker · Kubernetes · GPU computing
```

## Let’s compare notes

I am open to internships and early-career roles in applied AI/ML and research engineering, especially around semiconductor intelligence, speech and NLP, computer vision, multimodal systems, and trustworthy evaluation.

If one of these systems overlaps with a problem you are working on, [send me an email](mailto:harshsaand@yahoo.com), [connect on LinkedIn](https://www.linkedin.com/in/harsh-saand-961228230), or [open a technical question](https://github.com/HarshSaand/HarshSaand/issues/new?title=Technical%20question%3A%20&body=Hi%20Harsh%2C%0A%0AI%20was%20looking%20at%20%E2%80%A6).
