# image-handoff — Skill Card

| Field | Value |
|-------|-------|
| **Name** | image-handoff |
| **Version** | — |
| **One-liner** | Detect image generation requests and route them to the artist agent. |

## Trigger
- `!img <prompt>` — immediate handoff
- "draw me...", "generate an image of...", "make a picture of..."
- "sketch...", "render...", "visualize..."

## Key Commands

No CLI commands — this is a routing skill.

1. Detect explicit trigger (`!img`) or auto-detect + ask for confirmation
2. Extract prompt and style preferences from memory
3. Send to artist agent via `sessions_send`
4. Deliver result back to user
5. Log to `memory/image-requests.md`

## Dependencies
- Artist agent available via `sessions_send`

## Quick Example

```
User: !img a cat in space
→ Extract prompt: "a cat in space"
→ Send to artist agent with request ID
→ Return generated image to user
```

> Log request ID, prompt, model, result, and user feedback to `memory/image-requests.md`.
