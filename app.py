from flask import Flask, render_template, url_for, Response
from flask import request
from dotenv import load_dotenv
import google.generativeai as genai

from gemini_video import GeminiVideo
from gemini_interview import interview_evaluate
from gemini_tts import text_to_speech
from gcp_gcs import gcs_signed_url_v4
from upload import upload_audio

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


@app.route("/interview_question", methods=["GET", "POST"])
def interview_question():
    if request.method == "POST":
        question = request.form["question"]
        user_answer = request.form["user_answer"]

        # Request Gemini to evaluate the user's answer
        result = interview_evaluate(question, user_answer)

        return result
    
    return {"Status": "Interview question funcion is available now!"}

@app.route("/texttospeech", methods=["GET", "POST"])
def tts():
    if request.method == "POST":
        # Get text from post request with key "text"
        text = request.form["text"]

        # Call text to speech function to output the audio file in mp3 format
        text_to_speech(text)

        signed_url = gcs_signed_url_v4("wenshin-tts-bucket", "cloud_tts.mp3")

        upload_url = signed_url.generate_upload_signed_url_v4()

        upload_audio(upload_url)

        download_url = signed_url.generate_download_signed_url_v4()

        return download_url


        
    
    return {"Status": "Text to speech funcion is available now!"}

    

if __name__ == "__main__":
    app.run(debug=True)