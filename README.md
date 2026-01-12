<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776ab?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Matplotlib-3.7+-11557c?style=for-the-badge&logo=plotly&logoColor=white" alt="Matplotlib">
  <img src="https://img.shields.io/badge/Pandas-2.0+-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas">
  <img src="https://img.shields.io/badge/Tkinter-GUI-ff6f00?style=for-the-badge&logo=python&logoColor=white" alt="Tkinter">
  <img src="https://img.shields.io/badge/Version-2.0.0-success?style=for-the-badge" alt="Version">
</p>

<h1 align="center">📊 CSV Visualizer</h1>

<p align="center">
  <strong>🎓 Moderna desktop aplikacija za vizualizaciju rezultata ispita studenata</strong>
</p>

<p align="center">
  <em>Jednostavno učitajte CSV, filtrirajte podatke i generirajte prekrasne grafove — sve u par klikova!</em>
</p>

---

## ✨ Značajke

<table>
<tr>
<td width="50%">

### 🎨 Moderno sučelje
- 🌙 **Dark/Light tema** — prilagodite izgled prema vlastitim preferencijama
- 🖥️ **Responzivan dizajn** — prozor se prilagođava vašim potrebama
- 🎯 **Intuitivne kontrole** — sve je na dohvat ruke

</td>
<td width="50%">

### 📈 Napredna vizualizacija
- 📊 **6 tipova grafova** — stupčasti, tortni, histogram, linijski, box plot...
- 🎨 **Automatsko stiliziranje** — grafovi se prilagođavaju odabranoj temi
- 💾 **Izvoz u više formata** — PNG, PDF, SVG, JPEG

</td>
</tr>
<tr>
<td width="50%">

### 🔍 Filtriranje podataka
- 🗓️ **Filter po terminu** — analizirajte pojedine ispitne rokove
- 🎯 **Filter po ocjeni** — fokusirajte se na određene ocjene
- 🔎 **Pretraga po imenu** — brzo pronađite studente

</td>
<td width="50%">

### 📋 Statistika uživo
- 📊 **Broj studenata** — ukupan broj zapisa
- 📈 **Prosjek bodova/ocjena** — ključni pokazatelji
- ✅ **Prolaznost** — postotak uspješnih studenata
- 📉 **Min/Max/Medijan** — detaljna analiza

</td>
</tr>
</table>

---

## 🖼️ Tipovi grafova

| Graf | Opis |
|:----:|------|
| 📊 **Broj studenata po ocjeni** | Stupčasti graf koji prikazuje distribuciju ocjena |
| 🥧 **Udio ocjena** | Tortni dijagram s postotnim udjelima svake ocjene |
| 📈 **Histogram bodova** | Distribucija bodova s označenim pragom prolaza i prosjekom |
| 📉 **Prosjek bodova po terminu** | Linijski graf koji pokazuje trend kroz termine |
| ✅ **Prolaznost po terminu** | Stupčasti graf prolaznosti s bojama prema uspješnosti |
| 📦 **Box plot po terminu** | Statistička distribucija bodova za svaki termin |

---

## 🚀 Brzi početak

### 📋 Preduvjeti

- Python **3.11** ili noviji
- pip (Python package manager)

### ⚡ Instalacija

```bash
1️⃣ Klonirajte repozitorij
git clone https://github.com/Krapic/csv-visualizer.git
cd csv-visualizer

2️⃣ Kreirajte virtualno okruženje
python -m venv .venv

3️⃣ Aktivirajte virtualno okruženje
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 4️⃣ Instalirajte ovisnosti
pip install -r requirements.txt
```

### ▶️ Pokretanje

```bash
python run.py
```

🎉 **To je to!** Aplikacija će se otvoriti s automatski generiranim podacima.

---

## 📁 Struktura projekta

```
csv_visualizer/
├── 📂 config/
│   ├── 🎨 themes.py      # Light/Dark teme
│   └── ⚙️ settings.py    # Postavke aplikacije
├── 📂 data/
│   ├── 🏭 generator.py   # Generator sintetičkih podataka
│   ├── 📥 loader.py      # Učitavanje CSV datoteka
│   └── 📋 models.py      # Podatkovni modeli
├── 📂 gui/
│   ├── 🖥️ app.py         # Glavna aplikacija
│   └── 🧩 widgets.py     # Custom widgeti (gumbi, paneli...)
├── 📂 visualization/
│   └── 📊 graphs.py      # Generiranje grafova
└── 📂 utils/
    └── 🔧 __init__.py    # Pomoćne funkcije
```

