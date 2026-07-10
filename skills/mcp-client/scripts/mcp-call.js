#!/usr/bin/env node
/**
 * mcp-call.js — Spawn an MCP server and call a tool via JSON-RPC stdio
 *
 * Usage:
 *   node mcp-call.js <server-name> <tool-name> '<json-args>'
 *   node mcp-call.js --json <server-name> <tool-name> '<json-args>'
 *
 * Examples:
 *   node mcp-call.js desktop-commander read_file '{"path":"/tmp/test.txt","length":10}'
 *   node mcp-call.js --json memory get_notes '{}'
 */

const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const CONFIG_PATHS = [
  path.join(process.env.HOME, '.openclaw', 'openclaw.json'),
  path.join(process.env.HOME, '.openclaw', 'config.yaml'),
  path.join(process.env.HOME, '.openclaw', 'config.yml'),
];

function findConfig() {
  for (const p of CONFIG_PATHS) {
    if (fs.existsSync(p)) return p;
  }
  throw new Error('No OpenClaw config found at: ' + CONFIG_PATHS.join(', '));
}

function loadConfig(configPath) {
  const ext = path.extname(configPath).toLowerCase();
  const content = fs.readFileSync(configPath, 'utf8');

  if (ext === '.json') {
    return JSON.parse(content);
  }
  // Simple YAML parser for our needs
  const result = {};
  let currentSection = null;
  let currentKey = null;
  let indentStack = [];

  for (const line of content.split('\n')) {
    if (!line.trim() || line.trim().startsWith('#')) continue;
    const match = line.match(/^(\s*)(\w+):\s*(.*)$/);
    if (match) {
      const [, indent, key, value] = match;
      const depth = indent.length;
      // Very basic YAML — enough for mcp.servers block
      if (key === 'mcp') {
        result.mcp = {};
        currentSection = result.mcp;
      } else if (currentSection && key === 'servers') {
        currentSection.servers = {};
        currentKey = 'servers';
      }
    }
  }

  // Fallback: if YAML parsing fails, try to extract JSON-like structure
  try {
    // Look for JSON embedded in YAML
    const jsonMatch = content.match(/\{[\s\S]*\}/);
    if (jsonMatch) return JSON.parse(jsonMatch[0]);
  } catch (e) {
    // ignore
  }

  return result;
}

function getServerConfig(config, serverName) {
  const servers = config?.mcp?.servers || {};
  const server = servers[serverName];
  if (!server) {
    const available = Object.keys(servers).join(', ') || 'none';
    throw new Error(`Server "${serverName}" not found. Available: ${available}`);
  }
  return server;
}

