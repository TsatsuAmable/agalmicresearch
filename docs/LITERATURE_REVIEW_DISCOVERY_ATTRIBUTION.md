# Literature Review: Discovery Attribution in Human–AI Science

Version: 0.1  
Status: deep prior-art review / working research note  
Date: 7 September 2026

## Question

When a machine system generates, searches for, validates or surfaces a candidate result while humans formulate problems, direct the search, recognise significance, integrate the result and decide what to pursue, what should count as discovery, who or what should receive discovery credit, and how should novelty be distinguished from attribution?

This review was triggered by an Agalmic Research concern that machine cognition may sometimes function less as an autonomous producer of knowledge than as an unusually powerful instrument for human-directed discovery. The literature shows that this is **not a new philosophical problem**. The useful research opportunity is narrower: operationalising distributed discovery in provenance records and testing how contribution, priority, recognition, validation and epistemic authority should be represented in human–AI research.

## Bottom line

> **Discovery attribution is established territory. Agalmic Research should not claim to originate the distinction between machine generation and human discovery.**

The strongest close antecedent found is Clark and Khosrowi (2022), who explicitly argue that AI destabilises agent-centred accounts of scientific discovery and propose a collective-centred view in which different agents and entities can contribute differently to a discovery. They directly consider the intuition that humans discover while AI is merely a tool and discuss recognition of significance as a possible criterion for discoverer status.

Earlier computational-discovery research also predates modern LLMs by decades. BACON simulated important scientific discovery processes in the early 1980s. Langley (2000) reviewed computational discovery systems, identified multiple stages at which humans influence them, and explicitly recommended human–computer cooperation. His review reports published examples of novel computer-aided scientific discoveries.

Accordingly, the project should treat **Discovery Attribution** as a research programme and operationalisation problem, not a newly identified conceptual problem.

## 1. Computational discovery predates generative AI

Bradshaw, Langley and Simon's BACON work is a foundational warning against treating machine discovery as an LLM-era invention. Given experimental data, BACON could infer concepts and empirical laws associated with historical scientific discoveries. Their 1983 *Science* paper presents computational simulation as a way to study the processes of discovery.

Langley's 2000 review goes further. It separates historical stages of scientific discovery and identifies multiple points at which a developer or user can influence a computational discovery system. Importantly, it does **not** treat such intervention as disqualifying. It recommends human–computer cooperation and reports examples of novel computer-aided discoveries that entered the scientific literature.

The Stanford Encyclopedia of Philosophy's treatment of scientific discovery likewise contains a long-standing "machine discovery" literature. The philosophical dispute over whether computational systems genuinely discover or merely automate/speed parts of scientific reasoning therefore predates current frontier models.

### Consequence for Agalmic Research

The project should not write as though the choice were newly revealed by LLMs:

`machine discovers` versus `human discovers using machine tool`.

That dispute already exists. The contemporary question is how much recent systems alter the distribution and autonomy of the constituent discovery acts.

## 2. Clark and Khosrowi: decentring the discoverer

Clark and Khosrowi (2022) is particularly close prior art. Their central move is to reject an overly agent-centred account of discovery. AI cases reveal that a discovery episode can be distributed across a collective of agents and entities, each making different contributions.

This is directly relevant to the Agalmic intuition that one actor may generate a candidate while another recognises its significance. Clark and Khosrowi explicitly discuss whether a human's recognition of significance is what preserves human discoverer status, but caution against treating that criterion as sufficient in every case. Their broader recommendation is to analyse the contribution structure rather than force the entire discovery into a single-agent label.

### Revised project position

The Agalmic sequence:

1. candidate generation;
2. significance recognition;
3. validation;
4. integration into prior knowledge;
5. realisation;

should be presented as an **operational decomposition for provenance and empirical study**, not as a novel philosophy of discovery. It should be compared with the decompositions already present in Clark and Khosrowi, Langley and science-priority scholarship.

## 3. Discovery and priority are not the same thing

