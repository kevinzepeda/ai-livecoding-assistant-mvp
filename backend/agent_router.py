import openai
from session_store import get_session

async def route_message(session_code, user_input):
    history = get_session(session_code)

    messages = [{"role": m["role"], "content": m["content"]} for m in history]
    messages.append({"role": "user", "content": user_input})

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        max_tokens=1000,
    )
    return response.choices[0].message.content
