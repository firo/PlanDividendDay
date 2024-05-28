import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from streamlit_extras.buy_me_a_coffee import button

#st.set_page_config(layout="wide")

# Titolo dell'app
st.title('Pianificazione dei Dividendi di Titoli Azionari')

# Avvertimento legale
st.markdown("""
**Disclaimer:**
Questa applicazione è realizzata a scopo didattico per testare le funzionalità di Python e le librerie utilizzate. Non deve essere utilizzata come strumento finanziario su cui basare le proprie strategie di investimento. L'autore non si assume alcuna responsabilità per eventuali decisioni finanziarie prese sulla base delle informazioni fornite da questa applicazione.
""")

button(username="firo", floating=True, width=221)

# Sidebar per parametri di acquisto e vendita
st.sidebar.header("Parametri di Acquisto e Vendita")
acquisto = st.sidebar.slider('Giorni prima del dividendo per acquisto', -60, 60, -20)
vendita = st.sidebar.slider('Giorni dopo il dividendo per vendita', -60, 60, 2)

# Funzione per ottenere le date di stacco delle cedole e il nome dell'azienda
def get_dividend_dates(tickers):
    dividend_dates = []
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            dividends = stock.dividends
            if not dividends.empty:
                company_name = stock.info.get('longName', ticker)  # Ottieni il nome dell'azienda
                for date, value in dividends.items():
                    dividend_dates.append({'Ticker': ticker, 'Azienda': company_name, 'Date': date, 'Dividend': value})
        except Exception as e:
            st.error(f"Errore nel recupero dei dati per {ticker}: {e}")
    return pd.DataFrame(dividend_dates)

# Funzione per ottenere il prezzo corrente di un titolo
def get_current_price(ticker):
    try:
        stock = yf.Ticker(ticker)
        current_price = stock.history(period="1d")['Close'].iloc[0]
        return current_price
    except Exception as e:
        st.error(f"Errore nel recupero del prezzo corrente per {ticker}: {e}")
        return None

# Funzione per ottenere il prezzo di un titolo in una data specifica
def get_price_on_date(ticker, date):
    try:
        stock = yf.Ticker(ticker)
        history = stock.history(start=date - timedelta(days=1), end=date + timedelta(days=1))
        if not history.empty:
            return history['Close'].iloc[0]
        else:
            return None
    except Exception as e:
        st.error(f"Errore nel recupero del prezzo per {ticker} alla data {date}: {e}")
        return None

# Input per i ticker dei titoli azionari o il caricamento di un file CSV con i ticker
ticker_source = st.radio('Scegli la fonte dei ticker:', ['Inserimento manuale', 'Caricamento da file CSV'])

if ticker_source == 'Inserimento manuale':
    ticker_input = st.text_input('Inserisci i ticker separati da virgola')
    if ticker_input:
        tickers = [ticker.strip() for ticker in ticker_input.split(',')]
    else:
        tickers = []
