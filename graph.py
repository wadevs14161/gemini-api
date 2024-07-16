import plotly.graph_objects as go
import plotly.express as px

def plot(result_json):
    # Assuming result_json is the JSON output from the analysis
    # result_json = {
    #     "改進建議": [
    #         "建議面試者在準備面試時，多練習口語表達，提高語言表達的邏輯性。",
    #         "建議面試者在面試中提供更多具體的例子和數據佐證，以證明自己的工作經驗和能力。",
    #         "建議面試者在面試前做好功課，深入了解公司文化、業務和發展方向，以及招聘職位的具體需求。",
    #         "建議面試者積極參加招聘相關的講座和研討會，學習和提升招聘策略的知識和技能。"
    #     ],
    #     "整體表現": "面試者在視覺和聽覺上表現出積極且自信的態度，但語言內容的邏輯性略顯不足，需要加強。",
    #     "綜合總評分": 81,
    #     "聽覺評價": {
    #         "總評分": 85,
    #         "言語和聲紋": 90,
    #         "語速": 80,
    #         "音調": 85
    #     },
    #     "視覺評價": {
    #         "眼神交流": 85,
    #         "微笑是否自然": 90,
    #         "總評分": 85,
    #         "肢體動作": 75,
    #         "臉部情緒特徵": 80,
    #         "衣著整潔": 95
    #     },
    #     "言語內容": {
    #         "總評分": 70,
    #         "表達邏輯": 65,
    #         "言語用字": 90
    #     }
    # }

    # Data for radar charts
    auditory_categories = ["言語和聲紋", "語速", "音調"]
    auditory_values = [result_json["聽覺評價"]["言語和聲紋"], result_json["聽覺評價"]["語速"], result_json["聽覺評價"]["音調"]]

    visual_categories = ["眼神交流", "微笑是否自然", "肢體動作", "臉部情緒特徵", "衣著整潔"]
    visual_values = [result_json["視覺評價"]["眼神交流"], result_json["視覺評價"]["微笑是否自然"], result_json["視覺評價"]["肢體動作"], result_json["視覺評價"]["臉部情緒特徵"], result_json["視覺評價"]["衣著整潔"]]

    verbal_categories = ["表達邏輯", "言語用字"]
    verbal_values = [result_json["言語內容"]["表達邏輯"], result_json["言語內容"]["言語用字"]]

    # Create radar chart for auditory evaluation
    fig_auditory = go.Figure()

    fig_auditory.add_trace(go.Scatterpolar(
        r=auditory_values,
        theta=auditory_categories,
        fill='toself',
        name='聽覺評價'
    ))

    fig_auditory.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title="聽覺評價雷達圖"
    )

    # Create radar chart for visual evaluation
    fig_visual = go.Figure()

    fig_visual.add_trace(go.Scatterpolar(
        r=visual_values,
        theta=visual_categories,
        fill='toself',
        name='視覺評價'
    ))

    fig_visual.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title="視覺評價雷達圖"
    )

    # Create bar chart for verbal evaluation
    fig_verbal = px.bar(
        x=verbal_categories,
        y=verbal_values,
        labels={'x': '言語內容', 'y': '分數'},
        title="言語內容評分",
        range_y=[0, 100]
    )

    figs = dict()
    figs["auditory"] = fig_auditory
    figs["visual"] = fig_visual
    figs["verbal"] = fig_verbal

    fig_visual.show()
    fig_auditory.show()
    fig_verbal.show()

    return figs

