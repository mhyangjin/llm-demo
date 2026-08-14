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
get_table() / get_dimension() (MCP)  ← 컬럼-테이블 귀속 확인
  ↓
Athena SQL
```

---

## Rules

- The LLM never executes SQL.
- Always use MCP.
- **Never infer which table a column or filter belongs to.**  
  Always call `get_table()` or `get_dimension()` to obtain the table attribute.

---

## Step 2 Detail: Resolving Column-Table Mapping

`ResolveQueryResponse` returns `tables`, `dimensions`, and `filters`,  
but does **not** specify which table each column belongs to.

The LLM **must not guess** column-to-table assignments.  
Instead, call the MCP tools below to retrieve table metadata before writing SQL.

### MCP Tools for Table Metadata

| Tool | Purpose |
|------|---------|
| `get_table(name)` | Returns schema info (columns, types) for a table |
| `get_dimension(name)` | Returns which table a dimension column belongs to |

### Workflow

```text
ResolveQueryResponse received
  ↓
For each dimension/filter in the response:
  → call get_dimension(name)  or  get_table(name)
  → confirm the table that owns the column
  ↓
Build SQL using only the confirmed table.column mappings
```

### Example

`ResolveQueryResponse` returns:
```json
{
  "dimensions": ["customer"],
  "tables": ["inbox", "recipient"],
  "filters": [
    {"dimension": "result", "operator": "=", "value": "SUCCESS"}
  ]
}
```

Before writing SQL, call:
```python
get_dimension("result")   # → confirms which table owns the 'result' column
get_dimension("customer") # → confirms which table owns the 'customer' column
```

Only after receiving the response from the Semantic Layer may the LLM assign columns to tables in the SQL.

---

## ResolveQueryRequest Field Selection Rules

### metrics
Use **only** when the question asks for an **aggregated/calculated value**.

Keywords: 건수, 합계, 평균, 비율, 수, 몇 명, 몇 건, count, sum, rate

Examples:
- "채널별 발송 성공 **건수**" → `metrics=["발송 성공 건수"]`
- "이벤트별 **평균** 오픈율" → `metrics=["오픈율"]`

### filters
Use when the question **restricts or conditions** the result set.

Keywords: 성공한, 실패한, 오늘, 지난달, ~인, ~한, ~번, ~ID

Examples:
- "**성공한** 고객" → `filters=["발송 성공"]`
- "**오늘** 발송" → `filters=["오늘"]`
- "**이벤트 21번**" → `filters=["이벤트 ID 21"]`

### dimensions
Use when the question asks to **list, group by, or break down** by a specific field.

Keywords: ~별, 목록, 명단, ID, 리스트

Examples:
- "고객 **ID**를 알고 싶어" → `dimensions=["고객"]`
- "**채널별** 발송 건수" → `dimensions=["채널"]`

---

## Decision Guide

| Question type | metrics | dimensions | filters |
|--------------|---------|------------|---------|
| 건수/합계/평균 조회 | ✅ 사용 | 그룹 기준 | 조건 |
| 목록/ID 조회 | ❌ 사용 안 함 | 조회 대상 | 조건 |
| 조건부 목록 | ❌ 사용 안 함 | 조회 대상 | ✅ 조건 포함 |

Example — "오늘 이벤트 21번으로 발신한 내역 중 성공한 고객 ID":
```python
ResolveQueryRequest(
    metrics=[],              # 집계 없음 → 목록 조회
    dimensions=["고객"],     # 가져올 값: 고객 ID
    filters=["이벤트 ID 21", "오늘", "발송 성공"],  # 조건
)
```

