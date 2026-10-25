"""
Data Visualization with Matplotlib & Seaborn
============================================
Project 02 | Data Science & AI | InternCircle

Builds a set of clear, honest charts from seaborn's built-in "tips" dataset:
histogram, box plot, bar chart, scatter plot and a correlation heatmap,
plus a 2x2 dashboard image. Every chart answers one written question,
has a finding-style title, labelled axes with units, and a one-line takeaway.

Run:
    python visualize_tips.py
Outputs go to ./charts/ and ./takeaways.md
"""

from pathlib import Path
import textwrap

import matplotlib

matplotlib.use("Agg")  # works without a display (servers, Colab, CI)
import matplotlib.pyplot as plt
import seaborn as sns

# --------------------------------------------------------------------------
# Settings
# --------------------------------------------------------------------------
OUT_DIR = Path(__file__).parent / "charts"
DPI = 150

# Colour-blind-friendly palette (Okabe-Ito subset). No red + green together.
BLUE = "#0072B2"
ORANGE = "#E69F00"
SKY = "#56B4E9"
GREY = "#6B7280"
TIME_PALETTE = {"Lunch": ORANGE, "Dinner": BLUE}  # colour = time of day

sns.set_theme(style="whitegrid", palette=[BLUE, ORANGE, SKY, "#CC79A7"])
plt.rcParams.update({"axes.titleweight": "bold", "axes.titlesize": 11})


# --------------------------------------------------------------------------
# Data + the four questions
# --------------------------------------------------------------------------
DAY_NAMES = {"Thur": "Thursday", "Fri": "Friday", "Sat": "Saturday", "Sun": "Sunday"}

QUESTIONS = {
    "Q1": "How are bills distributed?",
    "Q2": "Do tips differ by day?",
    "Q3": "Does a bigger bill mean a bigger tip?",
    "Q4": "Which numbers move together?",
}


def load_data():
    tips = sns.load_dataset("tips")
    tips["tip_pct"] = tips["tip"] / tips["total_bill"] * 100
    return tips


# --------------------------------------------------------------------------
# Takeaways are computed from the data, so they can never drift from the charts
# --------------------------------------------------------------------------
def compute_takeaways(tips):
    bill = tips["total_bill"]
    share_10_25 = ((bill >= 10) & (bill <= 25)).mean() * 100

    day_mean = tips.groupby("day", observed=True)["tip"].mean()
    top_day, low_day = day_mean.idxmax(), day_mean.idxmin()

    corr = tips[["total_bill", "tip", "size"]].corr()
    r_bill_tip = corr.loc["total_bill", "tip"]
    pairs = {
        ("total bill", "tip"): corr.loc["total_bill", "tip"],
        ("total bill", "party size"): corr.loc["total_bill", "size"],
        ("tip", "party size"): corr.loc["tip", "size"],
    }
    (a, b), r_max = max(pairs.items(), key=lambda kv: kv[1])

    dinner = tips.loc[tips["time"] == "Dinner", "tip"].mean()
    lunch = tips.loc[tips["time"] == "Lunch", "tip"].mean()

    return {
        "hist": (
            f"{share_10_25:.0f}% of bills are between $10 and $25; the median bill is "
            f"${bill.median():.2f} and a few large bills stretch the right tail."
        ),
        "box": (
            f"{DAY_NAMES[top_day]} tips are highest (average ${day_mean[top_day]:.2f}) and "
            f"{DAY_NAMES[low_day]} the lowest (${day_mean[low_day]:.2f}), but the boxes overlap heavily."
        ),
        "scatter": (
            f"Tips rise with the bill (r = {r_bill_tip:.2f}); dinner tips average "
            f"${dinner:.2f} against ${lunch:.2f} at lunch."
        ),
        "heatmap": (
            f"The strongest relationship is {a} and {b} (r = {r_max:.2f}); "
            f"party size is only moderately linked to either."
        ),
        "bar": (
            f"Average tip per meal ranges from ${day_mean.min():.2f} to "
            f"${day_mean.max():.2f} across days, a gap of ${day_mean.max() - day_mean.min():.2f}."
        ),
    }


# --------------------------------------------------------------------------
# Individual chart functions (each draws onto a given axes)
# --------------------------------------------------------------------------
def plot_histogram(tips, ax):
    sns.histplot(tips["total_bill"], bins=20, color=BLUE, edgecolor="white", ax=ax)
    ax.set(
        title="Most bills are under 25 dollars",
        xlabel="Total bill (USD)",
        ylabel="Number of meals",
    )
    return ax


def plot_boxplot(tips, ax):
    sns.boxplot(data=tips, x="day", y="tip", color=SKY, linecolor=GREY, ax=ax)
    ax.set(
        title="Tips are similar across days, highest on Sunday",
        xlabel="Day of week",
        ylabel="Tip (USD)",
    )
    return ax


