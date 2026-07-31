# LLM Responsibilities

The LLM performs reasoning.

## Step 1

```text
Natural Language
  ↓
ResolveQueryRequest
```

---

## Step 2

```text
ResolveQueryResponse
  ↓
Athena SQL
```

---

## Rules

- The LLM never executes SQL.
- Always use MCP.
