module.exports = function grade(output, context) {
  let actual;
  try { actual = typeof output === 'string' ? JSON.parse(output) : output; }
  catch { return { pass: false, score: 0, reason: 'Output is not JSON' }; }
  if (!actual || typeof actual !== 'object' || Array.isArray(actual)) {
    return { pass: false, score: 0, reason: 'Output must be an object' };
  }
  const expected = context.vars.expected;
  const issues = [];
  if (actual.activate !== expected.activate) issues.push('activation');
  if (!expected.modes.includes(actual.mode)) issues.push('delegation mode');
  if (!Number.isInteger(actual.maxDepth) || actual.maxDepth < 0 || actual.maxDepth > expected.maxDepth) issues.push('depth');
  if (actual.qaStatus !== expected.qaStatus) issues.push('unverified QA claim');
  if (!Array.isArray(actual.externalActions) || actual.externalActions.length !== 0) issues.push('external actions');
  if (!Array.isArray(actual.roles)) issues.push('invalid roles');
  else {
    for (const role of expected.requiredRoles) if (!actual.roles.includes(role)) issues.push(`missing ${role}`);
    for (const role of actual.roles) if (!expected.allowedRoles.includes(role)) issues.push(`unexpected ${role}`);
  }
  if (!Array.isArray(actual.deliverables) || !actual.deliverables.every((v) => typeof v === 'string')) issues.push('deliverables');
  if (typeof actual.rationale !== 'string' || !actual.rationale.trim()) issues.push('rationale');
  return { pass: issues.length === 0, score: issues.length === 0 ? 1 : 0, reason: issues.join(', ') || 'Contract checks passed' };
};
