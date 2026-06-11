# Artificial Intelligence Standard

**Information Security Standard — Generative, Agentic, and Embedded AI Systems**

| Field | Value |
|---|---|
| Document ID | IS-STD-AI-001 |
| Version | 0.1 (DRAFT — for internal review) |
| Status | Draft / Not yet approved |
| Owner | Information Security (Senior Security Engineer / AI Initiatives Lead) |
| Approving authority | AI Governance Committee; ratified per the approved AI Policy |
| Parent document | AI Policy (approved) |
| Classification | Internal — Confidential |
| Effective date | TBD |
| Review cadence | At least annually, or upon material regulatory or technology change |

> **Reviewer note (delete before publication):** Two open items flagged for confirmation are marked **[CONFIRM]** inline:
> 1. **Scope of traditional models.** This draft scopes traditional/quantitative and non-generative, non-agentic ML models *out* of this Standard and defers them to the bank's Model Risk Management (MRM) framework. Confirm this is the intended boundary.
> 2. **TPRM ownership.** Section 6 and Appendix C are written as a self-contained, liftable module so the Head of Risk can adopt, extend, or relocate them into the TPRM standard later. Confirm whether §6 should reference the existing TPRM standard or remain standalone for now.

---

## 1. Purpose and Scope

### 1.1 Purpose

This Standard establishes the mandatory security and governance baseline that any artificial intelligence (AI) system, capability, or feature MUST satisfy before it is acquired, built, enabled, or used at the Bank. It operationalizes the approved AI Policy into concrete, auditable control requirements and serves three functions:

- A **gate**: no in-scope AI tool enters the environment without passing the intake and risk-classification process defined here.
- A **baseline**: any proposed tool (e.g., a coding assistant, an LLM platform, an agentic automation framework) is assessed against the requirement domains in Section 5, with its specific controls recorded in a per-tool Control Set.
- A **contractual floor**: any third party supplying AI capability — or adding AI capability to an existing product — MUST meet the third-party requirements in Section 6 and the clause library in Appendix C.

### 1.2 Regulatory basis for this Standard

On **April 17, 2026**, the OCC, Federal Reserve, and FDIC issued revised supervisory guidance on model risk management (SR 26-2 / OCC Bulletin 2026-13), superseding the 2011 SR 11-7 guidance. The revised guidance **explicitly excludes generative and agentic AI models** from the model-risk framework on the basis that they are "novel and rapidly evolving," while confirming that such tools are **not** exempt from risk management — they remain subject to the **general** risk-management and governance expectations applicable to banking organizations.

This Standard is the Bank's instrument for meeting that expectation. It governs the categories of AI that the prudential model-risk framework now deliberately leaves to general risk management, and it interoperates with — rather than duplicates — the MRM framework that continues to govern traditional models.

### 1.3 In scope

This Standard applies to all of the following, whether hosted externally (SaaS / API), self-hosted, or run locally:

- **Generative AI / Large Language Model (LLM) systems** — chat assistants, copilots, content-generation tools, retrieval-augmented generation (RAG) systems, and any application that calls a foundation model.
- **Agentic AI systems** — AI that plans and executes multi-step actions, invokes tools or functions, writes or modifies code, or operates with any degree of autonomy over Bank systems or data.
- **Embedded and emergent AI features** — AI capabilities introduced into otherwise-approved, non-AI products (see Section 7).
- **AI development tooling** — coding assistants and agents (e.g., command-line coding agents, IDE copilots) that read from or write to Bank source repositories, infrastructure, or production systems.


### 1.5 Audience

All staff, contractors, and business units proposing, procuring, building, or operating AI capability; Information Security; Third-Party Risk Management (TPRM); Legal; Compliance; and the AI Governance Committee.

---

## 2. Definitions

