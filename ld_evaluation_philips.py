"""
=============================================================
L&D Programme Evaluation Tool — Microsoft Forms Edition
=============================================================
Author:  Nasrum Bin Seron
Purpose: Analyses real participant feedback from a Microsoft
         Forms survey exported as CSV or XLSX. Handles mixed
         scale types (text ratings, 1-10 numeric, Yes/No)
         and produces a clean evaluation report.

         Built from the Effective Communication Mastery workshop
         delivered to Client Field Service Engineers,
         7 April 2026.

         Based on Kirkpatrick Level 1 (Reaction) evaluation.

Libraries: pandas, matplotlib, seaborn, numpy
Usage:     python ld_evaluation_Client.py
           Update FILE_PATH to point to your survey export.
=============================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import os
import textwrap

# ─────────────────────────────────────────────────────────
# CONFIGURATION — update these for a different workshop
# ─────────────────────────────────────────────────────────

FILE_PATH      = "Post-Workshop_Survey__Effective_Communication_Mastery_for_Client_-_7_Apr_2026_1-16_.xlsx"
PROGRAMME_NAME = "Effective Communication Mastery"
FACILITATOR    = "Nasrum Bin Seron"
DELIVERY_DATE  = "7 April 2026"
AUDIENCE       = "Field Service Engineers"
ORGANISATION   = "Client"
OUTPUT_DIR     = "output_ld_Client"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─────────────────────────────────────────────────────────
# SCALE MAPPINGS
# Convert text responses to numeric scores (all normalised
# to a 0-10 scale for consistent comparison)
# ─────────────────────────────────────────────────────────

SATISFACTION_MAP = {
    "Very satisfied":    10,
    "Satisfied":          7.5,
    "Neutral":            5,
    "Dissatisfied":       2.5,
    "Very dissatisfied":  0,
}

AGREEMENT_MAP = {
    "Extremely agree":   10,
    "Somewhat agree":     7.5,
    "Neutral":            5,
    "Somewhat disagree":  2.5,
    "Extremely disagree": 0,
}

EFFECTIVENESS_MAP = {
    "Extremely effective": 10,
    "Very effective":       8,
    "Somewhat effective":   6,
    "Neutral":              5,
    "Not effective":        2,
}

YESNO_MAP = {
    "Yes":   10,
    "Maybe":  5,
    "No":     0,
}

# ─────────────────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────────────────

print("=" * 60)
print(f"L&D EVALUATION REPORT")
print(f"Programme:  {PROGRAMME_NAME}")
print(f"Audience:   {AUDIENCE} | {ORGANISATION}")
print(f"Date:       {DELIVERY_DATE}")
print(f"Facilitator:{FACILITATOR}")
print("=" * 60)

df_raw = pd.read_excel(FILE_PATH)
df_raw.columns = df_raw.columns.str.strip()
n = len(df_raw)
print(f"\nLoaded {n} responses from survey file.")

# ─────────────────────────────────────────────────────────
# MAP COLUMNS TO NUMERIC SCORES
# ─────────────────────────────────────────────────────────

def map_col(series, mapping):
    return series.map(mapping).astype(float)

df = pd.DataFrame()
df["participant_id"] = [f"P{str(i).zfill(2)}" for i in range(1, n + 1)]

# Section 1: Overall satisfaction and outcomes
df["satisfaction_knowledge"] = map_col(
    df_raw["How satisfied are you with the knowledge you gained from the workshop?"],
    SATISFACTION_MAP)

df["achieved_outcome"] = map_col(
    df_raw["Do you feel you achieved your desired learning outcome?"],
    YESNO_MAP)

df["instructor_overall"] = pd.to_numeric(
    df_raw["How would you rate the instructor's overall teaching performance?"],
    errors="coerce")

df["recommend"] = pd.to_numeric(
    df_raw["How likely are you to recommend this course to a colleague?"],
    errors="coerce")

# Section 2: Instructor behaviour (agreement scale)
instructor_cols = {
    "Prepared well":              "The instructor prepared well at the start of each class",
    "Clear expectations":         "The instructor communicated clearly on course expectations",
    "Clear delivery":             "The instructor delivered course in a clear and easy-to-understand approach",
    "Encouraged participation":   "The instructor encouraged students in-class participation",
    "Maintained interest":        "The instructor maintained my interest throughout the whole course",
    "Answered questions":         "The instructor thoroughly answered questions from students",
    "Time management":            "The instructor had good time management during class",
    "Clear on assignments":       "The instructor communicated clearly on course assignments",
}

for short_name, col_name in instructor_cols.items():
    df[f"inst_{short_name}"] = map_col(df_raw[col_name], AGREEMENT_MAP)

# Section 3: Materials and activities
df["materials_rating"]    = map_col(df_raw["Instructional materials used in this course"], EFFECTIVENESS_MAP)
df["activities_rating"]   = map_col(df_raw["Learning activities used in this course"], EFFECTIVENESS_MAP)
df["tech_rating"]         = map_col(df_raw["Use of technologies in the class"], EFFECTIVENESS_MAP)
df["group_rating"]        = map_col(df_raw["Group activities organized after the class"], EFFECTIVENESS_MAP)
df["materials_effective"] = map_col(df_raw["How effective were the instructional materials used in this course?"], EFFECTIVENESS_MAP)
df["activities_effective"]= map_col(df_raw["How effective were the learning activities used in this course?"], EFFECTIVENESS_MAP)

# Open text
df["went_well"]    = df_raw["What went well?"].fillna("").str.strip()
df["improvements"] = df_raw["What can be improved or any suggestions?"].fillna("").str.strip()

# ─────────────────────────────────────────────────────────
# COMPUTE SUMMARY METRICS
# ─────────────────────────────────────────────────────────

inst_cols  = [c for c in df.columns if c.startswith("inst_")]
mat_cols   = ["materials_rating", "activities_rating", "tech_rating",
              "group_rating", "materials_effective", "activities_effective"]

df["instructor_mean"] = df[inst_cols].mean(axis=1)
df["materials_mean"]  = df[mat_cols].mean(axis=1)
df["overall_score"]   = df[["satisfaction_knowledge", "achieved_outcome",
                              "instructor_overall", "instructor_mean",
                              "materials_mean", "recommend"]].mean(axis=1)

positive_pct      = (df["overall_score"] >= 7.5).mean() * 100
recommend_mean    = df["recommend"].mean()
instructor_mean   = df["instructor_overall"].mean()
satisfaction_mean = df["satisfaction_knowledge"].mean()
achieved_pct      = (df["achieved_outcome"] == 10).mean() * 100
materials_mean    = df["materials_mean"].mean()

print(f"\n── Overall Metrics (all scores out of 10) ──────────")
print(f"  Respondents:                   {n}")
print(f"  Overall positive rate (>=7.5): {positive_pct:.1f}%")
print(f"  Achieved learning outcome:     {achieved_pct:.1f}%  (Yes responses)")
print(f"  Mean satisfaction (knowledge): {satisfaction_mean:.1f} / 10")
print(f"  Mean instructor rating:        {instructor_mean:.1f} / 10")
print(f"  Mean materials effectiveness:  {materials_mean:.1f} / 10")
print(f"  Likelihood to recommend:       {recommend_mean:.1f} / 10")

print(f"\n── Instructor Behaviour Scores ─────────────────────")
for col in inst_cols:
    label = col.replace("inst_", "")
    mean  = df[col].mean()
    bar   = "#" * int(mean * 2)
    print(f"  {label:<28} {mean:.1f}/10  {bar}")

print(f"\n── Open Feedback: What Went Well ───────────────────")
went_well_responses = [r for r in df["went_well"] if r and r not in ["-", "Yes", "yes", ""]]
for r in went_well_responses:
    print(f"  - {r[:100]}")

print(f"\n── Open Feedback: Suggestions ──────────────────────")
suggestions = [r for r in df["improvements"]
               if r and r.lower() not in ["nil", "-", "none", "none so far. thank you!", ""]]
for r in suggestions:
    print(f"  - {r[:100]}")

# ─────────────────────────────────────────────────────────
# VISUALISATIONS
# ─────────────────────────────────────────────────────────

sns.set_theme(style="whitegrid", font_scale=1.0)
BLUE  = "#2166ac"
GREEN = "#1a9641"
AMBER = "#f4a582"
RED   = "#d73027"
NAVY  = "#1f3a5c"

# ── Chart 1: Instructor behaviour scores ─────────────────
inst_labels = [c.replace("inst_", "") for c in inst_cols]
inst_means  = [df[c].mean() for c in inst_cols]

fig, ax = plt.subplots(figsize=(10, 5))
colors  = [GREEN if s >= 8.0 else BLUE if s >= 6.0 else AMBER for s in inst_means]
bars    = ax.barh(inst_labels, inst_means, color=colors)
ax.axvline(8.0, color=RED, linestyle="--", linewidth=1.2, label="Target (8.0 / 10)")
ax.set_xlim(0, 11)
ax.set_xlabel("Mean Score (out of 10)")
ax.set_title(f"Instructor Behaviour Scores\n{PROGRAMME_NAME} | {DELIVERY_DATE}",
             fontsize=13, fontweight="bold")
for bar, val in zip(bars, inst_means):
    ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height() / 2,
            f"{val:.1f}", va="center", fontsize=10)
ax.legend()
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/01_instructor_scores.png", dpi=150)
plt.close()
print("\nSaved: 01_instructor_scores.png")

# ── Chart 2: Overall rating distribution (1-10) ──────────
fig, axes = plt.subplots(1, 2, figsize=(11, 4))
for ax, col, title in zip(
    axes,
    ["instructor_overall", "recommend"],
    ["Instructor Overall Rating", "Likelihood to Recommend"]
):
    counts = df[col].value_counts().sort_index()
    ax.bar(counts.index.astype(int), counts.values, color=BLUE, edgecolor="white")
    ax.set_xlabel("Score (out of 10)")
    ax.set_ylabel("Number of Responses")
    ax.set_title(title, fontsize=12, fontweight="bold")
    ax.set_xticks(range(1, 11))
    mean_val = df[col].mean()
    ax.axvline(mean_val, color=RED, linestyle="--", linewidth=1.5,
               label=f"Mean: {mean_val:.1f}")
    ax.legend(fontsize=9)
fig.suptitle(f"Numeric Rating Distributions | {ORGANISATION}", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/02_rating_distributions.png", dpi=150)
plt.close()
print("Saved: 02_rating_distributions.png")

# ── Chart 3: Satisfaction and effectiveness breakdown ─────
categories = ["Knowledge\nSatisfaction", "Achieved\nOutcome",
              "Materials\nEffectiveness", "Activities\nEffectiveness",
              "Tech\nEffectiveness", "Group\nActivities"]
values     = [
    df["satisfaction_knowledge"].mean(),
    df["achieved_outcome"].mean(),
    df["materials_effective"].mean(),
    df["activities_effective"].mean(),
    df["tech_rating"].mean(),
    df["group_rating"].mean(),
]

fig, ax = plt.subplots(figsize=(10, 5))
colors  = [GREEN if v >= 8 else BLUE if v >= 6 else AMBER for v in values]
bars    = ax.bar(categories, values, color=colors, edgecolor="white", linewidth=1.2)
ax.axhline(8.0, color=RED, linestyle="--", linewidth=1.2, label="Target (8.0 / 10)")
ax.set_ylim(0, 11)
ax.set_ylabel("Mean Score (out of 10)")
ax.set_title(f"Satisfaction and Effectiveness Ratings\n{PROGRAMME_NAME}",
             fontsize=13, fontweight="bold")
for bar, val in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.2,
            f"{val:.1f}", ha="center", fontsize=10, fontweight="bold")
ax.legend()
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/03_satisfaction_effectiveness.png", dpi=150)
plt.close()
print("Saved: 03_satisfaction_effectiveness.png")

# ── Chart 4: Open feedback word themes ───────────────────
all_responses = went_well_responses
theme_keywords = {
    "Engaging":      ["engag", "interactive", "interest"],
    "Role play":     ["role play", "role-play", "roleplay", "scenario", "acting"],
    "Frameworks":    ["framework", "model", "heard", "3 step", "tool"],
    "Real examples": ["real", "example", "situation", "practical"],
    "Facilitator":   ["facilitator", "instructor", "articulate", "explain"],
}

theme_counts = {}
for theme, keywords in theme_keywords.items():
    count = sum(
        any(kw in r.lower() for kw in keywords)
        for r in all_responses
    )
    theme_counts[theme] = count

fig, ax = plt.subplots(figsize=(8, 4))
ax.barh(list(theme_counts.keys()), list(theme_counts.values()),
        color=BLUE, edgecolor="white")
ax.set_xlabel("Number of Responses Mentioning Theme")
ax.set_title("What Went Well — Key Themes\n(from open-text responses)",
             fontsize=13, fontweight="bold")
ax.set_xlim(0, max(theme_counts.values()) + 2)
for i, (theme, val) in enumerate(theme_counts.items()):
    ax.text(val + 0.1, i, str(val), va="center", fontsize=10)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/04_feedback_themes.png", dpi=150)
plt.close()
print("Saved: 04_feedback_themes.png")

# ── Chart 5: Improvement suggestions analysis ─────────────
# Filter out non-responses
NOISE = {"nil", "none", "none so far. thank you!", "-", "", "n/a", "na"}
suggestions_clean = [
    r for r in df["improvements"]
    if r and r.lower().strip() not in NOISE
]

# Categorise each suggestion into improvement themes
improvement_themes = {
    "More time needed":          ["more time", "time"],
    "Role play / scripts":       ["role play", "role-play", "script", "acting"],
    "Logistics / venue":         ["room", "cold", "chair", "venue", "comfort"],
    "Slide / content prep":      ["slide", "prepare", "ahead", "content"],
    "Engagement / participation":["engage", "confident", "scenario"],
}

improve_counts = {}
theme_examples = {}

for theme, keywords in improvement_themes.items():
    matched = [
        r for r in suggestions_clean
        if any(kw in r.lower() for kw in keywords)
    ]
    improve_counts[theme] = len(matched)
    theme_examples[theme] = matched  # keep for annotation

# Chart: horizontal bar of improvement themes
fig, ax = plt.subplots(figsize=(10, 5))
themes  = list(improve_counts.keys())
counts  = list(improve_counts.values())
colors  = [AMBER if c >= 2 else BLUE for c in counts]

bars = ax.barh(themes, counts, color=colors, edgecolor="white", linewidth=1.2)
ax.set_xlabel("Number of Responses Mentioning Theme")
ax.set_title(
    f"Areas for Improvement — Suggested by Participants\n{PROGRAMME_NAME} | {DELIVERY_DATE}",
    fontsize=13, fontweight="bold"
)
ax.set_xlim(0, max(counts) + 3 if max(counts) > 0 else 5)

for bar, val, theme in zip(bars, counts, themes):
    ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height() / 2,
            str(val), va="center", fontsize=10)
    # Annotate with one example quote if available
    if theme_examples[theme]:
        example = theme_examples[theme][0][:55] + "..." if len(theme_examples[theme][0]) > 55 else theme_examples[theme][0]
        ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2 - 0.22,
                f'e.g. "{example}"', va="center", fontsize=7.5,
                color="#666666", style="italic")

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/05_improvement_themes.png", dpi=150)
plt.close()
print("Saved: 05_improvement_themes.png")

# ── Chart 6: All raw suggestions displayed as a text panel ─
fig, ax = plt.subplots(figsize=(11, max(4, len(suggestions_clean) * 0.8 + 1.5)))
ax.axis("off")

title_text = f"Raw Improvement Suggestions — {n} respondents, {len(suggestions_clean)} provided feedback"
ax.text(0.0, 1.0, title_text, transform=ax.transAxes,
        fontsize=11, fontweight="bold", color=NAVY, va="top")

y_pos = 0.92
for i, suggestion in enumerate(suggestions_clean, 1):
    # Wrap long suggestions
    wrapped = textwrap.fill(suggestion, width=95)
    lines   = wrapped.split("\n")
    ax.text(0.0, y_pos, f"{i}.", transform=ax.transAxes,
            fontsize=10, fontweight="bold", color=AMBER, va="top")
    for j, line in enumerate(lines):
        ax.text(0.04, y_pos - j * 0.055, line, transform=ax.transAxes,
                fontsize=10, color="#1c1c1c", va="top")
    y_pos -= len(lines) * 0.055 + 0.04

    # Divider line
    ax.axhline(y_pos + 0.01, color="#dddddd", linewidth=0.7)

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/06_raw_suggestions.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved: 06_raw_suggestions.png")

# Print structured improvement analysis to console
print(f"\n── Improvement Suggestions Analysis ────────────────")
print(f"  {len(suggestions_clean)} of {n} participants provided actionable suggestions.\n")
for theme, examples in theme_examples.items():
    if examples:
        print(f"  [{improve_counts[theme]} mention(s)] {theme}")
        for ex in examples:
            print(f"      > {ex[:100]}")
        print()

uncategorised = [
    r for r in suggestions_clean
    if not any(
        any(kw in r.lower() for kw in keywords)
        for keywords in improvement_themes.values()
    )
]
if uncategorised:
    print(f"  [Other / uncategorised]")
    for r in uncategorised:
        print(f"      > {r[:100]}")

# ── Chart 7: One-page KPI summary dashboard ──────────────
fig = plt.figure(figsize=(12, 6))
fig.suptitle(
    f"Workshop Evaluation Summary  |  {PROGRAMME_NAME}\n"
    f"{DELIVERY_DATE}  |  {ORGANISATION}  |  Facilitator: {FACILITATOR}",
    fontsize=13, fontweight="bold", y=0.99
)

gs   = gridspec.GridSpec(2, 4, figure=fig, hspace=0.5, wspace=0.4)
kpis = [
    ("Respondents",          str(n),                      BLUE),
    ("Achieved Outcome",     f"{achieved_pct:.0f}% Yes",  GREEN if achieved_pct == 100 else BLUE),
    ("Knowledge Satisfaction",f"{satisfaction_mean:.1f}/10", GREEN if satisfaction_mean >= 8 else BLUE),
    ("Instructor Rating",    f"{instructor_mean:.1f}/10", GREEN if instructor_mean >= 8 else BLUE),
    ("Materials",            f"{materials_mean:.1f}/10",  GREEN if materials_mean >= 8 else BLUE),
    ("Recommend",            f"{recommend_mean:.1f}/10",  GREEN if recommend_mean >= 8 else BLUE),
    ("Positive Rate",        f"{positive_pct:.0f}%",      GREEN if positive_pct >= 80 else AMBER),
    ("Net Promoter Score",   f"{recommend_mean:.1f}/10",  GREEN if recommend_mean >= 9 else BLUE),
]

for idx, (label, value, color) in enumerate(kpis):
    row, col = divmod(idx, 4)
    ax_kpi = fig.add_subplot(gs[row, col])
    ax_kpi.set_facecolor(color + "22")
    ax_kpi.text(0.5, 0.62, value, ha="center", va="center",
                fontsize=20, fontweight="bold", color=color,
                transform=ax_kpi.transAxes)
    ax_kpi.text(0.5, 0.22, label, ha="center", va="center",
                fontsize=9, color="#444444",
                transform=ax_kpi.transAxes)
    ax_kpi.set_xticks([])
    ax_kpi.set_yticks([])
    for spine in ax_kpi.spines.values():
        spine.set_edgecolor(color)
        spine.set_linewidth(1.5)

plt.savefig(f"{OUTPUT_DIR}/07_summary_dashboard.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved: 07_summary_dashboard.png")

# ─────────────────────────────────────────────────────────
# EXPORT
# ─────────────────────────────────────────────────────────

export_cols = ["participant_id", "satisfaction_knowledge", "achieved_outcome",
               "instructor_overall", "instructor_mean",
               "materials_mean", "recommend", "overall_score",
               "went_well", "improvements"]
df[export_cols].to_csv(f"{OUTPUT_DIR}/full_participant_data.csv", index=False)
print(f"Saved: full_participant_data.csv")

print(f"\n── All outputs saved to: {OUTPUT_DIR}")
print("=" * 60)
print("Evaluation complete.")
