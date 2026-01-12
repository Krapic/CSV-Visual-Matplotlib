"""Custom widgeti s podrškom za teme."""

import tkinter as tk
from tkinter import ttk
from typing import Callable
import platform

from ..config import Theme, ThemeManager


def get_mono_font() -> str:
    """Vraća dostupan monospace font za sustav."""
    system = platform.system()
    if system == "Windows":
        # Probaj moderne fontove prvo
        preferred = ["Cascadia Code", "Consolas", "Courier New"]
    elif system == "Darwin":  # macOS
        preferred = ["SF Mono", "Menlo", "Monaco"]
    else:  # Linux
        preferred = ["JetBrains Mono", "Ubuntu Mono", "DejaVu Sans Mono", "Monospace"]

    # Vrati prvi dostupan ili fallback
    return preferred[0] if preferred else "TkFixedFont"


MONO_FONT = get_mono_font()


class Tooltip:
    """Tooltip widget koji se prikazuje na hover."""

    def __init__(self, widget: tk.Widget, text: str, delay: int = 500):
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tooltip_window: tk.Toplevel | None = None
        self._after_id: str | None = None

        self.widget.bind("<Enter>", self._schedule_show)
        self.widget.bind("<Leave>", self._hide)
        self.widget.bind("<ButtonPress>", self._hide)

    def _schedule_show(self, event=None):
        """Zakazuje prikaz tooltipa nakon delay-a."""
        self._cancel_scheduled()
        self._after_id = self.widget.after(self.delay, self._show)

    def _cancel_scheduled(self):
        """Otkazuje zakazani prikaz."""
        if self._after_id:
            self.widget.after_cancel(self._after_id)
            self._after_id = None

    def _show(self):
        """Prikazuje tooltip."""
        if self.tooltip_window:
            return

        theme = ThemeManager.get_current()

        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5

        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")

        # Stil tooltipa
        frame = tk.Frame(
            self.tooltip_window,
            bg=theme.bg_tertiary,
            highlightbackground=theme.border,
            highlightthickness=1
        )
        frame.pack()

        label = tk.Label(
            frame,
            text=self.text,
            bg=theme.bg_tertiary,
            fg=theme.fg_primary,
            font=("Segoe UI", 9),
            padx=8,
            pady=4
        )
        label.pack()

    def _hide(self, event=None):
        """Skriva tooltip."""
        self._cancel_scheduled()
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

    def update_text(self, new_text: str):
        """Ažurira tekst tooltipa."""
        self.text = new_text


class ThemedFrame(ttk.Frame):
    """Frame s podrškom za teme."""

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        ThemeManager.add_listener(self._on_theme_change)

    def _on_theme_change(self, theme: Theme):
        pass  # Override u podklasama

    def destroy(self):
        ThemeManager.remove_listener(self._on_theme_change)
        super().destroy()


class ModernButton(tk.Button):
    """Moderan gumb s hover efektima."""

    def __init__(
        self,
        master,
        text: str = "",
        command: Callable | None = None,
        primary: bool = False,
        **kwargs
    ):
        self.primary = primary
        self._theme = ThemeManager.get_current()

        super().__init__(
            master,
            text=text,
            command=command,
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 10, "bold" if primary else "normal"),
            padx=16,
            pady=8,
            **kwargs
        )

        self._apply_theme()
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        ThemeManager.add_listener(self._on_theme_change)

    def _apply_theme(self):
        theme = self._theme
        if self.primary:
            self.configure(
                bg=theme.btn_primary_bg,
                fg=theme.btn_primary_fg,
                activebackground=theme.accent_hover,
                activeforeground=theme.btn_primary_fg,
            )
        else:
            self.configure(
                bg=theme.btn_secondary_bg,
                fg=theme.btn_secondary_fg,
                activebackground=theme.bg_tertiary,
                activeforeground=theme.fg_primary,
            )

    def _on_enter(self, event):
        theme = self._theme
        if self.primary:
            self.configure(bg=theme.accent_hover)
        else:
            self.configure(bg=theme.bg_tertiary)

    def _on_leave(self, event):
        self._apply_theme()

    def _on_theme_change(self, theme: Theme):
        self._theme = theme
        self._apply_theme()

    def destroy(self):
        ThemeManager.remove_listener(self._on_theme_change)
        super().destroy()