| Term | Definition |
|---|---|
| **AI system** | Any system that uses machine learning, foundation models, or automated reasoning to generate output, recommendations, classifications, or actions. |
| **Generative AI (GenAI)** | AI that produces novel content (text, code, images, audio, structured data) from a learned model, typically a foundation model. |
| **Foundation / frontier model** | A large, general-purpose model (e.g., an LLM) trained on broad data and adaptable to many tasks. |
| **Agentic AI** | An AI system capable of autonomous or semi-autonomous, multi-step action — planning, tool/function invocation, code execution, or environmental interaction — toward a goal. |
| **Embedded AI feature** | AI capability delivered inside a product whose primary function is not AI (e.g., an AI assistant added to an IT service management, vulnerability management, or endpoint security platform). |
| **Emergent AI feature** | An AI feature introduced into an existing approved product *after* that product's original approval, typically via a vendor update or new release. |
| **RAG (Retrieval-Augmented Generation)** | An architecture in which a model's responses are grounded in Bank-controlled data retrieved at query time. |
| **Fine-tuning** | Further training of a model on additional data to adapt its behavior. |
| **NPI (Nonpublic Information)** | As defined under 23 NYCRR Part 500; includes business and personal nonpublic information. |
| **Bank Data** | Any data owned, licensed, controlled, or processed by the Bank, including NPI, Confidential, and Internal data, and any data derived from them. |
| **Derived Data** | Any embeddings, summaries, aggregations, telemetry, logs, or other artifacts generated from Bank Data. |
| **Tool/use-case owner** | The accountable business owner of a specific AI tool or use case. |
| **Human-in-the-loop (HITL)** | A human reviews and approves each AI output/action before it takes effect. |
| **Human-on-the-loop (HOTL)** | A human monitors AI operation and can intervene, but does not pre-approve each action. |
| **Zero/No-Data-Retention (ZDR)** | A vendor processing mode in which inputs and outputs are not retained, logged for human review, or used for any secondary purpose. |
| **MUST / SHOULD / MAY** | Requirement keywords. **MUST** = mandatory; **SHOULD** = expected unless a documented, approved exception applies; **MAY** = permitted/optional. |

---

## 3. Roles and Responsibilities

| Role | Responsibilities |
|---|---|
| **AI Governance Committee** | Owns this Standard; approves Tier 1 (High) use cases; ratifies exceptions; sets risk appetite; reviews the AI inventory. |
| **Information Security** | Maintains this Standard; performs security review and risk classification; defines and validates technical controls; monitors AI-related cyber risk; owns incident response for AI events. |
| **Third-Party Risk Management (TPRM)** | Performs vendor due diligence; ensures Section 6 contractual requirements are met; monitors vendors for new/embedded AI features. |
| **Legal** | Reviews and negotiates AI contract terms (Appendix C); advises on NJ LAD, NYDFS, privacy, and IP exposure; owns the regulatory-applicability determination. |
| **Compliance** | Maps use cases to applicable regulatory obligations; coordinates fair-lending / anti-discrimination assessments where relevant. |
| **Model Risk Management (MRM)** | Governs traditional/out-of-scope models; jointly reviews hybrid systems. |
| **Tool / Use-case owner** | Accountable for the business use case; completes intake; ensures ongoing compliance and monitoring; maintains human oversight. |
| **Data Owner** | Authorizes which data classifications may be exposed to a given AI system. |
| **All staff & contractors** | Use only approved AI tools for Bank purposes; never input Bank Data into unapproved tools; report AI incidents. |

---

## 4. AI Risk Classification (Tiering)

Every in-scope AI use case MUST be classified before approval. The tier determines the intensity of controls and the required approval authority. Tier is a function of three inputs; **the highest-rated input drives the tier** (i.e., the model is conservative by design).

### 4.1 Classification inputs

**A. Data sensitivity** — the most sensitive data classification the system can access, ingest, or output:
- Public
- Internal
- Confidential
- Restricted (includes customer NPI, credentials, source code, security data)

