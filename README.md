# Data Visualization with Matplotlib & Seaborn


A set of clear, honest charts built from seaborn's built-in **tips** dataset (244 restaurant meals), covering a histogram, box plot, bar chart, scatter plot and an annotated correlation heatmap, combined into a 2 x 2 dashboard image.

![Dashboard](charts/tips_overview.png)

## The four questions

| # | Question | Chart | Finding |
|---|----------|-------|---------|
| 1 | How are bills distributed? | Histogram | 70% of bills are between $10 and $25; median is $17.80 |
| 2 | Do tips differ by day? | Box plot + bar chart | Sunday highest ($3.26), Friday lowest ($2.73), but distributions overlap heavily |
| 3 | Does a bigger bill mean a bigger tip? | Scatter plot (colour = time of day) | Yes, r = 0.68 |
| 4 | Which numbers move together? | Correlation heatmap | Total bill and tip are the strongest pair (r = 0.68) |

Full written takeaways with each chart: [takeaways.md](takeaways.md)

## Project structure

```
.
├── visualize_tips.py          # all chart code; run to regenerate everything
├── tips_visualization.ipynb   # step-by-step notebook (outputs included)
├── takeaways.md               # one-sentence takeaway per chart
├── requirements.txt
└── charts/
    ├── tips_overview.png              # 2 x 2 dashboard, 150 dpi
    ├── 01_bill_distribution.png
    ├── 02_tips_by_day_boxplot.png
    ├── 03_bill_vs_tip_scatter.png
    ├── 04_correlation_heatmap.png
    └── 05_average_tip_by_day_bar.png
```

## How to run

```bash
pip install -r requirements.txt
python visualize_tips.py          # regenerates charts/ and takeaways.md
jupyter notebook tips_visualization.ipynb
```

Google Colab also works: upload the files, run `!pip install seaborn`, then open the notebook.

## Design choices

- **Right chart for the question**: histogram for one number, box/bar for groups, scatter for two numbers, heatmap for correlations.
- **Titles state the finding**, not just the variables; every axis has a label and units (USD).
- **Colour-blind-friendly palette** (blue / orange / sky blue). No red and green together. Colour is only used to mean something (time of day).
- **Honest axes**: the bar chart starts at zero, and error bars show the 95% confidence interval.
- **Takeaways are computed from the data**, so the text under each chart always matches the numbers.
- `tight_layout()` is used so no labels are cut off.

## Limitations

- Correlation is not causation: larger parties spend more, which partly drives bigger tips.
- Friday has only 19 meals, so its average is less reliable than Saturday's (87 meals).
