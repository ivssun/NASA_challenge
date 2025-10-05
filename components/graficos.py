import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from config.settings import COLORS

def render_probability_chart(data):
    df = pd.DataFrame({
        'Condición': list(data.keys()),
        'Probabilidad': [v * 100 for v in data.values()]
    })
    
    fig = go.Figure(data=[
        go.Bar(
            x=df['Condición'],
            y=df['Probabilidad'],
            marker=dict(
                color=df['Probabilidad'],
                colorscale=[[0, COLORS['success']], 
                           [0.5, COLORS['warning']], 
                           [1, COLORS['danger']]],
                showscale=True
            ),
            text=df['Probabilidad'].round(1),
            texttemplate='%{text}%',
            textposition='outside'
        )
    ])
    
    fig.update_layout(
        title="Probabilidades de Condiciones Extremas",
        xaxis_title="Condición Climática",
        yaxis_title="Probabilidad (%)",
        yaxis_range=[0, 100],
        template="plotly_white",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_time_series(dates, values, variable_name):
    df = pd.DataFrame({
        'Fecha': dates,
        'Valor': values
    })
    
    fig = px.line(
        df,
        x='Fecha',
        y='Valor',
        title=f"Serie Temporal: {variable_name}",
        markers=True
    )
    
    fig.update_traces(
        line_color=COLORS['primary'],
        line_width=3
    )
    
    fig.update_layout(
        template="plotly_white",
        height=350
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_distribution_chart(values, variable_name, threshold):
    fig = go.Figure()
    
    fig.add_trace(go.Histogram(
        x=values,
        name='Distribución',
        marker_color=COLORS['primary'],
        opacity=0.7
    ))
    
    fig.add_vline(
        x=threshold,
        line_dash="dash",
        line_color=COLORS['danger'],
        annotation_text=f"Umbral: {threshold}",
        annotation_position="top"
    )
    
    fig.update_layout(
        title=f"Distribución Histórica: {variable_name}",
        xaxis_title=variable_name,
        yaxis_title="Frecuencia",
        template="plotly_white",
        height=350
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_gauge_chart(value, max_value, title):
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        title={'text': title},
        delta={'reference': max_value * 0.5},
        gauge={
            'axis': {'range': [None, max_value]},
            'bar': {'color': COLORS['primary']},
            'steps': [
                {'range': [0, max_value * 0.33], 'color': COLORS['success']},
                {'range': [max_value * 0.33, max_value * 0.66], 'color': COLORS['warning']},
                {'range': [max_value * 0.66, max_value], 'color': COLORS['danger']}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': max_value * 0.8
            }
        }
    ))
    
    fig.update_layout(height=300)