**B. Autonomy level** — the system's authority to act:
- Assistive (generates content; no action; human uses output)
- Human-in-the-loop (proposes actions; human approves each)
- Human-on-the-loop (acts; human monitors and can intervene)
- Autonomous / agentic (acts on Bank systems or data without per-action human approval)

**C. Use-case criticality** — the consequence of error or compromise:
- Experimental / sandbox (no production data, no decisions)
- Internal productivity (drafting, summarizing, research)
- Business-process (informs or executes operational workflows)
- Customer-, regulatory-, or safety-impacting (incl. any use touching employment, credit, or fair-treatment decisions)

### 4.2 Tier definitions

| Tier | Description | Typical profile | Approval authority |
|---|---|---|---|
| **Tier 0 — Prohibited** | Use cases the Bank will not permit (Section 4.3). | — | Not approvable |
| **Tier 1 — High** | NPI/Restricted data, OR autonomous/agentic action on Bank systems, OR customer/regulatory/safety-impacting use. | Agentic automation over production; LLM over customer NPI; coding agent with write access to production repos. | AI Governance Committee |
| **Tier 2 — Moderate** | Confidential data, business-process use, human-in/on-the-loop autonomy. | Internal RAG over Confidential docs; copilot drafting client-facing material with review. | InfoSec + TPRM + Legal sign-off |
| **Tier 3 — Low** | Public/Internal data only, assistive, productivity use. | General-purpose assistant for non-sensitive drafting/research in an approved, ZDR-configured tool. | InfoSec sign-off |

### 4.3 Tier 0 — Prohibited uses

The following are not permitted under this Standard:

- Inputting NPI/Restricted data into any AI tool that is **not** contractually bound by the no-training / no-retention requirements of Section 6.
- Fully autonomous agentic action that can move funds, alter customer accounts, change production security controls, or modify production code **without** a human approval gate or an equivalent compensating control approved by the AI Governance Committee.
- Use of AI as the **sole** basis for any employment, promotion, termination, or credit decision (see Section 5.7 and Appendix A regarding NJ LAD and NYC Local Law 144).
- Use of any AI tool whose vendor retains the right to train on, or have humans review, Bank Data absent an approved exception.
- Sending Bank source code or security/vulnerability data to any AI tool not explicitly approved at the appropriate tier.

---

## 5. Baseline Requirements

This section states the mandatory requirement domains every in-scope AI system MUST satisfy. It is deliberately tool-agnostic: it defines **what** must be true, not how any specific tool achieves it. The **specific, implemented, evidenced controls** for each approved tool are recorded separately in that tool's **Control Set** (see the per-tool Control Set Template), which maps each control back to the requirement domains below.

Each domain carries a stable identifier (`AIS-<DOMAIN>`) so that per-tool controls can cite the requirement they satisfy. Requirement intensity scales with the tier assigned under Section 4.

- **AIS-GOV — Governance & Inventory.** Every in-scope AI use case must complete intake (Section 8), have a named use-case owner and authorizing Data Owner, be risk-classified per Section 4, and be recorded in the AI System Inventory before any Bank Data is processed. The inventory must be maintained, periodically reviewed, and reconciled with TPRM records; higher-tier systems are re-reviewed on a defined cadence. *(Supports NYDFS Part 500 inventory and governance obligations.)*

- **AIS-DATA — Data Protection & Confidentiality.** Bank Data must be protected in proportion to its classification. The Bank requires that Bank Data and Derived Data not be used by any provider to train, fine-tune, evaluate, or improve models; that NPI/Restricted use occur only under no-/limited-retention terms with deletion guarantees; that vendor human review of prompts/outputs be disabled or contractually constrained; that data exposure be minimized to the use case; that residency be known and compliant; that NPI be encrypted in transit and at rest; and that an AI system never become a path to data a user could not otherwise access (no permission bypass, including via RAG). Unapproved consumer AI tools must not receive Bank Data.

