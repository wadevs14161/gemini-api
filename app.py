from flask import Flask, render_template, url_for
from flask import request
from dotenv import load_dotenv
import google.generativeai as genai

from gemini_video import GeminiVideo

# Load environment variables
load_dotenv('.env')


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/call_llm", methods=["POST"])
def call_llm():
    if request.method == "POST":
        from gemini_chat import chat, role
        print("POST!")
        data = request.form
        print(data)
        to_llm = ""
        if len(chat.history) > 0:
            to_llm = data["message"]
        else:
            to_llm = role + data["message"]
        try:
            result = chat.send_message(to_llm)
        except Exception as e:
            print(e)
            return "我媽來了，她說不能聊這個(雙手比叉)"
        print(chat.history)
        # remove \n at the end of the result
        return result.text.replace("\n", "")
    
@app.route("/video", methods=["GET", "POST"])
def video():
    if request.method == "POST":
        gemini_video = GeminiVideo()

        # Get video file from the request
        video = request.files["video"]
        video.save(video.filename)

        print(video.filename)
        # Upload the video file
        video_file = gemini_video.upload_video(video.filename)

        # Analyze the video
        result = gemini_video.analyze_video(video_file)

        # Delete the video file
        gemini_video.delete_video(video_file)

        # Delete the local video file
        import os
        os.remove(video.filename)
        print("Deleted local file")

        return result

    return {"Status": "Video funcion is available now!"}
    

if __name__ == "__main__":
    app.run(debug=True)