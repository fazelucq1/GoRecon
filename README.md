# PyRecon🧭

Script Python per cercare URL con Google Dorks tramite l'API Google Custom Search e generare un report HTML professionale e grafici analitici.

## Requisiti
- Python 3.8+
- Dipendenze: `requests`, `python-dotenv`, `matplotlib`, `numpy`
- Google API Key e Custom Search Engine ID

## Installazione
1. Clona il repository:
   ```bash
   git clone https://github.com/fazelucq1/PyRecon.git
   cd PyRecon
   ```
2. Installa le dipendenze:
   ```bash
   pip install -r requirements.txt
   ```


## Utilizzo
Esegui lo script con parametri Google Dorks personalizzati:
```bash
python main.py --intitle "Gophish - Login" --inurl login --max-results 10
```
- **Parametri disponibili**:
  - `--query`: Query di base (es. `login page`)
  - `--intitle`: Cerca nel titolo (es. `Gophish - Login`)
  - `--inurl`: Cerca nell'URL (es. `login`)
  - `--site`: Limita a un dominio (es. `example.com`)
  - `--filetype`: Tipo di file (es. `pdf`)
  - `--intext`: Cerca nel testo (es. `admin`)
  - `--exclude`: Escludi termine (es. `signup`)
  - `--max-results`: Numero massimo di risultati (default: 10)

- **Esempio**:
  ```bash
  python main.py --site example.com --filetype pdf --exclude signup
  ```

- I risultati vengono salvati in `report.html`.
- I grafici vengono salvati in `charts/`.

## Report
Il report HTML include:
- Una tabella con gli URL trovati e i relativi domini.
- Grafici:
  - Conteggio URL per dominio (grafico a barre).
  - Distribuzione delle lunghezze degli URL (istogramma).

## Note
- Assicurati che il Custom Search Engine associato al CSE ID sia configurato per cercare su tutto il web su [cse.google.com](https://cse.google.com/cse/).
- L'API Google Custom Search ha un limite di 100 query gratuite al giorno.
- Usa responsabilmente, rispettando i termini di servizio di Google e le normative sulla privacy.

## Licenza
MIT
