# Pianificazione dei Dividendi di Titoli Azionari

**Disclaimer:**
Questa applicazione è realizzata a scopo didattico per testare le funzionalità di Python e le librerie utilizzate. Non deve essere utilizzata come strumento finanziario su cui basare le proprie strategie di investimento. L'autore non si assume alcuna responsabilità per eventuali decisioni finanziarie prese sulla base delle informazioni fornite da questa applicazione.

## Descrizione dell'Applicazione

### Scopo dell'Applicazione
L'applicazione è progettata per aiutare gli utenti a pianificare i loro investimenti in azioni basati sui dividendi. Consente agli utenti di inserire i ticker di azioni e ottenere informazioni dettagliate sulle date di stacco dei dividendi, il rendimento attuale e le medie storiche dei dividendi.

### Funzionalità Principali
1. **Inserimento dei Ticker**:
   - Gli utenti possono inserire manualmente i ticker delle azioni o caricare un file CSV contenente i ticker.

2. **Recupero dei Dati**:
   - Utilizza la libreria `yfinance` per ottenere le date di stacco dei dividendi, i valori dei dividendi, i nomi delle aziende e i prezzi correnti delle azioni.

3. **Elaborazione dei Dati**:
   - Calcola il rendimento percentuale dei dividendi rispetto al valore corrente dell'azione.
   - Fornisce la media dei dividendi degli ultimi 10 anni per ciascun ticker.
   - Calcola il delta percentuale tra il dividendo corrente e la media degli ultimi 10 anni.

4. **Visualizzazione dei Dati**:
   - Mostra i dati in una tabella ordinata per mese e giorno, rendendo facile per gli utenti vedere quando riceveranno i dividendi.
   - La tabella include colonne per il mese, giorno, ticker, nome dell'azienda, dividendi, rendimento percentuale, media dei dividendi degli ultimi 10 anni e il delta percentuale.

5. **Avvertimento Legale**:
   - Include un disclaimer che chiarisce che l'applicazione è a scopo didattico e non deve essere utilizzata come strumento per decisioni di investimento.

### Utilizzo dell'Applicazione
1. **Selezione della Fonte dei Ticker**:
   - L'utente sceglie se inserire i ticker manualmente o caricare un file CSV.

2. **Inserimento o Caricamento dei Ticker**:
   - L'utente inserisce i ticker separati da virgola o carica un file CSV con i ticker.

3. **Visualizzazione dei Risultati**:
   - L'applicazione elabora i dati e visualizza una tabella con tutte le informazioni necessarie per pianificare gli investimenti basati sui dividendi.

### Tecnologie Utilizzate
- **Streamlit**: Per creare l'interfaccia web interattiva.
- **yfinance**: Per recuperare dati finanziari dai ticker delle azioni.
- **Pandas**: Per la manipolazione e l'elaborazione dei dati.
- **Streamlit Extras**: Per aggiungere elementi interattivi come il pulsante "Buy Me a Coffee".

Questa applicazione è utile per gli investitori che desiderano organizzare e ottimizzare i loro portafogli in base ai pagamenti dei dividendi, fornendo una visione chiara e dettagliata delle informazioni rilevanti.


<a href="https://www.buymeacoffee.com/firo"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a coffee&emoji=☕&slug=firo&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>

