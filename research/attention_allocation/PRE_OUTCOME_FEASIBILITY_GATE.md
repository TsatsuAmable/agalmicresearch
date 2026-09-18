# Pre-outcome Feasibility Gate v0.1

Frozen before substantive allocation-policy outcomes are computed.

## PASS requires all of the following

1. **Temporal integrity:** every policy feature has auditable decision-time provenance; any unresolved field is quarantined. Automated leakage tests find no FUTURE_OUTCOME field reachable from policy matrices.
2. **Outcome support:** both historically selected and non-selected submissions have nonzero longitudinal outcome observability in every year retained for primary comparison. Any stratum violating support is excluded before policy fitting, not repaired by extrapolation.
3. **Differential observability is modelled, not ignored:** report match/outcome-observation probability by year, historical decision and available metadata. If decision remains a strong predictor of observability after decision-time covariates, primary claims are restricted to observable-outcome recovery unless a separately justified identification strategy is supplied.
4. **Entity resolution:** primary analyses use only unambiguous exact/persistent-ID matches or independently validated high-confidence matches. Ambiguous matches are quarantined. Sensitivity analysis must reproduce conclusions on exact/persistent-ID-only records where sample support permits.
5. **Lineage:** detected resubmissions cannot appear as independent candidates in the same primary evaluation without a declared lineage rule. Alternative defensible lineage rules are a required sensitivity analysis.
6. **Coverage window:** every outcome used in a primary comparison has the same fixed follow-up horizon for all included cohorts.
7. **Construct non-circularity:** no variable used to define future epistemic value may also enter the allocation policy for that simulated decision unless it was genuinely available then.
8. **Power/precision:** before policy comparison, simulation size and uncertainty procedure are fixed from corpus size and a smallest-effect-of-interest stated in natural units. If precision cannot distinguish that effect from noise, ABSTAIN rather than reinterpret a wide interval.

## CONDITIONAL PASS

Use when the conditions hold only for a prospectively defined subset, outcome family or claim class. The excluded scope must be stated before policy results are inspected.

## ABSTAIN

Required for unresolved temporal leakage; absent comparison support; outcome observability dominated by historical selection without defensible restriction/identification; circular value construction; irreducible lineage ambiguity affecting the primary contrast; or inadequate precision.

## Why there is no universal matching-percentage threshold

A single post-hoc percentage would hide the actual identification problem. Ninety percent overall matching can still be unusable if nearly all unresolved cases are rejected papers. Conversely, lower balanced coverage can support a carefully restricted descriptive estimand. The gate therefore evaluates support, differential missingness, temporal integrity and estimand scope jointly.

This gate does not license causal claims that acceptance would have caused rejected work to realise its observed future value.
