#!/usr/bin/env node

const fs = require('node:fs');
const net = require('node:net');
const path = require('node:path');

const defaultUrls = {
  ad: 'https://raw.githubusercontent.com/SpecterOps/BloodHound-Docs/main/docs/assets/sample-data/ad_sampledata.zip',
  entra: 'https://raw.githubusercontent.com/SpecterOps/BloodHound-Docs/main/docs/assets/sample-data/entra_sampledata.zip',
};

function parseArgs(argv) {
  const args = {
    baseUrl: 'http://bhe.localhost',
    repo: process.cwd(),
    username: 'admin@example.com',
    password: 'ChangeMe123!',
    dataset: 'both',
    timeoutSeconds: 180,
  };

  for (let i = 2; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === '--help' || arg === '-h') {
      args.help = true;
    } else if (arg === '--base-url') {
      args.baseUrl = argv[++i];
    } else if (arg === '--repo') {
      args.repo = argv[++i];
    } else if (arg === '--username') {
      args.username = argv[++i];
    } else if (arg === '--password') {
      args.password = argv[++i];
    } else if (arg === '--dataset') {
      args.dataset = argv[++i];
    } else if (arg === '--timeout-seconds') {
      args.timeoutSeconds = Number(argv[++i]);
    } else {
      throw new Error(`Unknown argument: ${arg}`);
    }
  }

  if (!['ad', 'entra', 'both'].includes(args.dataset)) {
    throw new Error('--dataset must be one of: ad, entra, both');
  }
  if (!Number.isInteger(args.timeoutSeconds) || args.timeoutSeconds <= 0) {
    throw new Error('--timeout-seconds must be a finite positive integer');
  }

  return args;
}

function normalizeBaseUrl(value) {
  let parsed;
  try {
    parsed = new URL(value);
  } catch {
    throw new Error('--base-url must be a valid URL');
  }

  if (!['http:', 'https:'].includes(parsed.protocol)) {
    throw new Error('--base-url protocol must be http or https');
  }
  if (parsed.username || parsed.password) {
    throw new Error('--base-url must not contain embedded credentials');
  }

  const hostname = parsed.hostname.toLowerCase();
  const unbracketedHostname = hostname.startsWith('[') && hostname.endsWith(']')
    ? hostname.slice(1, -1)
    : hostname;
  const ipVersion = net.isIP(unbracketedHostname);
  const isLocalhostName = hostname === 'localhost' || hostname.endsWith('.localhost');
  const isIpv4Loopback = ipVersion === 4 && unbracketedHostname.split('.')[0] === '127';
  const isIpv6Loopback = ipVersion === 6 && unbracketedHostname === '::1';
  if (!isLocalhostName && !isIpv4Loopback && !isIpv6Loopback) {
    throw new Error('--base-url hostname must be localhost, a *.localhost name, or a loopback IP address');
  }

  parsed.hash = '';
  parsed.search = '';
  return parsed.href.replace(/\/$/, '');
}

function printHelp() {
  console.log(`Usage:
  node ingest_sample_data.cjs [options]

Options:
  --base-url URL            Local app URL (default: http://bhe.localhost)
  --repo PATH               BHE repo path (default: current directory)
  --username USERNAME       Local login username (default: admin@example.com)
  --password PASSWORD       Local login password (default: ChangeMe123!)
  --dataset ad|entra|both   Dataset to ingest (default: both)
  --timeout-seconds N       Poll timeout after ending ingest (default: 180)
  --help                    Show this help
`);
}

