# Memory Palace Session: Formal Boundary / Null-Hypothesis Test for Agalmic Research

**Session ID:** `ar-session-2026-09-08-agalmic-formal-null-test`  
**Date:** 8 September 2026  
**Platform:** ChatGPT  
**Machine participant:** GPT-5.6 Sol  
**Human participant:** Human curator  
**Project:** Agalmic Research  
**Status:** exploratory / adversarial formalization and lineage test  
**Publication sensitivity:** open  
**Protocol:** Agalmic Research Memory Palace Protocol v0.3 + Research Provenance Protocol v0.1

## Session objective

Continue the adversarial boundary review by testing the null hypothesis proposed at the end of the preceding session:

> **H0: “Agalmic transition” adds no explanatory, predictive or measurement value beyond existing production economics, growth and innovation theory, operations/constraint research, resource economics, public-goods economics, industrial organization and socio-technical transition studies.**

The purpose of this session is not to rescue the label. It is to determine what, if anything, remains after translating the candidate Agalmic claims into established formalisms and measurement traditions.

## Starting epistemic state

Inherited from `ar-session-2026-09-08-agalmic-boundary-review`:

- Agalmic Research as a new economic theory: **not supported**.
- Agalmic Research as an alternative to economics: **rejected**.
- Recursive constraint displacement as novel: **rejected as novelty**.
- AI abundance creating human bottlenecks as novel: **rejected as novelty**.
- “Worthwhile futures” as a field-defining analytical objective: **contested and recommended for removal from the field definition**.
- Distinct interdisciplinary programme centred on transitions into and out of functional abundance: **plausible candidate, not established**.

## Search and comparison boundary

This tranche inspected or re-inspected the following literature families and representative antecedents:

- endogenous growth and non-rival knowledge;
- directed technical change;
- public-goods and club-goods theory;
- information goods and near-zero marginal reproduction cost;
- natural-resource scarcity indicators;
- complementarity, weak links and production networks;
- general-purpose technologies and growth bottlenecks;
- rebound effects / Jevons paradox;
- Growth Diagnostics;
- Theory of Constraints;
- socio-technical transition studies;
- original Agalmics lineage;
- contemporary post-scarcity / AI-abundance work.

This remains a targeted adversarial review rather than an exhaustive systematic review of EconLit, JSTOR, Scopus, Web of Science, non-English scholarship, all operations-research literature or all institutional-economics literature.

---

# 1. Formal representability test

## Candidate Agalmic claim

A technological, epistemic or institutional change can make one constraint sufficiently less binding that another constraint becomes decisive.

### Minimal standard model

Let a system choose inputs or capacities `x = (x1, ..., xn)` to maximize:

`V = B(F(x)) - Σ p_i x_i`

subject to:

`0 <= x_i <= K_i`.

Here:

- `F(x)` is output or realized capability;
- `B(.)` is benefit/utility/value from realized capability;
- `p_i` is the unit cost of input `i`;
- `K_i` is an upper capacity/supply constraint;
- `λ_i` is the Kuhn-Tucker shadow value of relaxing `K_i`.

For a binding constraint `j`, the first-order condition implies, schematically:

`λ_j = B'(F) F_j - p_j`.

Suppose technological change expands `K_k` or lowers `p_k` for another input `k`. Holding the rest of the adjustment path aside for the moment, the effect on the shadow value of a constrained complement `j` contains the terms:

`dλ_j / dK_k = B''(F) F_k F_j + B'(F) F_jk`.

The sign is not generally fixed.

- If `F_jk > 0` and technological complementarity is strong enough, relaxing `k` can increase the marginal value of scarce `j`.
- If the inputs are substitutes, or the concavity/demand term dominates, the shadow value of `j` can fall.
- If `j` has highly elastic supply, it may expand rather than become an economically salient bottleneck.
- If cheaper `k` induces sufficient additional demand, total use of both `k` and its complements can rise.

## Adversarial result

**The general scarcity-displacement mechanism requires no new Agalmic primitive.** It is representable with ordinary constrained optimization, complementarity/substitutability, shadow prices and demand responses.

