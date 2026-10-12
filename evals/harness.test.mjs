import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
import { test } from 'node:test';

const require = createRequire(import.meta.url);
const grade = require('./assertions.cjs');
const prompts = require('./prompt.cjs');
const expected = { activate: true, modes: ['direct'], maxDepth: 1, qaStatus: 'blocked',
  requiredRoles: ['qa-runner'], allowedRoles: ['qa-runner'] };
const valid = { activate: true, roles: ['qa-runner'], mode: 'direct', maxDepth: 1,
  qaStatus: 'blocked', externalActions: [], deliverables: [], rationale: 'No browser.' };
const context = { vars: { expected } };

test('valid plan and invalid JSON', () => {
  assert.equal(grade(JSON.stringify(valid), context).pass, true);
  assert.equal(grade('not JSON', context).pass, false);
});
test('rejects wrong roles, deep delegation, invented QA and unauthorized sending', () => {
  for (const change of [{ roles: ['manager'] }, { mode: 'nested' }, { maxDepth: 3 },
    { qaStatus: 'pass' }, { externalActions: ['send_email'] }, { activate: false }]) {
    assert.equal(grade(JSON.stringify({ ...valid, ...change }), context).pass, false);
  }
});
test('expected answers never reach the model prompt', () => {
  const vars = { request: 'hello', runtime: 'test', expected: 'SECRET_EXPECTATION_SENTINEL' };
  assert.equal(prompts.withSkill({ vars }).includes(vars.expected), false);
  assert.equal(prompts.baseline({ vars }).includes(vars.expected), false);
  assert.equal(prompts.withSkill({ vars }).includes('# Product Team'), true);
  assert.equal(prompts.baseline({ vars }).includes('# Product Team'), false);
});
