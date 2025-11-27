import sqlite3
from datetime import datetime
import os
import shutil

class GestioneChiaviDB:
    def __init__(self, db_name="gestione_chiavi.db"):
        self.db_name = db_name
        self.connessione = None
        self.crea_database()
    
    def connetti(self):
        """Crea connessione al database"""
        self.connessione = sqlite3.connect(self.db_name)
        self.connessione.row_factory = sqlite3.Row
        return self.connessione
    
    def disconnetti(self):
        """Chiude la connessione al database"""
        if self.connessione:
            self.connessione.close()
    
    def crea_database(self):
        """Crea le tabelle del database se non esistono"""
        conn = self.connetti()
        cursor = conn.cursor()
        
        # Tabella Case
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS case_vacanza (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_casa TEXT NOT NULL UNIQUE,
                indirizzo TEXT,
                note TEXT,
                numero_chiavi INTEGER DEFAULT 1,
                data_creazione TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Aggiungi colonna numero_chiavi se non esiste (per database esistenti)
        try:
            cursor.execute('ALTER TABLE case_vacanza ADD COLUMN numero_chiavi INTEGER DEFAULT 1')
        except sqlite3.OperationalError:
            pass  # La colonna esiste già
        
        # Tabella Collaboratori
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS collaboratori (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cognome TEXT NOT NULL,
                telefono TEXT,
                email TEXT,
                data_creazione TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(nome, cognome)
            )
        ''')
        
        # Tabella Movimenti Chiavi
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS movimenti_chiavi (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_casa INTEGER NOT NULL,
                id_collaboratore INTEGER NOT NULL,
                data_consegna TIMESTAMP NOT NULL,
                data_restituzione TIMESTAMP,
                note TEXT,
                FOREIGN KEY (id_casa) REFERENCES case_vacanza(id),
                FOREIGN KEY (id_collaboratore) REFERENCES collaboratori(id)
            )
        ''')
        
        conn.commit()
        self.disconnetti()
    
    # ==================== GESTIONE CASE ====================
    
    def aggiungi_casa(self, nome_casa, indirizzo="", note="", numero_chiavi=1):
        """Aggiunge una nuova casa al database"""
        try:
            conn = self.connetti()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO case_vacanza (nome_casa, indirizzo, note, numero_chiavi)
                VALUES (?, ?, ?, ?)
            ''', (nome_casa, indirizzo, note, numero_chiavi))
            conn.commit()
            casa_id = cursor.lastrowid
            self.disconnetti()
            return True, f"Casa '{nome_casa}' aggiunta con successo!"
        except sqlite3.IntegrityError:
            self.disconnetti()
            return False, f"Errore: Casa '{nome_casa}' già esistente!"
        except Exception as e:
            self.disconnetti()
            return False, f"Errore: {str(e)}"
    
    def visualizza_case(self):
        """Restituisce tutte le case con il numero di chiavi disponibili"""
        conn = self.connetti()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 
                c.id,
                c.nome_casa,
                c.indirizzo,
                c.note,
                c.data_creazione,
                COALESCE(c.numero_chiavi, 1) as totale_chiavi,
                COALESCE((
                    SELECT COUNT(*) 
                    FROM movimenti_chiavi m 
                    WHERE m.id_casa = c.id AND m.data_restituzione IS NULL
                ), 0) as chiavi_affidate,
                COALESCE(c.numero_chiavi, 1) - COALESCE((
                    SELECT COUNT(*) 
                    FROM movimenti_chiavi m 
                    WHERE m.id_casa = c.id AND m.data_restituzione IS NULL
                ), 0) as chiavi_disponibili
            FROM case_vacanza c
            ORDER BY c.nome_casa
        ''')
        case = cursor.fetchall()
        self.disconnetti()
        return case
    
    def get_chiavi_disponibili(self, casa_id):
        """Restituisce il numero di chiavi disponibili per una casa"""
        conn = self.connetti()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 
                COALESCE(numero_chiavi, 1) as totale_chiavi
            FROM case_vacanza
            WHERE id = ?
        ''', (casa_id,))
        casa = cursor.fetchone()
        
        if not casa:
            self.disconnetti()
            return 0
        
        cursor.execute('''
            SELECT COUNT(*) as affidate
            FROM movimenti_chiavi
            WHERE id_casa = ? AND data_restituzione IS NULL
        ''', (casa_id,))
        
        movimenti = cursor.fetchone()
        self.disconnetti()
        
        totale = casa['totale_chiavi']
        affidate = movimenti['affidate'] if movimenti else 0
        
        return totale - affidate
    
    def modifica_casa(self, casa_id, nome_casa, indirizzo="", note="", numero_chiavi=1):
        """Modifica i dati di una casa esistente"""
        try:
            conn = self.connetti()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE case_vacanza 
                SET nome_casa = ?, indirizzo = ?, note = ?, numero_chiavi = ?
                WHERE id = ?
            ''', (nome_casa, indirizzo, note, numero_chiavi, casa_id))
            conn.commit()
            righe = cursor.rowcount
            self.disconnetti()
            if righe > 0:
                return True, f"Casa '{nome_casa}' modificata con successo!"
            else:
                return False, "Casa non trovata!"
        except sqlite3.IntegrityError:
            self.disconnetti()
            return False, f"Errore: Una casa con il nome '{nome_casa}' esiste già!"
        except Exception as e:
            self.disconnetti()
            return False, f"Errore: {str(e)}"
    
    def elimina_casa(self, casa_id):
        """Elimina una casa dal database"""
        try:
            conn = self.connetti()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM case_vacanza WHERE id = ?', (casa_id,))
            conn.commit()
            righe = cursor.rowcount
            self.disconnetti()
            if righe > 0:
                return True, "Casa eliminata con successo!"
            else:
                return False, "Casa non trovata!"
        except Exception as e:
            self.disconnetti()
            return False, f"Errore: {str(e)}"
    
    def importa_case_da_excel(self, file_path):
        """Importa case da file Excel (Nome, Indirizzo, Numero Chiavi)"""
        try:
            import openpyxl
        except ImportError:
            return False, "Errore: Libreria 'openpyxl' non installata. Esegui: pip install openpyxl"
        
        try:
            workbook = openpyxl.load_workbook(file_path)
            sheet = workbook.active
            
            importate = 0
            errori = []
            
            # Salta la prima riga se contiene intestazioni
            righe = list(sheet.iter_rows(min_row=2, values_only=True))
            
            for idx, riga in enumerate(righe, start=2):
                if not riga or not riga[0]:  # Salta righe vuote
                    continue
                
                nome_casa = str(riga[0]).strip() if riga[0] else ""
                indirizzo = str(riga[1]).strip() if len(riga) > 1 and riga[1] else ""
                
                try:
                    numero_chiavi = int(riga[2]) if len(riga) > 2 and riga[2] else 1
                    if numero_chiavi < 1:
                        numero_chiavi = 1
                except (ValueError, TypeError):
                    numero_chiavi = 1
                
                if nome_casa:
                    successo, messaggio = self.aggiungi_casa(nome_casa, indirizzo, "", numero_chiavi)
                    if successo:
                        importate += 1
                    else:
                        errori.append(f"Riga {idx}: {messaggio}")
            
            workbook.close()
            
            if importate > 0:
                msg = f"Importate {importate} case con successo!"
                if errori:
                    msg += f"\n\nErrori ({len(errori)}):\n" + "\n".join(errori[:5])
                    if len(errori) > 5:
                        msg += f"\n... e altri {len(errori)-5} errori"
                return True, msg
            else:
                return False, "Nessuna casa importata.\n" + "\n".join(errori[:5])
                
        except Exception as e:
            return False, f"Errore durante l'importazione: {str(e)}"
    
    # ==================== GESTIONE COLLABORATORI ====================
    
    def aggiungi_collaboratore(self, nome, cognome, telefono="", email=""):
        """Aggiunge un nuovo collaboratore al database"""
        try:
            conn = self.connetti()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO collaboratori (nome, cognome, telefono, email)
                VALUES (?, ?, ?, ?)
            ''', (nome, cognome, telefono, email))
            conn.commit()
            collaboratore_id = cursor.lastrowid
            self.disconnetti()
            return True, f"Collaboratore '{nome} {cognome}' aggiunto con successo!"
        except sqlite3.IntegrityError:
            self.disconnetti()
            return False, f"Errore: Collaboratore '{nome} {cognome}' già esistente!"
        except Exception as e:
            self.disconnetti()
            return False, f"Errore: {str(e)}"
    
    def visualizza_collaboratori(self):
        """Restituisce tutti i collaboratori"""
        conn = self.connetti()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM collaboratori ORDER BY cognome, nome')
        collaboratori = cursor.fetchall()
        self.disconnetti()
        return collaboratori
    
    def modifica_collaboratore(self, collaboratore_id, nome, cognome, telefono="", email=""):
        """Modifica i dati di un collaboratore esistente"""
        try:
            conn = self.connetti()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE collaboratori 
                SET nome = ?, cognome = ?, telefono = ?, email = ?
                WHERE id = ?
            ''', (nome, cognome, telefono, email, collaboratore_id))
            conn.commit()
            righe = cursor.rowcount
            self.disconnetti()
            if righe > 0:
                return True, f"Collaboratore '{nome} {cognome}' modificato con successo!"
            else:
                return False, "Collaboratore non trovato!"
        except sqlite3.IntegrityError:
            self.disconnetti()
            return False, f"Errore: Un collaboratore '{nome} {cognome}' esiste già!"
        except Exception as e:
            self.disconnetti()
            return False, f"Errore: {str(e)}"
    
    def elimina_collaboratore(self, collaboratore_id):
        """Elimina un collaboratore dal database"""
        try:
            conn = self.connetti()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM collaboratori WHERE id = ?', (collaboratore_id,))
            conn.commit()
            righe = cursor.rowcount
            self.disconnetti()
            if righe > 0:
                return True, "Collaboratore eliminato con successo!"
            else:
                return False, "Collaboratore non trovato!"
        except Exception as e:
            self.disconnetti()
            return False, f"Errore: {str(e)}"
    
    # ==================== GESTIONE MOVIMENTI CHIAVI ====================
    
    def registra_consegna(self, id_casa, id_collaboratore, data_consegna=None, note=""):
        """Registra la consegna di una chiave"""
        if data_consegna is None:
            data_consegna = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Verifica se ci sono chiavi disponibili
        chiavi_disp = self.get_chiavi_disponibili(id_casa)
        if chiavi_disp <= 0:
            return False, "Errore: Non ci sono chiavi disponibili per questa casa!"
        
        try:
            conn = self.connetti()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO movimenti_chiavi (id_casa, id_collaboratore, data_consegna, note)
                VALUES (?, ?, ?, ?)
            ''', (id_casa, id_collaboratore, data_consegna, note))
            conn.commit()
            movimento_id = cursor.lastrowid
            self.disconnetti()
            return True, f"Consegna registrata con successo! ID: {movimento_id}"
        except Exception as e:
            self.disconnetti()
            return False, f"Errore: {str(e)}"
    
    def registra_restituzione(self, movimento_id, data_restituzione=None):
        """Registra la restituzione di una chiave"""
        if data_restituzione is None:
            data_restituzione = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            conn = self.connetti()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE movimenti_chiavi 
                SET data_restituzione = ?
                WHERE id = ? AND data_restituzione IS NULL
            ''', (data_restituzione, movimento_id))
            conn.commit()
            righe = cursor.rowcount
            self.disconnetti()
            if righe > 0:
                return True, "Restituzione registrata con successo!"
            else:
                return False, "Movimento non trovato o chiave già restituita!"
        except Exception as e:
            self.disconnetti()
            return False, f"Errore: {str(e)}"
    
    def visualizza_chiavi_consegnate(self):
        """Visualizza tutte le chiavi attualmente consegnate (non ancora restituite)"""
        conn = self.connetti()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 
                m.id,
                c.nome_casa,
                col.nome || ' ' || col.cognome as collaboratore,
                m.data_consegna,
                m.note
            FROM movimenti_chiavi m
            JOIN case_vacanza c ON m.id_casa = c.id
            JOIN collaboratori col ON m.id_collaboratore = col.id
            WHERE m.data_restituzione IS NULL
            ORDER BY m.data_consegna DESC
        ''')
        movimenti = cursor.fetchall()
        self.disconnetti()
        return movimenti
    
    def visualizza_storico_movimenti(self, limite=50):
        """Visualizza lo storico di tutti i movimenti"""
        conn = self.connetti()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 
                m.id,
                c.nome_casa,
                col.nome || ' ' || col.cognome as collaboratore,
                m.data_consegna,
                m.data_restituzione,
                m.note
            FROM movimenti_chiavi m
            JOIN case_vacanza c ON m.id_casa = c.id
            JOIN collaboratori col ON m.id_collaboratore = col.id
            ORDER BY m.data_consegna DESC
            LIMIT ?
        ''', (limite,))
        movimenti = cursor.fetchall()
        self.disconnetti()
        return movimenti
    
    def cerca_movimenti_per_casa(self, id_casa):
        """Cerca tutti i movimenti per una specifica casa"""
        conn = self.connetti()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 
                m.id,
                c.nome_casa,
                col.nome || ' ' || col.cognome as collaboratore,
                m.data_consegna,
                m.data_restituzione,
                m.note
            FROM movimenti_chiavi m
            JOIN case_vacanza c ON m.id_casa = c.id
            JOIN collaboratori col ON m.id_collaboratore = col.id
            WHERE m.id_casa = ?
            ORDER BY m.data_consegna DESC
        ''', (id_casa,))
        movimenti = cursor.fetchall()
        self.disconnetti()
        return movimenti
    
    def cerca_movimenti_per_collaboratore(self, id_collaboratore):
        """Cerca tutti i movimenti per uno specifico collaboratore"""
        conn = self.connetti()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 
                m.id,
                c.nome_casa,
                col.nome || ' ' || col.cognome as collaboratore,
                m.data_consegna,
                m.data_restituzione,
                m.note
            FROM movimenti_chiavi m
            JOIN case_vacanza c ON m.id_casa = c.id
            JOIN collaboratori col ON m.id_collaboratore = col.id
            WHERE m.id_collaboratore = ?
            ORDER BY m.data_consegna DESC
        ''', (id_collaboratore,))
        movimenti = cursor.fetchall()
        self.disconnetti()
        return movimenti
    
    # ==================== BACKUP E RIPRISTINO ====================
    
    def salva_backup(self, percorso_backup=None):
        """Salva un backup del database"""
        try:
            if percorso_backup is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                percorso_backup = f"backup_gestione_chiavi_{timestamp}.db"
            
            # Chiudi eventuali connessioni
            if self.connessione:
                self.disconnetti()
            
            # Copia il file del database
            shutil.copy2(self.db_name, percorso_backup)
            
            return True, f"Backup salvato in: {percorso_backup}"
        except Exception as e:
            return False, f"Errore durante il backup: {str(e)}"
    
    def carica_backup(self, percorso_backup):
        """Carica un backup del database"""
        try:
            if not os.path.exists(percorso_backup):
                return False, "File di backup non trovato!"
            
            # Chiudi eventuali connessioni
            if self.connessione:
                self.disconnetti()
            
            # Crea backup del database corrente prima di sovrascriverlo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_corrente = f"backup_pre_restore_{timestamp}.db"
            shutil.copy2(self.db_name, backup_corrente)
            
            # Ripristina il backup
            shutil.copy2(percorso_backup, self.db_name)
            
            return True, f"Backup ripristinato! Database corrente salvato in: {backup_corrente}"
        except Exception as e:
            return False, f"Errore durante il ripristino: {str(e)}"
    
    def salva_backup_automatico(self):
        """Salva un backup automatico nella cartella backups"""
        try:
            # Crea cartella backups se non esiste
            if not os.path.exists("backups"):
                os.makedirs("backups")
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            percorso = os.path.join("backups", f"auto_backup_{timestamp}.db")
            
            # Chiudi eventuali connessioni
            if self.connessione:
                self.disconnetti()
            
            shutil.copy2(self.db_name, percorso)
            
            # Mantieni solo gli ultimi 10 backup
            self.pulisci_vecchi_backup()
            
            return True, percorso
        except Exception as e:
            return False, str(e)
    
    def pulisci_vecchi_backup(self, max_backup=10):
        """Mantiene solo gli ultimi N backup automatici"""
        try:
            if not os.path.exists("backups"):
                return
            
            backups = [f for f in os.listdir("backups") if f.startswith("auto_backup_") and f.endswith(".db")]
            backups.sort(reverse=True)
            
            # Elimina i backup più vecchi
            for backup in backups[max_backup:]:
                os.remove(os.path.join("backups", backup))
        except Exception:
            pass  # Ignora errori nella pulizia
