from .semantic_prompt import SEMANTIC_REQUEST_PROMPT
from .sql_prompt import SQL_USER_PROMPT


def build_semantic_prompt(question: str) -> str:
    return SEMANTIC_REQUEST_PROMPT.format(
        question=question,
    )


def build_sql_prompt(
    question: str,
    semantic_context: dict,
) -> str:
    return SQL_USER_PROMPT.format(
        question=question,
        semantic_context=semantic_context,
    )