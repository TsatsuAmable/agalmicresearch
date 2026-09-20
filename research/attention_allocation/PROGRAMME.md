# Attention Allocation Under Cognitive Abundance

**Status:** empirical programme, feasibility phase  
**Gate:** NOT YET EVALUATED  
**Empirical policy simulations:** prohibited until feasibility criteria are frozen and the gate passes.  
**Synthetic engineering fixtures:** permitted only to test harness mechanics; they are non-evidentiary.

## Research question

Given more potentially valuable knowledge candidates than humans can evaluate, which allocation policies maximise realised epistemic value per unit of scarce human attention without systematically suppressing uncertain, novel, minority, dissenting, or otherwise unconventional candidates?

The programme is explicitly falsification-capable. Null, negative, contradictory, ambiguous, CONDITIONAL PASS and ABSTAIN outcomes are valid.

## Constructs kept separate

Candidate generation, candidate evaluation, selection, realised discovery and downstream epistemic value are separate stages. More generated candidates do not imply more discovery.

The initial pressure parameter is rho = lambda E[C] / B, where lambda is candidate arrival, C evaluation cost and B attention budget. This is a provisional experimental coordinate, not a claimed universal law.

## Current prior-art verdict

The broad allocation problem is **not novel**. Active learning already studies allocation of expensive oracle labels; bandit and exploration/exploitation literatures study scarce sampling; selective-label research establishes that historical decisions alter which outcomes become observable.

The programme can still contribute if it demonstrates something narrower and empirical: how scientific-candidate allocation policies behave as candidate pressure changes when outcome observability is selection-affected, novelty is measured pluralistically, and the evaluation preserves a temporal firewall.

A particularly important falsifier already exists. Teplitskiy et al. (2022) found no general anti-novelty pattern in peer review across their journal samples and instead observed higher acceptance for their novelty measure. The programme therefore MUST NOT encode “peer review suppresses novelty” as a premise.

Novelty measurement is itself contested. Fontana et al. (2020) found common combinatorial novelty indicators sensitive to construction and overlapping with interdisciplinarity. Embedding distance or atypical citation combinations may therefore be candidate measures, never ground truth.

## Empirical substrate

Development cohort: ICLR/OpenReview 2017–2022. Later years are held back for temporal validation.

Raw source records are immutable. Clean/canonical records are derived. Every field used by an allocation policy must be classified AVAILABLE_AT_DECISION_TIME. Future outcomes and fields with unresolved timestamps are blocked by architecture.

## Stage A synthetic engineering harness

A deterministic synthetic harness may be built and exercised before the empirical gate passes, but only to test software and protocol invariants. It must not be used to rank policies for the research programme or to support publication claims.

The harness must:

- expose identical candidate pools and budgets to every policy;
- structurally redact evaluator-only latent value from policy inputs;
- use multiple scenario families so one assumed world cannot masquerade as a general result;
- preserve deterministic seeds and versioned configuration;
- fail on budget overspend, duplicate selection or evaluator leakage;
- label all outputs `ENGINEERING_FIXTURE_ONLY`.

The authoritative specification is `research/attention_allocation/synthetic/STAGE_A_SPEC.md`.

## Feasibility before hypotheses

Before any empirical policy comparison, report completeness by year and decision; longitudinal match rates by decision/year/metadata; unresolved matches; lineage ambiguity; resubmissions; outcome-window completeness; missingness; and temporal leakage.

The gate criteria themselves must be frozen before substantive empirical policy outcomes are inspected. We will not invent a threshold after seeing whether it permits the desired experiment.

## Causal boundary

Later citations/publication are not intrinsic counterfactual values. Conference selection changes visibility, publication opportunity, subsequent attention and potentially the work itself. Retrospective policy simulation can describe recovery of *observable future outcomes* but cannot, without stronger identification, claim what rejected work would have achieved under acceptance.

## Immediate stop rules

