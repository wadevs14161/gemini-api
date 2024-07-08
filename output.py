a = {
    '優勢': ['視覺呈現良好，展現出專業形象，例如衣著整潔、眼神專注、臉部表情自然。'],
    '劣勢': ['言語內容不夠清晰，表達邏輯有些混亂，例如部分用語不夠精準、句子結構不夠完整、語句間缺乏邏輯銜接。',
            '聽覺表現較弱，例如語速過快，聲調略顯緊張，語氣不夠自信，給人一種不夠穩重和缺乏經驗的感覺。'],
    '改善方案': ['可以試著將面試內容整理成重點，用條理清晰的邏輯進行闡述，並使用精準的用語。',
              '可以多練習用錄音的方式練習面試，並仔細分析自己的語速、聲調和語氣，找出需要改進的地方。',
              '可以參加一些面試技巧課程，學習如何提升自己的面試表現。'],
    '改進建議': ['建議面試者在面試前做好充分的準備，練習清晰流暢的表達，並注意用詞的準確性。',
              '建議面試者放慢語速，調整聲調，讓語氣更穩定，展現出自信和沉穩的態度。',
              '建議面試者多練習一些面試技巧，例如如何用眼神與面試官交流、如何展現自己的優勢等。'],
    '整體表現': '面試者在視覺呈現上表現良好，但言語內容和聽覺表現則有待加強。',
    '綜合表現評分': 5.5,
    '評分': {'聽覺評價': {
                        '聲調': 5,
                        '言語和聲紋': 4,
                        '語速': 6
                        },
            '視覺評價': 7,
            '言語內容': {
                        '表達邏輯': 5, 
                        '言語用字': 6
                        }}}

import plotly.graph_objects as go

# Extracting data from the dictionary
overall_score = a['綜合表現評分']
visual_score = a['評分']['視覺評價']
verbal_content_score = a['評分']['言語內容']['表達邏輯'] + a['評分']['言語內容']['言語用字']
verbal_delivery_score = (a['評分']['聽覺評價']['聲調'] + a['評分']['聽覺評價']['言語和聲紋'] + a['評分']['聽覺評價']['語速']) / 3

# 1. Gauge Chart for Overall Score
fig_gauge = go.Figure(go.Indicator(
    domain={'x': [0, 1], 'y': [0, 1]},
    value=overall_score,
    mode="gauge+number+delta",
    title={'text': "Overall Performance Score"},
    gauge={
        'shape': "angular",
        'axis': {'range': [0, 10]},
        'steps': [
            {'range': [0, 4], 'color': "red"},
            {'range': [4, 7], 'color': "yellow"},
            {'range': [7, 10], 'color': "green"}
        ]
    }
))
fig_gauge.update_layout(margin=dict(t=50, b=10, l=10, r=10))

# 2. Bar Chart for Visual, Verbal, and Auditory Evaluation
evaluation_categories = ["Visual", "Verbal Content", "Verbal Delivery"]
evaluation_scores = [visual_score, verbal_content_score, verbal_delivery_score]
fig_bar = go.Figure(data=[go.Bar(x=evaluation_categories, y=evaluation_scores)])
fig_bar.update_layout(title="Evaluation Breakdown", xaxis_title="Category", yaxis_title="Score")

# 3. Scatter Plot with Subplots for Detailed Breakdown (assuming more components exist)
sub_categories_visual = ["Eye Contact", "Posture"]  # Replace with actual components
sub_scores_visual = [7, 8]  # Replace with actual scores
sub_categories_verbal_content = ["Clarity", "Accuracy"]  # Replace with actual components
sub_scores_verbal_content = [verbal_content_score - 1, verbal_content_score]  # Adjust based on actual scores
sub_categories_verbal_delivery = ["Speed", "Tone"]  # Replace with actual components
sub_scores_verbal_delivery = [a['評分']['聽覺評價']['語速'], a['評分']['聽覺評價']['聲調']]

fig_scatter = go.Figure()
fig_scatter.add_trace(go.Scatter(x=sub_categories_visual, y=sub_scores_visual, name="Visual"))
fig_scatter.add_trace(go.Scatter(x=sub_categories_verbal_content, y=sub_scores_verbal_content, name="Verbal Content"))
fig_scatter.add_trace(go.Scatter(x=sub_categories_verbal_delivery, y=sub_scores_verbal_delivery, name="Verbal Delivery"))
fig_scatter.update_layout(title="Detailed Evaluation Breakdown", xaxis_title="Component", yaxis_title="Score")

# Combine the graphs into a layout (optional)
# You can use grid subplots or other layout options from Plotly

# Display the graphs
fig_gauge.show()
fig_bar.show()
fig_scatter.show()