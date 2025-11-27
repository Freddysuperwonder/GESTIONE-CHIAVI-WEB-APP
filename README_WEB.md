# 🔑 GESTIONE CHIAVI CASE VACANZA - WEB APP

Applicazione web per la gestione della consegna e restituzione delle chiavi di case vacanza.

## 🚀 Come Avviare l'Applicazione Web

### Prima Installazione

1. **Installa le dipendenze**:
   ```bash
   pip install -r requirements.txt
   ```

### Avvio Applicazione

**Metodo 1 - Doppio Click (Windows)**:
- Doppio click su `AVVIA_WEB_APP.bat`

**Metodo 2 - Da Terminale**:
```bash
python app.py
```

### Accesso

Una volta avviato il server, apri il browser e vai a:
```
http://localhost:5000
```

L'applicazione sarà accessibile da:
- Il tuo computer: `http://localhost:5000`
- Altri dispositivi nella stessa rete: `http://TUO_IP:5000`

Per trovare il tuo IP locale:
```bash
ipconfig
```
Cerca "Indirizzo IPv4"

## 📱 Funzionalità

### Dashboard
- Visualizzazione statistiche (case, collaboratori, chiavi consegnate)
- Riepilogo chiavi attualmente consegnate
- Backup manuale del database

### Gestione Case
- ➕ Aggiungi nuove case
- ✏️ Modifica case esistenti
- 🗑️ Elimina case
- 📋 Visualizza movimenti per casa
- Impostazione numero chiavi disponibili
- Tracciamento chiavi disponibili/affidate in tempo reale

### Gestione Collaboratori
- ➕ Aggiungi nuovi collaboratori
- ✏️ Modifica collaboratori
- 🗑️ Elimina collaboratori
- 📋 Visualizza movimenti per collaboratore

### Gestione Movimenti
- ➕ Registra consegna chiavi
- ✅ Registra restituzione chiavi
- 📊 Visualizza chiavi attualmente consegnate
- 📜 Storico completo movimenti
- Blocco automatico se chiavi non disponibili

## 🌐 Deployment su Server

### Opzione 1: PythonAnywhere (Gratuito)
1. Crea account su [pythonanywhere.com](https://www.pythonanywhere.com)
2. Carica i file del progetto
3. Configura una Web App Flask
4. Imposta `app.py` come file principale

### Opzione 2: Heroku
1. Installa Heroku CLI
2. Aggiungi file `Procfile`:
   ```
   web: python app.py
   ```
3. Deploy:
   ```bash
   heroku create nome-app
   git push heroku main
   ```

### Opzione 3: Server Locale (Rete Locale)
1. Avvia `app.py`
2. Apri porta 5000 nel firewall
3. Condividi l'IP locale con gli altri utenti

## 🔒 Sicurezza

⚠️ **IMPORTANTE**: Questa versione è per uso in rete locale o demo.

Per uso in produzione su Internet:
- Aggiungi autenticazione utenti
- Usa HTTPS
- Configura CORS appropriatamente
- Modifica la `SECRET_KEY` in `app.py`

## 📂 Struttura File

```
GESTIONE CHIAVI WEB APP/
├── app.py                  # Applicazione Flask principale
├── database.py             # Gestione database SQLite
├── requirements.txt        # Dipendenze Python
├── AVVIA_WEB_APP.bat      # Launcher Windows
├── templates/              # Template HTML
│   ├── base.html          # Layout base
│   ├── index.html         # Dashboard
│   ├── case.html          # Gestione case
│   ├── collaboratori.html # Gestione collaboratori
│   └── movimenti.html     # Gestione movimenti
├── backups/               # Backup automatici database
└── gestione_chiavi.db     # Database SQLite
```

## 🛠️ Tecnologie Utilizzate

- **Backend**: Flask (Python)
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Design**: Responsive, Mobile-friendly

## ❓ Risoluzione Problemi

### Errore "Porta 5000 già in uso"
Modifica la porta in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8080)
```

### Errore "Flask non trovato"
Installa le dipendenze:
```bash
pip install -r requirements.txt
```

### Il database non si aggiorna
1. Ricarica la pagina (F5)
2. Svuota la cache del browser (CTRL+F5)
3. Verifica che non ci siano errori nella console del browser (F12)

## 📝 Note

- Il database viene creato automaticamente al primo avvio
- I backup automatici vengono salvati in `backups/`
- Tutti i dati sono memorizzati localmente in `gestione_chiavi.db`

## 🆕 Novità rispetto alla Versione Desktop

✅ Accessibile da qualsiasi dispositivo con browser
✅ Utilizzo simultaneo da più utenti (stesso database)
✅ Interfaccia responsive (smartphone, tablet, PC)
✅ Nessuna installazione necessaria sui client
✅ Aggiornamenti centralizzati

---

**Versione**: 3.0 Web
**Data**: Novembre 2025
