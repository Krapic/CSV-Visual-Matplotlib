# Osnovna vizualizacija podataka (Matplotlib)

Kratak primjer projekta za kolegij "Osnovna vizualizacija podataka". Koristi se sintetički dataset studenata računarstva (godina studija, smjer, ocjene, ECTS, sati učenja) i nekoliko grafova izrađenih u Matplotlibu.

## Struktura
- `main.py` – ulazna točka (CLI ili GUI).
- `student_viz/` – paket s konfiguracijom, učitavanjem podataka, grafovima i pipelineom.
  - `config.py` – putanje, teme.
  - `data.py` – učitavanje i filtriranje.
  - `plots.py` – sve Matplotlib vizualizacije.
  - `pipeline.py` – primjena tema, KPI, pokretanje grafova.
  - `gui_app.py` – Tkinter GUI.
- `scripts/generate_dataset.py` – reproducibilno generira `data/students.csv` (ili drugu putanju).
- `data/students.csv` – zadani primjer podataka (~180 redaka).
- `data/students_alt1.csv`, `data/students_alt2.csv` – dodatni primjeri (različiti seedovi).
- `requirements.txt` – ovisnosti (pandas, matplotlib, pillow).

## Što je u podacima?
Svaki redak predstavlja jednog studenta diplomskog studija (2 godine, max 120 ECTS):
- `date` – referentni datum unosa (YYYY-MM-DD)
- `student_id` – sintetički ID
- `year` – godina studija (1–2)
- `specialization` – smjer (`Programsko inž.`, `Računalni sustavi`)
- `city` – grad prebivališta (`Zagreb`, `Split`, `Rijeka`)
- `gender` – `M` ili `F`
- `avg_grade` – prosječna ocjena (2.0–5.0)
- `ects_completed` – ukupni položeni ECTS bodovi
- `weekly_hours` – procjena sati tjedno na učenje/projekte
- `attendance_rate` – prosječna prisutnost (0–1)
- `scholarship` – 1 ako student ima stipendiju (u sintetičkim podacima definirano kombinacijom ocjene i prisutnosti)

## Brzi start
```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# (po želji) regeneriraj dataset
python3 scripts/generate_dataset.py           # novi random dataset svaki put
# ili zadani seed / putanju radi reproducibilnosti:
# python3 scripts/generate_dataset.py --seed 42 --output data/students.csv

# pokreni GUI (default)
python3 main.py
```
Grafovi se spremaju u `figures/` (direktorij će se sam stvoriti).

### GUI način (default)
Pokreni samo `python3 main.py`. U GUI prozoru možeš:
- odabrati CSV i izlazni direktorij,
- filtrirati po smjeru, godini, gradu i “samo stipendisti” (prazan filter javlja grešku),
- generirati grafove i vidjeti ih odmah u tabovima,
- gledati KPI kartice (prosj. ocjena, prosj. ECTS, prosj. sati/tjedno, udio stipendija),
- birati light/dark temu (primjenjuje se i na Matplotlib),
- izvesti sve grafove u jedan PDF (`viz_report.pdf`),
- izvesti filtrirani CSV i vidjeti Top 10 (poseban tab s tablicom),
- pratiti status/progress i otvoriti direktorij s rezultatima,
- svaki klik na “Generiraj grafove” regenerira default dataset kako bi grafovi bili različiti (ako koristiš `data/students.csv`).

### CLI način (bez GUI)
```bash
python3 main.py --cli --theme light --regen --specialization "Programsko inž." --year 2 --city Zagreb --scholarship-only
# ili --theme dark; --regen pravi novi dataset ako je default
```

## Što se vizualizira?
- `01_grade_by_year.png` – prosječna ocjena po godini studija.
- `02_ects_by_specialization.png` – prosječni ECTS po godini i smjeru (side-by-side bar, max 60 po godini).
- `03_hours_vs_grade.png` – odnos tjednih sati i prosječne ocjene (raspršeni graf).
- `04_scholarship_rate.png` – udio stipendista po smjeru (horizontalni bar s oznakama).
- `05_grade_distribution.png` – distribucija prosječnih ocjena (histogram + Gauss KDE).
- `06_attendance_vs_grade.png` – prisustvo vs. prosječna ocjena s trend linijom.
- `07_gender_comparison.png` – usporedba prosjeka ocjena i udjela stipendija po spolu.

## Napomene
- Dataset je sintetički, ali reproducibilan (možeš navesti seed); default GUI regenerira novi set pri svakom kliku radi različitih grafova.
- Po potrebi mijenjaj stupce ili dodaj nove grafove u `main.py` — podaci se spremaju u `data/students.csv`, pa je lako eksperimentirati.
