from __future__ import annotations

import argparse

from rich import print

from .executor import execute_plan
from .planner import build_plan


def main() -> None:
    p = argparse.ArgumentParser(prog="planning-agent")
    p.add_argument("--task", required=True, help="Task to solve")
    p.add_argument(
        "--require-approval",
        action="store_true",
        help="Stop before execution and require a human approval step",
    )
    args = p.parse_args()

    plan = build_plan(args.task)

    print("[bold]Plan[/bold]")
    print(plan.model_dump())

    if args.require_approval:
        print("\n[yellow]Approval required. Exiting before execution.[/yellow]")
        return

    result = execute_plan(plan, require_approval=False)

    print("\n[bold]Result[/bold]")
    print(result.model_dump())


if __name__ == "__main__":
    main()
