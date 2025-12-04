import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import numpy as np

# Boje za grafove
BOJE_GRAFOVA = ["#003893", "#CE1126", "#4A90D9", "#E74C3C", "#2ECC71", "#F39C12"]
POZADINA_GRAF = "#f8f9fa"

# Hrvatska imena i prezimena
MUSKA_IMENA = [
    "Luka", "Ivan", "Marko", "Petar", "Josip", "Matej", "Filip", "Ante", "Tomislav",
    "Karlo", "Leon", "David", "Antonio", "Nikola", "Fran", "Lovro", "Borna", "Domagoj",
    "Tin", "Jan", "Roko", "Matija", "Jakov", "Andrija", "Marin", "Bruno", "Leo"
]

ZENSKA_IMENA = [
    "Ana", "Marija", "Ivana", "Petra", "Lucija", "Maja", "Sara", "Lana", "Eva",
    "Ema", "Mia", "Nika", "Lara", "Nina", "Tea", "Lea", "Paula", "Helena",
    "Karla", "Marta", "Katarina", "Valentina", "Klara", "Gabriela", "Nikolina"
]

PREZIMENA = [
    "Horvat", "Kovačević", "Babić", "Marić", "Novak", "Jurić", "Kovač", "Knežević",
    "Vuković", "Božić", "Blažević", "Perić", "Tomić", "Matić", "Pavlović", "Radić",
    "Šimić", "Nikolić", "Grgić", "Filipović", "Barić", "Lončar", "Pavić", "Šarić",
    "Jakić", "Klarić", "Vidović", "Mihaljević", "Tadić", "Lovrić", "Petrović"
]

TERMINI = ["2025-01", "2025-02", "2025-06", "2025-09"]
CSV_PUTANJA = "studenti_ispit.csv"


def bodovi_u_ocjenu(bodovi: int) -> int:
    if bodovi >= 90:
        return 5
    elif bodovi >= 80:
        return 4
    elif bodovi >= 65:
        return 3
    elif bodovi >= 50:
        return 2
    else:
        return 1


def generiraj_csv(putanja: str, broj_studenata: int = 50) -> pd.DataFrame:
    """Generira CSV s nasumičnim podacima studenata."""
    podaci = []
    koristena_imena = set()

    for i in range(1, broj_studenata + 1):
        while True:
            if random.random() < 0.5:
                ime = random.choice(MUSKA_IMENA)
            else:
                ime = random.choice(ZENSKA_IMENA)
            prezime = random.choice(PREZIMENA)
            puno_ime = f"{ime} {prezime}"
            if puno_ime not in koristena_imena:
                koristena_imena.add(puno_ime)
                break

        termin = random.choice(TERMINI)

        # Realistična distribucija bodova
        tip = random.random()
        if tip < 0.15:
            bodovi = int(np.clip(np.random.normal(25, 10), 0, 49))
        elif tip < 0.30:
            bodovi = int(np.clip(np.random.normal(55, 8), 50, 64))
        elif tip < 0.55:
            bodovi = int(np.clip(np.random.normal(70, 6), 65, 79))
        elif tip < 0.80:
            bodovi = int(np.clip(np.random.normal(85, 5), 80, 89))
        else:
            bodovi = int(np.clip(np.random.normal(93, 4), 90, 100))

        ocjena = bodovi_u_ocjenu(bodovi)

        podaci.append({
            "student_id": i,
            "ime": ime,
            "prezime": prezime,
            "termin": termin,
            "bodovi": bodovi,
            "ocjena": ocjena
        })

    df = pd.DataFrame(podaci)
    df.to_csv(putanja, index=False)
    return df