The broad proposition “relaxing one constraint can make another more important” is therefore not a new theorem. It is conditional comparative statics.

### Epistemic consequence

`H0` is **not rejected** on formal explanatory novelty.

### Relevant antecedents

- Romer, P. M. (1990), *Endogenous Technological Change*, Journal of Political Economy 98(5), DOI `10.1086/261725`.
- Acemoglu, D. (2002), *Directed Technical Change*, Review of Economic Studies 69(4), DOI `10.1111/1467-937X.00226`.
- Jones, C. I. (2011), *Intermediate Goods and Weak Links in the Theory of Economic Development*, AEJ: Macroeconomics 3(2), DOI `10.1257/mac.3.2.1`.
- Acemoglu, D., Autor, D., Patterson, C. (2024), *Bottlenecks: Sectoral Imbalances and the US Productivity Slowdown*, NBER Macroeconomics Annual 38, DOI `10.1086/729196`.

---

# 2. Recursive constraint-removal test

The candidate process:

`identify binding constraint -> relax constraint -> observe successor constraint -> repeat`

is almost directly anticipated by two mature approaches.

## Growth Diagnostics

Hausmann, Rodrik and Velasco frame development diagnosis around identifying binding constraints to growth. Rodrik (2010) explicitly describes successful practice as repeatedly identifying the most binding constraints and removing them with locally appropriate remedies.

## Theory of Constraints

Goldratt's focusing process identifies the system constraint, exploits it, subordinates the rest of the system, elevates it, and returns to identification if the constraint is broken.

## Adversarial result

Recursive displacement is **established antecedent**, not a distinctive Agalmic research algorithm.

### Epistemic consequence

`H0` is **not rejected** on recursive process novelty.

Sources:

- Hausmann, R., Rodrik, D., Velasco, A. (2005), *Growth Diagnostics*.
- Rodrik, D. (2010), *Diagnostics before Prescription*, Journal of Economic Perspectives 24(3), DOI `10.1257/jep.24.3.33`.
- Goldratt / Theory of Constraints focusing-step literature.

---

# 3. Non-rivality and near-zero marginal cost test

Original Agalmics is anchored in non-scarce goods: goods that can be transferred or copied without materially diminishing the holder's own supply. Modern economics already has powerful machinery for this territory.

## Non-rival knowledge

Romer's growth model explicitly treats technological knowledge as a **non-rival, partially excludable** input. Non-rivality creates non-convexity and changes the relevant market structure; it does not lie outside economics.

## Public and club goods

Public-goods theory distinguishes rivalry from excludability. Club-goods theory covers goods that may be non-rival up to congestion while remaining excludable.

## Information goods

Information-economics treatments emphasize high fixed cost and very low marginal reproduction cost. Low reproduction cost does not imply zero price, universal access or absence of market power.

## Adversarial result

Neither non-rivality nor near-zero marginal reproduction cost supplies a hard disciplinary boundary from economics.

However, these concepts remain valuable **dimensions** for describing how the economic character of a capability changes.

### Epistemic consequence

`H0` is **not rejected** on non-rivality / low-marginal-cost theory.

Representative sources:

- Romer (1990), DOI `10.1086/261725`.
- Samuelson public-goods lineage.
- Buchanan, J. M. (1965), *An Economic Theory of Clubs*, Economica 32(125), DOI `10.2307/2552442`.
- Shapiro, C. & Varian, H. R. (1999), *Information Rules*.

---

# 4. Successor-scarcity propagation test

A stronger candidate was that Agalmic Research might uniquely study how scarcity moves across linked systems after a focal abundance shock.

This also encounters strong antecedents.

## Production networks

Production-network economics explicitly studies how shocks propagate through input-output linkages and how microeconomic changes generate macroeconomic effects.

Jones (2011) models complementarity and weak links. Carvalho and Tahbaz-Salehi (2019) review the production-network literature as a mature field. Acemoglu, Autor and Patterson show empirically how uneven technological progress can itself create endogenous innovation bottlenecks across supplier and idea networks.

## General-purpose technologies

