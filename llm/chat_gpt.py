# import os
# from openai import AsyncOpenAI

# # client = AsyncOpenAI(api_key="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")
# # with open(f"{os.getcwd()}/config/compiled_prompt.txt", 'r', encoding='utf-8') as f:
# #     prompt = f.read()


# # async def get_response(query: str, context: str) -> str:
# #     response = await client.chat.completions.create(
# #         model="chatgpt-4o-latest",
# #         messages=[{"role": "user", "content": prompt},
# #                   {"role": "user", "content": query}],
# #         stream=False,
# #     )
    
# #     return response.choices[0].message.content