class ThemeToggle(tk.Frame):
    """Prekidač za dark/light mode."""

    def __init__(self, master, **kwargs):
        self._theme = ThemeManager.get_current()
        super().__init__(master, bg=self._theme.bg_secondary, **kwargs)

        self._create_widgets()
        ThemeManager.add_listener(self._on_theme_change)

    def _create_widgets(self):
        theme = self._theme

        self.label = tk.Label(
            self,
            text="☀️" if theme.name == "light" else "🌙",
            font=("Segoe UI", 14),
            bg=theme.bg_secondary,
            cursor="hand2"
        )
        self.label.pack(padx=5)
        self.label.bind("<Button-1>", self._toggle)

    def _toggle(self, event=None):
        ThemeManager.toggle()

    def _on_theme_change(self, theme: Theme):
        self._theme = theme
        self.configure(bg=theme.bg_secondary)
        self.label.configure(
            text="☀️" if theme.name == "light" else "🌙",
            bg=theme.bg_secondary
        )

    def destroy(self):
        ThemeManager.remove_listener(self._on_theme_change)
        super().destroy()


class StatsPanel(tk.Frame):
    """Panel za prikaz statistike."""

    def __init__(self, master, **kwargs):
        self._theme = ThemeManager.get_current()
        super().__init__(master, bg=self._theme.stats_bg, **kwargs)

        self._create_widgets()
        ThemeManager.add_listener(self._on_theme_change)

    def _create_widgets(self):
        theme = self._theme

        self.text = tk.Text(
            self,
            wrap=tk.WORD,
            font=("JetBrains Mono", 10),
            bg=theme.stats_bg,
            fg=theme.stats_fg,
            relief="flat",
            padx=15,
            pady=15,
            state=tk.DISABLED,
            borderwidth=0,
            highlightthickness=0,
        )
        self.text.pack(fill=tk.BOTH, expand=True)

    def update_stats(self, stats: dict):
        """Ažurira prikaz statistike."""
        self.text.config(state=tk.NORMAL)
        self.text.delete(1.0, tk.END)

        lines = []
        lines.append("━" * 32)
        lines.append("  UKUPNA STATISTIKA")
        lines.append("━" * 32)
        lines.append(f"  Broj studenata:    {stats['count']}")
        lines.append(f"  Prosječna ocjena:  {stats['avg_grade']:.2f}")
        lines.append(f"  Prosječni bodovi:  {stats['avg_score']:.2f}")
        lines.append(f"  Std. dev. bodova:  {stats['std_score']:.2f}")
        lines.append(f"  Min/Max bodovi:    {stats['min_score']} / {stats['max_score']}")
        lines.append(f"  Medijan bodova:    {stats['median_score']:.1f}")
        lines.append("")
        lines.append(f"  Prolaznost:        {stats['pass_rate']:.1f}%")
        lines.append(f"  Položilo:          {stats['passed_count']} / {stats['count']}")

        lines.append("")
        lines.append("━" * 32)
        lines.append("  DISTRIBUCIJA OCJENA")
        lines.append("━" * 32)

        total = stats["count"]
        for grade in [1, 2, 3, 4, 5]:
            count = stats["grade_distribution"].get(grade, 0)
            pct = (count / total) * 100 if total > 0 else 0
            bar = "█" * int(pct / 5)
            lines.append(f"  Ocjena {grade}: {count:3d} ({pct:5.1f}%) {bar}")

        lines.append("")
        lines.append("━" * 32)
        lines.append("  PO TERMINIMA")
        lines.append("━" * 32)

        for term, term_stats in stats["term_stats"].items():
            lines.append(
                f"  {term}: {term_stats['count']:3d} stud., "
                f"prosjek {term_stats['avg_score']:.1f}"
            )

        self.text.insert(tk.END, "\n".join(lines))
        self.text.config(state=tk.DISABLED)

    def clear(self):
        """Briše sadržaj."""
        self.text.config(state=tk.NORMAL)
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, "  Nema učitanih podataka.")
        self.text.config(state=tk.DISABLED)

    def _on_theme_change(self, theme: Theme):
        self._theme = theme
        self.configure(bg=theme.stats_bg)
        self.text.configure(bg=theme.stats_bg, fg=theme.stats_fg)

    def destroy(self):
        ThemeManager.remove_listener(self._on_theme_change)
        super().destroy()


