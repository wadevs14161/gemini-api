def interview_evaluate(instruction, question, user_answer):
    import google.generativeai as genai

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash-latest",
        generation_config={
            "temperature": 0.6,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
        },
        system_instruction=instruction)
    

    user_input = f"Question: {question}\nUser's response: {user_answer}"

    response = model.generate_content(user_input)

    import json
    result_json = json.loads(response.text[7:-4])

    return result_json




if __name__ == "__main__":
    system_instruction = """
                Please evaluate the user's response to the question.
                Give analysis / evaluation / suggested_modification each in 50 words.
                Return the result in JSON format.
            """
    question = "Tell us about a situation in which you had to adjust to changes over which you had no control. How did you handle it?"
    user_answer = "During a busy summer at my restaurant job, our kitchen manager unexpectedly quit. With a large staff and upcoming reservations, the pressure was on.  I volunteered to help coordinate the team and menu prep. While unfamiliar with the manager role, I focused on clear communication and collaboration with the chefs. We adjusted schedules, delegated tasks, and streamlined processes.  Though challenging, we kept the kitchen running smoothly. This experience showed me the value of adaptability and teamwork in unexpected situations."

    result = interview_evaluate(system_instruction, question, user_answer)
    from pprint import pprint
    pprint(result)
    print('-'*50)
    print(type(result))

