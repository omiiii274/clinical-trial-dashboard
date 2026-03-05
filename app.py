import numpy as np
import pandas as pd
from flask import Flask, render_template_string
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json
import os

app = Flask(__name__)

# ── Generate Simulated Clinical Trial Data ──
np.random.seed(42)

def generate_trial_data(n=500):
    arms = np.random.choice(['Treatment', 'Placebo'], n)
    age = np.random.normal(55, 12, n).astype(int)
    gender = np.random.choice(['Male', 'Female'], n)
    
    # Survival time (treatment arm has better survival)
    survival_time = np.where(
        arms == 'Treatment',
        np.random.exponential(24, n) + 6,
        np.random.exponential(18, n) + 3
    )
    survival_time = np.clip(survival_time, 1, 60)
    
    # Event occurred
    event = np.where(
        arms == 'Treatment',
        np.random.binomial(1, 0.35, n),
        np.random.binomial(1, 0.50, n)
    )
    
    # Response rate
    response = np.where(
        arms == 'Treatment',
        np.random.binomial(1, 0.65, n),
        np.random.binomial(1, 0.40, n)
    )
    
    # Subgroups
    subgroup = np.random.choice(['Age<55', 'Age>=55', 'Male', 'Female', 'Stage I-II', 'Stage III-IV'], n)
    
    return pd.DataFrame({
        'Patient_ID': range(1, n+1),
        'Arm': arms,
        'Age': age,
        'Gender': gender,
        'Survival_Months': np.round(survival_time, 1),
        'Event': event,
        'Response': response,
        'Subgroup': subgroup
    })

df = generate_trial_data(500)
df.to_csv('trial_data.csv', index=False)

# ── Kaplan-Meier Survival Curve ──
def kaplan_meier(times, events):
    unique_times = np.sort(np.unique(times[events == 1]))
    survival_prob = []
    n_at_risk = len(times)
    prob = 1.0
    km_times = [0]
    km_survival = [1.0]
    
    for t in unique_times:
        n_events = np.sum((times == t) & (events == 1))
        n_censored = np.sum((times == t) & (events == 0))
        prob *= (1 - n_events / n_at_risk)
        n_at_risk -= (n_events + n_censored)
        km_times.append(t)
        km_survival.append(prob)
        if n_at_risk <= 0:
            break
    
    return km_times, km_survival

# ── Create Figures ──
def create_survival_plot():
    fig = go.Figure()
    
    for arm, color in [('Treatment', '#2B7A78'), ('Placebo', '#E74C3C')]:
        arm_data = df[df['Arm'] == arm]
        times, survival = kaplan_meier(
            arm_data['Survival_Months'].values,
            arm_data['Event'].values
        )
        fig.add_trace(go.Scatter(
            x=times, y=survival,
            mode='lines', name=arm,
            line=dict(color=color, width=2, shape='hv')
        ))
    
    fig.update_layout(
        title='Kaplan-Meier Survival Curve',
        xaxis_title='Time (Months)',
        yaxis_title='Survival Probability',
        template='plotly_white',
        height=450, width=800
    )
    return fig

def create_forest_plot():
    subgroups = ['Overall', 'Age<55', 'Age>=55', 'Male', 'Female', 'Stage I-II', 'Stage III-IV']
    hr = [0.72, 0.65, 0.80, 0.70, 0.75, 0.60, 0.85]
    lower = [0.55, 0.45, 0.60, 0.50, 0.55, 0.40, 0.65]
    upper = [0.95, 0.90, 1.05, 0.95, 1.00, 0.85, 1.10]
    
    fig = go.Figure()
    
    for i, sg in enumerate(subgroups):
        color = '#2B7A78' if upper[i] < 1.0 else '#E74C3C'
        fig.add_trace(go.Scatter(
            x=[lower[i], upper[i]], y=[sg, sg],
            mode='lines', line=dict(color=color, width=2),
            showlegend=False
        ))
        fig.add_trace(go.Scatter(
            x=[hr[i]], y=[sg],
            mode='markers', marker=dict(size=10, color=color, symbol='diamond'),
            showlegend=False,
            text=f'HR={hr[i]:.2f} ({lower[i]:.2f}-{upper[i]:.2f})',
            hoverinfo='text'
        ))
    
    fig.add_vline(x=1.0, line_dash="dash", line_color="gray")
    fig.update_layout(
        title='Forest Plot — Hazard Ratios by Subgroup',
        xaxis_title='Hazard Ratio (95% CI)',
        template='plotly_white',
        height=400, width=800
    )
    return fig

