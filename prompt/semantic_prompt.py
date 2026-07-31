SEMANTIC_REQUEST_PROMPT = """
Convert the user's question into ResolveQueryRequest.

Return ONLY valid JSON.

Schema

{
    "metrics": [],
    "dimensions": [],
    "filters": [],
    "analysis": [],
    "patterns": []
}

Question

{question}
"""