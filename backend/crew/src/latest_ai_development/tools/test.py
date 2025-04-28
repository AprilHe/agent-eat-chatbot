from openai import OpenAI
client = OpenAI(api_key="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")

response = client.responses.create(
    model="gpt-4o-mini",
    input="Write a one-sentence bedtime story about a unicorn."
)

print(response.output_text)

