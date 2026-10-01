---
name: to-spec
description: "Turn the current conversation into a spec and write it into the parent Linear issue's description: no interview, just synthesis of what you've already discussed."
disable-model-invocation: true
---

This skill takes the current conversation context and codebase understanding and produces a spec. Do NOT interview the user; just synthesize what you already know.

The spec is written into the description of an existing Linear issue, the **parent**. This skill creates no new issue, writes no local file, and changes no labels, state, estimate or assignee. Splitting the spec into sub-issues is `/to-tickets`.

## Process

1. Identify the parent: the Linear issue passed as an argument, or the one the conversation is about. If neither is clear, ask the user which issue to write into. Read its full description and comments.

2. Explore the repo to understand the current state of the codebase, if you haven't already. Use the project's domain glossary vocabulary throughout the spec, and respect any ADRs in the area you're touching.

3. Sketch out the seams at which you're going to test the feature. Existing seams should be preferred to new ones. Use the highest seam possible. If new seams are needed, propose them at the highest point you can. The fewer seams across the codebase, the better - the ideal number is one.

Check with the user that these seams match their expectations.

4. Write the spec using the template below. The spec replaces the parent's description. Carry anything in the current description that the spec does not already cover into the matching section or into Further Notes; never drop it silently.

5. Show the user the complete new description and wait for approval. Then update the parent's description with it, and nothing else on the issue.

<spec-template>

## Problem Statement

The problem that the user is facing, from the user's perspective.

## Solution

The solution to the problem, from the user's perspective.

## Needs, by ticket

A short table, about ten rows, one line per row:

| # | Who | Needs | Ticket |
| -- | -- | -- | -- |
| 1 | <actor> | <what they need, in a few words> | <sub-issue> |

Each row names who needs something and what, not how it is built. The sub-issues do not exist yet, so write "pending" in the Ticket column; `/to-tickets` fills in the identifiers when it creates them.

## Implementation Decisions

A list of implementation decisions that were made. This can include:

- The modules that will be built/modified
- The interfaces of those modules that will be modified
- Technical clarifications from the developer
- Architectural decisions
- Schema changes
- API contracts
- Specific interactions

Do NOT include specific file paths or code snippets. They may end up being outdated very quickly.

Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it within the relevant decision and note briefly that it came from a prototype. Trim to the decision-rich parts, not a working demo, just the important bits.

## Testing Decisions

A list of testing decisions that were made. Include:

- A description of what makes a good test (only test external behavior, not implementation details)
- Which modules will be tested
- Prior art for the tests (i.e. similar types of tests in the codebase)

## Out of Scope

A description of the things that are out of scope for this spec.

## Further Notes

Any further notes about the feature.

</spec-template>
