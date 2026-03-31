## Workflow Orchestration

  ### 1. Plan Node Default
  - Enter plan mode for ANY non-trivial task (3+ steps or architectural decisions)
  - Always use context7 for research and documentation when implementing any apis or reviewing documentation.
  - If something goes sideways, STOP and re-plan immediately — don't keep pushing
  - Use plan mode for verification steps, not just building
  - Write detailed specs upfront to reduce ambiguity

  ### 2. Subagent Strategy
  - Use subagents liberally to keep main context window clean
  - Offload research, exploration, and parallel analysis to subagents
  - For complex problems, throw more compute at it via subagents
  - One task per subagent for focused execution

  ### 3. Self-Improvement Loop
  - After ANY correction from the user: update tasks/lessons.md with the pattern
  - Write rules for yourself that prevent the same mistake
  - Ruthlessly iterate on these lessons until mistake rate drops
  - Review tasks/lessons.md at session start

  ### 4. Verification Before Done
  - Never mark a task complete without proving it works
  - Diff behaviour between main and your changes when relevant
  - Ask yourself: "Would a staff engineer approve this?"
  - Run tests, check logs, demonstrate correctness

  ### 5. Demand Elegance (Balanced)
  - For non-trivial changes: pause and ask "is there a more elegant way?"
  - If a fix feels hacky: "Knowing everything I know now, implement the elegant solution"
  - Skip this for simple, obvious fixes — don't over-engineer

  ### 6. Autonomous Bug Fixing
  - When given a bug report: just fix it. Don't ask for hand-holding
  - Point at logs, errors, failing tests — then resolve them
  - Go fix failing CI tests without being told how

  ### 7. Debugging
  - When debugging, if you do not have clear logs, do research on web and context7 before guessing. 
  - If you have attempted a fix more than twice without advancing the issue, stop and re-evaluate your approach
  - After solving an issue, always give a clear RCA. 

  ## Task Management
  - Plan First: Write plan to tasks/todo.md with checkable items
  - Verify Plan: Check in before starting implementation
  - Track Progress: Mark items complete as you go
  - Explain Changes: High-level summary at each step
  - Document Results: Add review section to tasks/todo.md
  - Capture Lessons: Update tasks/lessons.md after corrections

  ## Core Principles
  - Simplicity First: Make every change as simple as possible. Impact minimal code.
  - No Laziness: Find root causes. No temporary fixes. Senior developer standards.
  - Minimal Impact: Changes should only touch what's necessary. Avoid introducing bugs.
  - Always use Context7 for SDK/library API documentation. For cloud provider workflows, IAM, and security practices, cross-check with a web search against official docs — Context7 may have stale information.