---

## 📊 Format CSV datoteke

Aplikacija očekuje CSV datoteku sa sljedećim stupcima:

| Stupac | Tip | Opis |
|--------|-----|------|
| `student_id` | int | Jedinstveni identifikator studenta |
| `ime` | string | Ime studenta |
| `prezime` | string | Prezime studenta |
| `termin` | string | Ispitni termin (npr. "Zimski", "Ljetni") |
| `bodovi` | int | Broj ostvarenih bodova (0-100) |
| `ocjena` | int | Ocjena (1-5) |

### 📝 Primjer CSV datoteke

```csv
student_id,ime,prezime,termin,bodovi,ocjena
1,Marko,Horvat,Zimski,85,4
2,Ana,Kovač,Zimski,92,5
3,Ivan,Babić,Ljetni,45,1
4,Petra,Novak,Ljetni,67,3
```

---

## 🎮 Kako koristiti

### 1️⃣ Generiranje podataka
Kliknite **🔄 Generiraj nove podatke** za automatsko kreiranje sintetičkih podataka za testiranje.

### 2️⃣ Učitavanje vlastite datoteke
Kliknite **📂 Učitaj CSV datoteku** i odaberite vašu CSV datoteku s podacima ispita.

### 3️⃣ Odabir grafa
Iz padajućeg izbornika odaberite željeni tip vizualizacije.

### 4️⃣ Filtriranje (opcionalno)
- Prebacite na **📋 Tablica** prikaz
- Koristite filtere za termin i ocjenu
- Pretražujte studente po imenu

### 5️⃣ Izvoz rezultata
- **💾 Spremi graf kao sliku** — PNG, PDF, SVG ili JPEG
- **📤 Izvezi podatke** — CSV ili Excel format

---

## 🌙 Teme

Aplikacija podržava dvije teme koje možete mijenjati u bilo kojem trenutku:

<table>
<tr>
<td align="center" width="50%">

### ☀️ Light tema
Svijetla tema idealna za dnevni rad s visokim kontrastom i čitljivošću.

</td>
<td align="center" width="50%">

### 🌙 Dark tema
Tamna tema koja smanjuje naprezanje očiju i štedi bateriju na OLED ekranima.

</td>
</tr>
</table>

---

## 🛠️ Tehnologije

<table>
<tr>
<td align="center" width="25%">
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" width="48" height="48" alt="Python">
<br><strong>Python 3.11+</strong>
<br><sub>Programski jezik</sub>
</td>
<td align="center" width="25%">
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/pandas/pandas-original.svg" width="48" height="48" alt="Pandas">
<br><strong>Pandas</strong>
<br><sub>Obrada podataka</sub>
</td>
<td align="center" width="25%">
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/matplotlib/matplotlib-original.svg" width="48" height="48" alt="Matplotlib">
<br><strong>Matplotlib</strong>
<br><sub>Vizualizacija</sub>
</td>
<td align="center" width="25%">
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/numpy/numpy-original.svg" width="48" height="48" alt="NumPy">
<br><strong>NumPy</strong>
<br><sub>Numeričke operacije</sub>
</td>
</tr>
</table>

---

## 📦 Ovisnosti

```txt
pandas>=2.0.0      # Manipulacija podacima
numpy>=1.24.0      # Numeričke operacije
matplotlib>=3.7.0  # Generiranje grafova
pillow>=9.0.0      # Obrada slika
```

---

## 🤝 Doprinos projektu

Doprinosi su dobrodošli! 🎉

1. 🍴 Forkajte repozitorij
2. 🌿 Kreirajte feature branch (`git checkout -b feature/AmazingFeature`)
3. 💾 Commitajte promjene (`git commit -m 'Add some AmazingFeature'`)
4. 📤 Pushajte branch (`git push origin feature/AmazingFeature`)
5. 🔃 Otvorite Pull Request

---

## 📄 Licenca

Ovaj projekt je izrađen u sklopu kolegija **Programiranje skriptni jezici** na Tehničkom fakultetu u Rijeci.

---

## 👨‍💻 Autor

<p align="center">
Frane Krapić
</p>

---

<p align="center">
  <strong>⭐ Ako vam se sviđa projekt, ostavite zvjezdicu! ⭐</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Made%20with-Python-1f425f.svg?style=flat-square" alt="Made with Python">
  <img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square" alt="PRs Welcome">
</p>
