# ICLR 2017 PeerRead source audit

**Date:** 2026-09-24  
**Programme:** Attention Allocation Under Cognitive Abundance  
**Track:** A v0.2 source comparability  
**Status:** outcome-blind provenance audit  
**Verdict:** `PEERREAD_ICLR2017_NOT_T0_ADMISSIBLE`  
**Citation outcomes opened:** **No**

## Question

Can PeerRead supply the missing ICLR 2017 submission-time paper text required by the frozen Track A representation protocol?

PeerRead is attractive because it contains real ICLR 2017 papers, real peer reviews and real accept/reject labels. The relevant question is not whether the dataset is genuine. It is whether the preserved PDFs represent the historical paper state **before review feedback could change the manuscript**.

## Dataset inventory

At audited PeerRead head `9bb37751781a900cee9e74ec3105997732c8e8e5`:

- ICLR 2017 review records: **427**
- PDFs: **427**
- parsed PDFs: **427**
- accepted records: **172**
- rejected records: **255**
- all 427 review records identify themselves as `ICLR 2017 conference submission`

The first repository commit adding the ICLR 2017 data is:

- commit: `89998022773306fdcad6a4097bf3a2dcd45807c6`
- date: **2018-02-14**

The repository timestamp is therefore much too late to prove submission-time state on its own.

## Canonical-frame reconciliation

The programme's local conference database currently contains:

- all ICLR 2017 submissions: **490**
- direct ACCEPT/REJECT decisions: **443**
  - ACCEPT: **198**
  - REJECT: **245**
- workshop-track invitations: **47**

This audit corrects an earlier planning upper bound of 442 direct ACCEPT/REJECT records to **443**. The one-record difference is immaterial to the earlier source-feasibility verdict.

Exact normalized-title reconciliation between PeerRead and the direct ACCEPT/REJECT frame gives:

- exact unique matches: **387**
- ambiguous exact-title matches: **0**
- PeerRead records unmatched to the current canonical frame: **40**
- canonical eligible records unmatched to PeerRead: **56**
- mapped ACCEPT: **172**
- mapped REJECT: **215**
- decision agreement: **387 / 387**
- decision disagreement: **0 / 387**

PeerRead therefore has strong evidence of genuine conference provenance and genuine decision labels.

## Temporal-provenance failure

The source nevertheless fails the T0 requirement.

PeerRead record **304**, *Making Neural Programming Architectures Generalize via Recursion*, is accepted.

Its preserved review record includes a meta-review stating that the authors added two tasks, **topological sort and quicksort**, based on reviewer discussion.

The preserved PeerRead PDF's parsed text explicitly presents four tasks:

1. grade-school addition;
2. bubble sort;
3. topological sort;
4. quicksort.

That is a direct positive witness that the preserved PDF incorporates post-submission reviewer-driven changes.

The relevant immutable PeerRead blobs are:

- review record: `9ec939a789b2186b0344829d9956d87d6633904d`
- parsed PDF: `eb10b8501d39ddcb3a2ab3dbc4a403daf88c178b`

This is stronger than a timestamp caveat. It demonstrates content contamination relative to the frozen submission-time estimand.

## Adjudication

`PEERREAD_ICLR2017_NOT_T0_ADMISSIBLE`

PeerRead may remain useful for other peer-review research questions. It is not admitted as the historical paper-text substrate for Track A v0.2.

No attempt will be made to rescue the source by:

- assuming rejected papers were less likely to be revised;
- using accepted and rejected PeerRead records under different temporal rules;
- treating current/revised manuscripts as if they were submission-time state;
- weakening the existing T0 definition.

Doing so would make historical paper observability depend on revision behaviour and potentially on conference outcome.

## Consequence for v0.2

With PeerRead rejected, the only remaining source stratum permitted by the frozen amendment is the conservatively deduplicated pre-cutoff ICLR 2021 arXiv set, whose optimistic maximum is **487** papers.

The best-case candidate arithmetic is therefore:

`4,060 verified 2018-2020 + 487 restricted 2021 arXiv = 4,547`

That is already **53 below** the frozen 4,600 exact-outcome-observable floor before any PDF-extraction or identity loss.

No technical acquisition of the 2021 arXiv PDFs can change that arithmetic.

The machine-readable audit is stored at:

`t0/peeread_audit/iclr2017_peeread_source_audit.json`
