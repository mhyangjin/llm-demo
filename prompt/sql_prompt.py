SQL_USER_PROMPT = """
Question

{question}

Semantic Metadata

{semantic_context}

Generate Athena SQL.

Use ONLY the supplied semantic metadata.
Do not invent any business metadata.
Return SQL only.
"""