ABSTAIN or redesign if longitudinal coverage of non-selected work is inadequate, selection strongly determines observability without a defensible correction, temporal leakage persists, value becomes circular, conclusions depend on arbitrary construct choices, or adversarial review finds an unresolved fatal flaw.

## Public outputs

Research-commons artefacts may be released throughout feasibility: acquisition tooling, provenance, corpus manifests, matching methodology, leakage tests, feasibility reports, synthetic engineering fixtures and negative results. A journal manuscript is downstream of evidence, not a production target.

## References

- Lakkaraju, H. et al. (2017). *The Selective Labels Problem*. KDD. DOI: 10.1145/3097983.3098066.
- Settles, B. (2009). *Active Learning Literature Survey*. UW-Madison TR1648.
- Uzzi, B. et al. (2013). *Atypical Combinations and Scientific Impact*. Science 342(6157), 468–472.
- Fontana, M. et al. (2020). *New and atypical combinations: An assessment of novelty and interdisciplinarity*. Research Policy 49(7), 104063.
- Teplitskiy, M. et al. (2022). *Is novel research worth doing? Evidence from peer review at 49 journals*. PNAS 119(47), e2118046119.
- OpenReview. *Using the API*.

## Track A manifest result — 20 September 2026

A deterministic ICLR 2020–2021 cohort manifest now freezes 5,602 records from the broad berenslab ICLR corpus and reconciles identity/decision state against PRRCA. The full frame contains 2,593 records for 2020 and 3,009 for 2021. PRRCA is incomplete and outcome-differential: witness coverage is 91.7% of accepted versus 77.1% of rejected records in 2020, and 91.7% versus 81.8% in 2021. It therefore remains a witness, not the canonical candidate frame.

This completes the two-year manifest, hashing, exclusion accounting, and accepted/rejected coverage requirements, but **does not pass the Track A gate**. The available title, abstract, and keyword values are later snapshots without sufficient evidence that they reproduce the state available at the simulated decision time. They remain `CURRENT_ONLY`. Empirical allocation-policy simulation is still prohibited until at least one usable feature family is `T0_OBSERVED` or `T0_DERIVABLE`.

The next falsifiable step is historical submission-state recovery, not another allocation algorithm: test documented OpenReview revision/version surfaces and provenance-bearing archives for original 2020–2021 submission snapshots. If that recovery fails, narrow the estimand further or ABSTAIN.

## T0 historical revision route — 20 September 2026

The temporal firewall now has a conservative content-recovery path. ResearchArcade's public OpenReview revision index records revision identifiers and OpenReview `tmdate`; OpenReview documents `tmdate` as a true modification timestamp that users cannot set or alter. Restricting the Track A cohort to the latest revision reference no later than the official submission deadline yields 1,816 ICLR 2020 candidates (82.1% of the ACCEPT/REJECT frame) and 195 ICLR 2021 candidates (7.5%). ICLR 2020 coverage is comparatively balanced across historical outcomes (79.9% ACCEPT, 83.0% REJECT); ICLR 2021 coverage is too sparse for a primary comparison.

A deterministic retrieval probe resolved 40/40 sampled historical revision references as public PDFs, and text extraction succeeded on the 20 sampled ICLR 2020 PDFs. This moves the blocker from *whether any T0 content route exists* to *whether bulk acquisition and extraction preserve adequate, non-differential support*.

These references are not yet allocator inputs. They remain `T0_OBSERVED_REVISION_REFERENCE` until the referenced PDF is acquired, hashed and successfully transformed under the frozen extraction protocol. Empirical policy simulation remains prohibited. The next gate is conservative, resumable acquisition of the ICLR 2020 revision PDFs followed by retrieval/extraction missingness analysis by historical decision. The 2020 window is an archival opportunity, not evidence that the same observability holds in other venue-years.

## T0 extraction gate — 20 September 2026

