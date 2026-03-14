from chat.prompts_org import build_event_prompt
from llm.ollama_client import call_llm


def explain_event_with_llm(
    ticker: str,
    start_date: str,
    end_date: str,
    event_name: str,
    event_outputs: dict
) -> str:

    prompt = build_event_prompt(
        ticker=ticker,
        start_date=start_date,
        end_date=end_date,
        event_name=event_name,
        event_outputs=event_outputs
    )

    return call_llm(prompt)
