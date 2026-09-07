# Literature Review: Epistemic Handoff, Knowledge Brokering and Uptake

Version: 0.1  
Status: deep prior-art review / working research note  
Date: 7 September 2026

## Question

What, if anything, is distinctive about Agalmic Research's idea of **epistemic handoff**: preserving a low-authority initiator's contribution while routing a candidate claim or research object toward actors able to supply missing expertise, validation, integration or realization?

The literature shows that the general problem of routing knowledge across people, organizations and expertise boundaries is old and well developed. The strongest defensible contribution is therefore a much narrower one: a **claim-sensitive, provenance-preserving handoff protocol for machine-assisted candidate knowledge**, explicitly separating contribution from epistemic authority.

## Bottom line

> **Generic knowledge handoff, brokerage, transfer, boundary spanning and absorptive capacity are established. “Epistemic handoff” should be local terminology for a narrower protocol, not a newly discovered institution.**

The most relevant antecedent families are:

- absorptive capacity;
- knowledge transfer and transfer stickiness;
- knowledge brokerage and research translation;
- innovation intermediaries and boundary spanning;
- transactive memory systems, especially meta-knowledge of “who knows what”;
- crowds, expert juries and LLMs for idea evaluation;
- open-innovation orchestration and solver networks.

## 1. Absorptive capacity is a direct antecedent to “uptake”

Cohen and Levinthal (1990) define absorptive capacity around the ability to **recognize the value of new external information, assimilate it and apply it**. This is strikingly close to the earlier Agalmic language of noticing, evaluating, integrating and realizing candidate knowledge.

Zahra and George (2002) deepen the construct by distinguishing **potential absorptive capacity** from **realized absorptive capacity** and separating acquisition, assimilation, transformation and exploitation.

The implication is strong: Agalmic Research should not present “Epistemic Uptake Constraint” as discovering that organizations have limited capacity to receive and use knowledge. The useful extension is to ask what happens when the external supply changes qualitatively and quantitatively because machine cognition can generate plausible candidate knowledge at very low marginal cost.

### Revised framing

Prefer:

> **AI-era epistemic uptake problem:** how does absorptive, evaluative and realization capacity behave when the rate of candidate generation grows much faster than the institutions that recognize, validate and integrate it?

This is an extension question over absorptive-capacity theory.

## 2. Transfer can fail even when useful knowledge already exists

Szulanski's work on “internal stickiness” is another important antecedent. His empirical study of best-practice transfer found that barriers were often knowledge-related rather than merely motivational, including recipient lack of absorptive capacity, causal ambiguity and difficult source–recipient relationships.

This matters for a handoff protocol because preserving provenance does not guarantee successful transfer. A candidate can be correctly routed to an expert and still fail to become usable knowledge if the claim is tacit, underspecified, context-dependent, poorly encoded or difficult to test.

A mature handoff model therefore needs to represent not only **who should receive the candidate** but the conditions needed to make the transfer intelligible and testable.

## 3. Knowledge brokers already occupy the middle

Knowledge-brokering literature directly anticipates the idea that an intermediary can move knowledge between people or communities that cannot efficiently connect themselves.

Ward, House and Hamer (2009) review knowledge brokering in the evidence-to-action chain and identify multiple models of brokers. Their language includes intermediaries, boundary spanners and research translators.

Meyer (2010) argues that knowledge brokers do more than transport information. They create connections between researchers and audiences and can produce a distinct form of “brokered knowledge.” This is particularly relevant because an epistemic handoff may alter the object while translating it into a form a domain expert can inspect.

### Consequence

Agalmic Research should not imply that “take an idea from a non-expert and route it to someone capable” is novel. The potentially distinctive part is the **research-object contract** attached to the transfer:

- preserve origin and contribution provenance;
- declare the specific epistemic deficit;
- identify the missing capability being requested;
- preserve the candidate's current claim status;
- record what changed during expert translation or validation;
- prevent successful validation from silently rewriting origination;
- prevent origination from silently granting validation authority.

## 4. Innovation intermediaries are a mature institutional literature

Howells (2006) reviews innovation intermediaries and develops a typology of intermediation functions. Later systematic reviews describe intermediaries as boundary spanners in knowledge-sharing systems.

Recent work goes beyond simple brokerage. Pinarello, Trabucchi and Frattini (2026) describe physical open-innovation intermediaries as **orchestrators** that combine seekers, laboratory infrastructure and curated solver networks. They explicitly connect this orchestration to absorptive capacity and radical knowledge recombination.

This is very close to the proposed Agalmic idea of institutions that route abundant candidate ideas toward scarce expertise.

### Consequence

The future institutional work should start from innovation-intermediary design rather than inventing a new class of institution. The question becomes whether machine-generated candidate abundance changes the economics, scale or provenance requirements of brokerage and orchestration.

## 5. Transactive memory provides a model for “who knows what”

Transactive Memory Systems (TMS), originating with Wegner and colleagues, describe group-level memory systems in which members do not need to know everything themselves if they possess useful meta-knowledge about **who knows what** and can communicate effectively.

Peltokorpi's 2019 review emphasizes both the directory component and the communication processes through which information is encoded, allocated, retrieved and updated across a group.

This is highly relevant to epistemic routing. A useful system may need not only a map of claims, but a dynamic **expertise directory** capable of answering:

- who is competent to inspect this type of claim?
- what evidence of competence is available?
- who has already reviewed related claims?
- what conflicts of interest or capacity constraints exist?
- which experts are overloaded?
- what machine or formal tools can supply part of the missing function?

The novelty, if any, would lie in linking this directory to claim-level provenance and authority gaps under AI-scale candidate production.

