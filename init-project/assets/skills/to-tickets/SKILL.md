---
name: to-tickets
description: Break a plan, spec, or the current conversation into tracer-bullet tickets in Linear, as sub-issues of the parent with native blocking links or as an in-place update of a single ticket, each sized and moved to Backlog - Groomed.
disable-model-invocation: true
---

# To Tickets

Break a plan, spec, or conversation into a set of **tickets**: tracer-bullet vertical slices, each declaring the tickets that **block** it. The tickets are written to Linear, either as sub-issues of an existing parent issue or, when the work is one ticket, as an update of that ticket in place.

## Process

### 1. Gather context

Work from whatever is already in the conversation context. If the user passes a reference (a Linear issue identifier or URL) as an argument, fetch it and read its full body and comments. That issue is the **source ticket**.

### 2. Explore the codebase (optional)

If you have not already explored the codebase, do so to understand the current state of the code. Ticket titles and descriptions should use the project's domain glossary vocabulary, and respect ADRs in the area you're touching.

Look for opportunities to prefactor the code to make the implementation easier. "Make the change easy, then make the easy change."

### 3. Draft vertical slices

Break the work into **tracer bullet** tickets.

<vertical-slice-rules>

- Each slice cuts a narrow but COMPLETE path through every layer (schema, API, UI, tests): vertical, NOT a horizontal slice of one layer
- A completed slice is demoable or verifiable on its own
- Each slice is sized to fit in a single fresh context window
- Any prefactoring should be done first

</vertical-slice-rules>

Give each ticket its **blocking edges**: the other tickets that must complete before it can start. A ticket with no blockers can start immediately.

**Wide refactors are the exception to vertical slicing.** A **wide refactor** is one mechanical change (rename a column, retype a shared symbol) whose **blast radius** fans across the whole codebase, so a single edit breaks thousands of call sites at once and no vertical slice can land green. Don't force it into a tracer bullet; sequence it as **expand–contract**. First expand: add the new form beside the old so nothing breaks. Then migrate the call sites over in batches sized by blast radius (per package, per directory), each batch its own ticket blocked by the expand, keeping CI green batch to batch because the old form still exists. Finally contract: delete the old form once no caller remains, in a ticket blocked by every migrate batch. When even the batches can't stay green alone, keep the sequence but let them share an integration branch that all block a final integrate-and-verify ticket; green is promised only there.

If the work is a single slice and there is a source ticket, the source ticket is updated in place instead of gaining a sub-issue.

### 4. Size each ticket

Give every ticket a point estimate: 1 point is half a dev-day with a coding agent writing the code. A ticket that is not sized is not ready for the betting table. A parent that gains sub-issues is not sized itself; its children carry the points.

Decide for each ticket whether it goes to the **betting table** (the default) or is **assigned into the current cycle**. A ticket is in the current cycle when its cycle is the team's active cycle, or when the user assigns it there now.

### 5. Quiz the user

Present the proposed breakdown as a numbered list. For each ticket, show:

- **Title**: short descriptive name
- **Blocked by**: which other tickets (if any) must complete first
- **What it delivers**: the end-to-end behaviour this ticket makes work
- **Points**
- **Betting table or current cycle** (and the assignee, for the current cycle)

Ask the user:

- Does the granularity feel right? (too coarse / too fine)
- Are the blocking edges correct: does each ticket only depend on tickets that genuinely gate it?
- Should any tickets be merged or split further?
- Are the sizes right?

Iterate until the user approves the breakdown.

### 6. Write the tickets to Linear

Before writing anything, confirm the `Betting Table` label and the `Backlog - Groomed` state exist in the team. If either is missing, stop and tell the user. Never create a label, and never apply `ready-for-agent` or `ready-for-human`.

Every ticket gets its estimate. Then, by where it goes:

- **Betting table**: add the `Betting Table` label and move it to `Backlog - Groomed`.
- **Current cycle**: set the assignee and the current cycle, keep its cycle state (such as `Todo`), and add no `Betting Table` label.

Adding a label keeps the ticket's existing labels.

**Several tickets:** create one sub-issue of the source ticket per ticket, in dependency order (blockers first), in the source ticket's team and project, so each ticket's blocking edges can reference real identifiers. Use Linear's native blocking relation for every edge, and also list the blockers in the ticket's "Blocked by" section. Then update the source ticket: move it to `Backlog - Groomed` unless it is in the current cycle, and fill the Ticket column of its "Needs, by ticket" table with the new identifiers. Change nothing else on it, and give it no estimate or `Betting Table` label.

**One ticket:** rewrite the source ticket's description in the issue template below, keeping every fact from the current description, and apply the estimate, label and state above. Create no new issue.

**No source ticket:** ask the user which existing issue the tickets belong under before writing anything.

<issue-template>

## Parent

A reference to the parent issue (omit this section on a single ticket updated in place that has no parent).

## What to build

The end-to-end behaviour this ticket makes work, from the user's perspective, not layer-by-layer implementation. One paragraph stating the end state.

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Evidence

- Each fact the ticket rests on, ending with its source and date (for example "Read from source, 2026-09-22").

## Blocked by

- A reference to each blocking ticket, or "None (can start immediately)".

## Out of scope

- Each excluded item, naming the ticket that owns it.

</issue-template>

Avoid specific file paths or code snippets: they go stale fast. Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it and note briefly that it came from a prototype. Trim to the decision-rich parts, not a working demo, just the important bits.
