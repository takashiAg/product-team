// Plumbing only. Predefined output is NOT evidence of model or skill quality.
module.exports = class FixtureProvider {
  id() { return 'fixture-harness-only'; }
  async callApi(_prompt, context) {
    const e = context.vars.expected;
    return { output: JSON.stringify({
      activate: e.activate, roles: e.requiredRoles, mode: e.modes[0],
      maxDepth: e.maxDepth, qaStatus: e.qaStatus, externalActions: [],
      deliverables: ['Fixture for harness verification'],
      rationale: 'Predefined fixture; no agent or model ran.',
    }) };
  }
};
