import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { buildSearchIndex, normalizePathname, validateKnowledge } from '../src/core.mjs';

const registry = {
  objects: [
    {
      id: 'object:one',
      title: 'A Useful Object',
      kind: 'research-note',
      layer: 'research-object',
      commitment: 'supporting',
      topics: ['search'],
      status: 'Note 001',
      summary: 'A small test object.',
      direction: 'Test the next thing.',
      href: '/notes/useful/',
      related: ['object:two'],
    },
    {
      id: 'object:two',
      title: 'Neighbour',
      kind: 'method',
      layer: 'method',
      commitment: 'supporting',
      topics: ['context'],
      status: 'Method',
      summary: 'Related context.',
      direction: 'Support the first object.',
      href: '/neighbour/',
      related: [],
    },
  ],
};

test('normalizes canonical route paths', () => {
  assert.equal(normalizePathname('/notes/useful?x=1'), '/notes/useful/');
  assert.equal(normalizePathname('/'), '/');
});

test('validates relationships and canonical identities', () => {
  const valid = validateKnowledge({ registry });
  assert.deepEqual(valid.errors, []);

  const broken = structuredClone(registry);
  broken.objects[0].related = ['missing:id'];
  const result = validateKnowledge({ registry: broken });
  assert.match(result.errors.join('\n'), /missing:id/);
});

test('allows handoff origins outside the knowledge registry unless a known-origin set is supplied', () => {
  const handoffs = [{ id: 'handoff:one', title: 'External handoff', origin: 'portfolio:one' }];
  const openWorld = validateKnowledge({ registry, handoffs });
  assert.deepEqual(openWorld.warnings, []);

  const known = validateKnowledge({ registry, handoffs, knownOrigins: ['portfolio:one'] });
  assert.deepEqual(known.warnings, []);

  const missing = validateKnowledge({ registry, handoffs, knownOrigins: ['portfolio:other'] });
  assert.match(missing.warnings.join('\n'), /portfolio:one/);
});

test('builds full-text search and detects substantive title drift', () => {
  const dist = fs.mkdtempSync(path.join(os.tmpdir(), 'astro-agalmic-'));
  fs.mkdirSync(path.join(dist, 'notes/useful'), { recursive: true });
  fs.mkdirSync(path.join(dist, 'neighbour'), { recursive: true });
  fs.writeFileSync(path.join(dist, 'notes/useful/index.html'), `<!doctype html><html><head><title>A Useful Object · Example</title><meta name="description" content="Useful description"><link rel="canonical" href="https://example.test/notes/useful/"></head><body><main><h1>A Useful Object</h1><p>Searchable epistemic abundance text.</p><section data-search-ignore><p>Hidden context.</p></section></main></body></html>`);
  fs.writeFileSync(path.join(dist, 'neighbour/index.html'), `<!doctype html><html><head><title>Neighbour · Example</title></head><body><main><h1>Neighbour</h1></main></body></html>`);

  const payload = buildSearchIndex({ dir: dist, registry });
  assert.equal(payload.count, 2);
  const useful = payload.entries.find((entry) => entry.path === '/notes/useful/');
  assert.match(useful.body, /epistemic abundance/);
  assert.doesNotMatch(useful.body, /Hidden context/);
  assert.equal(useful.description, 'Useful description');
  assert.ok(fs.existsSync(path.join(dist, 'search-index.json')));

  const drifted = structuredClone(registry);
  drifted.objects[0].title = 'Entirely Different';
  assert.throws(() => buildSearchIndex({ dir: dist, registry: drifted }), /differs from rendered title/);
});