def plot_scatter(tips, ax):
    sns.scatterplot(
        data=tips,
        x="total_bill",
        y="tip",
        hue="time",
        palette=TIME_PALETTE,
        hue_order=["Lunch", "Dinner"],
        alpha=0.8,
        ax=ax,
    )
    ax.set(
        title="Bigger bills bring bigger tips",
        xlabel="Total bill (USD)",
        ylabel="Tip (USD)",
    )
    ax.legend(title="Time of day", frameon=True)
    return ax


def plot_heatmap(tips, ax):
    corr = tips[["total_bill", "tip", "size"]].corr()
    sns.heatmap(
        corr,
        annot=True,
        fmt=".2f",
        cmap="Blues",
        vmin=0,
        vmax=1,
        linewidths=1,
        cbar_kws={"label": "Correlation (r)"},
        ax=ax,
    )
    ax.set_title("Bill and tip are the strongest pair")
    ax.set_xticklabels(["Total bill", "Tip", "Party size"], rotation=0)
    ax.set_yticklabels(["Total bill", "Tip", "Party size"], rotation=0)
    return ax


def plot_bar(tips, ax):
    sns.barplot(
        data=tips,
        x="day",
        y="tip",
        color=BLUE,
        errorbar=("ci", 95),
        capsize=0.15,
        ax=ax,
    )
    ax.set_ylim(bottom=0)  # honest bar chart: baseline at zero
    ax.set(
        title="Average tip differs by under a dollar across days",
        xlabel="Day of week",
        ylabel="Average tip (USD)",
    )
    return ax


CHARTS = [
    # key, filename, function, question, figure size
    ("hist", "01_bill_distribution.png", plot_histogram, "Q1"),
    ("box", "02_tips_by_day_boxplot.png", plot_boxplot, "Q2"),
    ("scatter", "03_bill_vs_tip_scatter.png", plot_scatter, "Q3"),
    ("heatmap", "04_correlation_heatmap.png", plot_heatmap, "Q4"),
    ("bar", "05_average_tip_by_day_bar.png", plot_bar, "Q2"),
]


def wrap(text, width=62):
    # escape "$" so matplotlib does not treat dollar amounts as math text
    return "\n".join(textwrap.wrap(text, width)).replace("$", r"\$")


def save_individual_charts(tips, takeaways):
    for key, filename, func, _ in CHARTS:
        fig, ax = plt.subplots(figsize=(7.5, 5.6))
        func(tips, ax)
        fig.text(0.5, 0.01, wrap(takeaways[key], 78), ha="center", va="bottom",
                 fontsize=9, color=GREY, style="italic")
        fig.tight_layout(rect=(0, 0.09, 1, 1))
        fig.savefig(OUT_DIR / filename, dpi=DPI)
        plt.close(fig)
        print(f"saved {OUT_DIR.name}/{filename}")


def save_dashboard(tips, takeaways):
    """2 x 2 dashboard: histogram, box plot, scatter plot, heatmap."""
    fig, axes = plt.subplots(2, 2, figsize=(13, 10))
    plot_histogram(tips, axes[0, 0])
    plot_boxplot(tips, axes[0, 1])
    plot_scatter(tips, axes[1, 0])
    plot_heatmap(tips, axes[1, 1])

    for ax, key in zip(axes.flat, ["hist", "box", "scatter", "heatmap"]):
        ax.text(0.5, -0.24, wrap(takeaways[key], 58), transform=ax.transAxes,
                ha="center", va="top", fontsize=9, color=GREY, style="italic")

    fig.suptitle("Restaurant tipping at a glance (244 meals, tips dataset)",
                 fontsize=15, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.97), h_pad=4.5, w_pad=3)
    fig.savefig(OUT_DIR / "tips_overview.png", dpi=DPI)
    plt.close(fig)
    print(f"saved {OUT_DIR.name}/tips_overview.png")


def write_takeaways(takeaways):
    lines = ["# Written takeaways", ""]
    items = [
        ("Q1", "hist", "01_bill_distribution.png", "Histogram"),
        ("Q2", "box", "02_tips_by_day_boxplot.png", "Box plot"),
        ("Q2", "bar", "05_average_tip_by_day_bar.png", "Bar chart"),
        ("Q3", "scatter", "03_bill_vs_tip_scatter.png", "Scatter plot"),
        ("Q4", "heatmap", "04_correlation_heatmap.png", "Correlation heatmap"),
    ]
    for q, key, fname, kind in items:
        lines += [
            f"## {kind}: {QUESTIONS[q]}",
            "",
            f"![{kind}](charts/{fname})",
            "",
            f"**Takeaway:** {takeaways[key]}",
            "",
        ]
    (Path(__file__).parent / "takeaways.md").write_text("\n".join(lines), encoding="utf-8")
    print("saved takeaways.md")


def main():
    OUT_DIR.mkdir(exist_ok=True)
    tips = load_data()
    takeaways = compute_takeaways(tips)
    save_individual_charts(tips, takeaways)
    save_dashboard(tips, takeaways)
    write_takeaways(takeaways)


if __name__ == "__main__":
    main()