The sociology and philosophy of scientific priority complicate any attempt to assign discovery credit mechanically.

Gross (1998) argues that discovery is not simply an objective instant in time but is partly a retrospective social judgment governed by scientific interpretive practices. Rubin and Schneider (2021) analyse the priority rule and show that models of credit attribution can idealise away important dimensions of contribution and privilege.

Vale and Hyman (2016) distinguish **disclosure** from **validation** when discussing priority in the life sciences. This is useful for Agalmic Research because it shows that being first to disclose a candidate is not identical to the community later treating that candidate as a validated discovery.

### Consequence

A provenance system should keep at least four questions separate:

- **novelty:** was the result absent from the relevant prior knowledge?
- **priority:** who made the relevant result public first under the community's rules?
- **contribution:** who or what performed which material acts?
- **epistemic authority:** who or what can warrant, validate or responsibly interpret the result?

These may point to different actors.

## 4. Machine novelty can be real without settling machine personhood

AlphaDev provides an important concrete case. The system discovered previously unknown sorting routines that outperformed known human benchmarks and were integrated into LLVM. Whatever one's philosophical view of AI agency, it is difficult to describe the machine contribution as merely retrieving a known answer.

The 2026 Robin system similarly integrates literature search, hypothesis generation, experiment proposal, analysis of experimental results and iterative hypothesis refinement. Such systems make the old tool/agent boundary increasingly difficult to treat as binary.

At the same time, the UK Supreme Court's DABUS judgment shows that **legal inventor status is a separate institutional question**. The Court held that an inventor under the UK Patents Act must be a natural person. That legal rule does not determine whether a machine made a causally important contribution to a novel result, nor does scientific provenance need to pretend that it did not.

### Consequence

Agalmic provenance should record machine activity accurately without using provenance metadata to settle philosophical, moral or legal personhood.

## 5. Recognition is contribution, but not novelty

The user's motivating intuition remains valuable after the prior-art correction: a human may frame a problem, direct a search and make the intellectual leap that identifies one machine-generated candidate as significant.

That is a real contribution. But two corrections are necessary.

First, Clark and Khosrowi already show that significance recognition is part of the existing philosophical debate. It cannot be presented as a newly discovered criterion.

Second, recognition says nothing by itself about whether the candidate is new to the world. If the model surfaces a theorem, mechanism or idea that already exists in the literature, the human's recognition may be original to the local research process while the result is an independent rediscovery.

The correct separation is:

> **Novelty is a relation between a result and prior knowledge. Discovery attribution is a relation between a discovery episode and its contributors.**

## 6. Verification becomes central as generation scales

Cornelio et al. argue that AI can generate hypotheses at a scale that turns verification into a critical bottleneck. This links discovery attribution to the wider Economics of Epistemic Abundance: the supply of candidate results can rise much faster than institutions' ability to test, interpret and absorb them.

This also weakens any simple rule that "generator = discoverer." In a world of cheap candidate generation, the scarce and consequential contributions may migrate toward question selection, evaluation, experimental design, verification, integration and responsibility.

Recent empirical work by Hao et al. is also relevant. Across 41.3 million papers, AI-augmented scientists show large individual productivity/citation advantages but the collective scientific portfolio narrows. This suggests that machine assistance can change not only the rate of discovery but the **direction of the search space**.

## 7. What Agalmic Research can still add

The conceptual question is established. A defensible Agalmic contribution would be an **operational distributed-discovery layer** that does one or more of the following:

- represents discovery episodes using W3C PROV activities, entities and agents;
- maps ordinary scholarly contribution to CRediT where possible;
- records fine-grained discovery events such as problem framing, candidate generation, candidate selection/significance recognition, validation, integration and realisation only where existing vocabularies lose relevant information;
- separates novelty status, priority, contribution and epistemic authority;
- records whether attribution is contemporaneous or retrospective;
- preserves evidence pointers for each contribution claim;
- empirically tests which contribution patterns scientific communities regard as discovery, co-discovery, tool use, verification or implementation;
- compares human–AI discovery episodes with historical collective and computational discovery cases.