Bresnahan and Trajtenberg's GPT framework makes complementary innovation central: a major enabling technology does not automatically realize its potential because downstream and upstream complements must co-evolve.

## Adversarial result

“Successor scarcity propagates across a network of complements” is not by itself a new mechanism.

### Epistemic consequence

`H0` is **not rejected** on network-propagation novelty.

Representative sources:

- Bresnahan, T. F. & Trajtenberg, M. (1995), *General Purpose Technologies: Engines of Growth?*, Journal of Econometrics 65(1), DOI `10.1016/0304-4076(94)01598-T`.
- Jones (2011), DOI `10.1257/mac.3.2.1`.
- Carvalho, V. M. & Tahbaz-Salehi, A. (2019), *Production Networks: A Primer*, Annual Review of Economics 11, DOI `10.1146/annurev-economics-080218-030212`.
- Acemoglu, Autor & Patterson (2024), DOI `10.1086/729196`.

---

# 5. Rebound and induced-demand test

A focal capability becoming cheaper may expand its use so much that total resource use, or use of a complement, does not fall as expected.

This is established terrain.

Energy economics has a long literature on the rebound effect and Jevons paradox. Efficiency lowers the effective price of an energy service, inducing more use and potentially offsetting expected resource savings. Modern reviews distinguish direct, indirect and economy-wide rebound mechanisms.

The recent AI-abundance literature applies a structurally similar mechanism to expert judgment: cheaper generation can induce more candidate production and recreate review scarcity.

## Adversarial result

“Abundance can recreate scarcity through induced demand” is an established mechanism family.

### Epistemic consequence

`H0` is **not rejected** on induced-demand novelty.

Representative sources:

- Greening, L. A., Greene, D. L., Difiglio, C. (2000), *Energy efficiency and consumption — the rebound effect — a survey*, Energy Policy 28, DOI `10.1016/S0301-4215(00)00021-5`.
- Gillingham, K., Rapson, D., Wagner, G. (2016), *The Rebound Effect and Energy Efficiency Policy*, Review of Environmental Economics and Policy 10(1), DOI `10.1093/reep/rev017`.
- Wu, C. (2026), *When AI Abundance Recreates Scarcity*, SSRN 7183798.

---

# 6. Scarcity-measurement test

The most promising surviving wedge was measurement: perhaps Agalmic Research could supply a cross-domain way to identify when something has moved from scarcity toward functional abundance.

The adversarial search weakens any claim that scarcity measurement itself is new.

Natural-resource economics has a long debate over indicators including:

- price;
- scarcity rent;
- unit cost;
- marginal discovery/extraction cost;
- supply elasticity;
- productivity / inverse multifactor productivity;
- physical or energetic constraints.

Stern's synthesis is particularly important because it explicitly argues that no single indicator captures every dimension of social scarcity and recommends empirical models and scenarios rather than pursuit of one perfect measure.

Public-goods and club-goods theory add orthogonal dimensions such as rivalry, excludability and congestion.

Industrial organization adds market power and concentration. Information economics adds replication cost and fixed-cost structure. Resource/environmental economics adds externalities and depletion. Production theory adds complementarity and substitution.

## Adversarial result

A scalar **Agalmic Abundance Index** would currently be poorly justified. It would combine heterogeneous dimensions with arbitrary weights and risk hiding the exact bottleneck that the programme wants to expose.

A more defensible contribution is a **non-scalar scarcity transition profile** that preserves the dimensions separately.

### Candidate profile

For a capability `g` at time `t`, record a vector such as:

`S_g(t) = [m, e, r, x, q, c, a, z, h]`

where, operationalized per domain:

- `m`: marginal resource/production cost of an additional usable unit;
- `e`: supply elasticity or scalable capacity over the relevant demand range;
- `r`: rivalry intensity;
- `x`: excludability and practical access friction;
- `q`: congestion / queueing burden;
- `c`: dependence on scarce complementary inputs;
- `a`: attention, expertise, verification or assimilation burden required for useful consumption;
- `z`: externalized ecological, physical or social resource burden;
- `h`: concentration/control over the limiting layer.

