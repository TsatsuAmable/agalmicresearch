# Frontier Throughput Instrumentation

This directory turns the **Frontier Throughput Audit** into replayable evidence.

## Source of truth

`events.jsonl` is an append-only event log. Each line is an independent JSON object with a stable `event_id` and `candidate_id`.

Stages:

`generate -> select -> validate -> realize -> assimilate`

Event types:

`entered | completed | disposition | human_attention | machine_effort`

Dispositions:

`promoted | rejected | parked | blocked | handed_off | published`

Human attention is recorded only when active human effort is observed or explicitly logged. Wall-clock delay must not be substituted for attention.

## Run

```bash
npm run audit:throughput
```

The reducer validates the log and emits a reproducible stage summary. Raw events remain authoritative; summaries are derived artefacts.

## Experimental use

1. Observe a fixed baseline window.
2. Identify a stage with growing backlog, age, or human-attention burden.
3. Apply one intervention.
4. Repeat the same observation window.
5. Treat a scarcity as displaced only if the intervention improves the constrained stage without degrading downstream evidence quality.

This is intentionally not a universal quality score. A justified rejection or handoff can be a successful outcome.