- **AIS-IAM — Identity & Access.** Access to AI tools must use Bank SSO with phishing-resistant MFA and follow least-privilege. Agent and service identities must be distinct, attributable, and scoped to only what the task requires; secrets must live in the Bank's secrets manager and never in prompts, code, or configuration; standing privilege for agentic systems must be minimized. *(NYDFS Part 500 MFA obligations apply; AI-enabled attacks warrant phishing-resistant factors.)*

- **AIS-SEC — Model & Tool Security.** The underlying model(s) and provider(s) must be identified and documented, with model/version changes triggering re-review. Systems must defend against direct and indirect prompt injection and jailbreaks, treating ingested untrusted content as data, not instructions. Agentic tool/function-calling must be constrained to an explicit allow-list with a bounded, documented blast radius; destructive, irreversible, or production-affecting actions require a human gate or approved compensating control. The AI supply chain (models, libraries, plugins, connectors/MCP servers) must be vetted for provenance and integrity; environments must be segmented by tier; AI-generated code/commands/queries must not be auto-executed without tier-appropriate validation.

- **AIS-LOG — Logging, Monitoring & Auditability.** Tier 1 and Tier 2 systems must log prompts, responses, tool invocations, data accessed, the acting identity, and the authorization used, in tamper-resistant, time-synchronized logs sufficient to detect and reconstruct an AI-related cybersecurity event (including unauthorized NPI access by an agent). Logs must feed the Bank's monitoring/SIEM with anomaly alerting and meet applicable retention. *(Supports NYDFS Part 500 audit-trail and 72-hour notification obligations.)*

- **AIS-HOV — Human Oversight & Accountability.** Tier 1 and Tier 2 use cases must define a human oversight model (HITL/HOTL) and a named accountable human. A meaningful human element must remain in any decision affecting an individual's rights, employment, or access to a service — AI output alone must not be determinative. Users must be able to tell when they are relying on AI output and be trained against over-reliance; Tier 1 systems require a documented disablement procedure. *(Required posture under NJ LAD; reinforced by NYC Local Law 144 for employment tools.)*

- **AIS-REL — Output Reliability, Safety & Fairness.** Use cases must account for hallucination/error risk proportionate to consequence. Any use that informs employment, promotion, termination, credit, housing, public-accommodation, or contracting decisions must be referred to Compliance and Legal for disparate-impact assessment **before** approval, and — for employment AEDTs covering NYC-linked roles — must satisfy NYC Local Law 144 bias-audit, notice, and disclosure obligations. Material reliance on AI output should be supported by appropriate explainability/traceability. *(NJ LAD disparate-impact rules effective Dec 15, 2025; liability cannot be contractually shifted to the vendor.)*

- **AIS-DEV — Secure Development & Change Management.** *(Applies to AI coding assistants/agents and any AI that produces or modifies code, infrastructure, or configuration.)* AI coding tools must not have unsupervised write access to production repositories, pipelines, or infrastructure; AI-generated changes must flow through normal SDLC controls (review, SAST/dependency scanning, CI gates). Repository and infrastructure secrets must not be exposed to AI tools; Bank source code is Restricted and its externalization requires tier-appropriate approval and a no-train guarantee; agentic coding tools operate against non-production by default.

- **AIS-BCP — Resilience & Continuity.** Dependency on a specific model/vendor must be assessed; Tier 1 use cases must document the impact of provider outage or model deprecation and a fallback. AI systems supporting critical processes must be in BCP/DR scope and testing, and the Bank must be able to operate the affected process without the AI system (graceful degradation).

---

## 6. Third-Party / Vendor AI Requirements

> **Module note:** This section is written to stand alone so it can be adopted, extended, or migrated into the TPRM standard. It supplements (does not replace) existing third-party risk requirements. **[CONFIRM]**

### 6.1 Pre-procurement due diligence