This notation is a **research convenience, not a claimed new theory or index**.

Do not aggregate these components into one score unless a specific empirical application supplies defensible units and weights.

### Candidate transition definition

A **scarcity transition** can provisionally be treated as a durable change in one or more components of `S_g(t)` large enough to change how access, rationing, production or use is organized in the domain under study.

The key empirical object is then:

`ΔS_g = S_g(t1) - S_g(t0)`

plus a record of which other capabilities' profiles changed after the focal shock.

This supports comparison without pretending that rivalry, price, attention and ecological burden are commensurable.

### Epistemic consequence

`H0` is **not rejected yet** on measurement novelty, but a residual research opportunity remains:

> Is there a useful, empirically reproducible cross-domain protocol for observing scarcity-character transitions that integrates established measures without collapsing them into a misleading scalar?

Classification: **candidate synthesis / measurement operationalization; novelty unassessed**.

Representative sources:

- Brown, G. M. & Field, B. C. (1978), *Implications of Alternative Measures of Natural Resource Scarcity*, Journal of Political Economy 86(2), DOI `10.1086/260664`.
- Stern, D. I. (1996), *The Theory of Natural Resource Scarcity Indicators: Towards a Synthesis*.
- Stern, D. I. (1999), *Use value, exchange value, and resource scarcity*, Energy Policy 27(8), DOI `10.1016/S0301-4215(99)00043-9`.

---

# 7. Predictive novelty test

The session attempted to derive predictions that would be uniquely Agalmic.

## Candidate prediction A

After a large fall in the cost of focal input `k`, rents or shadow values move toward complements with low supply elasticity.

**Status:** already implied by standard complementarity, scarcity-rent and bottleneck reasoning.

## Candidate prediction B

Making a capability cheap increases demand enough to recreate congestion or complement scarcity.

**Status:** rebound / induced-demand antecedent.

## Candidate prediction C

When a non-rival capability becomes cheap to reproduce, value capture shifts toward excludable complements or control points.

**Status:** information economics, complementary-assets theory and industrial organization antecedents.

## Candidate prediction D

Unbalanced technological progress creates bottlenecks elsewhere in the production/innovation network.

**Status:** directly anticipated by production-network and bottleneck literature.

## Candidate prediction E

Technical abundance may coexist with access scarcity where legal exclusion, concentration, congestion or scarce complements remain.

**Status:** public-goods, club-goods, IP and industrial-organization antecedents.

## Candidate prediction F

A sufficiently large multidimensional scarcity transition changes the dominant allocation or coordination institution around a capability.

**Status:** interesting but under-specified. Institutional economics and transition studies are likely antecedent families. It is not currently a defensible novel prediction.

## Adversarial result

No unique cross-domain prediction was established in this tranche.

### Epistemic consequence

`H0` is **not rejected** on predictive novelty.

---

# 8. What survives the null test?

The null survives on three strong interpretations:

1. **new economic mechanism** — not supported;
2. **new formal theory of bottleneck displacement** — not supported;
3. **new predictive law** — not supported.

The surviving object is weaker but still potentially useful:

> **Agalmic Research may be defensible as a problem-oriented comparative research programme that studies how the scarcity profile of a capability changes, especially when replication, marginal production cost or scalable supply changes sharply, and systematically traces the successor scarcities, access constraints, rents and externalities that emerge around that transition.**

This would be an interdisciplinary synthesis programme, not an alternative economics.

Its value would have to come from **comparison, operationalization and empirical accumulation**, not from renaming familiar mechanisms.

---

# 9. Relationship to original Agalmics

Robert Levin's 1999 formulation remains an important anchor:

> agalmics: the study and practice of the production and allocation of non-scarce goods.

Levin also explicitly recognized that non-scarce goods can require scarce inputs to produce, using programmer time and free software as an example.

The defensible modern extension is therefore not “economics studies scarcity; Agalmics studies abundance.” Modern economics already studies non-rival goods and changing constraints.

A narrower extension is:

