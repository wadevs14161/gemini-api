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
        },)


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
            請評價影片中人物的台風、聲調、表情、動作、言語、情緒等特徵，並給出評分。
            對於整體表現給出總結的建議。
            請以繁體中文及json格式呈現回答。
            '''
        
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
    v.analyze_video(video_file)
    v.delete_video(video_file)
