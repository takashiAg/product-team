import { spawnSync } from 'node:child_process';
import { mkdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const mode = process.argv[2];
if (!['smoke', 'live'].includes(mode)) throw new Error('Choose smoke or live');
const provider = process.env.EVAL_PROVIDER;
if (mode === 'live' && (!provider || !/^(openai|anthropic|ollama):/.test(provider))) {
  throw new Error('Set EVAL_PROVIDER to an explicit openai:, anthropic:, or ollama: provider and model.');
}
mkdirSync(path.join(root, 'evals/results'), { recursive: true });
const args = ['eval', '--config', 'evals/promptfooconfig.yaml', '--no-cache',
  '--output', `evals/results/${mode}.json`, '--max-concurrency', '1'];
if (mode === 'live') args.push('--providers', provider);
console.log(mode === 'smoke'
  ? 'FIXTURE-ONLY: tests the harness, not model behavior or subagent execution.'
  : `LIVE planning evaluation: ${provider}; may use paid inference. No actual subagents or browser are tested.`);
const result = spawnSync(path.join(root, 'evals/node_modules/.bin/promptfoo'), args, {
  cwd: root, stdio: 'inherit', env: { ...process.env, PROMPTFOO_DISABLE_TELEMETRY: '1' },
});
if (result.error) throw result.error;
process.exit(result.status ?? 1);
