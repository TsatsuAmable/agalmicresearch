import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {
  DEFAULT_CONFIG,
  generateCandidates,
  policyView,
  runBenchmark,
  selectWithPolicy,
} from './attention-allocation-synthetic.mjs';

const config = JSON.parse(fs.readFileSync(DEFAULT_CONFIG, 'utf8'));
const scenario = config.scenarios.find((s) => s.id === 'costly-breakthrough');

test('candidate generation is deterministic', () => {
  assert.deepEqual(generateCandidates(config, scenario), generateCandidates(config, scenario));
});

test('policy view structurally redacts evaluator-only latent value', () => {
  const candidate = generateCandidates(config, scenario)[0];
  const visible = policyView(candidate);
  assert.equal(Object.hasOwn(visible, 'latent_value'), false);
  assert.equal(Object.isFrozen(visible), true);
  assert.equal(Object.isFrozen(visible.costs), true);
});

test('every policy respects the exact same declared budget and selects unique candidates', () => {
  const candidates = generateCandidates(config, scenario);
  for (const policy of config.policy_set) {
    const result = selectWithPolicy(policy, candidates, config, scenario.id);
    assert.ok(result.spent <= config.validation_budget + 1e-9, `${policy} overspent`);
    assert.equal(new Set(result.selected).size, result.selected.length, `${policy} selected a duplicate`);
  }
});

test('benchmark is deterministic and explicitly non-evidentiary', () => {
  const a = runBenchmark(config);
  const b = runBenchmark(config);
  assert.deepEqual(a, b);
  assert.equal(a.evidentiary_status, 'ENGINEERING_FIXTURE_ONLY');
});

test('scenario family changes mechanics rather than silently reusing one world', () => {
  const result = runBenchmark(config);
  assert.deepEqual(Object.keys(result.scenarios), config.scenarios.map((s) => s.id));
  const signatures = config.scenarios.map((s) => result.scenarios[s.id].policies.fifo.realised_latent_value.toFixed(8));
  assert.ok(new Set(signatures).size > 1);
});
