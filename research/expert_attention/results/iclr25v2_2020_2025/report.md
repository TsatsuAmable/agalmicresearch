# ICLR Expert-Attention Preservation Audit: Phase 1

Dataset: Berenslab ICLR `25v2`
SHA-256: `48215679d54ea788b8dfc1177850845f047c5810554708273b617b67ce321859`

## Data audit

- Rows in analysis slice: **33,043**
- Rows with interpretable final decisions: **33,043**
- Rows with at least one parsed reviewer score: **32,604**
- Rows with a non-`unlabeled` topic: **17,983**
- Median within-paper reviewer-score SD: **1.000**
- 90th-percentile disagreement threshold: **1.789**

Resolved source columns:
```json
{
  "year": "year",
  "decision": "decision",
  "scores": "scores",
  "topic": "labels",
  "paper_id": "id"
}
```

## Construct-validity diagnostic

Reviewer scores and decisions are post-review outcomes. They are used here only to diagnose
measurement behaviour and to construct intentionally leaky comparison policies. They are not
candidate features for a deployable pre-review triage system.

Among score/year cells with enough topic observations, the largest observed
topic-to-topic acceptance-rate spread at approximately the same mean reviewer score was
**36.6%** in this dataset slice.

## 20% expert-attention budget stress test

| Policy | Accepted recall | High-disagreement recall | Worst topic recall |
|---|---:|---:|---:|
| random | 20.0% | 19.9% | 13.8% |
| post_review_raw_score_DIAGNOSTIC_ONLY | 60.8% | 10.0% | 11.3% |
| post_review_topic_normalized_score_DIAGNOSTIC_ONLY | 60.2% | 10.0% | 16.5% |

Interpretation rule: a policy does not become desirable merely because it preserves accepted
papers. If accepted-paper recall rises by sacrificing disagreement or starving some topics,
it is evidence of gatekeeping mimicry rather than successful scarcity displacement.

## Outputs

- `yearly_summary.csv`: counts, acceptance, scores, and disagreement by year.
- `topic_year_summary.csv`: the same quantities by topic and year.
- `score_conditional_topic_spread.csv`: acceptance variation across topics at similar scores.
- `preservation_frontier.csv`: random, raw-score, and topic-normalized-score stress tests.

## Next empirical step

Freeze these descriptive diagnostics, then build pre-review baselines using only information
available before expert review: title, abstract, keywords/topic, and claim/evidence descriptors.
Evaluate them on temporal splits. Add OpenAlex downstream outcomes only after the immediate
preservation behaviour is understood.
