def interview_evaluate(question, user_answer):
    import google.generativeai as genai

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash-latest",
        generation_config={
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
        },
        system_instruction="""
            請根據問題和回答，對面試表現給予專業的，
            1. 分析
            2. 評價
            3. 建議修改的回答
            ，回傳的格式為json。
        """)
    

    user_input = f"問題: {question}\n回答: {user_answer}"

    response = model.generate_content(user_input)

    import json
    result_json = json.loads(response.text[7:-4])

    return result_json




if __name__ == "__main__":
    question = "Tell us about a situation in which you had to adjust to changes over which you had no control. How did you handle it?"
    user_answer = "During a busy summer at my restaurant job, our kitchen manager unexpectedly quit. With a large staff and upcoming reservations, the pressure was on.  I volunteered to help coordinate the team and menu prep. While unfamiliar with the manager role, I focused on clear communication and collaboration with the chefs. We adjusted schedules, delegated tasks, and streamlined processes.  Though challenging, we kept the kitchen running smoothly. This experience showed me the value of adaptability and teamwork in unexpected situations."

    result = interview_evaluate(question, user_answer)
    from pprint import pprint
    pprint(result)

