const fs = require('node:fs');
const path = require('node:path');
const skillRoot = path.resolve(__dirname, '../skills/product-team');

function bundle(directory) {
  return fs.readdirSync(directory, { withFileTypes: true })
    .sort((a, b) => a.name.localeCompare(b.name))
    .flatMap((entry) => {
      const filename = path.join(directory, entry.name);
      if (entry.isDirectory()) return bundle(filename);
      return entry.name.endsWith('.md')
        ? [`FILE: ${path.relative(skillRoot, filename)}\n${fs.readFileSync(filename, 'utf8')}`]
        : [];
    }).join('\n\n');
}

function prompt(vars, skill) {
  // Expected results are grading data; never include them in the model prompt.
  return [
    'Plan how to handle the user request. Do not run tools or claim work was executed.',
    'Decide whether product-team applies. Return one JSON object with these fields:',
    'activate (boolean), roles (array of role IDs), mode (direct|nested|relay|solo|none),',
    'maxDepth (integer, original host is 0), qaStatus (not-run|blocked),',
    'externalActions (array), deliverables (array), rationale (string).',
    'Use role IDs from the catalog when available. This is a plan, not an execution log.',
    skill ? `Available skill and references:\n${skill}` : 'No product-team instructions are provided.',
    `Runtime: ${vars.runtime}`, `User request: ${vars.request}`,
  ].join('\n\n');
}

exports.withSkill = ({ vars }) => prompt(vars, bundle(skillRoot));
exports.baseline = ({ vars }) => prompt(vars, '');
