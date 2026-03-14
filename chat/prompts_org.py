def build_event_prompt(
    ticker: str,
    start_date: str,
    end_date: str,
    event_name: str,
    event_outputs: dict
) -> str:

    prompt = f"""
You are a financial explainer bot.

Your task:
- Explain the "{event_name}" analysis for a BEGINNER.
- Use ONLY the data provided below.
- Do NOT introduce new metrics.
- Do NOT make predictions.
- Do NOT give financial advice.

Context:
Stock: {ticker}
Period: {start_date} to {end_date}

Event outputs:
"""

    for k, v in event_outputs.items():
        prompt += f"- {k}: {v}\n"

    prompt += """
Explanation rules:
- Be clear and simple.
- Explain what the numbers mean.
- Focus on intuition.
"""

    return prompt.strip()
