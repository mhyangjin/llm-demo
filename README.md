# Semantic API

[한국어](#한국어) | [English](#english)

---

## 한국어

GitHub Copilot을 이용한 테스트 가이드입니다.

### 사전 준비

LLM Demo를 테스트하기 전에 `semantic-api` 프로젝트의 MCP Server를 먼저 실행해야 합니다.

예시:

```bash
python -m mcp_server.server
```

또는 프로젝트에서 사용하는 MCP 실행 명령을 사용합니다.

MCP Server가 정상 실행되면 LLM Demo는 MCP Tool을 통해 Semantic Layer와 통신할 수 있습니다.

### 주의

`semantic-api` 프로젝트와 `llm-demo` 프로젝트를 동일한 Workspace에서 열지 않는 것을 권장합니다.

GitHub Copilot은 Workspace 내 소스코드를 분석할 수 있으므로, Semantic Layer 프로젝트를 함께 열어두면 Resolver나 YAML 메타데이터를 직접 읽어 SQL을 생성할 수 있습니다.

실제 운영 환경(SageMaker)에서는 이러한 소스코드에 접근할 수 없으므로, 테스트 환경도 동일한 제약을 유지하는 것이 중요합니다.

### Copilot 테스트

새로운 Copilot Chat을 시작한 후 다음 프롬프트를 입력합니다.

```text
Read the following documents before answering.
docs/README.md
docs/ARCHITECTURE.md
docs/LLM.md
docs/MCP.md
docs/CODING_GUIDE.md
docs/COPILOT.md
Summarize your understanding of this project.
Wait for my first question.
```

Copilot이 프로젝트를 이해한 후 자연어 질문을 입력합니다.

예시 질문:

> 지난달 채널별 발송 성공 건수를 보여줘.

정상적인 AI Agent의 동작 순서:

```text
사용자 질문
      │
      ▼
ResolveQueryRequest 생성
      │
      ▼
Semantic Layer MCP 호출
      │
      ▼
ResolveQueryResponse 수신
      │
      ▼
Athena SQL 생성
```

LLM은 메트릭, 차원, 필터, 테이블을 직접 추론해서는 안 되며, 반드시 Semantic Layer가 반환한 메타데이터만 사용해야 합니다.

### 성공 기준

- MCP Tool을 이용하여 Semantic Layer를 조회한다.
- 반환된 메타데이터만 사용하여 SQL을 생성한다.
- 메타데이터를 임의로 생성하거나 추론하지 않는다.

### 실패 사례

- Semantic Layer를 호출하지 않고 SQL을 생성한다.
- Metric, Dimension, Filter, Table을 임의로 생성한다.
- Semantic Layer 소스코드를 직접 참고하여 SQL을 생성한다.

---

## English

Testing guide with GitHub Copilot.

### Prerequisites

Before testing the LLM Demo, start the Semantic Layer MCP Server from the `semantic-api` project.

Example:

```bash
python -m mcp_server.server
```

Or use the MCP startup command defined by your project.

Once the MCP Server is running, the LLM Demo can communicate with the Semantic Layer through the MCP Tool.

### Important

Open only the `llm-demo` project in your IDE.

Do not open the `semantic-api` project in the same workspace.

GitHub Copilot can analyze files inside the current workspace. If the Semantic Layer project is opened together with the demo project, Copilot may read the Resolver implementation or YAML metadata directly instead of calling the MCP Tool.

In production (SageMaker), the LLM has no access to the Semantic Layer source code. The local test environment should follow the same restriction.

### Copilot Test

Start a new Copilot Chat and enter the following prompt.

```text
Read the following documents before answering.
docs/README.md
docs/ARCHITECTURE.md
docs/LLM.md
docs/MCP.md
docs/CODING_GUIDE.md
docs/COPILOT.md
Summarize your understanding of this project.
Wait for my first question.
```

After Copilot understands the project, ask a natural language question.

Example:

> Show me the number of successful message deliveries by channel for last month.

Expected workflow:

```text
User Question
      │
      ▼
Create ResolveQueryRequest
      │
      ▼
Call Semantic Layer MCP
      │
      ▼
Receive ResolveQueryResponse
      │
      ▼
Generate Athena SQL
```

The LLM must never infer business metadata by itself. It must generate SQL using only the metadata returned by the Semantic Layer.

### Success Criteria

- Calls the Semantic Layer through the MCP Tool.
- Generates SQL using only the returned metadata.
- Does not invent or infer business metadata.

### Failure Cases

- Generates SQL without calling the Semantic Layer.
- Invents metrics, dimensions, filters, or table names.
- Reads Semantic Layer source code instead of using the MCP Tool.
