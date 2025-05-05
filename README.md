# PyRecon🧭

Script Python semplice per cercare URL con la query `intitle:"Gophish - Login" inurl:login` su Google e salvare i risultati in un file.

## Requisiti
- Python 3.8+
- Dipendenze: `requests`, `beautifulsoup4`

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
```bash
python main.py
```
I risultati vengono salvati in `results.txt`.

## Note
- Usa responsibly: rispetta i termini di servizio di Google.
- Potresti incontrare blocchi da Google; considera pause o proxy per uso intensivo.