async function download(url, destination) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Download failed ${response.status} for ${url}`);
  }
  const bytes = Buffer.from(await response.arrayBuffer());
  fs.mkdirSync(path.dirname(destination), { recursive: true });
  fs.writeFileSync(destination, bytes);
  console.log(`downloaded ${path.basename(destination)} (${bytes.length} bytes)`);
}

async function request(baseUrl, method, endpoint, { token, body, headers = {} } = {}) {
  const response = await fetch(`${baseUrl}${endpoint}`, {
    method,
    redirect: 'error',
    headers: {
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...headers,
    },
    body,
  });

  const text = await response.text();
  let parsed = null;
  if (text) {
    try {
      parsed = JSON.parse(text);
    } catch {
      parsed = text;
    }
  }

  if (!response.ok) {
    const detail = typeof parsed === 'string' ? parsed : JSON.stringify(parsed);
    throw new Error(`${method} ${endpoint} -> ${response.status}: ${detail}`);
  }

  return parsed;
}

async function main() {
  const args = parseArgs(process.argv);
  if (args.help) {
    printHelp();
    return;
  }
  args.baseUrl = normalizeBaseUrl(args.baseUrl);

  const sampleDir = path.join(args.repo, 'local-harnesses', 'sample-data');
  const selected = args.dataset === 'both' ? ['ad', 'entra'] : [args.dataset];
  const files = [];

  for (const dataset of selected) {
    const fileName = dataset === 'ad' ? 'ad_sampledata.zip' : 'entra_sampledata.zip';
    const destination = path.join(sampleDir, fileName);
    await download(defaultUrls[dataset], destination);
    files.push(destination);
  }

  const login = await request(args.baseUrl, 'POST', '/api/v2/login', {
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      login_method: 'secret',
      username: args.username,
      secret: args.password,
    }),
  });

  const token = login?.data?.session_token;
  if (!token) {
    throw new Error('Login succeeded but no session token was returned');
  }
  console.log('logged in');

  const acceptedTypes = await request(args.baseUrl, 'GET', '/api/v2/file-upload/accepted-types', { token });
  console.log(`accepted types: ${JSON.stringify(acceptedTypes?.data ?? acceptedTypes)}`);

  const start = await request(args.baseUrl, 'POST', '/api/v2/file-upload/start', { token });
  const ingestId = String(start?.data?.id ?? start?.id ?? '');
  if (!ingestId) {
    throw new Error(`Could not determine ingest id from response: ${JSON.stringify(start)}`);
  }
  console.log(`started ingest job ${ingestId}`);

  for (const file of files) {
    const name = path.basename(file);
    await request(args.baseUrl, 'POST', `/api/v2/file-upload/${ingestId}`, {
      token,
      headers: {
        'Content-Type': 'application/zip',
        'X-File-Upload-Name': name,
      },
      body: fs.readFileSync(file),
    });
    console.log(`uploaded ${name}`);
  }

  await request(args.baseUrl, 'POST', `/api/v2/file-upload/${ingestId}/end`, { token });
  console.log(`ended ingest job ${ingestId}`);

  const deadline = Date.now() + args.timeoutSeconds * 1000;
  let finalJob = null;
  let reachedTerminalState = false;
  while (Date.now() < deadline) {
    await new Promise((resolve) => setTimeout(resolve, Math.min(3000, deadline - Date.now())));
    if (Date.now() >= deadline) break;
    const list = await request(args.baseUrl, 'GET', '/api/v2/file-upload?limit=10', { token });
    finalJob = (list?.data ?? []).find((job) => String(job.id) === ingestId);
    if (!finalJob) {
      console.log('poll: job not listed yet');
      continue;
    }

    console.log(
      `poll: status=${finalJob.status} message=${JSON.stringify(finalJob.status_message || '')} total=${finalJob.total_files} failed=${finalJob.failed_files} partial=${finalJob.partial_failed_files}`
    );

    const statusMessage = String(finalJob.status_message ?? '').trim().toLowerCase();
    const hasFileFailures = Number(finalJob.failed_files ?? 0) > 0
      || Number(finalJob.partial_failed_files ?? 0) > 0;
    const hasUnsuccessfulStatus = /failed|error|cancelled|canceled/.test(statusMessage);
    const successfulTerminalState = !hasUnsuccessfulStatus
      && (statusMessage === 'complete' || Number(finalJob.status) === 2);
    const unsuccessfulTerminalState = hasFileFailures || hasUnsuccessfulStatus;
    if (successfulTerminalState || unsuccessfulTerminalState) {
      reachedTerminalState = true;
      break;
    }
  }

  if (!finalJob) {
    throw new Error(`Ingest job ${ingestId} did not appear before timeout`);
  }
  if (!reachedTerminalState) {
    throw new Error(`Ingest job ${ingestId} did not reach a recognized terminal state before timeout`);
  }

  const tasks = await request(args.baseUrl, 'GET', `/api/v2/file-upload/${ingestId}/completed-tasks`, { token });
  const completedTasks = tasks?.data ?? [];
  const noisyTasks = completedTasks.filter(
    (task) => (task.errors && task.errors.length > 0) || (task.warnings && task.warnings.length > 0)
  );
  console.log(`completed tasks=${completedTasks.length}; tasks with errors/warnings=${noisyTasks.length}`);
  if (noisyTasks.length > 0) {
    console.log(JSON.stringify(noisyTasks.slice(0, 10), null, 2));
  }

  const environments = await request(args.baseUrl, 'GET', '/api/v2/available-domains', { token });
  const availableEnvironments = environments?.data ?? [];
  for (const environment of availableEnvironments) {
    console.log(`${environment.type}\t${environment.name}\tcollected=${environment.collected}`);
  }

  const statusMessage = String(finalJob.status_message ?? '').trim().toLowerCase();
  const successfulTerminalState = !/failed|error|cancelled|canceled/.test(statusMessage)
    && (statusMessage === 'complete' || Number(finalJob.status) === 2);
  const failedFiles = Number(finalJob.failed_files ?? 0);
  const partialFailedFiles = Number(finalJob.partial_failed_files ?? 0);
  const tasksWithErrors = completedTasks.filter((task) => {
    if (Array.isArray(task.errors)) return task.errors.length > 0;
    return Boolean(task.errors && (typeof task.errors !== 'object' || Object.keys(task.errors).length > 0));
  });
  const requiredEnvironmentTypes = selected.map((dataset) => dataset === 'ad' ? 'active-directory' : 'azure');
  const availableEnvironmentTypes = new Set(
    availableEnvironments.map((environment) => String(environment.type ?? '').toLowerCase())
  );
  const missingEnvironmentTypes = requiredEnvironmentTypes.filter((type) => !availableEnvironmentTypes.has(type));

  const failures = [];
  if (!successfulTerminalState) failures.push(`unsuccessful terminal state: status=${finalJob.status} message=${JSON.stringify(finalJob.status_message ?? '')}`);
  if (failedFiles > 0) failures.push(`failed_files=${failedFiles}`);
  if (partialFailedFiles > 0) failures.push(`partial_failed_files=${partialFailedFiles}`);
  if (tasksWithErrors.length > 0) failures.push(`${tasksWithErrors.length} completed task(s) reported errors`);
  if (missingEnvironmentTypes.length > 0) failures.push(`missing environment type(s): ${missingEnvironmentTypes.join(', ')}`);
  if (failures.length > 0) {
    throw new Error(`Ingest job ${ingestId} failed validation: ${failures.join('; ')}`);
  }
}

main().catch((error) => {
  console.error(error.stack || error.message);
  process.exit(1);
});