def fig_broj_studenata_po_ocjeni(df: pd.DataFrame):
    ocjene_counts = df["ocjena"].value_counts().sort_index()
    sve_ocjene = [1, 2, 3, 4, 5]
    vrijednosti = [ocjene_counts.get(o, 0) for o in sve_ocjene]

    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor(POZADINA_GRAF)
    ax.set_facecolor(POZADINA_GRAF)

    bars = ax.bar([str(o) for o in sve_ocjene], vrijednosti, color=BOJE_GRAFOVA[:5],
                  edgecolor="white", linewidth=1.5)

    ax.set_title("Broj studenata po ocjeni", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Ocjena", fontsize=11)
    ax.set_ylabel("Broj studenata", fontsize=11)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_ylim(bottom=0)
    ax.margins(x=0)

    for bar, v in zip(bars, vrijednosti):
        if v > 0:
            ax.text(bar.get_x() + bar.get_width()/2, v + 0.3, str(v),
                    ha="center", va="bottom", fontsize=10, fontweight="bold")

    fig.tight_layout()
    return fig


def fig_udjel_ocjena(df: pd.DataFrame):
    ocjene_counts = df["ocjena"].value_counts().sort_index()
    labels = [f"Ocjena {int(o)}" for o in ocjene_counts.index]

    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor(POZADINA_GRAF)

    wedges, texts, autotexts = ax.pie(
        ocjene_counts.values,
        labels=labels,
        autopct="%.1f%%",
        startangle=90,
        colors=BOJE_GRAFOVA[:len(labels)],
        explode=[0.02] * len(labels),
        shadow=True
    )

    for autotext in autotexts:
        autotext.set_fontsize(10)
        autotext.set_fontweight("bold")

    ax.set_title("Udio ocjena", fontsize=14, fontweight="bold", pad=15)
    fig.tight_layout()
    return fig


def fig_histogram_bodova(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor(POZADINA_GRAF)
    ax.set_facecolor(POZADINA_GRAF)

    # Fiksni raspon 0-100 s 10 binova
    n, bins, patches = ax.hist(df["bodovi"], bins=10, range=(0, 100), edgecolor="white", linewidth=1.2)

    for i, patch in enumerate(patches):
        bin_center = (bins[i] + bins[i+1]) / 2
        if bin_center < 50:
            patch.set_facecolor("#E74C3C")
        elif bin_center < 65:
            patch.set_facecolor("#F39C12")
        elif bin_center < 80:
            patch.set_facecolor("#4A90D9")
        elif bin_center < 90:
            patch.set_facecolor("#2ECC71")
        else:
            patch.set_facecolor("#003893")

    ax.axvline(x=50, color="#CE1126", linestyle="--", linewidth=2, label="Prolaz (50)")
    ax.axvline(x=df["bodovi"].mean(), color="#003893", linestyle="-.", linewidth=2,
               label=f"Prosjek ({df['bodovi'].mean():.1f})")

    ax.set_title("Raspodjela bodova", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Broj bodova", fontsize=11)
    ax.set_ylabel("Broj studenata", fontsize=11)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_xlim(0, 100)
    ax.set_ylim(bottom=0)
    ax.legend(loc="upper right", fontsize=9)

    fig.tight_layout()
    return fig


def fig_prosjek_bodova_po_terminu(df: pd.DataFrame):
    prosjeci = df.groupby("termin")["bodovi"].mean().sort_index()

    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor(POZADINA_GRAF)
    ax.set_facecolor(POZADINA_GRAF)

    ax.plot(prosjeci.index, prosjeci.values, marker="o", markersize=10,
            linewidth=2.5, color="#003893", markerfacecolor="#CE1126",
            markeredgecolor="white", markeredgewidth=2)

    ax.fill_between(prosjeci.index, prosjeci.values, alpha=0.2, color="#003893")

    ax.set_title("Prosječan broj bodova po ispitnom terminu", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Termin", fontsize=11)
    ax.set_ylabel("Prosječan broj bodova", fontsize=11)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_ylim(bottom=0)
    ax.margins(x=0)

    for x, y in zip(prosjeci.index, prosjeci.values):
        ax.annotate(f"{y:.1f}", (x, y), textcoords="offset points",
                    xytext=(0, 12), ha="center", fontsize=10, fontweight="bold")

    fig.tight_layout()
    return fig


def fig_prolaznost_po_terminu(df: pd.DataFrame):
    def izracunaj_prolaznost(grupa):
        prolaz = (grupa["ocjena"] >= 2).sum()
        return (prolaz / len(grupa)) * 100 if len(grupa) > 0 else 0

    prolaznost = df.groupby("termin").apply(izracunaj_prolaznost).sort_index()

    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor(POZADINA_GRAF)
    ax.set_facecolor(POZADINA_GRAF)

    bars = ax.bar(prolaznost.index, prolaznost.values, color="#2ECC71",
                  edgecolor="white", linewidth=1.5)

    for bar in bars:
        if bar.get_height() < 50:
            bar.set_color("#E74C3C")
        elif bar.get_height() < 70:
            bar.set_color("#F39C12")

    ax.axhline(y=50, color="#CE1126", linestyle="--", linewidth=2, alpha=0.7)

    ax.set_title("Prolaznost po ispitnom terminu", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Termin", fontsize=11)
    ax.set_ylabel("Prolaznost (%)", fontsize=11)
    ax.set_ylim(0, 105)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.margins(x=0)

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height + 2, f"{height:.1f}%",
                ha="center", va="bottom", fontsize=10, fontweight="bold")

    fig.tight_layout()
    return fig


def fig_boxplot_bodova_po_terminu(df: pd.DataFrame):
    termini = sorted(df["termin"].unique())
    podaci = [df[df["termin"] == t]["bodovi"].values for t in termini]

    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor(POZADINA_GRAF)
    ax.set_facecolor(POZADINA_GRAF)

    bp = ax.boxplot(podaci, labels=termini, patch_artist=True)

    for i, box in enumerate(bp["boxes"]):
        box.set_facecolor(BOJE_GRAFOVA[i % len(BOJE_GRAFOVA)])
        box.set_alpha(0.7)

    for median in bp["medians"]:
        median.set_color("#CE1126")
        median.set_linewidth(2)

    ax.axhline(y=50, color="#CE1126", linestyle="--", linewidth=1.5, alpha=0.5, label="Prolaz")

    ax.set_title("Distribucija bodova po terminu", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Termin", fontsize=11)
    ax.set_ylabel("Bodovi", fontsize=11)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_ylim(0, 100)
    ax.margins(x=0)
    ax.legend(loc="lower right", fontsize=9)

    fig.tight_layout()
    return fig


class Aplikacija(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Vizualizacija rezultata ispita")
        self.geometry("1400x800")
        self.minsize(1200, 700)
        self.configure(bg="#f0f0f0")

        self.df: pd.DataFrame | None = None
        self.canvas: FigureCanvasTkAgg | None = None
        self.trenutni_graf = tk.StringVar()

        self._konfiguriraj_stilove()
        self._kreiraj_gui()

        # Generiraj početne podatke i prikaži graf
        self._generiraj_i_prikazi()

    def _konfiguriraj_stilove(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TFrame", background="#f0f0f0")
        style.configure("TLabel", background="#f0f0f0", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10), padding=8)
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"))
        style.configure("TLabelframe", background="#f0f0f0")
        style.configure("TLabelframe.Label", font=("Segoe UI", 11, "bold"), background="#f0f0f0")
        style.configure("TCombobox", font=("Segoe UI", 10), padding=5)

        style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), foreground="#003893")

    def _kreiraj_gui(self):
        glavni_okvir = ttk.Frame(self, padding=15)
        glavni_okvir.pack(fill=tk.BOTH, expand=True)

        glavni_okvir.columnconfigure(0, weight=1, minsize=320)
        glavni_okvir.columnconfigure(1, weight=4)
        glavni_okvir.rowconfigure(0, weight=1)

        lijevi_panel = ttk.Frame(glavni_okvir)
        lijevi_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 15))

        lbl_title = ttk.Label(
            lijevi_panel,
            text="Vizualizacija rezultata ispita",
            style="Header.TLabel"
        )
        lbl_title.pack(anchor="w", pady=(0, 20))

        okvir_graf = ttk.LabelFrame(lijevi_panel, text="Odabir grafa", padding=10)
        okvir_graf.pack(fill=tk.X, pady=(0, 15))

        self.combo_tip_grafa = ttk.Combobox(
            okvir_graf,
            textvariable=self.trenutni_graf,
            state="readonly",
            values=[
                "Broj studenata po ocjeni",
                "Udio ocjena",
                "Histogram bodova",
                "Prosjek bodova po terminu",
                "Prolaznost po terminu",
                "Box plot bodova po terminu",
            ],
            font=("Segoe UI", 10)
        )
        self.combo_tip_grafa.pack(fill=tk.X, pady=(0, 10))
        self.combo_tip_grafa.current(0)
        self.combo_tip_grafa.bind("<<ComboboxSelected>>", lambda e: self._prikazi_graf())

        btn_prikazi = ttk.Button(
            okvir_graf, text="Generiraj nove podatke",
            command=self._generiraj_i_prikazi,
            style="Accent.TButton"
        )
        btn_prikazi.pack(fill=tk.X)

        okvir_statistika = ttk.LabelFrame(lijevi_panel, text="Osnovna statistika", padding=10)
        okvir_statistika.pack(fill=tk.BOTH, expand=True)

        self.text_statistika = tk.Text(
            okvir_statistika,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg="#ffffff",
            relief="flat",
            padx=10,
            pady=10,
            state=tk.DISABLED
        )
        self.text_statistika.pack(fill=tk.BOTH, expand=True)

        desni_panel = ttk.Frame(glavni_okvir)
        desni_panel.grid(row=0, column=1, sticky="nsew")

        desni_panel.rowconfigure(0, weight=1)
        desni_panel.columnconfigure(0, weight=1)

        self.okvir_graf = tk.Frame(desni_panel, bg="#ffffff", relief="solid", bd=1)
        self.okvir_graf.grid(row=0, column=0, sticky="nsew")

    def _generiraj_nove_podatke(self):
        """Generira nove nasumične podatke i sprema u CSV."""
        self.df = generiraj_csv(CSV_PUTANJA, broj_studenata=50)
        self.osvjezi_statistiku()

    def _generiraj_i_prikazi(self):
        """Generira nove podatke i prikazuje odabrani graf."""
        self._generiraj_nove_podatke()
        self._prikazi_graf()

    def osvjezi_statistiku(self):
        self.text_statistika.config(state=tk.NORMAL)
        self.text_statistika.delete(1.0, tk.END)

        if self.df is None:
            self.text_statistika.insert(tk.END, "Nema učitanih podataka.")
            self.text_statistika.config(state=tk.DISABLED)
            return

        df = self.df
        tekst = []
        tekst.append(f"{'='*30}")
        tekst.append("UKUPNA STATISTIKA")
        tekst.append(f"{'='*30}")
        tekst.append(f"Broj studenata: {len(df)}")
        tekst.append(f"Prosječna ocjena: {df['ocjena'].mean():.2f}")
        tekst.append(f"Prosječni bodovi: {df['bodovi'].mean():.2f}")
        tekst.append(f"Std. dev. bodova: {df['bodovi'].std():.2f}")
        tekst.append(f"Min bodovi: {df['bodovi'].min()}")
        tekst.append(f"Max bodovi: {df['bodovi'].max()}")
        tekst.append(f"Medijan bodova: {df['bodovi'].median():.1f}")

        prolaz = (df["ocjena"] >= 2).sum()
        prolaznost = (prolaz / len(df)) * 100 if len(df) > 0 else 0
        tekst.append(f"\nProlaznost: {prolaznost:.1f}%")
        tekst.append(f"Položilo: {prolaz} / {len(df)}")

        tekst.append(f"\n{'='*30}")
        tekst.append("DISTRIBUCIJA OCJENA")
        tekst.append(f"{'='*30}")
        ocjene_counts = df["ocjena"].value_counts().sort_index()
        for ocjena in [1, 2, 3, 4, 5]:
            broj = ocjene_counts.get(ocjena, 0)
            postotak = (broj / len(df)) * 100 if len(df) > 0 else 0
            bar = "█" * int(postotak / 5)
            tekst.append(f"Ocjena {ocjena}: {broj:3d} ({postotak:5.1f}%) {bar}")

        tekst.append(f"\n{'='*30}")
        tekst.append("PO TERMINIMA")
        tekst.append(f"{'='*30}")
        for termin in sorted(df["termin"].unique()):
            df_termin = df[df["termin"] == termin]
            prosj = df_termin["bodovi"].mean()
            tekst.append(f"{termin}: {len(df_termin):3d} stud., prosjek {prosj:.1f}")

        self.text_statistika.insert(tk.END, "\n".join(tekst))
        self.text_statistika.config(state=tk.DISABLED)

    def _prikazi_graf(self):
        if self.df is None:
            return

        naziv = self.trenutni_graf.get()
        if not naziv:
            naziv = "Broj studenata po ocjeni"

        graf_funkcije = {
            "Broj studenata po ocjeni": fig_broj_studenata_po_ocjeni,
            "Udio ocjena": fig_udjel_ocjena,
            "Histogram bodova": fig_histogram_bodova,
            "Prosjek bodova po terminu": fig_prosjek_bodova_po_terminu,
            "Prolaznost po terminu": fig_prolaznost_po_terminu,
            "Box plot bodova po terminu": fig_boxplot_bodova_po_terminu,
        }

        if naziv not in graf_funkcije:
            messagebox.showerror("Greška", "Nepoznat tip grafa.")
            return

        fig = graf_funkcije[naziv](self.df)

        if self.canvas is not None:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None

        self.canvas = FigureCanvasTkAgg(fig, master=self.okvir_graf)
        self.canvas.draw()
        widget = self.canvas.get_tk_widget()
        widget.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        plt.close(fig)


def main():
    app = Aplikacija()
    app.mainloop()


if __name__ == "__main__":
    main()