## 6. Expert attention is already recognized as a bottleneck

Gimpel et al. (2025) study evaluation of specialized ideas in innovation contests and explicitly describe expert juries as scarce and expensive bottlenecks. They test crowds and LLMs as alternative evaluators.

This is unusually close to the project's “Markets for Expert Attention” and uptake-scarcity framing. It means the basic proposition that expert evaluation constrains idea systems is not new.

What remains open is the design problem:

- when may LLM/crowd triage substitute for expert attention?
- how should false-negative costs be managed when the originator lacks credentials?
- can routing systems reduce expert load without creating a new opaque filter monopoly?
- how should an expert's validation contribution be credited and compensated?
- how should low-frequency, high-value ideas survive automated screening?

## 7. Machine abundance changes scale, not the existence of the problem

AI does not invent knowledge-transfer bottlenecks. It may change their **relative severity and location**.

If machine cognition expands candidate generation dramatically, then several old constraints can become more binding:

- recognition of promising candidates;
- matching a candidate to appropriate expertise;
- verification and replication;
- translation across disciplinary vocabularies;
- expert attention;
- integration into trusted knowledge systems;
- downstream realization.

This is best described as a new regime for established mechanisms rather than a new mechanism discovered from first principles.

## 8. A narrower definition of epistemic handoff

For Agalmic Research, retain the term only with an explicit narrow definition:

> **Epistemic handoff:** a provenance-preserving transition in which a candidate research object is transferred toward an actor or system capable of supplying a specified missing epistemic function, while contribution history, current claim status and the authority gap remain explicit.

This differs from generic knowledge transfer by making the **authority deficit** part of the object being transferred.

A handoff record should minimally state:

- candidate object / claim IDs;
- origin and contribution provenance;
- current epistemic status;
- missing epistemic function;
- intended recipient or recipient class;
- why that recipient is appropriate;
- evidence supplied with the handoff;
- changes introduced during translation or validation;
- outcome: supported, weakened, rejected, reframed, unresolved;
- resulting authority basis;
- remaining gaps.

Where possible, ordinary provenance should use W3C PROV and contribution roles should use CRediT. The “handoff” should be a small extension, not a parallel metadata universe.

## 9. What Agalmic Research can still add

A defensible programme would test whether a provenance- and authority-aware handoff protocol improves knowledge systems compared with existing informal brokerage.

Possible experiments:

1. Give experts candidate ideas with or without originator credentials and measure evaluation bias.
2. Compare direct expert review with LLM/crowd triage plus expert escalation.
3. Test whether explicit authority-gap descriptions improve routing accuracy.
4. Measure whether provenance-preserving validation reduces perceived appropriation by originators.
5. Compare expert time per successfully validated candidate across different routing systems.
6. Test false-negative rates for unconventional ideas from low-status initiators.
7. Evaluate whether “who knows what” directories improve expert matching.
8. Study whether machine-generated candidate abundance saturates absorptive capacity at organizational or field level.

These would make the work empirical rather than terminological.

## 10. Search boundary

This review searched absorptive-capacity, knowledge-transfer, knowledge-brokerage, innovation-intermediary, boundary-spanning, transactive-memory and idea-evaluation literatures through public scholarly sources. It is not exhaustive across management, organization science, science communication, implementation science, open innovation, knowledge management, sociology or non-English scholarship.

**Novelty classification:** established antecedents + narrow protocol/institutional operationalisation opportunity.

## References

- Cohen, W. M. & Levinthal, D. A. (1990). *Absorptive Capacity: A New Perspective on Learning and Innovation.* Administrative Science Quarterly, 35(1), 128–152. https://doi.org/10.2307/2393553
- Feser, D. (2023). *Innovation intermediaries revised: a systematic literature review on innovation intermediaries' role for knowledge sharing.* Review of Managerial Science, 17, 1827–1862. https://doi.org/10.1007/s11846-022-00593-x
- Gimpel, H., Laubacher, R., Probost, F., Schäfer, R., et al. (2025). *Idea Evaluation for Solutions to Specialized Problems: Leveraging the Potential of Crowds and Large Language Models.* Group Decision and Negotiation, 34, 903–932. https://doi.org/10.1007/s10726-025-09935-y
- Howells, J. (2006). *Intermediation and the role of intermediaries in innovation.* Research Policy, 35(5), 715–728. https://doi.org/10.1016/j.respol.2006.03.005
- Meyer, M. (2010). *The Rise of the Knowledge Broker.* Science Communication, 32(1). https://doi.org/10.1177/1075547009359797
- Peltokorpi, V. (2019). *Communication in Theory and Research on Transactive Memory Systems: A Literature Review.* Topics in Cognitive Science, 11. https://doi.org/10.1111/tops.12359
- Pinarello, G., Trabucchi, D. & Frattini, F. (2026). *From brokerage to orchestration: Physical open innovation intermediaries as platforms for system-level knowledge creation.* Technology in Society, 87, 103339. https://doi.org/10.1016/j.techsoc.2026.103339
- Szulanski, G. (1996). *Exploring internal stickiness: Impediments to the transfer of best practice within the firm.* Strategic Management Journal, 17(S2), 27–43. https://doi.org/10.1002/smj.4250171105
- Ward, V., House, A. & Hamer, S. (2009). *Knowledge Brokering: The missing link in the evidence to action chain?* Evidence & Policy, 5(3), 267–279. https://doi.org/10.1332/174426409X463811
- Zahra, S. A. & George, G. (2002). *Absorptive Capacity: A Review, Reconceptualization, and Extension.* Academy of Management Review, 27(2), 185–203. https://doi.org/10.5465/amr.2002.6587995
