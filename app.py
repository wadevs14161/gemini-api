from flask import Flask, render_template, url_for, Response
from flask import request
from dotenv import load_dotenv

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
        print("POST!")
        data = request.form
        print(data)

        from gemini_chat import GeminiChat

        newChat = GeminiChat()

        to_llm = ""
        if len(newChat.chat.history) > 0:
            to_llm = data["usermsg"]
        else:
            to_llm = newChat.role + data["usermsg"]
        try:
            result = newChat.chat.send_message(to_llm)
        except Exception as e:
            print(e)
            return "請注意，您的訊息可能包含不當內容，請重新輸入。"
        print(newChat.chat.history)
        # remove \n at the end of the result
        return result.text.replace("\n", "")
    
@app.route("/video", methods=["GET", "POST"])
def video():
    if request.method == "POST":
        gemini_video = GeminiVideo()

        # Get video file from the request
        video = request.files["video"]
        if not video:
            return {"error": "No video file found"}
        video.save(video.filename)

        prompt = ""
        if "prompt" in request.form:
            prompt = request.form["prompt"]
        else:
            prompt = '''
                1. 請總結並評價面試者的整體表現。

                2. 請針對面試者下列的表現做出評分(1-100分):
                - 視覺評價: 1. 臉部情緒特徵(30%): 是否友善、正向、自信? 或是木訥、膽怯、害羞。 2. 肢體動作(20%): 是否沉穩、自信、大方； 3. 眼神交流 (15%)、4. 微笑是否自然 (15%)、5. 衣著整潔(20%)。
                - 言語內容: 1. 言語用字(30%): 是否得體、2. 表達邏輯 (70%): 是否清晰、通順，抑或前後矛盾。
                - 聽覺評價: 1. 語速(20%): 是否太快/太慢、2. 音調(30%): 太高或太低、3. 言語和聲紋(50%): 能否展現沉穩、熱情、自信、大方、好相處的態度，抑或畏縮、沒自信。
                
                3. 請根據上述分析，請按權重為視覺評價、言語內容、聽覺評價，個別產生各項的總評分(1-100分):
                4. 請按照以下比例計算綜合總評分(1-100分):
                - 視覺評價占總評分比例為40%，
                - 言語內容占總評分比例為30%，
                - 聽覺評分占總評分比例為30%。

                5. 請針對面試者的優勢和劣勢進行SWOT分析:
                    - 優勢: 1. 面試者的優勢是什麼? 2. 面試者的優勢可能如何幫助他們在指定的職位中取得成功?
                    - 劣勢: 1. 面試者的劣勢是什麼? 2. 面試者的劣勢可能如何影響他們的錄取機會、以及在指定職位中的表現?
                    - 機會: 1. 根據面試者的履歷背景，面試者有什麼潛在機會，或獨特的定位?
                    - 威脅: 1. 根據面試者的履歷背景及個人定位，面試者面臨的潛在威脅是什麼?

                6. 提出具體的改進建議及改善方案。
                請以繁體中文回答，並以json格式回傳結果。
            '''


        print(video.filename)
        # Upload the video file
        video_file = gemini_video.upload_video(video.filename)

        # Analyze the video
        result = gemini_video.analyze_video(video_file, prompt)

        # Delete the video file
        gemini_video.delete_video(video_file)

        # Delete the local video file
        import os
        os.remove(video.filename)
        print("Deleted local file")

        # Plot the result
        from graph import plot

        # figs is a dictionary of "auditory", "visual", "verbal" charts
        # They are fig objects from plotly.graph_objects respectively
        figs = plot(result)

        return_dict = {
            "result": result,
            "figs": figs
        }

        print(return_dict)
        
        return return_dict
        # return result

    return {"Status": "Video funcion is available now!"}


@app.route("/interview_question", methods=["GET", "POST"])
def interview_question():
    if request.method == "POST":
        question, user_answer, system_instruction = "", "", ""

        if "system_instruction" in request.form:
            system_instruction = request.form["system_instruction"]
        else:
            system_instruction = """
                Please evaluate the user's response to the question.
                Give analysis / evaluation / suggested_modification each in 50 words.
                Return the result in JSON format.
            """
        if "question" in request.form:
            question = request.form["question"]

        if "user_answer" in request.form:
            user_answer = request.form["user_answer"]
            

        # Request Gemini to evaluate the user's answer
        result = interview_evaluate(system_instruction, question, user_answer)

        return result
    
    return {"Status": "Interview question function is available now!"}

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