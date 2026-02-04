from __future__ import annotations

import re
from typing import List

from .models import Plan, PlanStep, ToolCall
from tools.registry import list_tools


def _slugify(text: str) -> str:
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip().lower()).strip("-")
    return text or "step"


def build_plan(task: str) -> Plan:
    """A deliberately simple, deterministic planner.

    This starter does NOT call an LLM. It demonstrates the *planning interface*.
    Replace this with your preferred LLM planner later.
    """

    goal = task.strip()
    tools = list_tools()

    steps: List[PlanStep] = []

    # Heuristic: if the task looks like it needs arithmetic, add calculator tool.
    if re.search(r"\b(\d+\s*[-+*/]\s*\d+|calculate|计算)\b", goal, flags=re.I):
        steps.append(
            PlanStep(
                id=_slugify("compute"),
                title="Compute any required numbers",
                rationale="Use a calculator tool for deterministic arithmetic.",
                tool_call=ToolCall(tool="calculator", args={"expression": goal}),
                expected_output="A numeric result (if applicable).",
            )
        )

    # Always add a drafting step (no tool) as the final reasoning/write-up.
    steps.append(
        PlanStep(
            id=_slugify("draft"),
            title="Draft the final response",
            rationale="Synthesize outputs from prior steps into a helpful answer.",
            tool_call=None,
            expected_output="A clear, structured final answer.",
        )
    )

    # Include a note of available tools in rationale to make planning transparent.
    if steps and tools:
        steps[0].rationale += f" (Available tools: {', '.join(tools)})"

    return Plan(goal=goal, steps=steps)
