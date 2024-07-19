class GeminiVideo:
    import google.generativeai as genai
    from google.generativeai.types import HarmCategory, HarmBlockThreshold
    import time

    # Set up the model
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash-latest",
        safety_settings={
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        },
        generation_config={
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
        },
        system_instruction="你是一位專業的人士招聘獵頭顧問，正在為一家公司尋找合適的新員工。你將根據影片中人物的面試表現，對面試表現給予專業的分析與評價。"
        )



    def upload_video(self, video_file_name):
        # Upload the video file
        print(f"Uploading file...")
        video_file = __class__.genai.upload_file(path=video_file_name)
        print(f"Completed upload: {video_file.uri}")

        # Wait for the video to be processed
        while video_file.state.name == "PROCESSING":
            print("Waiting for video to be processed.")
            __class__.time.sleep(3)
            video_file = __class__.genai.get_file(video_file.name)

        if video_file.state.name == "FAILED":
            raise ValueError(video_file.state.name)
        print(f"Video processing complete: " + video_file.uri)

        return video_file


    def analyze_video(self, video_file, prompt):
        # Create the prompt.
        prompt = prompt
        
        # Make the LLM request.
        print("Gemini思考中...")
        response = __class__.model.generate_content(
            [prompt, video_file], request_options={"timeout": 600}
        )

        # print(response.text)
        # print(type(response.text))
        import json
        result_json = json.loads(response.text[7:-4])

        return result_json
        

    def delete_video(self, video_file):
        # Delete the cloud video file
        __class__.genai.delete_file(video_file.name)
        print(f"Deleted file {video_file.uri}")

    



if __name__ == "__main__":
    v = GeminiVideo()
    file_path = "static/videos/intro-49.mov"
    video_file = v.upload_video(file_path)

    prompt = '''
    1. 請針對面試者下列的表現做出評分(1-100分):
    - 視覺評價: 1. 臉部情緒特徵(30%): 是否友善、正向、自信? 或是木訥、膽怯、害羞。 2. 肢體動作(20%): 是否沉穩、自信、大方； 3. 眼神交流 (15%)、4. 微笑是否自然 (15%)、5. 衣著整潔(20%)。
    - 聽覺評價: 1. 語速(20%): 是否太快/太慢、2. 音調(30%): 太高或太低、3. 言語和聲紋(50%): 能否展現沉穩、熱情、自信、大方、好相處的態度，抑或畏縮、沒自信。
    - 言語內容: 1. 言語用字(30%): 是否得體、2. 表達邏輯 (70%): 是否清晰、通順，抑或前後矛盾。
    
    請根據上述分析，請按權重為視覺評價、聽覺評價、言語內容，分別產生各項的總評分(1-100分):
    
    2. 請分析面試者的
    - 整體表現
    - 改進建議。
    請以繁體中文回答。
    以json格式回傳結果，格式如下:
    response = {
        "整體表現": "",
        "改進建議": "",
        "聽覺評價": {"總評分": , "言語和聲紋": , "語速": , "音調": },
        "視覺評價": {
                "微笑是否自然": ,
                "眼神交流": ,
                "總評分": ,
                "肢體動作": ,
                "臉部情緒特徵": ,
                "衣著整潔": },
        "言語內容": {
                "總評分": , 
                "表達邏輯": , 
                "言語用字": },
    }

    '''

    from pprint import pprint
    pprint(v.analyze_video(video_file, prompt))
    v.delete_video(video_file)