The historical-PDF extraction protocol is frozen before bulk acquisition completes. Extraction is offline, verifies each source PDF hash against the acquisition ledger, preserves whole-document page order, records page-level failures and text-quality warnings, and never uses historical decision labels to change extraction behavior. A separate diagnostic joins decision labels only after extraction to measure missingness.

A ten-PDF smoke test completed 10/10 without extraction or integrity failures. This is an engineering validation only. The ICLR 2020 bulk acquisition is now running under the five-second minimum request interval; empirical policy evaluation remains gated until acquisition completes and decision-stratified retrieval/extraction missingness is audited.

## Outcome-blind candidate representation gate — 20 September 2026

The candidate representation protocol is now frozen before the empirical cohort is complete. To preserve the temporal firewall, the primary representation deliberately avoids pretrained language-model embeddings. It uses only T0 historical PDF text, cohort-internal TF-IDF, deterministic truncated SVD and transparent cosine-geometry descriptors. These geometry measures are operational descriptors, not ground-truth novelty.

A 166-document engineering fixture produced a deterministic 128-dimensional representation with bitwise-identical array outputs across reruns. The fixture remains non-evidentiary. Representation generation is still gated behind the completed acquisition/extraction audit and final frozen eligible cohort; no policy ranking is licensed by this work.

## Track A policy preregistration — 20 September 2026

The first transparent allocation-policy family is frozen before downstream-value outcomes are joined. The primary experiment uses equal candidate-count budgets at 5%, 10%, 20%, 40%, and 80% of the eligible cohort, with six outcome-blind policies: seeded random, centrality, centroid-distance, local-sparsity, greedy k-center coverage, and a fixed 25% exploration-quota mixture. These rules consume only the frozen T0 representation and immutable row identity for tie-breaking.

A 166-document engineering fixture produced exact-budget, duplicate-free, deterministic selections for every policy and budget, with byte-identical outputs across reruns. Pairwise selection overlap was inspected only as an engineering diagnostic. No historical decision or downstream-value outcome was joined. The empirical gate remains closed until bulk acquisition/extraction, decision-stratified missingness, eligible-cohort freeze, and representation regeneration are complete.

## Downstream outcome preregistration — 20 September 2026

The first downstream-recognition proxy and its precision rules are frozen before any policy is scored. The primary outcome is C5: the count of distinct OpenAlex works citing the matched candidate identity cluster during the conservative fixed window 26 September 2019 through 25 September 2024. The primary policy metric is high-recognition recall at the 20% attention budget, where high recognition is prospectively defined as the C5 top decile within the frozen primary matched cohort. The smallest effect of interest is five percentage points absolute recall versus seeded random, with a 10,000-replicate paired bootstrap used for interval estimation.

Metadata-only probes revealed an important identity issue before outcome acquisition: one candidate can appear as multiple OpenAlex work IDs representing preprint, conference, repository or archival manifestations. The primary matching rule therefore forms an exact-normalized-title plus author-overlap identity cluster and unions citing work IDs across cluster members before counting. These probes did not request citation outcomes and were used only to validate matching mechanics.

A network-free linkage-preparation script now builds the evaluation-only query manifest for the 1,816 ICLR 2020 T0 reference candidates. Actual OpenAlex outcome acquisition remains prohibited until the existing feasibility gate passes.

## Frozen downstream execution engine — 20 September 2026

The post-gate downstream engine is now implemented before real outcome inspection. Separate scripts acquire OpenAlex identity metadata, resolve exact-title+author identity clusters, acquire citing-work IDs only inside the frozen five-year window, and evaluate the preregistered policies. Metadata and citation acquisition are hard-gated behind an explicit post-feasibility-gate flag and enforce provider limits plus a configurable cost ceiling.

The identity resolver was tested on synthetic duplicate manifestations, and the evaluator was tested against deterministic synthetic C5 outcomes for the 166-document engineering representation. These tests validated mechanics only. No real citation outcome has been acquired or joined to a policy selection. The entire outcome path therefore remains dormant until the T0 acquisition/extraction missingness gate is adjudicated.

