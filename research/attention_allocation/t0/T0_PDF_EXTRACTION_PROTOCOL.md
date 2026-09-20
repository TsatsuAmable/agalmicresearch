# T0 PDF Extraction Protocol v0.1

**Date frozen:** 20 September 2026  
**Scope:** ICLR 2020 historical PDFs identified by the pre-deadline revision-reference audit.

## Purpose

Convert successfully acquired historical revision PDFs into a deterministic text corpus without introducing post-decision information or silently changing the cohort.

## Frozen extraction rule

1. Only PDFs already present in the acquisition ledger with `status=ok` are eligible.
2. Before extraction, recompute SHA-256 and require an exact match with the acquisition ledger.
3. Extraction is offline. The extractor performs no network requests and has no fallback to current OpenReview PDFs, arXiv, publisher copies, OCR services, or other sources.
4. Extract the entire PDF in page order using `pypdf` with `strict=False`.
5. Preserve page boundaries. Store page text as an ordered JSON array in gzip-compressed files outside the git repository.
6. Do not use decision labels, review content, acceptance status, citations accrued after submission, or later metadata to alter extraction behavior.
7. Record page count, non-empty page count, character count, extracted-text SHA-256, page-level extraction errors, and source-PDF SHA-256.
8. Extraction failures remain failures. No hidden repair or alternate-source substitution is allowed in this stage.

## Quality flags

Quality flags are diagnostic and do not automatically exclude records:

- `ZERO_TEXT`: extracted character count is zero.
- `LOW_TEXT_LT_1000`: more than zero but fewer than 1,000 extracted characters.
- `PAGE_EXTRACTION_ERRORS`: at least one page raised an extraction exception.

The 1,000-character flag is an operational warning threshold only. It is not a scientific admissibility threshold and must not be tuned after inspecting outcome labels.

## Leakage boundary

The extraction process sees only the acquired historical PDF and acquisition integrity metadata. Historical decision labels are joined only later by the separate missingness-audit script.

No semantic embedding, novelty score, citation feature, language-model score, author reputation feature, or downstream-value proxy is generated at this stage.

## Promotion gate

A T0 revision reference may be promoted to `T0_OBSERVED_PDF` only after:

- the historical PDF has been successfully acquired;
- its SHA-256 is recorded;
- the extractor verifies that same SHA-256;
- extraction status and quality flags are recorded;
- aggregate acquisition/extraction missingness is measured separately for ACCEPT and REJECT;
- any material outcome-differential missingness is treated as a methodological risk rather than patched by substituting later sources.

Only after this gate may a separate, pre-specified feature protocol be designed for allocation-policy evaluation.