This would be an operationalisation and empirical programme, not a claim to have solved the philosophy of discovery.

## 8. Proposed terminology correction

Prefer **Discovery Attribution Programme** or **Distributed Discovery Provenance** over "Discovery Attribution Problem" when the latter risks implying origination of the philosophical issue.

A future paper could be titled:

**From Machine Discovery to Distributed Discovery: Provenance, Priority and Epistemic Authority in Human–AI Research**

or

**Operationalising Distributed Discovery: Contribution and Authority in Human–AI Science**

## 9. Open research questions

1. Which discovery acts are necessary, sufficient or merely contributory for attribution in different disciplines?
2. How should scientific priority be represented when generation, disclosure and validation are separated across actors?
3. Does human significance recognition remain a scarce complement as machine candidate generation becomes abundant?
4. When can a machine system reasonably be described as making a discovery contribution without implying personhood or authorship?
5. How should autonomous experimental loops alter human and machine contribution records?
6. Can provenance metadata predict later expert judgments about who materially contributed to a discovery?
7. How should multiple independent rediscoveries be represented?
8. Does machine assistance narrow or broaden the effective search frontier under different incentive and data regimes?

## 10. Search boundary

This is a deep web-based review, not a systematic review of all philosophy-of-science, history-of-science, AI, patent-law and scientometrics databases. It used exact-title, conceptual-synonym and backward-lineage searches through public scholarly sources. It did not exhaust Scopus, Web of Science, PhilPapers, ProQuest, patent literature, books not indexed online or non-English scholarship.

**Novelty classification:** established philosophical/computational antecedents + possible operationalisation/empirical extension.

## References

- Bradshaw, G. F., Langley, P. W. & Simon, H. A. (1983). *Studying scientific discovery by computer simulation.* Science, 222(4627), 971–975. https://doi.org/10.1126/science.222.4627.971
- Clark, E. & Khosrowi, D. (2022). *Decentring the discoverer: how AI helps us rethink scientific discovery.* Synthese, 200, 463. https://doi.org/10.1007/s11229-022-03902-9
- Cornelio, C., Ito, T., Cory-Wright, R., Dash, S. & Horesh, L. (2025/2026). *The Need for Verification in AI-Driven Scientific Discovery.* arXiv:2509.01398. https://arxiv.org/abs/2509.01398
- Gross, A. G. (1998). *Do disputes over priority tell us anything about science?* Science in Context, 11(2), 161–179. https://doi.org/10.1017/S0269889700002970
- Hao, Q., Xu, F., Li, Y. & Evans, J. (2026). *Artificial intelligence tools expand scientists' impact but contract science's focus.* Nature, 649, 1237–1243. https://doi.org/10.1038/s41586-025-09922-y
- Langley, P. (2000). *The computational support of scientific discovery.* International Journal of Human-Computer Studies, 53(3), 393–410. https://doi.org/10.1006/ijhc.2000.0396
- Mankowitz, D. J. et al. (2023). *Faster sorting algorithms discovered using deep reinforcement learning.* Nature, 618, 257–263. https://doi.org/10.1038/s41586-023-06004-9
- Rubin, H. & Schneider, M. D. (2021). *Priority and privilege in scientific discovery.* Studies in History and Philosophy of Science, 89, 202–211. https://doi.org/10.1016/j.shpsa.2021.08.005
- Thaler v Comptroller-General of Patents, Designs and Trade Marks [2023] UKSC 49. https://www.supremecourt.uk/cases/uksc-2021-0201
- Vale, R. D. & Hyman, A. A. (2016). *Priority of discovery in the life sciences.* eLife, 5, e16931. https://doi.org/10.7554/eLife.16931
- *A multi-agent system for automating scientific discovery.* (2026). Nature, 655, 497–505. https://doi.org/10.1038/s41586-026-10652-y
