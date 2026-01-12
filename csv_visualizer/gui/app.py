"""Glavna GUI aplikacija."""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from .. import __version__
from ..config import Theme, ThemeManager, get_settings
from ..data import DataGenerator, DataLoader, ExamData
from ..data.loader import DataValidationError
from ..visualization import GraphManager
from .widgets import (
    ModernButton,
    ThemeToggle,
    StatsPanel,
    DataTable,
    SearchBar,
    FilterPanel,
    StatusBar,
    Tooltip,
)


class Application(tk.Tk):
    """Glavna aplikacija za vizualizaciju podataka."""

    def __init__(self):
        super().__init__()

        self.settings = get_settings()
        self._theme = ThemeManager.get_current()

        # Inicijaliziraj temu iz postavki
        if self.settings.theme != self._theme.name:
            ThemeManager.set_theme(self.settings.theme)
            self._theme = ThemeManager.get_current()

        # Podaci
        self.data: ExamData | None = None
        self._filtered_data: ExamData | None = None
        self._term_filter: str | None = None
        self._grade_filter: int | None = None
        self._search_query: str = ""
        self.generator = DataGenerator()
        self.graph_manager = GraphManager()

        # Canvas i figure
        self.canvas: FigureCanvasTkAgg | None = None
        self.current_fig: Figure | None = None
        self.current_graph = tk.StringVar()

        # View mode
        self.view_mode = tk.StringVar(value="graph")  # "graph" ili "table"

        self._setup_window()
        self._configure_styles()
        self._create_ui()

        # Listener za teme
        ThemeManager.add_listener(self._on_theme_change)

        # Generiraj početne podatke
        self._generate_and_display()

    def _setup_window(self):
        """Postavlja prozor."""
        self.title(f"CSV Visualizer v{__version__} - Vizualizacija rezultata ispita")
        self.geometry(f"{self.settings.window_width}x{self.settings.window_height}")
        self.minsize(self.settings.min_width, self.settings.min_height)
        self.configure(bg=self._theme.bg_primary)

        # Ikona (ako postoji)
        try:
            self.iconbitmap("icon.ico")
        except tk.TclError:
            pass

    def _configure_styles(self):
        """Konfigurira ttk stilove."""
        style = ttk.Style()
        style.theme_use("clam")

        theme = self._theme

        style.configure("TFrame", background=theme.bg_primary)
        style.configure("TLabel", background=theme.bg_primary, foreground=theme.fg_primary)
        style.configure("TLabelframe", background=theme.bg_primary)
        style.configure(
            "TLabelframe.Label",
            background=theme.bg_primary,
            foreground=theme.fg_primary,
            font=("Segoe UI", 11, "bold")
        )

        style.configure(
            "TCombobox",
            fieldbackground=theme.bg_primary,
            background=theme.bg_secondary,
            foreground=theme.fg_primary,
            arrowcolor=theme.fg_primary,
            padding=8,
        )

        style.map(
            "TCombobox",
            fieldbackground=[("readonly", theme.bg_primary)],
            selectbackground=[("readonly", theme.accent)],
            selectforeground=[("readonly", theme.btn_primary_fg)],
        )

        # Header stil
        style.configure(
            "Header.TLabel",
            font=("Segoe UI", 18, "bold"),
            foreground=theme.accent,
            background=theme.bg_primary,
        )

        # Subtitle stil
        style.configure(
            "Subtitle.TLabel",
            font=("Segoe UI", 11),
            foreground=theme.fg_muted,
            background=theme.bg_primary,
        )

    def _create_ui(self):
        """Kreira korisničko sučelje."""
        theme = self._theme

        # Glavni container
        self.main_frame = tk.Frame(self, bg=theme.bg_primary, padx=20, pady=15)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        self._create_header()

        # Content area (lijevo + desno)
        content = tk.Frame(self.main_frame, bg=theme.bg_primary)
        content.pack(fill=tk.BOTH, expand=True, pady=(15, 0))

        # Lijevi panel (kontrole)
        self._create_left_panel(content)

        # Desni panel (graf/tablica)
        self._create_right_panel(content)

        # Status bar
        self._create_status_bar()

        # Keyboard shortcuts
        self._setup_shortcuts()

    def _create_header(self):
        """Kreira header s naslovom i theme toggleom."""
        theme = self._theme

        self.header_frame = tk.Frame(self.main_frame, bg=theme.bg_primary)
        self.header_frame.pack(fill=tk.X)

        # Lijeva strana - naslov
        self.title_frame = tk.Frame(self.header_frame, bg=theme.bg_primary)
        self.title_frame.pack(side=tk.LEFT)

        self.title_label = ttk.Label(
            self.title_frame,
            text="CSV Visualizer",
            style="Header.TLabel"
        )
        self.title_label.pack(anchor="w")

        self.subtitle_label = ttk.Label(
            self.title_frame,
            text="Vizualizacija rezultata ispita studenata",
            style="Subtitle.TLabel"
        )
        self.subtitle_label.pack(anchor="w")

        # Desna strana - theme toggle
        self.theme_toggle = ThemeToggle(self.header_frame)
        self.theme_toggle.pack(side=tk.RIGHT, padx=10)
        Tooltip(self.theme_toggle, "Promijeni temu (Ctrl+T)")

    def _create_left_panel(self, parent):
        """Kreira lijevi panel s kontrolama."""
        theme = self._theme

        left_panel = tk.Frame(parent, bg=theme.bg_secondary, width=340)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))
        left_panel.pack_propagate(False)

        # Padding unutar panela
        inner = tk.Frame(left_panel, bg=theme.bg_secondary, padx=15, pady=15)
        inner.pack(fill=tk.BOTH, expand=True)

        # === Odabir grafa ===
        graph_section = tk.Frame(inner, bg=theme.bg_secondary)
        graph_section.pack(fill=tk.X, pady=(0, 15))

        graph_label = tk.Label(
            graph_section,
            text="Tip grafa",
            font=("Segoe UI", 11, "bold"),
            bg=theme.bg_secondary,
            fg=theme.fg_primary
        )
        graph_label.pack(anchor="w", pady=(0, 8))

        self.combo_graph = ttk.Combobox(
            graph_section,
            textvariable=self.current_graph,
            state="readonly",
            values=GraphManager.get_available_graphs(),
            font=("Segoe UI", 10)
        )
        self.combo_graph.pack(fill=tk.X)
        self.combo_graph.current(0)
        self.combo_graph.bind("<<ComboboxSelected>>", lambda e: self._display_graph())

        # === View mode toggle ===
        view_section = tk.Frame(inner, bg=theme.bg_secondary)
        view_section.pack(fill=tk.X, pady=15)

        view_label = tk.Label(
            view_section,
            text="Prikaz",
            font=("Segoe UI", 11, "bold"),
            bg=theme.bg_secondary,
            fg=theme.fg_primary
        )
        view_label.pack(anchor="w", pady=(0, 8))

        view_btns = tk.Frame(view_section, bg=theme.bg_secondary)
        view_btns.pack(fill=tk.X)

        self.btn_graph_view = ModernButton(
            view_btns,
            text="📊 Graf",
            command=lambda: self._set_view("graph"),
            primary=True
        )
        self.btn_graph_view.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        self.btn_table_view = ModernButton(
            view_btns,
            text="📋 Tablica",
            command=lambda: self._set_view("table"),
            primary=False
        )
        self.btn_table_view.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))

        # === Akcije ===
        action_section = tk.Frame(inner, bg=theme.bg_secondary)
        action_section.pack(fill=tk.X, pady=15)

        action_label = tk.Label(
            action_section,
            text="Akcije",
            font=("Segoe UI", 11, "bold"),
            bg=theme.bg_secondary,
            fg=theme.fg_primary
        )
        action_label.pack(anchor="w", pady=(0, 8))

        self.btn_generate = ModernButton(
            action_section,
            text="🔄 Generiraj nove podatke",
            command=self._generate_and_display,
            primary=True
        )
        self.btn_generate.pack(fill=tk.X, pady=(0, 8))
        Tooltip(self.btn_generate, "Generiraj nove sintetičke podatke (Ctrl+G)")

        self.btn_load = ModernButton(
            action_section,
            text="📂 Učitaj CSV datoteku",
            command=self._load_csv
        )
        self.btn_load.pack(fill=tk.X, pady=(0, 8))
        Tooltip(self.btn_load, "Učitaj postojeću CSV datoteku (Ctrl+O)")

        self.btn_save = ModernButton(
            action_section,
            text="💾 Spremi graf kao sliku",
            command=self._save_graph
        )
        self.btn_save.pack(fill=tk.X, pady=(0, 8))
        Tooltip(self.btn_save, "Spremi trenutni graf kao sliku (Ctrl+S)")

        self.btn_export = ModernButton(
            action_section,
            text="📤 Izvezi podatke (CSV)",
            command=self._export_data
        )
        self.btn_export.pack(fill=tk.X)
        Tooltip(self.btn_export, "Izvezi podatke u CSV ili Excel format (Ctrl+E)")

        # === Statistika ===
        stats_section = tk.Frame(inner, bg=theme.bg_secondary)
        stats_section.pack(fill=tk.BOTH, expand=True, pady=(15, 0))

        stats_label = tk.Label(
            stats_section,
            text="Statistika",
            font=("Segoe UI", 11, "bold"),
            bg=theme.bg_secondary,
            fg=theme.fg_primary
        )
        stats_label.pack(anchor="w", pady=(0, 8))

        self.stats_panel = StatsPanel(stats_section)
        self.stats_panel.pack(fill=tk.BOTH, expand=True)

        self.left_panel = left_panel
        self.left_inner = inner

    def _create_right_panel(self, parent):
        """Kreira desni panel za graf/tablicu."""
        theme = self._theme

        right_panel = tk.Frame(parent, bg=theme.bg_primary)
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Toolbar s filterima (za tablicu)
        self.toolbar_frame = tk.Frame(right_panel, bg=theme.bg_secondary)

        # Filter panel
        self.filter_panel = FilterPanel(
            self.toolbar_frame,
            on_filter=self._on_filter
        )
        self.filter_panel.pack(side=tk.LEFT, padx=10, pady=8)

        # Search bar
        self.search_bar = SearchBar(
            self.toolbar_frame,
            on_search=self._on_search
        )
        self.search_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), pady=8)

        # Container za graf
        self.graph_frame = tk.Frame(
            right_panel,
            bg=theme.bg_secondary,
            highlightthickness=1,
            highlightbackground=theme.border
        )
        self.graph_frame.pack(fill=tk.BOTH, expand=True)

        # Container za tablicu (inicijalno skriven)
        self.table_frame = tk.Frame(right_panel, bg=theme.bg_secondary)
        self.data_table = DataTable(self.table_frame)
        self.data_table.pack(fill=tk.BOTH, expand=True)

        self.right_panel = right_panel

    def _set_view(self, mode: str):
        """Postavlja prikaz (graf ili tablica)."""
        self.view_mode.set(mode)

        if mode == "graph":
            self.btn_graph_view.primary = True
            self.btn_table_view.primary = False
            self.toolbar_frame.pack_forget()
            self.table_frame.pack_forget()
            self.graph_frame.pack(fill=tk.BOTH, expand=True)
            self._display_graph()
        else:
            self.btn_graph_view.primary = False
            self.btn_table_view.primary = True
            self.graph_frame.pack_forget()
            self.toolbar_frame.pack(fill=tk.X, pady=(0, 10))
            self.table_frame.pack(fill=tk.BOTH, expand=True)
            self._display_table()

        # Osvježi gumbe
        self.btn_graph_view._apply_theme()
        self.btn_table_view._apply_theme()

    def _generate_data(self) -> bool:
        """Generira nove podatke."""
        try:
            self.data = self.generator.generate_and_save()
            self._filtered_data = None
            self._term_filter = None
            self._grade_filter = None
            self._search_query = ""
            self._update_stats()
            self._update_filter_terms()
            return True
        except (IOError, ValueError, RuntimeError) as e:
            messagebox.showerror("Greška", f"Greška pri generiranju:\n{e}")
            return False

    def _generate_and_display(self):
        """Generira podatke i prikazuje graf."""
        if self._generate_data():
            if self.view_mode.get() == "graph":
                self._display_graph()
            else:
                self._display_table()

    def _load_csv(self):
        """Učitava CSV datoteku."""
        path = filedialog.askopenfilename(
            title="Odaberi CSV datoteku",
            filetypes=[
                ("CSV datoteke", "*.csv"),
                ("Sve datoteke", "*.*")
            ],
            initialdir=self.settings.last_opened_path or "."
        )

        if not path:
            return

        try:
            self.data = DataLoader.load(path)
            self._filtered_data = None
            self._term_filter = None
            self._grade_filter = None
            self._search_query = ""
            self.settings.last_opened_path = path
            self.settings.save()
            self._update_stats()
            self._update_filter_terms()

            if self.view_mode.get() == "graph":
                self._display_graph()
            else:
                self._display_table()

            messagebox.showinfo(
                "Uspjeh",
                f"Učitano {len(self.data)} zapisa iz:\n{path}"
            )

        except FileNotFoundError as e:
            messagebox.showerror("Greška", str(e))
        except DataValidationError as e:
            messagebox.showerror("Greška validacije", str(e))
        except Exception as e:
            messagebox.showerror("Greška", f"Neočekivana greška:\n{e}")

    def _display_graph(self):
        """Prikazuje odabrani graf."""
        data = self._filtered_data or self.data
        if data is None:
            return

        graph_name = self.current_graph.get()
        if not graph_name:
            graph_name = GraphManager.get_available_graphs()[0]

        try:
            fig = self.graph_manager.get_graph_by_name(graph_name, data)
        except ValueError as e:
            messagebox.showerror("Greška", str(e))
            return

        # Očisti prethodni canvas
        if self.canvas is not None:
            self.canvas.get_tk_widget().destroy()
            if self.current_fig is not None:
                plt.close(self.current_fig)
            self.canvas = None

        self.current_fig = fig
        self.canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        self.canvas.draw()

        widget = self.canvas.get_tk_widget()
        widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def _display_table(self):
        """Prikazuje tablicu s podacima."""
        data = self._filtered_data or self.data
        if data is None:
            self.data_table.clear()
            return

        self.data_table.load_data(data.dataframe)

    def _apply_filters(self):
        """Primjenjuje sve aktivne filtere na podatke."""
        if not self.data:
            self._filtered_data = None
            return

        filtered = self.data

        # Primijeni filter po terminu
        if self._term_filter:
            filtered = filtered.filter_by_term(self._term_filter)

        # Primijeni filter po ocjeni
        if self._grade_filter:
            filtered = filtered.filter_by_grade(self._grade_filter)

        # Primijeni pretragu po imenu
        if self._search_query:
            filtered = filtered.search(self._search_query)

        # Ako nema filtera, koristi originalne podatke
        if not self._term_filter and not self._grade_filter and not self._search_query:
            self._filtered_data = None
        else:
            self._filtered_data = filtered

    def _on_filter(self, term: str | None, grade: int | None):
        """Handler za filtriranje po terminu/ocjeni."""
        self._term_filter = term
        self._grade_filter = grade
        self._apply_filters()

        if self.view_mode.get() == "table":
            self._display_table()

        self._update_stats()

    def _on_search(self, query: str):
        """Handler za pretraživanje."""
        self._search_query = query
        self._apply_filters()

        if self.view_mode.get() == "table":
            self._display_table()

        self._update_stats()

    def _update_stats(self):
        """Ažurira prikaz statistike."""
        data = self._filtered_data or self.data
        if data is None:
            self.stats_panel.clear()
            return

        stats = data.get_statistics()
        self.stats_panel.update_stats(stats)

    def _update_filter_terms(self):
        """Ažurira dostupne termine u filter panelu."""
        if self.data:
            self.filter_panel.update_terms(self.data.terms)

    def _save_graph(self):
        """Sprema graf kao sliku."""
        if self.current_fig is None:
            messagebox.showwarning("Upozorenje", "Nema grafa za spremanje.")
            return

        path = filedialog.asksaveasfilename(
            title="Spremi graf kao...",
            defaultextension=f".{self.settings.default_format}",
            filetypes=[
                ("PNG slika", "*.png"),
                ("PDF dokument", "*.pdf"),
                ("SVG slika", "*.svg"),
                ("JPEG slika", "*.jpg"),
            ],
            initialdir=self.settings.last_save_path or "."
        )

        if not path:
            return

        try:
            self.current_fig.savefig(
                path,
                dpi=self.settings.default_dpi,
                bbox_inches="tight",
                facecolor=self.current_fig.get_facecolor()
            )
            self.settings.last_save_path = path
            self.settings.save()
            messagebox.showinfo("Uspjeh", f"Graf spremljen u:\n{path}")
        except Exception as e:
            messagebox.showerror("Greška", f"Greška pri spremanju:\n{e}")

    def _export_data(self):
        """Izvozi podatke u CSV datoteku."""
        data = self._filtered_data or self.data
        if data is None:
            messagebox.showwarning("Upozorenje", "Nema podataka za izvoz.")
            return

        path = filedialog.asksaveasfilename(
            title="Izvezi podatke kao...",
            defaultextension=".csv",
            filetypes=[
                ("CSV datoteka", "*.csv"),
                ("Excel datoteka", "*.xlsx"),
            ],
            initialdir=self.settings.last_save_path or "."
        )

        if not path:
            return

        try:
            if path.endswith(".xlsx"):
                data.dataframe.to_excel(path, index=False, engine="openpyxl")
            else:
                data.dataframe.to_csv(path, index=False, encoding="utf-8")

            self.settings.last_save_path = path
            self.settings.save()

            filter_info = ""
            if self._filtered_data:
                filter_info = f"\n(Filtrirano: {len(data)} od {len(self.data)} zapisa)"

            messagebox.showinfo(
                "Uspjeh",
                f"Podaci izvezeni u:\n{path}{filter_info}"
            )
        except ImportError:
            # openpyxl nije instaliran
            if path.endswith(".xlsx"):
                messagebox.showerror(
                    "Greška",
                    "Za izvoz u Excel format potrebno je instalirati 'openpyxl'.\n\n"
                    "Instalirajte s: pip install openpyxl"
                )
        except Exception as e:
            messagebox.showerror("Greška", f"Greška pri izvozu:\n{e}")

    def _on_theme_change(self, theme: Theme):
        """Handler za promjenu teme."""
        self._theme = theme

        # Spremi postavku
        self.settings.theme = theme.name
        self.settings.save()

        # Ažuriraj stilove
        self._configure_styles()

        # Ažuriraj pozadine
        self.configure(bg=theme.bg_primary)
        self.main_frame.configure(bg=theme.bg_primary)
        self.header_frame.configure(bg=theme.bg_primary)
        self.title_frame.configure(bg=theme.bg_primary)
        self.left_panel.configure(bg=theme.bg_secondary)
        self.left_inner.configure(bg=theme.bg_secondary)
        self.right_panel.configure(bg=theme.bg_primary)
        self.toolbar_frame.configure(bg=theme.bg_secondary)
        self.graph_frame.configure(
            bg=theme.bg_secondary,
            highlightbackground=theme.border
        )
        self.table_frame.configure(bg=theme.bg_secondary)

        # Ažuriraj labele u lijevom panelu
        for widget in self.left_inner.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.configure(bg=theme.bg_secondary)
                for child in widget.winfo_children():
                    if isinstance(child, tk.Label):
                        child.configure(bg=theme.bg_secondary, fg=theme.fg_primary)
                    elif isinstance(child, tk.Frame):
                        child.configure(bg=theme.bg_secondary)

        # Ponovno prikaži graf s novom temom
        if self.view_mode.get() == "graph" and self.data:
            self._display_graph()

    def _create_status_bar(self):
        """Kreira status bar na dnu prozora."""
        self.status_bar = StatusBar(self)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def _setup_shortcuts(self):
        """Postavlja keyboard shortcuts."""
        # Ctrl+G - Generiraj podatke
        self.bind("<Control-g>", lambda e: self._generate_and_display())

        # Ctrl+O - Učitaj CSV
        self.bind("<Control-o>", lambda e: self._load_csv())

        # Ctrl+S - Spremi graf
        self.bind("<Control-s>", lambda e: self._save_graph())

        # Ctrl+E - Izvezi podatke
        self.bind("<Control-e>", lambda e: self._export_data())

        # Ctrl+T - Promijeni temu
        self.bind("<Control-t>", lambda e: ThemeManager.toggle())

        # F5 - Refresh (generiraj nove podatke)
        self.bind("<F5>", lambda e: self._generate_and_display())

        # Ctrl+1 do Ctrl+6 - Brzi odabir grafa
        for i in range(6):
            self.bind(f"<Control-Key-{i+1}>", lambda e, idx=i: self._select_graph(idx))

    def _select_graph(self, index: int):
        """Odabire graf po indeksu."""
        graphs = GraphManager.get_available_graphs()
        if 0 <= index < len(graphs):
            self.current_graph.set(graphs[index])
            self._display_graph()

    def _update_status_bar(self):
        """Ažurira status bar s informacijama o podacima."""
        data = self._filtered_data or self.data
        if data and hasattr(self, 'status_bar'):
            count = len(data)
            if self._filtered_data and self.data:
                total = len(self.data)
                self.status_bar.set_info(f"Prikazano {count} od {total} zapisa")
            else:
                self.status_bar.set_info(f"Ukupno {count} zapisa")

    def destroy(self):
        """Čisti resurse pri zatvaranju."""
        ThemeManager.remove_listener(self._on_theme_change)

        if self.current_fig is not None:
            plt.close(self.current_fig)

        super().destroy()
