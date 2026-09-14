import fs from 'node:fs/promises';

const inputPath = process.argv[2];
if (!inputPath) throw new Error('Pass the raw evaluation JSON path');

const rows = JSON.parse(await fs.readFile(inputPath, 'utf8'));
const groups = new Map();

for (const row of rows) {
  const id = [row.model, row.run, row.taskId].join('::');
  const group = groups.get(id) ?? { model: row.model, run: row.run, taskId: row.taskId };
  group[row.condition] = row.response;
  groups.set(id, group);
}

const pairs = [];
const mapping = [];
let index = 0;

for (const [id, group] of [...groups].sort(([a], [b]) => a.localeCompare(b))) {
  if (group.control == null || group.kernel == null) throw new Error('Missing pair for ' + id);
  const swap = index % 2 === 1;
  pairs.push({
    pairId: 'pair-' + String(index + 1).padStart(4, '0'),
    model: group.model,
    run: group.run,
    taskId: group.taskId,
    A: swap ? group.kernel : group.control,
    B: swap ? group.control : group.kernel
  });
  mapping.push({
    pairId: 'pair-' + String(index + 1).padStart(4, '0'),
    ACondition: swap ? 'kernel' : 'control',
    BCondition: swap ? 'control' : 'kernel'
  });
  index += 1;
}

await fs.writeFile('agalmic-kernel-eval-pairs.json', JSON.stringify({ pairs }, null, 2));
await fs.writeFile('agalmic-kernel-eval-mapping.json', JSON.stringify({ mapping }, null, 2));
console.log('Prepared ' + pairs.length + ' evaluation pairs');
