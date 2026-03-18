import streamlit as st
from collections import Counter
from chat_history import get_today_moods, load_history

def show_mood_pie(pet_name):
    moods = get_today_moods(pet_name)
    if not moods:
        st.info("Aaj ki koi conversation nahi hai abhi tak!")
        return
    counts = Counter(moods)
    labels = list(counts.keys())
    values = list(counts.values())
    import plotly.graph_objects as go
    fig = go.Figure(data=[go.Pie(
        labels=labels, values=values, hole=0.4,
        marker_colors=["#2e7d32","#c62828","#e65100","#1565c0","#7b1fa2","#555"]
    )])
    fig.update_layout(
        title_text=f"{pet_name} ka aaj ka mood",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        margin=dict(t=40, b=0, l=0, r=0),
        height=300
    )
    st.plotly_chart(fig, use_container_width=True)

def show_mood_bar_chart(pet_name):
    history = load_history(pet_name)
    if not history:
        st.info("Koi history nahi mili!")
        return
    from datetime import datetime, timedelta
    import plotly.graph_objects as go
    last7 = [(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(6, -1, -1)]
    mood_counts = {date: Counter() for date in last7}
    for msg in history:
        d = msg.get("date")
        m = msg.get("mood")
        if d in mood_counts and m:
            mood_counts[d][m] += 1
    all_moods = ["Happy", "Hungry", "Angry", "Playful", "Annoyed", "Sad"]
    colors    = ["#2e7d32","#e65100","#c62828","#1565c0","#f9a825","#7b1fa2"]
    fig = go.Figure()
    for mood, color in zip(all_moods, colors):
        fig.add_trace(go.Bar(
            name=mood,
            x=last7,
            y=[mood_counts[d].get(mood, 0) for d in last7],
            marker_color=color
        ))
    fig.update_layout(
        barmode="stack",
        title_text=f"{pet_name} — Last 7 days mood",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        xaxis=dict(gridcolor="#333"),
        yaxis=dict(gridcolor="#333"),
        legend=dict(orientation="h", y=-0.2),
        margin=dict(t=40, b=60, l=0, r=0),
        height=320
    )
    st.plotly_chart(fig, use_container_width=True)