function callMcp(serverConfig, toolName, toolArgs) {
  return new Promise((resolve, reject) => {
    const { command, args = [], env: serverEnv = {} } = serverConfig;
    const childEnv = { ...process.env, ...serverEnv };

    const child = spawn(command, args, {
      stdio: ['pipe', 'pipe', 'pipe'],
      env: childEnv,
    });

    let output = '';
    let errOutput = '';
    let requestId = 0;

    child.stdout.on('data', (d) => {
      output += d.toString();
    });

    child.stderr.on('data', (d) => {
      errOutput += d.toString();
    });

    function send(msg) {
      const line = JSON.stringify({ jsonrpc: '2.0', ...msg });
      child.stdin.write(line + '\n');
    }

    // Step 1: Initialize
    setTimeout(() => {
      requestId++;
      send({
        id: requestId,
        method: 'initialize',
        params: {
          protocolVersion: '2024-11-05',
          capabilities: {},
          clientInfo: { name: 'mcp-call', version: '1.0' },
        },
      });
    }, 500);

    // Step 2: List tools or call tool
    setTimeout(() => {
      requestId++;
      if (toolName === 'tools/list') {
        send({
          id: requestId,
          method: 'tools/list',
          params: {},
        });
      } else {
        send({
          id: requestId,
          method: 'tools/call',
          params: {
            name: toolName,
            arguments: toolArgs,
          },
        });
      }
    }, 1500);

    // Step 3: Collect and return
    setTimeout(() => {
      child.kill();

      // Parse all JSON-RPC messages
      const lines = output.split('\n').filter((l) => l.trim());
      let result = null;
      let error = null;

      for (const line of lines) {
        try {
          const msg = JSON.parse(line);
          if (msg.id === 2 && msg.result !== undefined) {
            result = msg.result;
          }
          if (msg.id === 2 && msg.error) {
            error = msg.error;
          }
          // Also capture tools/list results
          if (msg.id === 2 && msg.result?.tools) {
            result = msg.result;
          }
        } catch (e) {
          // ignore non-JSON lines
        }
      }

      // Also check for result in any message (not just id 2)
      if (!result && !error) {
        for (const line of lines) {
          try {
            const msg = JSON.parse(line);
            if (msg.result !== undefined) {
              result = msg.result;
            }
            if (msg.error) {
              error = msg.error;
            }
          } catch (e) {
            // ignore
          }
        }
      }

      if (error) {
        reject(new Error(`MCP error: ${JSON.stringify(error)}`));
        return;
      }

      if (!result) {
        // Maybe tool returned nothing, or we need to check stderr
        if (errOutput) {
          reject(new Error(`Server stderr: ${errOutput.slice(0, 500)}`));
          return;
        }
        reject(new Error('No result received from MCP server'));
        return;
      }

      resolve(result);
    }, 8000);

    child.on('error', (err) => {
      reject(new Error(`Failed to spawn: ${err.message}`));
    });
  });
}

function formatResult(result, asJson) {
  if (result.isError) {
    const text = result.content?.[0]?.text || 'Unknown error';
    if (asJson) {
      return JSON.stringify({ error: text });
    }
    return `Error: ${text}`;
  }

  // Handle tools/list response
  if (result.tools) {
    const tools = result.tools.map(t => ({
      name: t.name,
      description: t.description?.slice(0, 80)
    }));
    return asJson ? JSON.stringify(tools, null, 2) : tools.map(t => `${t.name}: ${t.description}`).join('\n');
  }

  const content = result.content || [];
  const texts = content
    .filter((c) => c.type === 'text')
    .map((c) => c.text)
    .join('\n');

  const images = content.filter((c) => c.type === 'image');

  if (asJson) {
    return JSON.stringify({ text: texts, images: images.length });
  }

  return texts || '(no text output)';
}

async function main() {
  const args = process.argv.slice(2);
  let asJson = false;
  let serverName, toolName, toolArgsRaw;

  if (args[0] === '--json') {
    asJson = true;
    [, serverName, toolName, toolArgsRaw] = args;
  } else {
    [serverName, toolName, toolArgsRaw] = args;
  }

  if (!serverName || !toolName) {
    console.error('Usage: node mcp-call.js [--json] <server-name> <tool-name> \'<json-args>\'');
    console.error('');
    console.error('Examples:');
    console.error('  node mcp-call.js desktop-commander read_file \'{\\"path\\":\\"/tmp/test.txt\\"}\'');
    console.error('  node mcp-call.js --json memory get_notes \'{}\'');
    process.exit(1);
  }

  let toolArgs = {};
  if (toolArgsRaw) {
    try {
      toolArgs = JSON.parse(toolArgsRaw);
    } catch (e) {
      console.error(`Invalid JSON args: ${e.message}`);
      process.exit(1);
    }
  }

  try {
    const configPath = findConfig();
    const config = loadConfig(configPath);
    const serverConfig = getServerConfig(config, serverName);

    const result = await callMcp(serverConfig, toolName, toolArgs);
    const output = formatResult(result, asJson);
    console.log(output);
    process.exit(0);
  } catch (err) {
    console.error(err.message);
    process.exit(1);
  }
}

main();