> **Original Agalmics begins with the existence of non-scarce goods. Agalmic Research asks how goods or capabilities enter, leave or only appear to enter such states, and what scarce complements still condition their production, access and useful employment.**

This is a lineage-positioned extension, not a claim that Levin or economics omitted all of these mechanisms.

Source for the historical formulation: Robert Levin, *The Marginalization of Scarcity* (1999), preserved in historical mirrors and discussion archives.

---

# 10. Candidate empirical programme

The next useful test is empirical rather than definitional.

## Pilot question

Can the same non-scalar scarcity-transition profile produce useful, non-trivial comparisons across domains with very different technologies and institutions?

## Candidate cases

Choose cases with large, independently documented cost/scalability shocks and observable successor bottlenecks. Suitable candidates include:

1. **Digital copying / software distribution** — reproduction cost and rivalry collapse; investigate attention, maintenance, support, IP, platform control and discovery.
2. **Genome sequencing** — dramatic cost decline; investigate interpretation, clinical validation, data governance and expert capacity.
3. **Solar photovoltaic generation** — major cost decline; investigate grid connection, storage, transmission, permitting, land and intermittency.
4. **Generative AI inference / content generation** — dramatic fall in candidate-generation cost; investigate verification, trusted signal, compute/energy, human review and institutional legitimacy.

The first three offer longer historical windows. Generative AI is useful as a live case but should not carry the initial empirical claim by itself.

## Minimum variables

For each case, pre-register domain-valid proxies for:

- unit/marginal cost trajectory;
- supply/capacity elasticity or scaling rate;
- access price and effective access population;
- rivalry/congestion regime;
- focal output/use volume;
- complement cost or delay shares;
- queues / waiting times where meaningful;
- concentration or control at key complements;
- externalized resource burden;
- institutional changes surrounding access and allocation.

## Success criterion

The comparative protocol earns a place in the programme if it reveals reproducible transition patterns or distinctions that are hard to see when each case is described only in its native literature.

## Failure criterion

Retire or absorb the framework into existing disciplines if the profile merely restates ordinary domain metrics without improving comparison, diagnosis, hypothesis generation or empirical prediction.

---

# 11. Field-status verdict after the formal null test

| Claim | Verdict |
|---|---|
| Agalmic Research is a new economic theory | **Rejected on current evidence** |
| Agalmic Research is an alternative to economics | **Rejected** |
| Constraint displacement is a novel mechanism | **Rejected as novelty** |
| Successor-scarcity propagation is uniquely Agalmic | **Rejected as novelty** |
| A scalar abundance index is presently justified | **Rejected** |
| A non-scalar scarcity-transition profile may be useful | **Plausible; novelty and utility unassessed** |
| Agalmic Research can be a comparative interdisciplinary programme | **Plausible, conditional on empirical utility** |
| Original Agalmics remains useful lineage | **Supported** |
| “Worthwhile futures” belongs in the analytical field definition | **No; better treated as institutional/ethical selection criterion** |

The strongest current epistemic status is therefore:

> **candidate interdisciplinary research programme; distinctive empirical and measurement value not yet demonstrated.**

---

# 12. Consequence for the canonical definition

The current canonical v0.2 definition remains **contested by accumulated evidence**.

This tranche deliberately does not rewrite it. The null test was intended to determine whether a replacement has intellectual support before promotion.

The evidence now supports a subsequent definition revision that should:

1. remove “worthwhile futures” from the analytical field definition;
2. explicitly state that Agalmic Research is not an alternative to economics;
3. anchor the programme in original Agalmics and the study of non-scarce goods;
4. describe the modern extension as comparative study of transitions in scarcity profiles and successor scarcities;
5. avoid claiming a new economic law, scalar abundance metric or unique bottleneck mechanism;
6. preserve “worthwhile futures” only as a criterion governing the institution's own research selection, if retained at all.

Promotion should be a separate decision event.

---

# 13. Epistemic handoff

The remaining boundary question now requires stronger external authority than the current contributors possess.

Recommended expertise:

- microeconomic / production theory;
- public economics and information economics;
- natural-resource and environmental economics;
- industrial organization;
- innovation economics and production networks;
- measurement / index-number theory;
- economic history of technological cost collapse;
- socio-technical transition studies.