## T0 technical-availability adjudicator — 20 September 2026

The final acquisition/extraction missingness decision rule is now frozen before the live pipeline completes. A primary-usable historical PDF requires successful extraction, at least 1,000 extracted characters and zero page-level extraction errors. PASS requires at least 95% usable retention overall and separately among historical ACCEPT and REJECT strata, with the entire 95% Newcombe-Wilson confidence interval for the ACCEPT-minus-REJECT usable-fraction gap contained inside ±5 percentage points. CONDITIONAL requires at least 90% retention in each stratum with the observed gap inside ±5 points; otherwise the technical gate ABSTAINS.

The ±5-point margin is tied prospectively to the programme's already-frozen five-percentage-point smallest downstream effect of interest. Synthetic complete fixtures exercise PASS, CONDITIONAL and ABSTAIN correctly. The live pipeline is explicitly non-adjudicable until every reference candidate has terminal acquisition and, where required, terminal extraction state.

## Outcome-blind T0 finalization chain — 20 September 2026

The post-acquisition transition is now executable without opening the downstream-outcome box. Once the T0 acquisition/extraction pipeline reaches terminal state, a single finalizer runs the frozen technical-availability adjudicator. PASS or CONDITIONAL permits a deterministic decision-free cohort freeze, regeneration of the historical TF-IDF/SVD representation, and reproduction of the preregistered allocation selections. ABSTAIN stops the chain.

The cohort freezer deliberately strips historical decision labels. The final representation and selection artefacts therefore remain outcome-blind. A 100-document complete fixture exercised the full chain end to end and produced a frozen cohort with no tested decision/review/citation strings, a `FROZEN_T0_REPRESENTATION`, and `FROZEN_T0_POLICY_SELECTIONS`.

Technical completion still does not unlock OpenAlex citation outcomes. The finalizer writes that boundary explicitly: broader outcome-support, entity-resolution, lineage and precision requirements remain to be adjudicated before downstream evaluation can run.

## Prospective design-precision audit — 20 September 2026

The outcome-blind finalizer now performs a precision diagnostic after final policy selections are frozen and before any downstream citation outcome is acquired. Under a design null with exactly the preregistered top-decile count of high-recognition candidates distributed uniformly over the frozen cohort, the variance of each fixed-policy recall difference versus seeded random is determined by cohort size and the symmetric difference between the two selected sets. This permits an outcome-free check against the already-frozen five-percentage-point smallest effect of interest.

The audit is diagnostic rather than a realized power calculation: citation ties and the paired bootstrap can change final interval width. Nevertheless, an obvious failure here is directly relevant to the broader pre-outcome feasibility gate. A 100-document end-to-end fixture correctly flags all five structured-policy contrasts as precision-inadequate, demonstrating that the system can stop or reframe an underpowered claim before acquiring real outcomes.

## OpenAlex identity feasibility — 20 September 2026

Downstream identity observability has now been measured without acquiring citation outcomes. OR-batched exact-title queries reduced 1,816 candidate lookups to 73 OpenAlex requests. The frozen exact-title plus author-overlap rule links 1,693 candidates (93.23%): 528/549 historical ACCEPT candidates (96.17%) and 1,165/1,267 historical REJECT candidates (91.95%). The ACCEPT-minus-REJECT match gap is +4.23 percentage points with a 95% Newcombe-Wilson interval of [+1.84, +6.31] points, so equivalence within the existing ±5-point observability margin is not established.

This is a feasibility finding, not an outcome result. No citation counts or citing-work sets were requested. The exact-match cohort is large enough to remain a candidate substrate, but it is not observability-neutral with respect to historical selection. Any later primary analysis must therefore be explicitly conditional on the matched cohort; unmatched candidates cannot be assigned zero downstream value.

