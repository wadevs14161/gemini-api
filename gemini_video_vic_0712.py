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


    def analyze_video(self, video_file):
        # Create the prompt.
        prompt = '''
            1. 請總結並評價面試者的整體表現。

            2. 請針對面試者下列的表現做出評分(1-100分):
               - 視覺評價: 1. 臉部情緒特徵(30%): 是否友善、正向、自信? 或是木訥、膽怯、害羞。 2. 肢體動作(20%): 是否沉穩、自信、大方； 3. eye contact (15%)、4. 微笑是否自然 (15%)、5. 衣著整潔(20%)。
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
            請以繁體中文及json格式呈現回答。
            '''
        # prompt = '''  1st Version:
        #     1. 請總結並評價面試者的整體表現。
        #     2. 請針對面試者下列的表現做出評分(1-10分):
        #        - 視覺評價: 臉部情緒特徵、肢體動作、eye contact、微笑是否自然、衣著整潔等。
        #        - 言語內容: 1. 言語用字: 是否得體、2. 表達邏輯: 是否清晰、通順，抑或前後矛盾。
        #        - 聽覺評價: 1.語速: 是否太快/太慢、2. 聲調: 是否沉穩/太高/太低、3. 言語和聲紋: 能否展現自信、大方、好相處的態度，抑或畏縮、沒自信。
               
        #     3. 請根據上述分析，產生綜合表現評分(1-10分):
        #        - 視覺評價占總評分比例為40%，
        #        - 言語內容占總評分比例為30%，
        #        - 聽覺評分占總評分比例為30%。
        #     4. 請針對面試者的優勢和劣勢進行分析，並提出具體的改進建議及改善方案。
        #     請以繁體中文及json格式呈現回答。
        #     '''
        
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
    file_path = "static/videos/example-1.mp4"
    video_file = v.upload_video(file_path)
    from pprint import pprint
    pprint(v.analyze_video(video_file))
    v.delete_video(video_file)
