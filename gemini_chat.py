import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
# from dotenv import load_dotenv

# load_dotenv(".env")

class GeminiChat:
    def __init__(self):
        self.llm = genai.GenerativeModel(
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

        self.chat = self.llm.start_chat(history=[])

        self.role = """
            你是一個面試官。
            """

    def llm_chat(self, to_llm):
        to_llm = "我: " + to_llm

        response = self.chat.send_message(to_llm)

        return response.text.replace("\n", "")


def llm_chat(to_llm):
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
    你是一個面試官。
    """

    to_llm = "我: " + to_llm
    return chat.send_message(to_llm)

if __name__ == "__main__":
    chat = GeminiChat()
    print(chat.llm_chat("你好"))