The batching run also exposed and repaired a client-side OpenAlex filter-grammar defect. Unquoted title values containing commas received HTTP 400 and were never admitted as data. Corrected quoted filters were used for retry, and raw provenance was reconciled across 34 valid v0 responses and 39 corrected v1 responses. Multiple OpenAlex manifestations were common enough to validate the preregistered identity-cluster design: 283 matched candidates have two work records and 5 have three.

## Final identity-observability gate — 20 September 2026

The downstream-observability check is now defined on the actual frozen T0 policy substrate rather than only on the pre-finalization candidate frame. After technical finalization, the audit intersects the final decision-free cohort and preregistered selections with the already-frozen exact OpenAlex identity clusters, without reading citation outcomes.

It reports exact-identity support overall and by historical decision, match support for every policy and budget, the expected primary policy-vs-random recall shift that could arise solely from unequal identity observability, prospective precision on the matched substrate, and identity support across centroid-distance and local-sparsity quintiles of the outcome-blind representation. Historical decision remains diagnostic only and never enters allocation.

A 100-document complete fixture exercised the full audit without citation outcomes. Ninety-four identities were observable; expected primary policy-vs-random observability shifts were between -1.06 and +1.06 percentage points, while the small fixture remained precision-inadequate. The live result cannot be adjudicated until the T0 acquisition/extraction pipeline reaches terminal state and the final cohort and policy selections are frozen.

## Resubmission / manuscript lineage audit — 20 September 2026

The outcome-free lineage audit now compares all 1,816 ICLR 2020 T0 candidates against 30,568 later ICLR records from 2021–2026 using a frozen primary exact-title+author rule and a conservative near-title sensitivity rule. The method follows bibliographic record-linkage prior art but retains later records as manuscript lineage rather than collapsing them as duplicates.

Primary exact lineage is rare: 0/549 historical ACCEPT candidates versus 10/1,267 historical REJECT candidates. The ACCEPT-minus-REJECT difference is -0.79 percentage points with a 95% Newcombe-Wilson interval of [-1.45, -0.01] points. Including the frozen near-title sensitivity rule yields 2/549 ACCEPT and 17/1,267 REJECT candidates with lineage, a difference of -0.98 points with interval [-1.82, +0.10]. Both magnitudes are far inside the existing ±5-point materiality margin.

Three historical REJECT candidates have later ACCEPT descendants under the sensitivity rule: *Regularization Matters in Policy Optimization*, *Self-Supervised State-Control through Intrinsic Mutual Information Rewards*, and *Deep symbolic regression*. These concrete cases show why later citation visibility cannot automatically be attributed to the original 2020 manuscript state. They remain flagged for a downstream lineage sensitivity analysis rather than being post-hoc deleted.

Seventeen of nineteen detected lineage edges occur in ICLR 2021, with only one each in 2022 and 2023. The audit is deterministic across reruns and reads no citation, OpenAlex or future-value outcome fields. The next lineage step is mechanical: intersect these frozen flags with the final technically usable cohort and final policy selections after T0 acquisition completes.

## Final lineage substrate gate — 20 September 2026

The manuscript-lineage audit now has a frozen final-substrate stage. After technical acquisition/extraction determines the actual usable T0 cohort and the preregistered policies are regenerated, the final lineage audit re-intersects the already-frozen exact and near-title lineage flags with that cohort and with every policy selection before any citation outcome is opened.

The final gate reports exact lineage, exact-plus-sensitivity lineage and later-ACCEPT lineage overall, by historical decision, and by policy/budget. At the primary 20% attention budget, every structured policy is compared with seeded random using the existing ±5 percentage-point materiality margin. Historical ACCEPT/REJECT balance also requires the full Newcombe-Wilson interval to lie inside ±5 points for both exact and sensitivity lineage.

A 100-document complete fixture exercised the gate without citation outcomes. It contained one exact-lineage and two sensitivity-lineage candidates. Policy-vs-random lineage differences were at most five percentage points, while historical-decision equivalence was intentionally not declared because the small fixture produced a wide confidence interval. This is the desired behavior: small samples do not earn false reassurance.