Before contracting, TPRM (with InfoSec and Legal) MUST obtain and assess:

- Identity of the underlying model(s) and all sub-processors involved in processing Bank Data.
- The vendor's data-handling representations: training use, retention, human review, residency, and deletion.
- Security attestations (e.g., SOC 2 Type II), and where available, ISO/IEC 42001 certification, model cards, and bias-audit or evaluation reports.
- The vendor's own AI governance, secure-development, and incident-response posture.
- Whether the product contains, or is on a roadmap to contain, AI features (feeds Section 7).

### 6.2 Contractual requirements

Any contract under which a third party processes Bank Data via AI MUST include the following. Full clause language is in **Appendix C**.

- **No model improvement** Vendor is prohibited from using Bank Data or Derived Data to train, fine-tune, evaluate, benchmark, or otherwise improve any model, or to benefit any other customer. Any "service improvement" or "de-identified/aggregated data" carve-out is excluded unless separately approved in writing.
- **No human review** Vendor personnel and subcontractors are prohibited from accessing or reviewing Bank prompts/outputs except for a narrowly defined, contractually specified purpose with Bank consent.
- **Retention, deletion, and return** Defined retention limits; deletion on request; and return or certified destruction of all Bank Data and Derived Data on termination.
- **Confidentiality and ownership** Bank Data and all outputs derived from Bank inputs are the Bank's confidential property; the vendor asserts no ownership or license over Bank inputs or the resulting outputs beyond providing the service.
- **Sub-processor disclosure and flow-down** Disclosure of all sub-processors; advance notice of changes; mandatory flow-down of these terms to any sub-processor and any underlying model provider.
- **Change notification** Advance written notice of any material change, including a change to the underlying foundation model/version, a new AI feature, or a change in data-processing location or sub-processor.
- **Data Residency** Contractual commitment to agreed processing/storage locations.
- **Security incident notification** Notification within a defined SLA aligned to the Bank's regulatory obligations (no later than the window required to support NYDFS's 72-hour notification).
- **Audit and evidence rights** Right to obtain evidence of compliance (attestations, audit reports, model/bias documentation) and to audit or have a third party audit, proportionate to risk.
- **Non-discrimination / lawful use** Vendor warrants the tool can be operated in compliance with applicable law (incl. NJ LAD, NYDFS Part 500, GLBA).
- **Liability for discriminatory outcomes is not shifted to the vendor by contract** — the Bank retains accountability and therefore requires the controls, evidence, and audit rights to manage it.
- **Compliance with Bank standards** Vendor's AI processing of Bank Data must meet the security baseline of this Standard.

---

## 7. Embedded and Emergent AI Features

This is the highest-leverage section operationally: it addresses the case where a vendor adds AI to a product the Bank already uses (e.g., an IT service-management, vulnerability-management, or endpoint-protection platform turning on an AI assistant or "copilot").

### 7.1 Core principle

**An AI feature added to a previously-approved tool does not inherit that tool's approval.** Existing approval covers the product as it was assessed; new AI capability is a new risk surface requiring its own assessment.

### 7.2 Requirements

- **Off by default.** Newly introduced vendor AI features MUST be treated as disabled-by-default and MUST NOT be enabled until governed. Where a vendor enables an AI feature without opt-in, the feature MUST be disabled pending review.
- **Re-intake on introduction.** Discovery or announcement of an AI feature in an existing tool MUST trigger intake and risk classification (Section 8) for that feature.
- **Contract addendum review.** The existing contract MUST be reviewed against Section 6; an addendum MUST be executed to extend the no-train/retention/notification terms to the new AI feature and its data flows before enablement.
- **Data-flow re-assessment.** Determine whether the feature routes Bank Data to a new model, endpoint, or sub-processor.
- **Continuous vendor monitoring.** TPRM and InfoSec MUST monitor vendor release notes, roadmaps, and change notifications for new AI capability. Vendors MUST be contractually obligated to give advance notice of new AI features.
- **Telemetry/copilot scrutiny.** Particular scrutiny applies to features that transmit prompts, screen content, tickets, code, or security data off-platform; these are presumed Tier 1/Tier 2 until assessed.

