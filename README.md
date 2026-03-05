# ══════════════ WRITE README.md ══════════════
readme = """# 🏥 Clinical Trial Results Dashboard

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square)
![Flask](https://img.shields.io/badge/Flask-3.0-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen?style=flat-square)

> Interactive web dashboard for visualising randomised controlled trial (RCT) results — built with Flask and Plotly.

---

## 📊 Results

### Kaplan–Meier Survival Curves
![Survival Curve](images/survival_curve.png)

### Forest Plot — Hazard Ratios by Subgroup  
![Forest Plot](images/forest_plot.png)

### Overall Response Rate
![Response Rate](images/response_rate.png)

### Subgroup Response Analysis
![Subgroup Response](images/subgroup_response.png)

---

## 🛠️ Tech Stack

| Category | Tools |
|----------|-------|
| Backend | Python, Flask |
| Visualisation | Plotly Dash, Matplotlib |
| Database | PostgreSQL |
| Deployment | AWS EC2, Docker |

## 🚀 How to Run

```bash
git clone https://github.com/omiiii274/clinical-trial-dashboard.git
cd clinical-trial-dashboard
pip install -r requirements.txt
python build.py