The strongest handoff question is:

> **Does a non-scalar scarcity-transition profile and cross-domain comparative programme identify a coherent research object that existing literatures do not already study together, and can it support reproducible empirical work without smuggling normative judgments into the definition of abundance?**

---

# 14. Discovery Event Ledger

## Event 01 — null hypothesis adopted

- **Contributor:** human curator accepted the adversarial next step; machine participant formulated and executed the structured test.
- **Before:** candidate programme distinctiveness.
- **After:** formal null under active examination.
- **Epistemic status:** exploratory.

## Event 02 — standard optimization representation

- **Contribution:** machine participant translated scarcity displacement into an ordinary constrained optimization / shadow-price model.
- **Result:** no unique formal primitive required.
- **Status change:** formal-mechanism novelty weakened to established antecedents + synthesis.

## Event 03 — network and rebound antecedents

- **Contribution:** literature comparison across production networks, GPTs and rebound economics.
- **Result:** successor scarcity and induced demand are mature mechanism families.
- **Status change:** predictive novelty weakened.

## Event 04 — scalar metric rejected

- **Contribution:** adversarial comparison with scarcity-indicator and public-goods literatures.
- **Decision:** do not create a one-number abundance index.
- **Reason:** heterogeneous dimensions and arbitrary weighting would conceal rather than expose scarcity.
- **Reversal condition:** a specific empirical application supplies validated commensuration and demonstrates predictive/diagnostic value.

## Event 05 — non-scalar profile retained

- **Contribution:** machine synthesis constrained by prior art.
- **Decision:** retain a scarcity-transition profile only as a candidate comparative research instrument.
- **Novelty:** unassessed.
- **Reversal condition:** retire if a mature existing framework already performs the same cross-domain function or pilot studies add no analytical value.

## Event 06 — canonical definition remains unmodified

- **Decision:** preserve the contested v0.2 definition during the null-test tranche rather than conflate research evidence with promotion.
- **Next decision:** separate definition revision after review of this result.

---

# 15. Roads Not Taken Register

## Rejected after examination

- “Economics allocates scarcity; Agalmics transforms constraints.”
- Recursive constraint removal as the novel core mechanism.
- Successor scarcity propagation as uniquely Agalmic.
- Non-rivality as outside economics.
- A scalar Agalmic Abundance Index.
- “Worthwhile futures” as the field's analytical objective.

## Deferred

- Full general-equilibrium formalization of the scarcity-transition profile.
- A cross-domain empirical pilot.
- Definition v0.3 promotion.
- Construction of a public dataset of historical abundance transitions.
- Econometric identification strategy for successor-scarcity effects.

## Surfaced but unexamined

- Transaction-cost economics as an account of allocation-regime changes.
- Mechanism-design approaches to abundance and access.
- Complexity-economics measures of regime transition.
- Index-number theory for partial comparability without scalarization.
- Economic-history literature on radical price decline and dematerialization.
- Commons-governance literature as a bridge between non-rivality and institutional access.

## Excluded by scope

- Patent prior-art search.
- Normative theory of socially desirable abundance.
- Constitutional Attention as a societal governance system.
- Implementation in Nemosyne/Moneta.

> **Unknown or never-surfaced alternatives are not represented in this graph. Their absence must not be interpreted as rejection.**

---

# Closeout

## Final authority status

The session result is **curator-defended exploratory synthesis**, not expert-reviewed economic theory.

## Null-hypothesis result

**H0 is not rejected for explanatory theory or prediction.**

**H0 remains open for measurement/comparative research utility.** The only defensible residual contribution is a candidate non-scalar, cross-domain research protocol for studying transitions in scarcity characteristics and tracing successor scarcity.

## Recommended next action

Do not attempt another universal economic law. Run a small empirical comparative pilot and seek external economics/measurement review. If the profile fails to add insight beyond native domain frameworks, narrow Agalmic Research back toward original Agalmics and treat the wider programme as an institutional research theme rather than a distinct field.
