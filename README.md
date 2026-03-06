# 🏥 Clinical Trial Results Dashboard

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square)
![Flask](https://img.shields.io/badge/Flask-3.0-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen?style=flat-square)

Interactive web dashboard for visualising randomised controlled trial (RCT) results built with Flask and Plotly.

---

## 📊 Results

### Kaplan–Meier Survival Curves
Shows treatment arm has significantly better survival compared to placebo.

![Survival Curve](images/survival_curve.png)

---

### Forest Plot — Hazard Ratios by Subgroup
Treatment benefit observed across most subgroups except Stage III-IV.

![Forest Plot](images/forest_plot.png)

---

### Overall Response Rate
Treatment arm achieved 65% response rate vs 40% for placebo.

![Response Rate](images/response_rate.png)

---

### Subgroup Response Analysis
Response rates broken down by patient subgroup and treatment arm.

![Subgroup Response](images/subgroup_response.png)

---

## 🛠️ Tech Stack

| Category | Tools |
|----------|-------|
| Backend | Python, Flask |
| Visualisation | Plotly Dash, Matplotlib |
| Database | PostgreSQL |
| Deployment | AWS EC2, Docker |
| Data | Pandas, NumPy |

## 🚀 How to Run

```bash
git clone https://github.com/omiiii274/clinical-trial-dashboard.git
cd clinical-trial-dashboard
pip install -r requirements.txt
python build.py
