import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
export const DEFAULT_CONFIG = path.resolve(__dirname, '../research/attention_allocation/synthetic/scenario.v0.1.json');

const clamp01 = (x) => Math.max(0, Math.min(1, x));

export function seededRng(seed) {
  let a = seed >>> 0;
  return function rng() {
    a |= 0;
    a = (a + 0x6D2B79F5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function normal(rng) {
  const u1 = Math.max(rng(), Number.EPSILON);
  const u2 = rng();
  return Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
}

function hashString(s) {
  let h = 2166136261;
  for (const ch of s) {
    h ^= ch.charCodeAt(0);
    h = Math.imul(h, 16777619);
  }
  return h >>> 0;
}

export function generateCandidates(config, scenario) {
  const rng = seededRng((config.seed ^ hashString(scenario.id)) >>> 0);
  const out = [];
  for (let i = 0; i < config.candidate_count; i++) {
    const quality = rng();
    const novelty = rng();
    const minority = rng() < 0.18;
    const plausibility = clamp01(quality + normal(rng) * scenario.plausibility_noise);
    const uncertainty = clamp01(0.65 * (1 - Math.abs(plausibility - 0.5) * 2) + 0.35 * rng());

    const human = 1 + Math.floor(rng() * 5 + novelty * scenario.novelty_cost_weight);
    const compute = 1 + Math.floor(rng() * 5);
    const lab = Math.floor(rng() * 4 + novelty * scenario.novelty_cost_weight * 0.5);
    const elapsed = 1 + Math.floor(rng() * 8);
    const cw = config.cost_weights;
    const validationCost = human * cw.human + compute * cw.compute + lab * cw.lab + elapsed * cw.elapsed;

    const w = scenario.latent_weights;
    const weighted = w.quality * quality + w.novelty * novelty + w.minority * Number(minority);
    const residualWeight = Math.max(0, 1 - w.quality - w.novelty - w.minority);
    const latentValue = clamp01(weighted + residualWeight * rng() + normal(rng) * scenario.latent_noise);

    out.push({
      id: `${scenario.id}-${String(i + 1).padStart(4, '0')}`,
      arrival_index: i,
      plausibility,
      novelty,
      uncertainty,
      minority,
      validation_cost: validationCost,
      costs: { human, compute, lab, elapsed },
      latent_value: latentValue,
    });
  }
  return out;
}

export function policyView(candidate) {
  return Object.freeze({
    id: candidate.id,
    arrival_index: candidate.arrival_index,
    plausibility: candidate.plausibility,
    novelty: candidate.novelty,
    uncertainty: candidate.uncertainty,
    minority: candidate.minority,
    validation_cost: candidate.validation_cost,
    costs: Object.freeze({ ...candidate.costs }),
  });
}

function rankCandidates(policy, visible, seed) {
  if (policy === 'fifo') return [...visible].sort((a, b) => a.arrival_index - b.arrival_index);
  if (policy === 'plausibility') return [...visible].sort((a, b) => b.plausibility - a.plausibility || a.arrival_index - b.arrival_index);
  if (policy === 'efficiency') return [...visible].sort((a, b) => (b.plausibility / b.validation_cost) - (a.plausibility / a.validation_cost) || a.arrival_index - b.arrival_index);
  if (policy === 'uncertainty') return [...visible].sort((a, b) => b.uncertainty - a.uncertainty || a.arrival_index - b.arrival_index);
  if (policy === 'diversity') return [...visible].sort((a, b) => (b.novelty + 0.25 * Number(b.minority)) - (a.novelty + 0.25 * Number(a.minority)) || a.arrival_index - b.arrival_index);
  if (policy === 'random') {
    const rng = seededRng(seed >>> 0);
    return visible.map((c) => ({ c, k: rng() })).sort((a, b) => a.k - b.k).map((x) => x.c);
  }
  throw new Error(`Unknown policy: ${policy}`);
}

function packBudget(ranked, budget) {
  const selected = [];
  let spent = 0;
  for (const c of ranked) {
    if (spent + c.validation_cost <= budget + 1e-9) {
      selected.push(c.id);
      spent += c.validation_cost;
    }
  }
  return { selected, spent };
}

function selectExplorationQuota(visible, budget, fraction) {
  const exploreBudget = budget * fraction;
  const exploitBudget = budget - exploreBudget;
  const exploreRank = [...visible].sort((a, b) => (b.novelty + 0.3 * Number(b.minority)) - (a.novelty + 0.3 * Number(a.minority)) || a.arrival_index - b.arrival_index);
  const explore = packBudget(exploreRank, exploreBudget);

  const used = new Set(explore.selected);
  const exploitRank = [...visible].filter((c) => !used.has(c.id)).sort((a, b) => b.plausibility - a.plausibility || a.arrival_index - b.arrival_index);
  const exploit = packBudget(exploitRank, exploitBudget + Math.max(0, exploreBudget - explore.spent));
  return { selected: [...explore.selected, ...exploit.selected], spent: explore.spent + exploit.spent };
}

export function selectWithPolicy(policy, candidates, config, scenarioId) {
  const visible = candidates.map(policyView);
  if (visible.some((c) => Object.hasOwn(c, 'latent_value'))) throw new Error('Policy view leaked latent_value');
  if (policy === 'exploration_quota') {
    return selectExplorationQuota(visible, config.validation_budget, config.exploration_fraction);
  }
  const ranked = rankCandidates(policy, visible, config.seed ^ hashString(`${scenarioId}:${policy}`));
  return packBudget(ranked, config.validation_budget);
}

export function evaluateSelection(candidates, selection, budget) {
  const byId = new Map(candidates.map((c) => [c.id, c]));
  const selected = selection.selected.map((id) => {
    const c = byId.get(id);
    if (!c) throw new Error(`Unknown selected id: ${id}`);
    return c;
  });

  const unique = new Set(selection.selected);
  if (unique.size !== selection.selected.length) throw new Error('Duplicate candidate selected');
  if (selection.spent > budget + 1e-9) throw new Error('Budget exceeded');

  const topCount = Math.max(1, Math.ceil(candidates.length * 0.1));
  const topIds = new Set([...candidates].sort((a, b) => b.latent_value - a.latent_value).slice(0, topCount).map((c) => c.id));
  const unconventionalTop = [...candidates].filter((c) => topIds.has(c.id) && (c.novelty >= 0.75 || c.minority));
  const selectedIds = new Set(selection.selected);
  const recoveredTop = [...topIds].filter((id) => selectedIds.has(id)).length;
  const recoveredUnconventional = unconventionalTop.filter((c) => selectedIds.has(c.id)).length;

  const sum = (xs, f) => xs.reduce((acc, x) => acc + f(x), 0);
  return {
    selected_count: selected.length,
    budget_spent: selection.spent,
    budget_residual: budget - selection.spent,
    realised_latent_value: sum(selected, (c) => c.latent_value),
    mean_selected_value: selected.length ? sum(selected, (c) => c.latent_value) / selected.length : 0,
    top_decile_recall: recoveredTop / topIds.size,
    unconventional_top_decile_recall: unconventionalTop.length ? recoveredUnconventional / unconventionalTop.length : null,
    mean_selected_novelty: selected.length ? sum(selected, (c) => c.novelty) / selected.length : 0,
    mean_selected_validation_cost: selected.length ? sum(selected, (c) => c.validation_cost) / selected.length : 0,
  };
}

export function runBenchmark(config) {
  const scenarios = {};
  for (const scenario of config.scenarios) {
    const candidates = generateCandidates(config, scenario);
    const policies = {};
    for (const policy of config.policy_set) {
      const selection = selectWithPolicy(policy, candidates, config, scenario.id);
      policies[policy] = evaluateSelection(candidates, selection, config.validation_budget);
    }
    scenarios[scenario.id] = {
      candidate_count: candidates.length,
      validation_budget: config.validation_budget,
      policies,
    };
  }
  return {
    benchmark: 'attention-allocation-stage-a',
    version: config.version,
    seed: config.seed,
    evidentiary_status: 'ENGINEERING_FIXTURE_ONLY',
    scenarios,
  };
}

function parseArgs(argv) {
  const out = { config: DEFAULT_CONFIG, output: null, fixture: false };
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === '--engineering-fixture') out.fixture = true;
    else if (arg === '--config') out.config = path.resolve(argv[++i]);
    else if (arg === '--out') out.output = path.resolve(argv[++i]);
    else throw new Error(`Unknown argument: ${arg}`);
  }
  return out;
}

if (process.argv[1] && path.resolve(process.argv[1]) === __filename) {
  const args = parseArgs(process.argv.slice(2));
  if (!args.fixture) {
    throw new Error('Synthetic policy execution is gated. Re-run with --engineering-fixture to exercise mechanics only; do not treat output as empirical evidence.');
  }
  const config = JSON.parse(fs.readFileSync(args.config, 'utf8'));
  const result = runBenchmark(config);
  const rendered = JSON.stringify(result, null, 2) + '\n';
  if (args.output) fs.writeFileSync(args.output, rendered);
  else process.stdout.write(rendered);
}
