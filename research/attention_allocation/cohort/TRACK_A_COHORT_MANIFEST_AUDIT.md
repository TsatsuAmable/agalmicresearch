# Track A Cohort Manifest Audit v0.1

**Status:** feasibility artefact; empirical policy comparison remains gated.

## Result

A deterministic two-year cohort manifest now exists for ICLR 2020–2021, reconciled against two independent public corpora. The reconciliation improves coverage knowledge but does not establish decision-time provenance for title, abstract, or keywords. Those fields therefore remain CURRENT_ONLY; no allocator input is yet T0-admissible.

Manifest SHA-256: 7a2f692468ef3e86ecebe71d6f5642d55588c7498e5dd016d7644f18199a195a

## Coverage

| Year | Full cohort | Accept | Reject | Withdrawn | Desk reject | PRRCA witness | Accept witness | Reject witness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2020 | 2593 | 687 | 1526 | 369 | 11 | 1807 | 630/687 (91.7%) | 1177/1526 (77.1%) |
| 2021 | 3009 | 859 | 1735 | 398 | 17 | 2208 | 788/859 (91.7%) | 1419/1735 (81.8%) |

## Adversarial findings

- 2020: independent witness coverage is materially higher for accepted papers than rejected papers; this source must not define the canonical candidate pool.
- 2020: decision mismatches across overlapping records: 0; normalized-title mismatches: 0.
- 2021: independent witness coverage is materially higher for accepted papers than rejected papers; this source must not define the canonical candidate pool.
- 2021: decision mismatches across overlapping records: 1; normalized-title mismatches: 1.
- The broader berenslab corpus supplies the full candidate frame used here, including withdrawn and desk-rejected records, but it is a later scrape and therefore freezes current snapshots rather than proving submission-time state.
- PRRCA is useful as an independent identity/decision witness but is incomplete and outcome-differential for the primary ACCEPT/REJECT comparison.

## Gate verdict

**CONDITIONAL / NOT YET PASS.** Manifest construction, source hashing, exclusion accounting, and accepted/rejected coverage measurement are now complete for two years. The remaining blocker is temporal provenance: at least one allocator-visible submission field must be upgraded from CURRENT_ONLY to T0_OBSERVED or T0_DERIVABLE before empirical policy simulation.

## Source provenance

- berenslab/iclr-dataset commit: 9f09cbbfb8ff844b7267906c8b9d9419fdad9d6c; parquet SHA-256: 47a04232b1c229d81109a498da32dfbe0157d35d19941561924398a9106932e2.
- ntunlplab/PRRCA commit: 2c48f54980560b7f44f98719a8d7082f0a587ef6; selected-file aggregate SHA-256: bee8d8ad3a0b44d768d93a3684ffe13624408fa06c88baed3d6dc128fb49c78c.

The manifest stores content hashes rather than treating later-scraped text as admissible historical evidence.