def create_response_plot():
    response_data = df.groupby('Arm')['Response'].mean().reset_index()
    response_data['Response'] = response_data['Response'] * 100
    
    fig = px.bar(
        response_data, x='Arm', y='Response',
        color='Arm', color_discrete_map={'Treatment': '#2B7A78', 'Placebo': '#E74C3C'},
        title='Overall Response Rate (%)',
        labels={'Response': 'Response Rate (%)'}
    )
    fig.update_layout(template='plotly_white', height=400, width=600, showlegend=False)
    return fig

# ── Save plots as images ──
os.makedirs('images', exist_ok=True)
create_survival_plot().write_image('images/survival_curve.png')
create_forest_plot().write_image('images/forest_plot.png')
create_response_plot().write_image('images/response_rate.png')
print("✅ Static images saved to /images/")

# ── Flask Dashboard ──
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Clinical Trial Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body { font-family: 'Segoe UI', sans-serif; margin: 0; background: #f5f7fa; }
        .header { background: #1B3A4B; color: white; padding: 20px 40px; }
        .header h1 { margin: 0; font-size: 24px; }
        .header p { margin: 5px 0 0; opacity: 0.8; font-size: 14px; }
        .container { max-width: 1200px; margin: 20px auto; padding: 0 20px; }
        .card { background: white; border-radius: 8px; padding: 20px; margin-bottom: 20px; 
                box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .stats-row { display: flex; gap: 20px; margin-bottom: 20px; }
        .stat-card { flex: 1; background: white; border-radius: 8px; padding: 20px; 
                     text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .stat-value { font-size: 36px; font-weight: bold; color: #1B3A4B; }
        .stat-label { font-size: 14px; color: #666; margin-top: 5px; }
        .charts-row { display: flex; gap: 20px; }
        .chart-half { flex: 1; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🏥 Clinical Trial Results Dashboard</h1>
        <p>Randomised Controlled Trial — Treatment vs Placebo | N={{ n_patients }}</p>
    </div>
    <div class="container">
        <div class="stats-row">
            <div class="stat-card">
                <div class="stat-value">{{ n_patients }}</div>
                <div class="stat-label">Total Patients</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{{ treatment_n }}</div>
                <div class="stat-label">Treatment Arm</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{{ placebo_n }}</div>
                <div class="stat-label">Placebo Arm</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{{ response_rate }}%</div>
                <div class="stat-label">Treatment Response Rate</div>
            </div>
        </div>
        <div class="card">
            <div id="survival"></div>
        </div>
        <div class="charts-row">
            <div class="card chart-half">
                <div id="forest"></div>
            </div>
            <div class="card chart-half">
                <div id="response"></div>
            </div>
        </div>
    </div>
    <script>
        Plotly.newPlot('survival', {{ survival_json | safe }});
        Plotly.newPlot('forest', {{ forest_json | safe }});
        Plotly.newPlot('response', {{ response_json | safe }});
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    treatment_data = df[df['Arm'] == 'Treatment']
    return render_template_string(
        HTML_TEMPLATE,
        n_patients=len(df),
        treatment_n=len(df[df['Arm'] == 'Treatment']),
        placebo_n=len(df[df['Arm'] == 'Placebo']),
        response_rate=round(treatment_data['Response'].mean() * 100, 1),
        survival_json=create_survival_plot().to_json(),
        forest_json=create_forest_plot().to_json(),
        response_json=create_response_plot().to_json()
    )

if __name__ == '__main__':
    print("\n🚀 Dashboard running at http://127.0.0.1:5000")
    app.run(debug=True)
