# Claude Prompt Guidelines

## Core Principles

- You are implementing an AI Text-to-SQL system.
- The Semantic Layer is an external system.
- Always obtain metadata through the MCP tool.
- Do not invent metrics, dimensions, or tables.
- The Semantic Layer is the single source of truth.

## Workflow

```text
Question
  ↓
ResolveQueryRequest
  ↓
MCP Tool
  ↓
ResolveQueryResponse
  ↓
Athena SQL
```