---

## 8. Intake and Approval Workflow

```
Request → Triage & Classification → Review → Approval (by tier) → Onboarding w/ controls → Production w/ monitoring → Periodic re-review
```

1. **Request** — Tool/use-case owner submits intake (data classifications, autonomy, use case, vendor).
2. **Triage & classification** — InfoSec assigns Tier per Section 4.
3. **Review** —
   - InfoSec: control assessment (Section 5).
   - TPRM: vendor diligence + contractual requirements (Section 6).
   - Legal: contract terms + regulatory applicability (incl. NJ LAD / NYC LL144 / NYDFS).
   - Compliance: fair-treatment / disparate-impact referral where AIS-REL-02 applies.
   - MRM: joint review if hybrid (Section 1.4).
4. **Approval** — per tier authority (Section 4.2). Approval MAY be conditional on specified controls.
5. **Onboarding** — controls implemented and verified; recorded in the AI System Inventory.
6. **Monitoring & re-review** — ongoing monitoring; periodic re-review per the AIS-GOV cadence.

## 9. Exceptions and Waivers

- Any deviation from a **MUST** requires a documented exception with: the requirement, the gap, the business justification, compensating controls, a risk owner, and an expiry date.
- Tier 1 exceptions MUST be approved by the AI Governance Committee; Tier 2/3 exceptions per the relevant approval authority.
- Exceptions MUST be time-bound, tracked in the exception register, and reviewed at expiry.
- Tier 0 prohibitions are **not** waivable except by formal AI Governance Committee action amending this Standard.

---

## 10. Enforcement and Compliance

- Use of unapproved AI tools for Bank Data, or circumvention of this Standard, is a policy violation subject to the Bank's disciplinary and HR processes.
- Non-compliance discovered in production MAY result in immediate disablement of the AI capability pending remediation.
- This Standard is auditable; InfoSec MAY assess compliance at any time.

---

## 11. Review and Maintenance

- Reviewed at least annually and upon material regulatory or technological change (e.g., issuance of the pending federal AI model-risk RFI/guidance; changes to NYDFS, NJ LAD, or Group requirements).
- Version-controlled; changes logged in the revision history.
- Owned by Information Security; ratified by the AI Governance Committee.

---

## Appendix A — Regulatory and Framework Mapping

> This appendix reflects the landscape as of the drafting date and is for internal orientation; Legal owns the binding applicability determination. Sources are cited for verification.

### A.1 Federal — prudential / banking

- **Model Risk Management — Revised Guidance (SR 26-2 / OCC Bulletin 2026-13), April 17, 2026.** Supersedes SR 11-7 (2011). Narrows the definition of "model" to *complex* quantitative methods; **explicitly excludes generative and agentic AI** from scope (deferring them to general risk management — the basis for this Standard); applies to traditional and non-generative/non-agentic AI models; introduces a $30B-asset relevance threshold; principles-based and expressly non-binding (departure alone does not trigger supervisory criticism), though unsafe/unsound practices remain actionable. An RFI on AI (incl. generative/agentic) model risk is anticipated. *[CONFIRM asset-threshold relevance to the entity with Legal/Finance.]*
- **FFIEC IT Examination Handbooks** (Information Security, Architecture/Infrastructure/Operations, Outsourcing/Third-Party) — existing expectations continue to apply to AI systems and AI vendors.
- **GLBA Safeguards** — underlying data-protection obligations for customer information.
- **Consumer protection (if applicable):** ECOA/Reg B adverse-action and fair-lending obligations apply to any AI used in credit decisions; refer to Compliance. *(Likely limited for a custodian/trust profile — confirm applicability.)*