## Broader pre-outcome feasibility adjudicator — 20 September 2026

The programme now has a single fail-closed adjudicator that combines the frozen technical, identity-observability, lineage, coverage, construct and precision evidence before any real citation outcome can be acquired. It SHA-256 binds every input and emits `PASS_PRE_OUTCOME`, `CONDITIONAL_PASS_PRE_OUTCOME`, or `ABSTAIN_PRE_OUTCOME`, plus an explicit boolean controlling whether citation acquisition is authorized.

PASS requires the fully frozen outcome-blind T0 representation and selections, nonzero exact identity support in both historical decision strata and every primary policy selection, acceptable observability and lineage behavior, the fixed 2019-09-26 through 2024-09-25 C5 window, construct non-circularity, and prospective precision for the frozen five-percentage-point smallest effect. Historical observability or lineage imbalance can yield a conditional exact-matched-cohort claim only when the actual primary policy contrast remains inside the frozen materiality bound. No precision-adequate primary contrast means ABSTAIN.

A complete 100-document fixture demonstrates the intended behavior. It passes temporal integrity, exact identity support, entity resolution, fixed coverage and construct checks, while carrying technical/observability/lineage restrictions. Because 0/5 primary contrasts are prospectively precise enough for the frozen five-point effect, the adjudicator returns `ABSTAIN_PRE_OUTCOME` and leaves citation acquisition unauthorized. A negative feasibility verdict is therefore operationally real rather than merely stated in prose.

## Fail-closed post-gate outcome runner — 20 September 2026

The downstream execution path is now complete but dormant. A single wrapper reads the broader pre-outcome adjudication and exits before network activity unless citation acquisition is explicitly authorized by `PASS_PRE_OUTCOME` or `CONDITIONAL_PASS_PRE_OUTCOME`. An ABSTAIN verdict cannot accidentally be overridden by passing a convenience flag to the citation script.

When authorized, the preferred OpenAlex acquirer batches up to 100 exact identity work IDs under one `cites` OR filter and asks each returned citing work for `referenced_works`. This allows the response to be attributed back to the exact frozen candidate identities while preserving the preregistered C5 definition. Raw pages, batch membership hashes, provider cost and network-attempt counts are frozen. The default total provider budget is $0.09, and a partial run stops and remains resumable rather than changing the protocol or silently dropping candidates.

After complete C5 acquisition, the unchanged frozen evaluator runs the primary comparison. Two mandatory lineage sensitivity views are then evaluated with identical machinery: one excludes every exact/near-lineage candidate and one excludes only candidates with a later ACCEPT descendant. The views hard-link or byte-copy frozen outcomes; they do not recalculate or transform outcome values.

Pre-outcome validation confirms the firewall: an ABSTAIN fixture performs zero network activity; an authorized fixture with a sub-request cost cap also performs zero network activity and reports a partial state; synthetic page attribution correctly assigns and deduplicates citing works across target identities. Real Track A citation outcomes remain unopened pending the live broader gate.

## Track A v0.1 terminal feasibility result — 20 September 2026

Track A v0.1 has reached its frozen pre-outcome verdict: `ABSTAIN_PRE_OUTCOME`. The historical acquisition itself is excellent: 1,815/1,816 T0 candidates are primary-usable, with 549/549 historical ACCEPT and 1,266/1,267 historical REJECT candidates retained. Exact OpenAlex identity support on that final cohort is 1,692/1,815 (93.22%). Historical decision-linked identity neutrality is not established, but the actual frozen policies differ from seeded random by only -0.30 to -0.65 percentage points of expected recall due solely to identity availability. Final lineage balance also passes, with 10 exact lineage candidates, 19 under the conservative sensitivity rule and three later-ACCEPT descendants.

