#!/usr/bin/env node

const fs = require('node:fs');
const path = require('node:path');

const defaultUrls = {
  ad: 'https://raw.githubusercontent.com/SpecterOps/BloodHound-Docs/main/docs/assets/sample-data/ad_sampledata.zip',
  entra: 'https://raw.githubusercontent.com/SpecterOps/BloodHound-Docs/main/docs/assets/sample-data/entra_sampledata.zip',
};

function parseArgs(argv) {
  const args = {
    baseUrl: 'http://bhe.localhost',
    repo: process.cwd(),
    username: 'admin',
    password: 'admin',
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

  return args;
}

function printHelp() {
  console.log(`Usage:
  node ingest_sample_data.cjs [options]

Options:
  --base-url URL            Local app URL (default: http://bhe.localhost)
  --repo PATH               BHE repo path (default: current directory)
  --username USERNAME       Local login username (default: admin)
  --password PASSWORD       Local login password (default: admin)
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
  while (Date.now() < deadline) {
    await new Promise((resolve) => setTimeout(resolve, 3000));
    const list = await request(args.baseUrl, 'GET', '/api/v2/file-upload?limit=10', { token });
    finalJob = (list?.data ?? []).find((job) => String(job.id) === ingestId);
    if (!finalJob) {
      console.log('poll: job not listed yet');
      continue;
    }

    console.log(
      `poll: status=${finalJob.status} message=${JSON.stringify(finalJob.status_message || '')} total=${finalJob.total_files} failed=${finalJob.failed_files} partial=${finalJob.partial_failed_files}`
    );

    if (finalJob.status_message === 'Complete' || finalJob.status === 2 || finalJob.failed_files > 0) {
      break;
    }
  }

  if (!finalJob) {
    throw new Error(`Ingest job ${ingestId} did not appear before timeout`);
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
  for (const environment of environments?.data ?? []) {
    console.log(`${environment.type}\t${environment.name}\tcollected=${environment.collected}`);
  }
}

main().catch((error) => {
  console.error(error.stack || error.message);
  process.exit(1);
});
