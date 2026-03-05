import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import os

os.makedirs('images', exist_ok=True)
np.random.seed(42)

print("=" * 60)
print("🏥 CLINICAL TRIAL DASHBOARD — Building Project")
print("=" * 60)

# ══════════════ GENERATE DATA ══════════════
n = 500
arms = np.random.choice(['Treatment', 'Placebo'], n)
age = np.random.normal(55, 12, n).astype(int)
gender = np.random.choice(['Male', 'Female'], n)

survival_time = np.where(
    arms == 'Treatment',
    np.random.exponential(24, n) + 6,
    np.random.exponential(18, n) + 3
)
survival_time = np.clip(survival_time, 1, 60).round(1)

event = np.where(
    arms == 'Treatment',
    np.random.binomial(1, 0.35, n),
    np.random.binomial(1, 0.50, n)
)

response = np.where(
    arms == 'Treatment',
    np.random.binomial(1, 0.65, n),
    np.random.binomial(1, 0.40, n)
)

subgroup = np.random.choice(
    ['Age<55', 'Age>=55', 'Male', 'Female', 'Stage I-II', 'Stage III-IV'], n
)

df = pd.DataFrame({
    'Patient_ID': range(1, n + 1),
    'Arm': arms, 'Age': age, 'Gender': gender,
    'Survival_Months': survival_time, 'Event': event,
    'Response': response, 'Subgroup': subgroup
})
df.to_csv('trial_data.csv', index=False)
print(f"✅ Data: {len(df)} patients generated")

# ══════════════ KAPLAN-MEIER FUNCTION ══════════════
def kaplan_meier(times, events):
    order = np.argsort(times)
    times = times[order]
    events = events[order]
    unique_times = np.unique(times[events == 1])
    
    n_at_risk = len(times)
    prob = 1.0
    km_t = [0]
    km_s = [1.0]
    
    for t in unique_times:
        mask_t = times == t
        d = np.sum(mask_t & (events == 1))
        c = np.sum(mask_t & (events == 0))
        if n_at_risk > 0:
            prob *= (1 - d / n_at_risk)
        n_at_risk -= (d + c)
        km_t.append(t)
        km_s.append(prob)
        if n_at_risk <= 0:
            break
    return km_t, km_s

# ══════════════ FIGURE 1: SURVIVAL CURVE ══════════════
fig, ax = plt.subplots(figsize=(10, 6))

for arm, color, ls in [('Treatment', '#2B7A78', '-'), ('Placebo', '#E74C3C', '--')]:
    arm_data = df[df['Arm'] == arm]
    t, s = kaplan_meier(arm_data['Survival_Months'].values, arm_data['Event'].values)
    ax.step(t, s, where='post', color=color, linewidth=2.5, linestyle=ls, label=arm)

ax.set_xlabel('Time (Months)', fontsize=13)
ax.set_ylabel('Survival Probability', fontsize=13)
ax.set_title('Kaplan–Meier Survival Curves by Treatment Arm', fontsize=15, fontweight='bold')
ax.legend(fontsize=12, loc='lower left')
ax.set_ylim(0, 1.05)
ax.set_xlim(0, 60)
ax.grid(alpha=0.3)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Add median survival lines
for arm, color in [('Treatment', '#2B7A78'), ('Placebo', '#E74C3C')]:
    arm_data = df[df['Arm'] == arm]
    t, s = kaplan_meier(arm_data['Survival_Months'].values, arm_data['Event'].values)
    for i in range(len(s)):
        if s[i] <= 0.5:
            ax.axhline(y=0.5, color='gray', linestyle=':', alpha=0.5)
            ax.axvline(x=t[i], color=color, linestyle=':', alpha=0.5)
            ax.annotate(f'Median: {t[i]:.1f}m', xy=(t[i], 0.5),
                       fontsize=9, color=color,
                       xytext=(t[i] + 2, 0.55))
            break

plt.tight_layout()
plt.savefig('images/survival_curve.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ Image: images/survival_curve.png")

# ══════════════ FIGURE 2: FOREST PLOT ══════════════
subgroups = ['Overall', 'Age < 55', 'Age ≥ 55', 'Male', 'Female', 'Stage I–II', 'Stage III–IV']
hr =    [0.72, 0.65, 0.80, 0.70, 0.75, 0.60, 0.85]
lower = [0.55, 0.45, 0.60, 0.50, 0.55, 0.40, 0.65]
upper = [0.95, 0.90, 1.05, 0.95, 1.00, 0.85, 1.10]

fig, ax = plt.subplots(figsize=(10, 7))

for i, sg in enumerate(subgroups):
    color = '#2B7A78' if upper[i] < 1.0 else '#E74C3C'
    # CI line
    ax.plot([lower[i], upper[i]], [i, i], color=color, linewidth=2, solid_capstyle='round')
    # Point estimate
    ax.plot(hr[i], i, 'D', color=color, markersize=10, zorder=5)
    # Text
    ax.text(1.25, i, f'{hr[i]:.2f} ({lower[i]:.2f}–{upper[i]:.2f})',
            va='center', fontsize=10, fontfamily='monospace')

ax.axvline(x=1.0, color='black', linestyle='--', linewidth=1, alpha=0.7)
ax.set_yticks(range(len(subgroups)))
ax.set_yticklabels(subgroups, fontsize=11)
ax.set_xlabel('Hazard Ratio (95% CI)', fontsize=13)
ax.set_title('Forest Plot — Treatment Effect by Subgroup', fontsize=15, fontweight='bold')
ax.set_xlim(0.2, 1.5)
ax.invert_yaxis()
ax.grid(axis='x', alpha=0.3)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Favours labels
ax.text(0.6, len(subgroups) + 0.3, '← Favours Treatment', fontsize=9, color='#2B7A78')
ax.text(1.05, len(subgroups) + 0.3, 'Favours Placebo →', fontsize=9, color='#E74C3C')

plt.tight_layout()
plt.savefig('images/forest_plot.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ Image: images/forest_plot.png")

# ══════════════ FIGURE 3: RESPONSE RATES ══════════════
fig, ax = plt.subplots(figsize=(8, 6))

arms_list = ['Treatment', 'Placebo']
rates = [df[df['Arm'] == a]['Response'].mean() * 100 for a in arms_list]
colors = ['#2B7A78', '#E74C3C']

bars = ax.bar(arms_list, rates, color=colors, width=0.5, edgecolor='white', linewidth=2)

for bar, rate in zip(bars, rates):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1.5,
            f'{rate:.1f}%', ha='center', va='bottom', fontsize=16, fontweight='bold')

ax.set_ylabel('Response Rate (%)', fontsize=13)
ax.set_title('Overall Response Rate by Arm', fontsize=15, fontweight='bold')
ax.set_ylim(0, 85)
ax.grid(axis='y', alpha=0.3)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('images/response_rate.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ Image: images/response_rate.png")

# ══════════════ FIGURE 4: SUBGROUP RESPONSE ══════════════
fig, ax = plt.subplots(figsize=(12, 6))

subgroups_data = df.groupby(['Subgroup', 'Arm'])['Response'].mean().unstack() * 100
subgroups_data.plot(kind='bar', ax=ax, color=['#E74C3C', '#2B7A78'], width=0.7)

ax.set_ylabel('Response Rate (%)', fontsize=12)
ax.set_title('Response Rate by Subgroup and Treatment Arm', fontsize=14, fontweight='bold')
ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha='right')
ax.legend(title='Arm', fontsize=10)
ax.grid(axis='y', alpha=0.3)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('images/subgroup_response.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ Image: images/subgroup_response.png")