The decisive failure is prospective precision. At N=1,815 and a 20% attention budget, the five structured policy-vs-random primary contrasts have 95% design half-widths between 7.71 and 7.93 percentage points, wider than the frozen five-point smallest effect of interest. Zero of five comparisons are precision-adequate. The broader adjudicator therefore prohibits citation acquisition. The real post-gate runner was executed against this verdict and recorded `network_activity_started=false`; the C5 outcome remains sealed.

This is the programme's first substantive negative feasibility result. It does not imply that the policies have no effect. It establishes that the v0.1 ICLR 2020 design cannot resolve the effect size it promised to distinguish. The firewall therefore prevented a potentially interesting but underpowered outcome from being opened and retrospectively rationalized.

## Track A v0.2 prospective redesign — 20 September 2026

Using only the outcome-blind v0.1 policy-overlap geometry, an exact-observable matched N of roughly 4,321–4,571 would be required to bring the prospective 95% recall-difference half-width to five percentage points. v0.2 therefore targets at least 4,600 exact-outcome-observable candidates, with acquisition margin above that floor.

The current design draft proposes year-stratified ICLR 2017–2021 cohorts. The frozen metadata contains 7,496 ACCEPT+REJECT records across those five years before T0-revision, technical and identity gates. Policies will be selected independently within each year at the same 20% budget, and high recognition will be defined within year over an equal five-year follow-up horizon. The next stage is metadata-only: establish conservative historical deadlines, recover the revision index, build candidate counts and rerun the prospective precision gate before downloading another multi-year PDF corpus. The v0.1 citation box remains unopened.

## Track A v0.2 source-feasibility gate — 20 September 2026

The metadata-only v0.2 source gate has now produced a stopping result before any new bulk PDF or citation acquisition. Historical snapshot audits identified clean pre-review Git snapshots for ICLR 2018 and ICLR 2019. The first ICLR 2018 snapshot is approximately 103.1 hours after the conservative paper deadline and retains extracted anonymous text for 826/828 ACCEPT+REJECT candidates; the first ICLR 2019 snapshot is approximately 91.9 hours after deadline and retains all 1,419 candidates. Neither snapshot contains official reviews, public/official discussion comments, or decision records. They are therefore useful pre-review historical states, but not proof of the exact submission-deadline state; post-deadline edits before capture remain a declared temporal sensitivity.

The ResearchArcade revision export is no longer treated as a denominator for historical-state availability. Its explicit revision references remain valid positive provenance evidence, but legacy base states can be absent from the export, which explains the otherwise implausible zero pre-deadline candidates for 2017–2019 under a naive filter.

A separate ICLR 2021 source audit disqualified the archived `reviewed_version_(pdf)` route. Among all 2,594 ACCEPT+REJECT candidates with archived root notes, the field exists for 0/859 historical ACCEPT candidates and 1,735/1,735 historical REJECT candidates. This perfect selection linkage makes it inadmissible as a neutral primary historical-text source regardless of its convenience.

The currently verified pre-review/decision-time candidate upper bound is therefore 4,060: 826 from ICLR 2018, 1,419 from ICLR 2019 and the frozen 1,815-candidate ICLR 2020 v0.1 T0 cohort. Even granting every one of the 442 ICLR 2017 ACCEPT+REJECT records as an optimistic perfect historical source yields only 4,502 candidates, still 98 below the prospective 4,600 exact-outcome-observable target before technical or identity attrition. The gate returns `SOURCE_FEASIBILITY_INADEQUATE_NEUTRAL_COHORT_REQUIRED`, with bulk content acquisition and citation acquisition both prohibited.

The next critical path is neutral historical-state recovery for ICLR 2021 or an explicitly preregistered additional cohort/venue. A support request has been sent to OpenReview asking for immutable ICLR 2021 deadline-state revisions, a documented legacy revision-reference retrieval route, or a complete public pre-review archive. The v0.1 C5 outcome remains sealed.
