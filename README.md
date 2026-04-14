# L&D Programme Evaluation Tool

A Python-based evaluation tool for Learning and Development practitioners who want to move beyond Excel for post-workshop analysis. Handles real **Microsoft Forms** survey exports with mixed scale types, applies the **Kirkpatrick Level 1 and 2 framework**, categorises improvement themes from open-text responses, and produces a clean set of charts and a one-page KPI dashboard.

Built from practice designing and delivering training programmes at Temasek Polytechnic and for industry professionals in a corporate setting.

---

## What it does

**Level 1 (Reaction):** Analyses participant feedback across multiple question types — satisfaction scales, agreement scales, effectiveness scales, Yes/No, and 1-10 numeric ratings. Normalises all responses to a common 0-10 scale for consistent comparison.

**Improvement analysis:** Extracts and categorises open-text suggestions into actionable improvement themes, annotated with example quotes. Displays all raw suggestions in a formatted panel so nothing gets lost.

**Reporting:** Produces 7 charts and a CSV export covering instructor behaviour, satisfaction, effectiveness, numeric distributions, improvement themes, raw suggestions, and a one-page KPI summary dashboard.

---

## Charts produced

| Chart | Description |
|---|---|
| `01_instructor_scores.png` | Mean scores per instructor behaviour dimension |
| `02_rating_distributions.png` | Distribution of 1-10 ratings for overall performance and likelihood to recommend |
| `03_satisfaction_effectiveness.png` | Satisfaction and effectiveness scores across all dimensions |
| `04_feedback_themes.png` | What went well — key themes from open-text responses |
| `05_improvement_themes.png` | Areas for improvement — categorised and annotated with example quotes |
| `06_raw_suggestions.png` | All raw improvement suggestions displayed verbatim |
| `07_summary_dashboard.png` | One-page KPI summary (8 key metrics) |

---

## Real data results

The tool was applied to a real 16-respondent post-workshop survey following a professional development session delivered to field service engineers in a corporate setting. Selected outputs:

| Metric | Result |
|---|---|
| Respondents | 16 |
| Achieved learning outcome | 100% Yes |
| Knowledge satisfaction | 8.9 / 10 |
| Instructor overall rating | 9.8 / 10 |
| Likelihood to recommend | 9.1 / 10 |
| Overall positive rate | 100% |

Top improvement themes identified: role play and script quality (3 mentions), more time requested (2 mentions), deeper engagement in scenario activities (2 mentions).

---

## Handling mixed scale types

Microsoft Forms surveys often combine multiple question formats. This tool maps all of them to a normalised 0-10 scale:

| Response type | Example | Mapped to |
|---|---|---|
| Satisfaction text | "Very satisfied" | 10 |
| Agreement text | "Somewhat agree" | 7.5 |
| Effectiveness text | "Somewhat effective" | 6 |
| Yes / No / Maybe | "Yes" | 10 / 5 / 0 |
| Numeric 1-10 | 9 | 9 (direct) |

Mapping tables are defined at the top of the script and easy to adjust for different scales.

---

## Using your own Microsoft Forms data

**Step 1:** Export your survey from Microsoft Forms as Excel (.xlsx) via Responses > Open in Excel.

**Step 2:** Update the configuration block at the top of the script:

```python
FILE_PATH      = "your_survey_export.xlsx"
PROGRAMME_NAME = "Your Workshop Name"
FACILITATOR    = "Your Name"
DELIVERY_DATE  = "Month Year"
AUDIENCE       = "Your Audience"
ORGANISATION   = "Your Organisation"
```

**Step 3:** Map your column names to the script variables. Each question from your form becomes a column in the exported Excel file. Update the column references in the MAP COLUMNS section to match your form's exact question text.

**Step 4:** Adjust the improvement theme keywords to match the kinds of suggestions your participants typically give:

```python
improvement_themes = {
    "More time needed":          ["more time", "time"],
    "Role play / scripts":       ["role play", "script"],
    "Logistics / venue":         ["room", "cold", "chair"],
    # Add your own themes here
}
```

---

## Requirements

```
pandas
numpy
matplotlib
seaborn
openpyxl
```

Install with:
```bash
pip install pandas numpy matplotlib seaborn openpyxl
```

---

## Run

```bash
python ld_evaluation_philips.py
```

Output saved to `output_ld_philips/`

---

## Theoretical grounding

This tool applies the **Kirkpatrick Four-Level Model** (Kirkpatrick and Kirkpatrick, 2006):

| Level | What it measures | Status |
|---|---|---|
| 1 — Reaction | Did participants find the training valuable? | Implemented |
| 2 — Learning | Did knowledge or skills improve? | Implemented (if pre/post scores available) |
| 3 — Behaviour | Did behaviour change on the job? | Requires follow-up survey |
| 4 — Results | Did it affect organisational outcomes? | Requires business data |

Levels 3 and 4 require post-training follow-up data beyond a single feedback survey. This tool handles Levels 1 and 2 in a single automated report.

---

## Background

Built by **Nasrum Bin Seron**, Lecturer in Biomedical Engineering at Temasek Polytechnic and holder of the Certificate in Teaching and Learning for Polytechnic Educators (CTLPE). Developed to demonstrate that L&D evaluation can be data-driven, automated, and educator-led — without needing a dedicated analytics team.

---

## Licence

MIT — free to use and adapt with attribution.
