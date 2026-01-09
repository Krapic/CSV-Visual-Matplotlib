"""Generiranje grafova s podrškom za teme."""

from enum import Enum
from typing import Callable
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import pandas as pd

from ..config import ThemeManager, Theme
from ..data import ExamData


class GraphType(Enum):
    """Tipovi dostupnih grafova."""
    STUDENTS_BY_GRADE = "Broj studenata po ocjeni"
    GRADE_SHARE = "Udio ocjena"
    SCORE_HISTOGRAM = "Histogram bodova"
    AVG_SCORE_BY_TERM = "Prosjek bodova po terminu"
    PASS_RATE_BY_TERM = "Prolaznost po terminu"
    BOX_PLOT_BY_TERM = "Box plot bodova po terminu"


class GraphManager:
    """Upravlja generiranjem grafova s podrškom za teme."""

    def __init__(self):
        self._graph_functions: dict[GraphType, Callable] = {
            GraphType.STUDENTS_BY_GRADE: self._fig_students_by_grade,
            GraphType.GRADE_SHARE: self._fig_grade_share,
            GraphType.SCORE_HISTOGRAM: self._fig_score_histogram,
            GraphType.AVG_SCORE_BY_TERM: self._fig_avg_score_by_term,
            GraphType.PASS_RATE_BY_TERM: self._fig_pass_rate_by_term,
            GraphType.BOX_PLOT_BY_TERM: self._fig_boxplot_by_term,
        }

    @property
    def theme(self) -> Theme:
        """Trenutna tema."""
        return ThemeManager.get_current()

    def _create_figure(
        self,
        figsize: tuple[int, int] = (8, 5),
        set_ax_bg: bool = True
    ) -> tuple[Figure, plt.Axes]:
        """Kreira figuru s temom."""
        fig, ax = plt.subplots(figsize=figsize)

        theme = self.theme
        fig.patch.set_facecolor(theme.graph_bg)

        if set_ax_bg:
            ax.set_facecolor(theme.graph_bg)

        # Stiliziranje osi
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color(theme.graph_grid)
        ax.spines["bottom"].set_color(theme.graph_grid)

        ax.tick_params(colors=theme.graph_fg, labelcolor=theme.graph_fg)
        ax.xaxis.label.set_color(theme.graph_fg)
        ax.yaxis.label.set_color(theme.graph_fg)

        return fig, ax

    def get_graph(self, graph_type: GraphType, data: ExamData) -> Figure:
        """
        Generira graf.

        Args:
            graph_type: Tip grafa
            data: Podaci za vizualizaciju

        Returns:
            Matplotlib Figure objekt
        """
        if graph_type not in self._graph_functions:
            raise ValueError(f"Nepoznat tip grafa: {graph_type}")

        return self._graph_functions[graph_type](data.dataframe)

    def get_graph_by_name(self, name: str, data: ExamData) -> Figure:
        """Generira graf po nazivu."""
        for graph_type in GraphType:
            if graph_type.value == name:
                return self.get_graph(graph_type, data)
        raise ValueError(f"Nepoznat naziv grafa: {name}")

    @classmethod
    def get_available_graphs(cls) -> list[str]:
        """Vraća listu dostupnih grafova."""
        return [gt.value for gt in GraphType]

    def _fig_students_by_grade(self, df: pd.DataFrame) -> Figure:
        """Stupčasti graf broja studenata po ocjeni."""
        theme = self.theme
        fig, ax = self._create_figure()

        grade_counts = df["ocjena"].value_counts().sort_index()
        all_grades = [1, 2, 3, 4, 5]
        values = [grade_counts.get(g, 0) for g in all_grades]

        colors = list(theme.graph_colors[:5])
        bars = ax.bar(
            [str(g) for g in all_grades],
            values,
            color=colors,
            edgecolor=theme.graph_bg,
            linewidth=2
        )

        ax.set_title(
            "Broj studenata po ocjeni",
            fontsize=14,
            fontweight="bold",
            pad=15,
            color=theme.graph_fg
        )
        ax.set_xlabel("Ocjena", fontsize=11)
        ax.set_ylabel("Broj studenata", fontsize=11)
        ax.set_ylim(bottom=0)

        for bar, v in zip(bars, values):
            if v > 0:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    v + 0.3,
                    str(v),
                    ha="center",
                    va="bottom",
                    fontsize=10,
                    fontweight="bold",
                    color=theme.graph_fg
                )

        fig.tight_layout()
        return fig

    def _fig_grade_share(self, df: pd.DataFrame) -> Figure:
        """Pie chart udjela ocjena."""
        theme = self.theme
        fig, ax = self._create_figure(set_ax_bg=False)

        grade_counts = df["ocjena"].value_counts().sort_index()
        labels = [f"Ocjena {int(g)}" for g in grade_counts.index]

        colors = list(theme.graph_colors[:len(labels)])
        wedges, texts, autotexts = ax.pie(
            grade_counts.values,
            labels=labels,
            autopct="%.1f%%",
            startangle=90,
            colors=colors,
            explode=[0.02] * len(labels),
            shadow=False,
            textprops={"color": theme.graph_fg}
        )

        for autotext in autotexts:
            autotext.set_fontsize(10)
            autotext.set_fontweight("bold")
            autotext.set_color(theme.graph_bg)

        ax.set_title(
            "Udio ocjena",
            fontsize=14,
            fontweight="bold",
            pad=15,
            color=theme.graph_fg
        )

        fig.tight_layout()
        return fig

    def _fig_score_histogram(self, df: pd.DataFrame) -> Figure:
        """Histogram raspodjele bodova."""
        theme = self.theme
        fig, ax = self._create_figure()

        n, bins, patches = ax.hist(
            df["bodovi"],
            bins=10,
            range=(0, 100),
            edgecolor=theme.graph_bg,
            linewidth=1.5
        )

        # Boje prema ocjenama
        grade_colors = {
            "fail": theme.error,
            "pass": theme.warning,
            "good": theme.graph_colors[0],
            "very_good": theme.success,
            "excellent": theme.graph_colors[4] if len(theme.graph_colors) > 4 else theme.info,
        }

        for i, patch in enumerate(patches):
            bin_center = (bins[i] + bins[i + 1]) / 2
            if bin_center < 50:
                patch.set_facecolor(grade_colors["fail"])
            elif bin_center < 65:
                patch.set_facecolor(grade_colors["pass"])
            elif bin_center < 80:
                patch.set_facecolor(grade_colors["good"])
            elif bin_center < 90:
                patch.set_facecolor(grade_colors["very_good"])
            else:
                patch.set_facecolor(grade_colors["excellent"])

        # Linije za prolaz i prosjek
        ax.axvline(x=50, color=theme.error, linestyle="--", linewidth=2, label="Prolaz (50)")
        mean_score = df["bodovi"].mean()
        ax.axvline(
            x=mean_score,
            color=theme.info,
            linestyle="-.",
            linewidth=2,
            label=f"Prosjek ({mean_score:.1f})"
        )

        ax.set_title(
            "Raspodjela bodova",
            fontsize=14,
            fontweight="bold",
            pad=15,
            color=theme.graph_fg
        )
        ax.set_xlabel("Broj bodova", fontsize=11)
        ax.set_ylabel("Broj studenata", fontsize=11)
        ax.set_xlim(0, 100)
        ax.set_ylim(bottom=0)

        legend = ax.legend(loc="upper right", fontsize=9)
        legend.get_frame().set_facecolor(theme.graph_bg)
        for text in legend.get_texts():
            text.set_color(theme.graph_fg)

        fig.tight_layout()
        return fig

    def _fig_avg_score_by_term(self, df: pd.DataFrame) -> Figure:
        """Linijski graf prosječnih bodova po terminu."""
        theme = self.theme
        fig, ax = self._create_figure()

        averages = df.groupby("termin")["bodovi"].mean().sort_index()

        ax.plot(
            averages.index,
            averages.values,
            marker="o",
            markersize=10,
            linewidth=2.5,
            color=theme.graph_colors[0],
            markerfacecolor=theme.graph_colors[1],
            markeredgecolor=theme.graph_bg,
            markeredgewidth=2
        )

        ax.fill_between(
            averages.index,
            averages.values,
            alpha=0.2,
            color=theme.graph_colors[0]
        )

        ax.set_title(
            "Prosječan broj bodova po ispitnom terminu",
            fontsize=14,
            fontweight="bold",
            pad=15,
            color=theme.graph_fg
        )
        ax.set_xlabel("Termin", fontsize=11)
        ax.set_ylabel("Prosječan broj bodova", fontsize=11)
        ax.set_ylim(bottom=0)

        for x, y in zip(averages.index, averages.values):
            ax.annotate(
                f"{y:.1f}",
                (x, y),
                textcoords="offset points",
                xytext=(0, 12),
                ha="center",
                fontsize=10,
                fontweight="bold",
                color=theme.graph_fg
            )

        fig.tight_layout()
        return fig

    def _fig_pass_rate_by_term(self, df: pd.DataFrame) -> Figure:
        """Stupčasti graf prolaznosti po terminu."""
        theme = self.theme
        fig, ax = self._create_figure()

        def calc_pass_rate(group: pd.DataFrame) -> float:
            passed = (group["ocjena"] >= 2).sum()
            return (passed / len(group)) * 100 if len(group) > 0 else 0.0

        pass_rates = df.groupby("termin").apply(calc_pass_rate, include_groups=False).sort_index()

        bars = ax.bar(
            pass_rates.index,
            pass_rates.values,
            color=theme.success,
            edgecolor=theme.graph_bg,
            linewidth=2
        )

        # Boje prema prolaznosti
        for bar in bars:
            height = bar.get_height()
            if height < 50:
                bar.set_color(theme.error)
            elif height < 70:
                bar.set_color(theme.warning)

        ax.axhline(y=50, color=theme.error, linestyle="--", linewidth=2, alpha=0.7)

        ax.set_title(
            "Prolaznost po ispitnom terminu",
            fontsize=14,
            fontweight="bold",
            pad=15,
            color=theme.graph_fg
        )
        ax.set_xlabel("Termin", fontsize=11)
        ax.set_ylabel("Prolaznost (%)", fontsize=11)
        ax.set_ylim(0, 105)

        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height + 2,
                f"{height:.1f}%",
                ha="center",
                va="bottom",
                fontsize=10,
                fontweight="bold",
                color=theme.graph_fg
            )

        fig.tight_layout()
        return fig

    def _fig_boxplot_by_term(self, df: pd.DataFrame) -> Figure:
        """Box plot distribucije bodova po terminu."""
        theme = self.theme
        fig, ax = self._create_figure()

        terms = sorted(df["termin"].unique())
        data = [df[df["termin"] == t]["bodovi"].values for t in terms]

        bp = ax.boxplot(data, labels=terms, patch_artist=True)

        for i, box in enumerate(bp["boxes"]):
            color_idx = i % len(theme.graph_colors)
            box.set_facecolor(theme.graph_colors[color_idx])
            box.set_alpha(0.7)
            box.set_edgecolor(theme.graph_fg)

        for median in bp["medians"]:
            median.set_color(theme.error)
            median.set_linewidth(2)

        for whisker in bp["whiskers"]:
            whisker.set_color(theme.graph_fg)

        for cap in bp["caps"]:
            cap.set_color(theme.graph_fg)

        for flier in bp["fliers"]:
            flier.set_markerfacecolor(theme.graph_fg)
            flier.set_markeredgecolor(theme.graph_fg)

        ax.axhline(y=50, color=theme.error, linestyle="--", linewidth=1.5, alpha=0.5, label="Prolaz")

        ax.set_title(
            "Distribucija bodova po terminu",
            fontsize=14,
            fontweight="bold",
            pad=15,
            color=theme.graph_fg
        )
        ax.set_xlabel("Termin", fontsize=11)
        ax.set_ylabel("Bodovi", fontsize=11)
        ax.set_ylim(0, 100)

        legend = ax.legend(loc="lower right", fontsize=9)
        legend.get_frame().set_facecolor(theme.graph_bg)
        for text in legend.get_texts():
            text.set_color(theme.graph_fg)

        fig.tight_layout()
        return fig
