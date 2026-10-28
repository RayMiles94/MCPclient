# MCP Chat Client

A minimal command-line client that connects to a [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server over stdio and lets Claude use the server's tools to answer your queries.

## How it works

1. The client launches your MCP server as a subprocess (`python` for `.py` scripts, `node` for `.js` scripts).
2. It connects over stdio and lists the tools the server exposes.
3. Each query is sent to Claude together with those tool definitions.
4. If Claude requests a tool call, the client executes it on the MCP server, sends the result back to Claude, and returns Claude's final answer.

```
You ──query──▶ Client ──messages + tools──▶ Claude
                 ▲                            │ tool_use
                 │                            ▼
            MCP Server ◀──call_tool────── Client
                 └──────tool_result──────────▶ Claude ──▶ final answer
```

## Requirements

- Python 3.10+
- An Anthropic API key
- An MCP server script (`.py` or `.js`) to connect to

### Dependencies

```bash
pip install anthropic mcp python-dotenv
```

## Setup

Create a `.env` file in the project root:

```env
ANTHROPIC_API_KEY=your_api_key_here
```

The key is loaded automatically via `python-dotenv`.

## Usage

```bash
python client.py <path_to_server_script>
```

Examples:

```bash
python client.py ./weather_server.py
python client.py ./build/index.js
```

On startup the client prints the names of the tools exposed by the server:

```
Connected to server with tools: ['get_forecast', 'get_alerts']
```

In interactive mode, type a query at the `Query:` prompt, or type `quit` to exit.

## Configuration

| Setting      | Location              | Description                               |
|--------------|-----------------------|-------------------------------------------|
| `MODEL`      | top of `client.py`    | Claude model used for requests            |
| `max_tokens` | `process_query`       | Max tokens per response (default `1000`)  |

## Code overview

| Function         | Purpose                                                                                       |
|------------------|-----------------------------------------------------------------------------------------------|
| `server_params`  | Builds the `StdioServerParameters` used to launch the server (`python` or `node`).            |
| `process_query`  | Sends a query to Claude, executes any requested tool calls via MCP, and returns the final text.|
| `chat_loop`      | Interactive REPL that reads queries and prints responses.                                     |
| `main`           | Parses CLI arguments, connects to the server, and lists available tools.                      |

## Limitations

- Only `.py` and `.js` server scripts are supported.
- Only one round of tool calls is handled per query; if Claude requests further tool calls in its follow-up response, they are not executed.
- Only text content from tool results is passed back to Claude.
- Each query is independent; conversation history is not kept between queries.

## Troubleshooting

- **`usage: python client.py <path_to_server_script>`**: you didn't pass a server script path.
- **`Server script must be a .py or .js file`**: the path has an unsupported extension.
- **Authentication errors**: check that `ANTHROPIC_API_KEY` is set in `.env`.
- **Model not found**: verify the `MODEL` value is a valid model ID.
