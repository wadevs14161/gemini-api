import requests
from IPython.display import Image, display

# image_url = "https://i.imgur.com/1HzX3QH.jpg"
# content = requests.get(image_url).content
# Image(content)


from configparser import ConfigParser
import os

# Set up config parser
config = ConfigParser()
config.read("config.ini")

# Set up Google Gemini API key
os.environ["GOOGLE_API_KEY"] = config["Gemini"]["API_KEY"]

from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest")
# example
# image_url = "https://i.imgur.com/1HzX3QH.jpg"
image_url = "https://i.ibb.co/KyNtMw5/IMG-20240321-172354614-AE.jpg"
# image_url = "images.jpeg"
# image from static/images folder
image_url = "stock.png"
# user_question = "Please rate the people in the image based on their facial expressions."
# user_question += " Please give a score from 1 to 10 for the following emotions: happiness, sadness, anger, surprise, disgust, fear, and neutral."
user_question = "請分析我的投資情況。"
user_question += " 請使用繁體中文回答。"
message = HumanMessage(
    content=[
        {
            "type": "text",
            "text": user_question,
        },  # You can optionally provide text parts
        {
            "type": "image_url", 
            "image_url": image_url},
    ]
)
result = llm.invoke([message])
print("問：", user_question)
print("答：", result.content.lstrip(" "))
if "http" in image_url:
    content = requests.get(image_url).content
else:
    content = image_url
# Image(content)