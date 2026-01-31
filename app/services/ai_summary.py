import os
from dotenv import load_dotenv


load_dotenv()

# USE_AI = os.getenv("OPENAI_API_KEY") is not None

USE_AI = True

if USE_AI:
    from app.services.ai_client import OllamaClient
    ai_client = OllamaClient()
else:
    ai_client = None

def generate_summary(metrics: dict):
    if not USE_AI:
        return local_summary(metrics)

    try:
        from openai import OpenAI

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        prompt = f"""
You are an operations analyst.
Explain the following metrics in clear, concise business language.
Highlight anything notable.

Metrics:
- Total Requests: {metrics['total_requests']}
- Total Cost: {metrics['total_cost']}
- Average Cost per Request: {metrics['average_cost_per_request']}
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You explain operational data clearly."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return local_summary(metrics)



def generate_ai_summary(metrics: dict):
    if not USE_AI:
        return "AI summarization is disabled."

    prompt = f"""
    You are a data analyst.

    Given the following metri   cs, write a concise insight summary.
    Highlight anomalies and risks.

    Metrics:
    {metrics}
    """

    return ai_client.generate(prompt)




def local_summary(metrics: dict):
    return (
        f"During this period, a total of {metrics['total_requests']} requests were handled "
        f"at a total cost of {metrics['total_cost']}. "
        f"The average cost per request was approximately "
        f"{metrics['average_cost_per_request']}, indicating overall operational efficiency."
    )

# Test block
# if __name__ == "__main__":
#     test_metrics = {
#         "users": 1240,
#         "conversion_rate": "1.2%",
#         "checkout_dropoff": "63%"
#     }

#     print(generate_ai_summary(test_metrics))