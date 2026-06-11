"""Chart skill demand from the collected counts.

Reads data/skill_demand.csv, computes each term's share of all Tashkent
vacancies, and draws a sorted horizontal bar chart to output/.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd

TOOLS = {"1C", "Excel", "SQL", "Python", "Power BI", "Tableau",
         "machine learning"}  # everything else is a role keyword


def main() -> None:
    df = pd.read_csv("data/skill_demand.csv")
    total = int(df.loc[df.label == "all vacancies", "vacancies"].iloc[0])
    d = df[df.label != "all vacancies"].sort_values("vacancies")

    fig, ax = plt.subplots(figsize=(8, 5.5), dpi=150)
    colors = ["#1a6fb5" if l in TOOLS else "#c98a2b" for l in d.label]
    ax.barh(d.label, d.vacancies, color=colors)

    # Annotate each bar with the raw count and its share of all postings.
    for i, v in enumerate(d.vacancies):
        ax.text(v + 30, i, f"{v}  ({100 * v / total:.1f}%)",
                va="center", fontsize=8)

    ax.set_xlim(0, d.vacancies.max() * 1.22)
    ax.set_title(f"Mentions in Tashkent vacancies on hh.uz "
                 f"(n = {total:,} postings)", fontsize=11, loc="left")
    ax.set_xlabel("vacancies matching search term")
    ax.legend(handles=[mpatches.Patch(color="#1a6fb5", label="tool / skill"),
                       mpatches.Patch(color="#c98a2b", label="role keyword")],
              frameon=False, fontsize=8, loc="lower right")
    ax.spines[["top", "right"]].set_visible(False)
    fig.text(0.01, 0.01, "Source: tashkent.hh.uz public search counts",
             fontsize=7, color="#666666")
    fig.tight_layout(rect=[0, 0.03, 1, 1])
    fig.savefig("output/fig1_skill_demand.png")


if __name__ == "__main__":
    main()
