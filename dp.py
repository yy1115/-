from openai import OpenAI
from config import DP_KEY


 
client = OpenAI(api_key=DP_KEY, base_url="https://api.deepseek.com")

def get_result(sys_prompt, user_input):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_input},
        ],
        stream=False
    )

    # print(response.choices[0].message.content)
    return response.choices[0].message.content