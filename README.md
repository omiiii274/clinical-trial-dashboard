# 🏥 Clinical Trial Results Dashboard

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square)
![Flask](https://img.shields.io/badge/Flask-3.0-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen?style=flat-square)

## 📋 About This Project

This is an interactive web dashboard that displays results from a simulated clinical trial (Randomised Controlled Trial) comparing a new treatment against placebo in 500 patients. Healthcare professionals, medical writers, and health economists can use this type of tool to explore trial outcomes without generating static PDF reports manually.

In the pharmaceutical industry, tools like this support Health Technology Assessment (HTA) submissions to bodies like NICE (UK) and EMA (Europe), medical affairs presentations, and evidence communication to payers, regulators, and clinicians.

## ❓ Problem This Solves

Clinical trial teams typically share results through static PowerPoint slides and PDF documents. When a stakeholder wants to see results for a different patient subgroup or compare specific endpoints, someone must manually create new charts. This wastes hours of analyst time every week.

A dynamic dashboard lets anyone explore the data instantly — filter by treatment arm, select a subgroup, compare endpoints — all without waiting for a new report.

## 🔬 What The Dashboard Shows

**1. Kaplan–Meier Survival Curves**
- Compares how long patients survive in the Treatment group vs Placebo group
- Treatment patients survived significantly longer (median 28.3 months vs 19.7 months for placebo)
- The two curves separate clearly from month 6, showing the treatment starts working early

**2. Forest Plot — Hazard Ratios by Subgroup**
- Shows whether the treatment works better or worse in different patient groups (age, gender, disease stage)
- Each diamond represents the treatment effect (Hazard Ratio) with a confidence interval
- If the diamond is to the LEFT of the dotted line (HR < 1.0), the treatment is better than placebo
- Treatment benefit was found in 5 out of 7 subgroups
- Stage III-IV patients showed weaker benefit (HR crosses 1.0), meaning the treatment may not work as well for advanced disease

**3. Overall Response Rate**
- Simple bar chart comparing how many patients responded to treatment vs placebo
- Treatment: 65.2% responded
- Placebo: 40.1% responded
- This 25 percentage point difference is clinically meaningful

**4. Subgroup Response Analysis**
- Breaks down response rates by patient subgroup AND treatment arm
- Helps identify which patient groups benefit most from treatment
- Largest treatment advantage seen in patients aged under 55

## 📊 Key Numbers

| What | Treatment | Placebo |
|------|-----------|---------|
| Number of patients | 250 | 250 |
| Median survival | 28.3 months | 19.7 months |
| Response rate | 65.2% | 40.1% |
| Hazard Ratio (overall) | 0.72 | — |
| 95% Confidence Interval | 0.55 – 0.95 | — |

A Hazard Ratio of 0.72 means treatment patients had a 28% lower risk of death compared to placebo patients.

## 🛠️ Tools Used

| What | Tool |
|------|------|
| Programming language | Python 3.9 |
| Web framework | Flask 3.0 |
| Charts and plots | Matplotlib, Plotly Dash |
| Web page design | HTML5, CSS3 |
| Database (designed) | PostgreSQL |
| Cloud hosting (designed) | AWS EC2, Docker |
| Data handling | Pandas, NumPy |

## 📁 Files In This Project
