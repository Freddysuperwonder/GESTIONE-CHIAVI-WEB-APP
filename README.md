# 🔑 GESTIONE CHIAVI CASE VACANZA# Gestione Chiavi Case Vacanza



Sistema completo per la gestione della consegna e restituzione delle chiavi di case vacanza.Applicazione Python per la gestione della consegna e restituzione delle chiavi delle case vacanza.



## 📋 COME AVVIARE IL PROGRAMMA## 🎯 Funzionalità



### ✅ VERSIONE CONSIGLIATA - Interfaccia Grafica- **Gestione Case**: Aggiungi, visualizza ed elimina case vacanza

**Doppio click su:** `AVVIA_VERSIONE_GRAFICA.bat`- **Gestione Collaboratori**: Gestisci l'anagrafica dei collaboratori

- **Gestione Movimenti**: Registra consegne e restituzioni delle chiavi con tracciamento completo

### 📝 Versione Testuale (Console)- **Storico**: Visualizza lo storico di tutti i movimenti

**Doppio click su:** `AVVIA_VERSIONE_TESTUALE.bat`- **Ricerca**: Cerca movimenti per casa o collaboratore

- **Dashboard**: Riepilogo in tempo reale dello stato delle chiavi

---

## 📦 Installazione

## 🎯 FUNZIONALITÀ PRINCIPALI

1. Assicurati di avere Python 3.6 o superiore installato

### 🏘️ Gestione Case Vacanza2. Clona o scarica il progetto

- Aggiungi, modifica, elimina case3. Esegui l'applicazione

- Imposta numero di chiavi disponibili per casa

- Visualizza chiavi disponibili/affidate in tempo reale## 🚀 Avvio Applicazione

- Importa elenco case da file Excel

- Ricerca collaboratori con chiavi di una casa specifica### Versione Grafica (Consigliata)

Doppio click su:

### 👥 Gestione Collaboratori```

- Aggiungi, modifica, elimina collaboratoriavvia_interfaccia_grafica.bat

- Anagrafica completa (nome, cognome, telefono, email)```

- Ricerca case affidate a un collaboratoreOppure da terminale:

```

### 🔑 Movimenti Chiavipython gui_main.py

- Registra consegna chiavi```

- Registra restituzione chiavi

- Blocco automatico se chiavi non disponibili### Versione Console

- Storico completo di tutti i movimentiDoppio click su:

- Visualizzazione chiavi attualmente consegnate```

avvia_gestione_chiavi.bat

### 💾 Backup e Sicurezza```

- **Backup automatico** alla chiusura del programmaOppure da terminale:

- Pulsante "Save" per backup manuali```

- Pulsante "Load" per ripristinare backup precedentipython main.py

- I backup automatici sono salvati in `backups/` (ultimi 10)```



---## Struttura del Database



## 📁 STRUTTURA FILEIl database SQLite contiene 3 tabelle:



### File Principali### Tabella `case`

- `AVVIA_VERSIONE_GRAFICA.bat` - Avvia interfaccia grafica ⭐- id (chiave primaria)

- `AVVIA_VERSIONE_TESTUALE.bat` - Avvia versione console- nome_casa (univoco)

- `gestione_chiavi.db` - Database SQLite con tutti i dati- indirizzo

- `esempio_importazione_case.xlsx` - Esempio per importazione Excel- note

- data_creazione

### File Python (Non Modificare)

- `gui_main.py` - Interfaccia principale### Tabella `collaboratori`

- `gui_case.py` - Sezione case- id (chiave primaria)

- `gui_collaboratori.py` - Sezione collaboratori- nome

- `gui_movimenti.py` - Sezione movimenti- cognome

- `database.py` - Gestione database- telefono

- `main.py` - Versione console- email

- data_creazione

### Cartelle

- `backups/` - Backup automatici (creata automaticamente)### Tabella `movimenti_chiavi`

- id (chiave primaria)

---- id_casa (chiave esterna)

- id_collaboratore (chiave esterna)

## 📊 IMPORTAZIONE CASE DA EXCEL- data_consegna

- data_restituzione (NULL se non ancora restituita)

Il file Excel deve avere questa struttura:- note



| Nome Casa | Indirizzo | Numero Chiavi |## Utilizzo

|-----------|-----------|---------------|

| Villa Mare Blu | Via del Mare 15, Rimini | 2 |1. **Aggiungi Case e Collaboratori**: Prima di registrare movimenti, aggiungi almeno una casa e un collaboratore

| Casa Montagna | Via Alpina 22, Pesaro | 3 |2. **Registra Consegna**: Quando consegni una chiave a un collaboratore

3. **Registra Restituzione**: Quando il collaboratore restituisce la chiave

- **Colonna A**: Nome Casa (obbligatorio)4. **Visualizza Stato**: Controlla quali chiavi sono attualmente consegnate

- **Colonna B**: Indirizzo (opzionale)5. **Consulta Storico**: Visualizza tutti i movimenti passati

- **Colonna C**: Numero Chiavi (opzionale, default 1)

- La prima riga può contenere intestazioni## 📁 File del Progetto



Usa `esempio_importazione_case.xlsx` come riferimento.### File Principali

- `gui_main.py`: Applicazione con interfaccia grafica (Tkinter)

---- `main.py`: Applicazione console a menu

- `database.py`: Gestione del database SQLite e operazioni CRUD

## 🆘 RISOLUZIONE PROBLEMI

### Moduli Interfaccia Grafica

### Il programma non si avvia- `gui_case.py`: Interfaccia gestione case vacanza

1. Verifica che Python sia installato- `gui_collaboratori.py`: Interfaccia gestione collaboratori

2. Esegui `AVVIA_VERSIONE_GRAFICA.bat` come Amministratore- `gui_movimenti.py`: Interfaccia gestione movimenti chiavi



### Errore "openpyxl non trovato"### File di Supporto

L'importazione Excel non funzionerà. Installa con:- `test_demo.py`: Script per popolare il database con dati di esempio

```- `avvia_interfaccia_grafica.bat`: Launcher per versione grafica

pip install openpyxl- `avvia_gestione_chiavi.bat`: Launcher per versione console

```- `gestione_chiavi.db`: Database SQLite (creato automaticamente al primo avvio)



### I dati sono scomparsi## Note

1. Vai nella cartella `backups/`

2. Trova l'ultimo backup `auto_backup_YYYYMMDD_HHMMSS.db`- Il database viene creato automaticamente al primo avvio

3. Avvia il programma → Home → "Load" → Seleziona il backup- Le date vengono registrate automaticamente se non specificate

- È possibile inserire date personalizzate nel formato: YYYY-MM-DD HH:MM

---

## 📝 NOTE TECNICHE

- **Database**: SQLite3 (gestione_chiavi.db)
- **Framework GUI**: Tkinter (integrato in Python)
- **Requisiti**: Python 3.6+
- **Librerie opzionali**: openpyxl (per importazione Excel)

---

## 📌 VERSIONE

Versione 2.0 - Novembre 2025

Sviluppato per la gestione professionale delle chiavi di case vacanza.
