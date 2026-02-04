from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


class ToolCall(BaseModel):
    """A single tool invocation."""

    tool: str = Field(..., description="Tool name from the registry")
    args: Dict[str, Any] = Field(default_factory=dict)


class PlanStep(BaseModel):
    """One executable step in a plan."""

    id: str
    title: str
    rationale: str = ""
    tool_call: Optional[ToolCall] = None
    expected_output: str = ""


class Plan(BaseModel):
    """A plan is an ordered list of steps with optional tool calls."""

    goal: str
    steps: List[PlanStep] = Field(default_factory=list)


class StepResult(BaseModel):
    step_id: str
    status: Literal["ok", "skipped", "error"]
    output: str = ""
    error: str = ""


class RunResult(BaseModel):
    goal: str
    plan: Plan
    results: List[StepResult]
    final_answer: str