class DataTable(tk.Frame):
    """Tablica za prikaz podataka s sortiranjem."""

    def __init__(self, master, **kwargs):
        self._theme = ThemeManager.get_current()
        super().__init__(master, bg=self._theme.bg_secondary, **kwargs)

        self._sort_column = None
        self._sort_reverse = False
        self._data = None

        self._create_widgets()
        ThemeManager.add_listener(self._on_theme_change)

    def _create_widgets(self):
        theme = self._theme

        # Treeview s scrollbarom
        columns = ("id", "ime", "prezime", "termin", "bodovi", "ocjena")

        style = ttk.Style()
        style.configure(
            "DataTable.Treeview",
            background=theme.bg_secondary,
            foreground=theme.fg_primary,
            fieldbackground=theme.bg_secondary,
            rowheight=28,
            font=("Segoe UI", 10)
        )
        style.configure(
            "DataTable.Treeview.Heading",
            background=theme.bg_tertiary,
            foreground=theme.fg_primary,
            font=("Segoe UI", 10, "bold")
        )
        style.map(
            "DataTable.Treeview",
            background=[("selected", theme.accent)],
            foreground=[("selected", theme.btn_primary_fg)]
        )

        # Container za treeview i scrollbar - sačuvaj referencu
        self._container = tk.Frame(self, bg=theme.bg_secondary)
        self._container.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(
            self._container,
            columns=columns,
            show="headings",
            style="DataTable.Treeview",
            selectmode="browse"
        )

        # Vertikalni scrollbar
        self._v_scrollbar = ttk.Scrollbar(
            self._container, orient=tk.VERTICAL, command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=self._v_scrollbar.set)

        # Horizontalni scrollbar
        self._h_scrollbar = ttk.Scrollbar(
            self._container, orient=tk.HORIZONTAL, command=self.tree.xview
        )
        self.tree.configure(xscrollcommand=self._h_scrollbar.set)

        # Definicija stupaca
        column_config = {
            "id": ("ID", 60),
            "ime": ("Ime", 120),
            "prezime": ("Prezime", 140),
            "termin": ("Termin", 100),
            "bodovi": ("Bodovi", 80),
            "ocjena": ("Ocjena", 80),
        }

        for col, (heading, width) in column_config.items():
            self.tree.heading(
                col,
                text=heading,
                command=lambda c=col: self._sort_by(c)
            )
            self.tree.column(col, width=width, anchor="center")

        # Grid layout za scrollbarove
        self.tree.grid(row=0, column=0, sticky="nsew")
        self._v_scrollbar.grid(row=0, column=1, sticky="ns")
        self._h_scrollbar.grid(row=1, column=0, sticky="ew")

        self._container.grid_rowconfigure(0, weight=1)
        self._container.grid_columnconfigure(0, weight=1)

    def load_data(self, df):
        """Učitava podatke u tablicu."""
        self._data = df

        # Očisti postojeće
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Dodaj redove
        for _, row in df.iterrows():
            values = (
                row["student_id"],
                row["ime"],
                row["prezime"],
                row["termin"],
                row["bodovi"],
                row["ocjena"]
            )
            self.tree.insert("", tk.END, values=values)

    def _sort_by(self, column: str):
        """Sortira tablicu po stupcu."""
        if self._data is None:
            return

        if self._sort_column == column:
            self._sort_reverse = not self._sort_reverse
        else:
            self._sort_column = column
            self._sort_reverse = False

        # Mapiranje naziva stupaca
        col_map = {
            "id": "student_id",
            "ime": "ime",
            "prezime": "prezime",
            "termin": "termin",
            "bodovi": "bodovi",
            "ocjena": "ocjena"
        }

        sorted_df = self._data.sort_values(
            by=col_map[column],
            ascending=not self._sort_reverse
        )

        self.load_data(sorted_df)

    def clear(self):
        """Briše tablicu."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        self._data = None

    def _on_theme_change(self, theme: Theme):
        self._theme = theme
        self.configure(bg=theme.bg_secondary)
        self._container.configure(bg=theme.bg_secondary)

        style = ttk.Style()
        style.configure(
            "DataTable.Treeview",
            background=theme.bg_secondary,
            foreground=theme.fg_primary,
            fieldbackground=theme.bg_secondary,
        )
        style.configure(
            "DataTable.Treeview.Heading",
            background=theme.bg_tertiary,
            foreground=theme.fg_primary,
        )
        style.map(
            "DataTable.Treeview",
            background=[("selected", theme.accent)],
            foreground=[("selected", theme.btn_primary_fg)]
        )

    def destroy(self):
        ThemeManager.remove_listener(self._on_theme_change)
        super().destroy()


class FilterPanel(tk.Frame):
    """Panel za filtriranje podataka po terminu i ocjeni."""

    def __init__(
        self,
        master,
        on_filter: Callable[[str | None, int | None], None],
        **kwargs
    ):
        self._theme = ThemeManager.get_current()
        super().__init__(master, bg=self._theme.bg_secondary, **kwargs)

        self._on_filter = on_filter
        self._terms: list[str] = []
        self._create_widgets()
        ThemeManager.add_listener(self._on_theme_change)

    def _create_widgets(self):
        theme = self._theme

        # Termin filter
        term_frame = tk.Frame(self, bg=theme.bg_secondary)
        term_frame.pack(side=tk.LEFT, padx=(0, 15))

        term_label = tk.Label(
            term_frame,
            text="Termin:",
            font=("Segoe UI", 10),
            bg=theme.bg_secondary,
            fg=theme.fg_primary
        )
        term_label.pack(side=tk.LEFT, padx=(0, 5))

        self.term_var = tk.StringVar(value="Svi")
        self.term_combo = ttk.Combobox(
            term_frame,
            textvariable=self.term_var,
            state="readonly",
            values=["Svi"],
            width=12,
            font=("Segoe UI", 10)
        )
        self.term_combo.pack(side=tk.LEFT)
        self.term_combo.bind("<<ComboboxSelected>>", self._on_change)

        # Ocjena filter
        grade_frame = tk.Frame(self, bg=theme.bg_secondary)
        grade_frame.pack(side=tk.LEFT, padx=(0, 15))

        grade_label = tk.Label(
            grade_frame,
            text="Ocjena:",
            font=("Segoe UI", 10),
            bg=theme.bg_secondary,
            fg=theme.fg_primary
        )
        grade_label.pack(side=tk.LEFT, padx=(0, 5))

        self.grade_var = tk.StringVar(value="Sve")
        self.grade_combo = ttk.Combobox(
            grade_frame,
            textvariable=self.grade_var,
            state="readonly",
            values=["Sve", "1", "2", "3", "4", "5"],
            width=8,
            font=("Segoe UI", 10)
        )
        self.grade_combo.pack(side=tk.LEFT)
        self.grade_combo.bind("<<ComboboxSelected>>", self._on_change)

        # Reset gumb
        self.reset_btn = tk.Label(
            self,
            text="⟲ Reset",
            font=("Segoe UI", 10),
            bg=theme.bg_secondary,
            fg=theme.accent,
            cursor="hand2"
        )
        self.reset_btn.pack(side=tk.LEFT, padx=10)
        self.reset_btn.bind("<Button-1>", self._reset)

        self._term_frame = term_frame
        self._grade_frame = grade_frame
        self._term_label = term_label
        self._grade_label = grade_label

    def update_terms(self, terms: list[str]):
        """Ažurira dostupne termine."""
        self._terms = terms
        self.term_combo["values"] = ["Svi"] + sorted(terms)

    def _on_change(self, event=None):
        term = self.term_var.get()
        grade = self.grade_var.get()

        term_filter = None if term == "Svi" else term
        grade_filter = None if grade == "Sve" else int(grade)

        self._on_filter(term_filter, grade_filter)

    def _reset(self, event=None):
        self.term_var.set("Svi")
        self.grade_var.set("Sve")
        self._on_filter(None, None)

    def _on_theme_change(self, theme: Theme):
        self._theme = theme
        self.configure(bg=theme.bg_secondary)
        self._term_frame.configure(bg=theme.bg_secondary)
        self._grade_frame.configure(bg=theme.bg_secondary)
        self._term_label.configure(bg=theme.bg_secondary, fg=theme.fg_primary)
        self._grade_label.configure(bg=theme.bg_secondary, fg=theme.fg_primary)
        self.reset_btn.configure(bg=theme.bg_secondary, fg=theme.accent)

    def destroy(self):
        ThemeManager.remove_listener(self._on_theme_change)
        super().destroy()


class SearchBar(tk.Frame):
    """Traka za pretraživanje."""

    def __init__(self, master, on_search: Callable[[str], None], **kwargs):
        self._theme = ThemeManager.get_current()
        super().__init__(master, bg=self._theme.bg_secondary, **kwargs)

        self._on_search = on_search
        self._create_widgets()
        ThemeManager.add_listener(self._on_theme_change)

    def _create_widgets(self):
        theme = self._theme

        # Ikona pretraživanja
        self.icon_label = tk.Label(
            self,
            text="🔍",
            font=("Segoe UI", 12),
            bg=theme.bg_secondary
        )
        self.icon_label.pack(side=tk.LEFT, padx=(10, 5))

        # Entry za unos
        self.entry = tk.Entry(
            self,
            font=("Segoe UI", 11),
            bg=theme.bg_primary,
            fg=theme.fg_primary,
            insertbackground=theme.fg_primary,
            relief="flat",
            highlightthickness=1,
            highlightbackground=theme.border,
            highlightcolor=theme.accent,
        )
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=8)
        self.entry.bind("<KeyRelease>", self._on_key)
        self.entry.bind("<Return>", self._on_key)

        # Placeholder
        self.entry.insert(0, "Pretraži po imenu...")
        self.entry.configure(fg=theme.fg_muted)
        self.entry.bind("<FocusIn>", self._on_focus_in)
        self.entry.bind("<FocusOut>", self._on_focus_out)

        # Gumb za brisanje
        self.clear_btn = tk.Label(
            self,
            text="✕",
            font=("Segoe UI", 10),
            bg=theme.bg_secondary,
            fg=theme.fg_muted,
            cursor="hand2"
        )
        self.clear_btn.pack(side=tk.RIGHT, padx=10)
        self.clear_btn.bind("<Button-1>", self._clear)

    def _on_key(self, event):
        query = self.entry.get()
        if query != "Pretraži po imenu...":
            self._on_search(query)

    def _on_focus_in(self, event):
        if self.entry.get() == "Pretraži po imenu...":
            self.entry.delete(0, tk.END)
            self.entry.configure(fg=self._theme.fg_primary)

    def _on_focus_out(self, event):
        if not self.entry.get():
            self.entry.insert(0, "Pretraži po imenu...")
            self.entry.configure(fg=self._theme.fg_muted)

    def _clear(self, event=None):
        self.entry.delete(0, tk.END)
        self._on_search("")
        self._on_focus_out(None)

    def _on_theme_change(self, theme: Theme):
        self._theme = theme
        self.configure(bg=theme.bg_secondary)
        self.icon_label.configure(bg=theme.bg_secondary)

        # Provjeri je li placeholder aktivan
        is_placeholder = self.entry.get() == "Pretraži po imenu..."
        self.entry.configure(
            bg=theme.bg_primary,
            fg=theme.fg_muted if is_placeholder else theme.fg_primary,
            insertbackground=theme.fg_primary,
            highlightbackground=theme.border,
            highlightcolor=theme.accent,
        )
        self.clear_btn.configure(bg=theme.bg_secondary, fg=theme.fg_muted)

    def destroy(self):
        ThemeManager.remove_listener(self._on_theme_change)
        super().destroy()
