from __future__ import annotations

from typing import List

from .models import Plan, RunResult, StepResult
from tools.registry import get_tool


def execute_plan(plan: Plan, require_approval: bool = False) -> RunResult:
    results: List[StepResult] = []

    if require_approval:
        # In real apps you might ask a user/UI for approval. Here we just block.
        raise RuntimeError(
            "Approval gate is enabled. Integrate your UI/CLI approval flow in agent/cli.py."
        )

    for step in plan.steps:
        if step.tool_call is None:
            results.append(StepResult(step_id=step.id, status="skipped", output="No tool"))
            continue

        try:
            tool = get_tool(step.tool_call.tool)
            out = tool.run(**step.tool_call.args)
            results.append(StepResult(step_id=step.id, status="ok", output=str(out)))
        except Exception as e:  # noqa: BLE001
            results.append(StepResult(step_id=step.id, status="error", error=str(e)))

    # Minimal final answer: echo task + any tool outputs.
    tool_outputs = "\n".join(
        f"- {r.step_id}: {r.output}" for r in results if r.status == "ok" and r.output
    )
    final = f"Goal: {plan.goal}\n\nTrace:\n{tool_outputs}\n\nAnswer:\n(Replace this with LLM-based write-up.)"

    return RunResult(goal=plan.goal, plan=plan, results=results, final_answer=final)
