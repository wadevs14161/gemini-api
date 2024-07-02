import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv(".env")

from google.generativeai.types import HarmCategory, HarmBlockThreshold

llm = genai.GenerativeModel(
    "gemini-1.5-flash-latest",
    safety_settings={
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    },
    generation_config={
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
    },
)
chat = llm.start_chat(history=[])
# Please replace the content with your own role description
role = """
妳是一個二十五歲的年輕女性，喜歡游泳和閱讀。
妳聊天的目的是為了請對方送妳一份禮物。
以下是對方問的問題，你直接用這個角色回答就好，不用再舉例。
"""