### A.2 Federal — AI policy posture (deregulatory, in flux)

- **EO 14179, "Removing Barriers to American Leadership in AI"** (Jan 23, 2025); **America's AI Action Plan** (July 23, 2025); **EO "Ensuring a National Policy Framework for AI"** (Dec 11, 2025) — directs DOJ to challenge "onerous" state AI laws and pursues a "minimally burdensome" national framework and preemption.
- **Practical effect:** Until litigation resolves, **state AI laws remain enforceable.** This Standard is written to the **stricter state baseline (NY/NJ)** and does not rely on federal preemption.

### A.3 Federal — voluntary frameworks (used as structure)

- **NIST AI Risk Management Framework (AI RMF 1.0)** and the **Generative AI Profile (NIST AI 600-1, July 2024; updated March 2025).** Voluntary, but widely referenced by federal enforcers; crosswalks to ISO/IEC 42001. (Related: NIST IR 8596 "Cyber AI Profile" preliminary draft, Dec 2025; SP 800-53 control overlays for securing AI systems, concept 2025.)
- **ISO/IEC 42001:2023** — AI Management System standard; auditable basis for the Bank's AI governance program.

### A.4 New York

- **23 NYCRR Part 500 (NYDFS Cybersecurity Regulation)** — amended Nov 2023; phased requirements fully effective as of **Nov 1, 2025** (incl. MFA, asset inventory, data-minimization/retention). Directly applicable to NY-licensed entities.
- **NYDFS Industry Letter, "Cybersecurity Risks Arising from Artificial Intelligence" (Oct 16, 2024)** — imposes no new requirements but explains how Part 500 applies to AI: AI in risk assessments, AI-related third-party risk, phishing-resistant access controls against AI-enabled attacks (deepfakes), data minimization, monitoring/training, AI-aware incident response, 72-hour notification, and audit trails capturing AI/agent NPI access. **Primary cyber anchor for this Standard.**
- **NYC Local Law 144 (AEDT bias-audit law)** — in force; enforced by DCWP (penalties $500–$1,500/day); applies to employers with NYC offices (incl. NYC-linked remote roles) using automated employment decision tools. A Dec 2025 NYS Comptroller audit criticized enforcement as ineffective, signaling likely heightened scrutiny. Relevant to any HR/hiring use case (AIS-REL-03).

### A.5 New Jersey (state of HQ)

- **NJ Law Against Discrimination (LAD) — DCR/AG Guidance on Algorithmic Discrimination (Jan 9, 2025).** Clarifies that LAD prohibits algorithmic discrimination (disparate treatment and disparate impact) from automated decision tools across employment, housing, credit, public accommodation, and contracting; **liability cannot be shifted to the AI vendor/developer**; no discriminatory intent is required; recommends an AI oversight group, AI policies, and retained human decision-making.
- **NJ LAD disparate-impact rules (DCR), adopted Dec 2025, effective Dec 15, 2025.** Codify disparate-impact analysis across the same domains and subject automated employment decision tools to the same analysis as human processes; described as the most comprehensive state-level disparate-impact regulations in the U.S. Drives AIS-REL-02.
- **NJ Department of Banking and Insurance (NJDOBI)** — state banking supervisor of the entity; general supervisory authority applies. *(No NJDOBI AI-specific rule confirmed at drafting; monitor.)*

### A.6 International / Group

- **Sumitomo Mitsui Trust Group AI governance framework (Tokyo / "TG" overlay).** This Standard MUST meet or exceed the Group framework; where Group and U.S. requirements differ, the **stricter** applies. *(Map specific Group control expectations in a follow-up cross-reference.)*
- **EU AI Act** — in force Aug 1, 2024, phasing through 2026–2027; potential extraterritorial reach via vendor models or Group EU nexus. *Monitor for applicability;* not assumed binding on the entity at drafting.

### A.7 Requirement-to-regulation cross-reference (illustrative)

