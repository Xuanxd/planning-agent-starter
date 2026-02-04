# planning-agent-starter

A minimal **plan-then-execute** Planning Agent starter template in **Python**, with pluggable tools.

## What you get

- A simple Agent loop that:
  1) builds a **plan** (structured steps)
  2) (optionally) requires **human approval** before execution
  3) executes steps with a small, safe toolset
  4) returns a final answer + execution trace

- Extensible tool interface (`tools/base.py`)
- Example tool: calculator (`tools/calculator.py`)
- Example tasks in `examples/`

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python -m agent.cli --task "Summarize my plan for learning Rust in 2 weeks"
python -m agent.cli --task "计算 12*7+3"

# stop before execution (approval gate)
python -m agent.cli --task "Draft an email outline" --require-approval
```

## Repo structure

- `agent/` core planning agent (planner + executor + CLI)
- `tools/` tool interfaces + implementations
- `examples/` runnable examples

## Next steps

- Replace `agent/planner.py` with an LLM-based planner
- Add more tools and register them in `tools/registry.py`
- Add tests + CI

## License

MIT