else:
    uploaded_file = st.file_uploader("Carica un file CSV", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        tickers = df['Ticker'].tolist()
    else:
        tickers = []

# Controlla se ci sono ticker da elaborare
if tickers:
    # Ottieni le date di stacco delle cedole
    dividend_dates_df = get_dividend_dates(tickers)
    
    if not dividend_dates_df.empty:
        # Converte la colonna delle date in datetime senza fuso orario (offset-naive)
        dividend_dates_df['Date'] = pd.to_datetime(dividend_dates_df['Date']).dt.tz_localize(None)
        
        # Aggiungi colonna del mese e giorno
        dividend_dates_df['Mese'] = dividend_dates_df['Date'].dt.strftime('%B')
        dividend_dates_df['Giorno'] = dividend_dates_df['Date'].dt.day
        
        # Rinomina la colonna Dividend in Dividendi
        dividend_dates_df.rename(columns={'Dividend': 'Dividendi'}, inplace=True)
        
        # Ordina il DataFrame per mese e giorno
        ordered_months = ['January', 'February', 'March', 'April', 'May', 'June', 
                          'July', 'August', 'September', 'October', 'November', 'December']
        ordered_months_italian = ['Gennaio', 'Febbraio', 'Marzo', 'Aprile', 'Maggio', 'Giugno', 
                                  'Luglio', 'Agosto', 'Settembre', 'Ottobre', 'Novembre', 'Dicembre']
        month_mapping = dict(zip(ordered_months, ordered_months_italian))
        dividend_dates_df['Mese'] = dividend_dates_df['Mese'].map(month_mapping)
        dividend_dates_df['Mese'] = pd.Categorical(dividend_dates_df['Mese'], categories=ordered_months_italian, ordered=True)
        dividend_dates_df.sort_values(['Mese', 'Giorno'], inplace=True)
        
        # Filtra per l'anno corrente
        current_year = datetime.now().year
        current_year_dividends_df = dividend_dates_df[dividend_dates_df['Date'].dt.year == current_year]
        
        # Media delle cedole per gli ultimi 10 anni
        last_10_years = current_year - 10
        historical_dividends_df = dividend_dates_df[dividend_dates_df['Date'].dt.year >= last_10_years]
        historical_dividends_mean = historical_dividends_df.groupby('Ticker')['Dividendi'].mean().reset_index()
        historical_dividends_mean.rename(columns={'Dividendi': 'Media 10 anni'}, inplace=True)

        # Merge per aggiungere la media dei dividendi degli ultimi 10 anni
        current_year_dividends_df = pd.merge(current_year_dividends_df, historical_dividends_mean, on='Ticker', how='left')
        
        # Calcola il valore percentuale del dividendo rispetto al valore corrente del titolo
        current_year_dividends_df['Valore Corrente'] = current_year_dividends_df['Ticker'].apply(get_current_price)
        #st.write('--> valore corrente: ',(current_year_dividends_df['Ticker'].apply(get_current_price)))
        
        current_year_dividends_df['Rendimento (%)'] = (current_year_dividends_df['Dividendi'] / current_year_dividends_df['Valore Corrente']) * 100
        #st.write('--> dividendi correnti: ',current_year_dividends_df['Dividendi'])
        dividendi_correnti = current_year_dividends_df['Dividendi']
        valore_corrente = current_year_dividends_df['Valore Corrente']
        
        # Calcola il delta percentuale tra il valore corrente del dividendo e la media degli ultimi 10 anni
        current_year_dividends_df['Delta (%)'] = ((current_year_dividends_df['Dividendi'] - current_year_dividends_df['Media 10 anni']) / current_year_dividends_df['Media 10 anni']) * 100
        
        # Calcola il guadagno in base ai parametri di acquisto e vendita
        def calcola_guadagno(row):
            try:
                data_dividendo = row['Date']
                prezzo_acquisto = get_price_on_date(row['Ticker'], data_dividendo + timedelta(days=acquisto))
                prezzo_vendita = get_price_on_date(row['Ticker'], data_dividendo + timedelta(days=vendita))
                
                #st.write(data_dividendo + timedelta(days=acquisto))
                #st.write(data_dividendo + timedelta(days=vendita))
                
                if prezzo_acquisto is not None and prezzo_vendita is not None:
                    guadagno = prezzo_vendita - prezzo_acquisto
                    return guadagno
                else:
                    return None
            except Exception as e:
                st.error(f"Errore nel calcolo del guadagno per {row['Ticker']} alla data {data_dividendo}: {e}")
                return None
        
        # Applicare la funzione calcola_guadagno
        guadagno_assoluto = current_year_dividends_df.apply(
            lambda row: calcola_guadagno(row) if datetime.now().replace(tzinfo=None) > row['Date'] + timedelta(days=vendita) else None, axis=1
        )
        
        #st.write('--> guadagno assoluto: ', guadagno_assoluto )
        #st.write('--> dividendi + guadagno: ', guadagno_assoluto + dividendi_correnti)

        current_year_dividends_df['Guadagno (%)'] = (guadagno_assoluto / valore_corrente) * 100

        #st.write('--> time delta shift: ', acquisto)
        #st.write('--> time delta shift: ', vendita)
        #st.write('--> Dividend Day: ', (dividend_dates_df['Date']).dt.strftime('%d/%m/%y'))
        current_year_dividends_df['Acquisto'] = (current_year_dividends_df['Date'] + timedelta(days=acquisto)).dt.strftime('%d/%m')
        current_year_dividends_df['Vendita'] = (current_year_dividends_df['Date'] + timedelta(days=vendita)).dt.strftime('%d/%m')

        # Seleziona e ordina le colonne necessarie ('Ticker'))
        current_year_dividends_df = current_year_dividends_df[['Mese', 'Giorno', 'Azienda', 'Dividendi', 'Media 10 anni', 'Rendimento (%)', 'Acquisto', 'Vendita','Guadagno (%)']]
        
        # Mostra la tabella con le date di stacco delle cedole
        st.write(f"Date di stacco delle cedole raggruppate per mese per l'anno {current_year}:")
        st.dataframe(current_year_dividends_df)

        st.write("Il Rendimento (%) è riferito al dividendo.")
        st.write("Acquisto e Vendita sono le date di ingresso e uscita, qualora la data del dividendo sia nel passato.")

        #current_year_trade_df = 
    else:
        st.write("Nessuna data di stacco delle cedole trovata.")
else:
    st.write("Inserisci dei ticker per procedere.")