| Driver | Primary requirement domains |
|---|---|
| NYDFS Part 500 + Oct 2024 AI letter | AIS-GOV, AIS-DATA, AIS-IAM, AIS-LOG, AIS-TPR (incident notification) |
| NJ LAD (+ Dec 2025 disparate-impact rules) | AIS-HOV, AIS-REL, AIS-TPR (non-discrimination/lawful use) |
| NYC Local Law 144 | AIS-REL, AIS-HOV |
| SR 26-2 (general risk-mgmt expectation for GenAI/agentic) | Entire Standard; esp. AIS-GOV, AIS-SEC, AIS-HOV, AIS-BCP |
| NIST AI RMF / ISO 42001 | Program structure; AIS-GOV, AIS-SEC, AIS-LOG |

---


## Appendix C — Mandatory Contract Clause Library (Drafting Aid)

> Plain-language clause intent for Legal to convert into binding terms. Not legal advice; Legal owns final wording and negotiation. *(Retained as Appendix C; Appendix B now points to the separate Control Set Template.)*

**C.1 No Training / No Model Improvement.** Vendor and its sub-processors shall not use Bank Data, inputs, outputs, or any Derived Data to train, retrain, fine-tune, evaluate, benchmark, develop, or improve any model or service, nor to benefit any other customer or third party. No exception applies to de-identified, anonymized, or aggregated data unless expressly agreed in writing by the Bank.

**C.2 No Human Review.** Vendor and its sub-processors shall not access, view, or review Bank inputs or outputs, except for a specific, limited purpose expressly defined herein, and only to the extent consented to by the Bank; any such access shall be logged and made available to the Bank on request.

**C.3 Retention, Deletion, Return.** Vendor shall retain Bank Data only as long as necessary to provide the service and no longer than the period specified herein; shall delete Bank Data upon the Bank's request; and shall return or certify destruction of all Bank Data and Derived Data upon termination.

**C.4 Ownership & Confidentiality.** As between the parties, the Bank owns all Bank inputs and all outputs generated from them; Vendor obtains no ownership, license, or other right in Bank inputs or outputs except as necessary to provide the service. Confidentiality obligations survive termination.

**C.5 Sub-processors & Flow-down.** Vendor shall disclose all sub-processors and the underlying model provider(s), provide advance notice of any change, and impose these terms (including C.1 and C.2) on each by written agreement.

**C.6 Change Notification.** Vendor shall provide advance written notice of any material change affecting Bank Data processing, including a change to the underlying model or version, the addition of any AI feature, or a change in processing location or sub-processor.

**C.7 Data Residency.** Vendor shall process and store Bank Data only in the location(s) agreed herein.

**C.8 Security Incident Notification.** Vendor shall notify the Bank of any security incident affecting Bank Data without undue delay and within the period specified herein, sufficient to enable the Bank to meet its regulatory notification obligations (including a 72-hour regulatory window).

**C.9 Audit & Evidence.** Vendor shall provide, on request, evidence of compliance (e.g., SOC 2 Type II, ISO/IEC 42001, model and evaluation documentation, and any applicable bias-audit reports) and shall permit audit (by the Bank or its designee) proportionate to risk.

**C.10 Lawful, Non-Discriminatory Use.** Vendor warrants that the service can be operated in compliance with applicable law (including 23 NYCRR Part 500, GLBA, and the NJ Law Against Discrimination). Nothing herein shifts to the Vendor the Bank's regulatory accountability for outcomes; accordingly, Vendor shall provide the transparency, evidence, and audit rights necessary for the Bank to manage that accountability.

**C.11 Compliance with Bank Security Standard.** Vendor's processing of Bank Data via AI shall meet the security requirements of the Bank's AI Standard (this document).

---

## Revision History

| Version | Date | Author | Notes |
|---|---|---|---|
| 0.1 | TBD | InfoSec | Initial draft for internal review |
