---
name: ask-sme
description: Post a question on a Linear ticket for its SME, reporter or team lead to answer, and add the needs-info label.
disable-model-invocation: true
---

# Ask SME

Post a question on a Linear ticket as a comment and add the `needs-info` label. The comment's first word names who answers:

- `SME:` the ticket's subject matter expert, who decides requirements and the definition of done. This is the default.
- `Reporter:` the person who filed the request.
- `Lead:` the team lead who approved it.

Someone else relays the question to that person and writes the answer back, so the comment must be answerable on its own.

## Process

### 1. Identify the ticket

Use the Linear issue passed as an argument, or the one the conversation is about. If neither is clear, ask the user. Read its description and comments so the question does not ask for something already answered.

### 2. Pick who answers

If the user's question starts with `SME:`, `Reporter:` or `Lead:` (any capitalization), that person answers. Otherwise the SME answers. Write the word exactly as shown above.

### 3. Draft the comment

The first line starts with the target word, followed by the question. Write for someone who has never opened Linear or the code:

- Plain words: no ticket identifiers, links, file paths or engineering terms.
- Enough context to answer without reading the ticket.
- Related questions go in one comment as a numbered list; each can carry your best guess for the person to confirm or correct.

### 4. Confirm, then post

Show the user the exact comment and wait for approval. Then:

1. Confirm the `needs-info` label exists in the ticket's team. If it does not, stop and tell the user; never create a label.
2. Post the comment on the ticket.
3. Add `needs-info`, keeping the ticket's other labels. If it is already there, leave it.

Change nothing else: not the state, assignee, estimate or description. Do not remove `needs-info` later; it comes off when the answer is written back.
