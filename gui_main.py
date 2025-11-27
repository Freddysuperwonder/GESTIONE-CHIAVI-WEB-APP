import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from database import GestioneChiaviDB
from gui_case import FrameGestioneCase
from gui_collaboratori import FrameGestioneCollaboratori
from gui_movimenti import FrameGestioneMovimenti

class ApplicazioneGestioneChiavi:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestione Chiavi Case Vacanza")
        self.root.geometry("1200x800")
        
        # Database
        self.db = GestioneChiaviDB()
        
        # Configurazione stile
        self.configura_stile()
        
        # Crea l'interfaccia
        self.crea_intestazione()
        self.crea_menu_laterale()
        self.crea_area_principale()
        
        # Mostra la prima sezione
        self.mostra_home()
        
        # Configura salvataggio automatico alla chiusura
        self.root.protocol("WM_DELETE_WINDOW", self.chiudi_applicazione)
    
    def configura_stile(self):
        """Configura lo stile dell'applicazione"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colori
        self.colore_primario = "#2c3e50"
        self.colore_secondario = "#3498db"
        self.colore_successo = "#27ae60"
        self.colore_pericolo = "#e74c3c"
        self.colore_sfondo = "#ecf0f1"
        
        # Stile pulsanti
        style.configure("Menu.TButton",
                       font=('Segoe UI', 11),
                       padding=15,
                       background=self.colore_primario,
                       foreground="white")
        
        style.configure("Primary.TButton",
                       font=('Segoe UI', 10),
                       padding=10,
                       background=self.colore_secondario)
        
        style.configure("Success.TButton",
                       font=('Segoe UI', 10),
                       padding=10,
                       background=self.colore_successo)
        
        style.configure("Danger.TButton",
                       font=('Segoe UI', 10),
                       padding=10,
                       background=self.colore_pericolo)
        
        # Stile Treeview
        style.configure("Treeview",
                       font=('Segoe UI', 9),
                       rowheight=25)
        style.configure("Treeview.Heading",
                       font=('Segoe UI', 10, 'bold'))
    
    def crea_intestazione(self):
        """Crea l'intestazione dell'applicazione"""
        frame_intestazione = tk.Frame(self.root, bg=self.colore_primario, height=80)
        frame_intestazione.pack(fill=tk.X, side=tk.TOP)
        frame_intestazione.pack_propagate(False)
        
        # Titolo
        tk.Label(frame_intestazione,
                text="🔑 GESTIONE CHIAVI CASE VACANZA",
                font=('Segoe UI', 20, 'bold'),
                bg=self.colore_primario,
                fg="white").pack(pady=20)
    
    def crea_menu_laterale(self):
        """Crea il menu laterale di navigazione"""
        self.frame_menu = tk.Frame(self.root, bg=self.colore_primario, width=250)
        self.frame_menu.pack(fill=tk.Y, side=tk.LEFT)
        self.frame_menu.pack_propagate(False)
        
        # Pulsanti menu
        pulsanti = [
            ("🏠 Home", self.mostra_home),
            ("🏘️ Case Vacanza", self.mostra_case),
            ("👥 Collaboratori", self.mostra_collaboratori),
            ("🔑 Movimenti Chiavi", self.mostra_movimenti),
            ("❌ Esci", self.esci)
        ]
        
        for testo, comando in pulsanti:
            btn = tk.Button(self.frame_menu,
                          text=testo,
                          command=comando,
                          font=('Segoe UI', 12),
                          bg=self.colore_primario,
                          fg="white",
                          activebackground=self.colore_secondario,
                          activeforeground="white",
                          bd=0,
                          cursor="hand2",
                          anchor="w",
                          padx=20,
                          pady=15)
            btn.pack(fill=tk.X, pady=2)
            
            # Effetto hover
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=self.colore_secondario))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=self.colore_primario))
    
    def crea_area_principale(self):
        """Crea l'area principale dove verranno mostrate le sezioni"""
        self.area_principale = tk.Frame(self.root, bg=self.colore_sfondo)
        self.area_principale.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)
    
    def pulisci_area_principale(self):
        """Rimuove tutti i widget dall'area principale"""
        for widget in self.area_principale.winfo_children():
            widget.destroy()
    
    def mostra_home(self):
        """Mostra la schermata home con il riepilogo"""
        self.pulisci_area_principale()
        
        # Container principale
        container = tk.Frame(self.area_principale, bg=self.colore_sfondo)
        container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Titolo
        tk.Label(container,
                text="Dashboard",
                font=('Segoe UI', 24, 'bold'),
                bg=self.colore_sfondo,
                fg=self.colore_primario).pack(anchor="w", pady=(0, 20))
        
        # Frame pulsanti backup (NUOVO)
        frame_backup = tk.Frame(container, bg=self.colore_sfondo)
        frame_backup.pack(fill=tk.X, pady=(0, 20))
        
        tk.Button(frame_backup,
                 text="💾 Save (Salva Backup)",
                 command=self.salva_backup,
                 font=('Segoe UI', 10, 'bold'),
                 bg="#27ae60",
                 fg="white",
                 cursor="hand2",
                 padx=20,
                 pady=10).pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame_backup,
                 text="📂 Load (Carica Backup)",
                 command=self.carica_backup,
                 font=('Segoe UI', 10, 'bold'),
                 bg="#3498db",
                 fg="white",
                 cursor="hand2",
                 padx=20,
                 pady=10).pack(side=tk.LEFT, padx=5)
        
        tk.Label(frame_backup,
                text="💡 Il backup viene salvato automaticamente alla chiusura del programma",
                font=('Segoe UI', 9, 'italic'),
                bg=self.colore_sfondo,
                fg="#7f8c8d").pack(side=tk.LEFT, padx=15)
        
        # Frame per le statistiche
        frame_stats = tk.Frame(container, bg=self.colore_sfondo)
        frame_stats.pack(fill=tk.X, pady=10)
        
        # Ottieni statistiche
        num_case = len(self.db.visualizza_case())
        num_collaboratori = len(self.db.visualizza_collaboratori())
        num_chiavi_consegnate = len(self.db.visualizza_chiavi_consegnate())
        
        # Cards statistiche
        self.crea_card_statistica(frame_stats, "🏘️ Case Vacanza", str(num_case), "#3498db", 0)
        self.crea_card_statistica(frame_stats, "👥 Collaboratori", str(num_collaboratori), "#9b59b6", 1)
        self.crea_card_statistica(frame_stats, "🔑 Chiavi Consegnate", str(num_chiavi_consegnate), "#e74c3c", 2)
        
        # Separatore
        ttk.Separator(container, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=30)
        
        # Chiavi attualmente consegnate
        tk.Label(container,
                text="Chiavi Attualmente Consegnate",
                font=('Segoe UI', 16, 'bold'),
                bg=self.colore_sfondo,
                fg=self.colore_primario).pack(anchor="w", pady=(0, 10))
        
        # Frame per la tabella
        frame_tabella = tk.Frame(container, bg="white", relief=tk.RIDGE, bd=2)
        frame_tabella.pack(fill=tk.BOTH, expand=True)
        
        # Tabella chiavi consegnate
        colonne = ("id", "casa", "collaboratore", "data_consegna")
        tree = ttk.Treeview(frame_tabella, columns=colonne, show="headings", height=10)
        
        tree.heading("id", text="ID")
        tree.heading("casa", text="Casa")
        tree.heading("collaboratore", text="Collaboratore")
        tree.heading("data_consegna", text="Data Consegna")
        
        tree.column("id", width=50, anchor="center")
        tree.column("casa", width=250)
        tree.column("collaboratore", width=200)
        tree.column("data_consegna", width=150, anchor="center")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabella, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)
        
        # Popola la tabella
        chiavi = self.db.visualizza_chiavi_consegnate()
        for chiave in chiavi:
            tree.insert("", tk.END, values=(
                chiave['id'],
                chiave['nome_casa'],
                chiave['collaboratore'],
                chiave['data_consegna']
            ))
        
        if not chiavi:
            tree.insert("", tk.END, values=("", "Nessuna chiave consegnata", "", ""))
    
    def crea_card_statistica(self, parent, titolo, valore, colore, colonna):
        """Crea una card per visualizzare una statistica"""
        card = tk.Frame(parent, bg=colore, relief=tk.RAISED, bd=2)
        card.grid(row=0, column=colonna, padx=10, sticky="ew")
        parent.grid_columnconfigure(colonna, weight=1)
        
        tk.Label(card,
                text=titolo,
                font=('Segoe UI', 12),
                bg=colore,
                fg="white").pack(pady=(20, 5))
        
        tk.Label(card,
                text=valore,
                font=('Segoe UI', 36, 'bold'),
                bg=colore,
                fg="white").pack(pady=(5, 20))
    
    def mostra_case(self):
        """Mostra la sezione gestione case"""
        self.pulisci_area_principale()
        frame = FrameGestioneCase(self.area_principale, self.db, self.colore_sfondo, self.colore_primario)
        frame.pack(fill=tk.BOTH, expand=True)
    
    def mostra_collaboratori(self):
        """Mostra la sezione gestione collaboratori"""
        self.pulisci_area_principale()
        frame = FrameGestioneCollaboratori(self.area_principale, self.db, self.colore_sfondo, self.colore_primario)
        frame.pack(fill=tk.BOTH, expand=True)
    
    def mostra_movimenti(self):
        """Mostra la sezione gestione movimenti"""
        self.pulisci_area_principale()
        frame = FrameGestioneMovimenti(self.area_principale, self.db, self.colore_sfondo, self.colore_primario)
        frame.pack(fill=tk.BOTH, expand=True)
    
    def esci(self):
        """Chiude l'applicazione"""
        if messagebox.askokcancel("Esci", "Vuoi davvero uscire dall'applicazione?"):
            self.chiudi_applicazione()
    
    def chiudi_applicazione(self):
        """Gestisce la chiusura dell'applicazione con backup automatico"""
        # Salva backup automatico
        successo, messaggio = self.db.salva_backup_automatico()
        
        if successo:
            print(f"✅ Backup automatico salvato: {messaggio}")
        else:
            print(f"⚠️ Errore backup automatico: {messaggio}")
        
        self.root.quit()
    
    def salva_backup(self):
        """Salva manualmente un backup del database"""
        file_path = filedialog.asksaveasfilename(
            title="Salva Backup Database",
            defaultextension=".db",
            filetypes=[("Database SQLite", "*.db"), ("Tutti i file", "*.*")],
            initialfile=f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        )
        
        if file_path:
            successo, messaggio = self.db.salva_backup(file_path)
            
            if successo:
                messagebox.showinfo("Backup Salvato", messaggio)
            else:
                messagebox.showerror("Errore Backup", messaggio)
    
    def carica_backup(self):
        """Carica un backup del database"""
        if not messagebox.askyesno("Conferma Caricamento",
                                   "ATTENZIONE: Caricare un backup sovrascriverà tutti i dati attuali!\n\n"
                                   "Un backup del database corrente verrà creato automaticamente.\n\n"
                                   "Vuoi continuare?"):
            return
        
        file_path = filedialog.askopenfilename(
            title="Seleziona Backup da Caricare",
            filetypes=[("Database SQLite", "*.db"), ("Tutti i file", "*.*")]
        )
        
        if file_path:
            successo, messaggio = self.db.carica_backup(file_path)
            
            if successo:
                messagebox.showinfo("Backup Caricato", messaggio + "\n\nAggiorna la pagina per vedere i dati ripristinati.")
                self.mostra_home()  # Ricarica la home per aggiornare i dati
            else:
                messagebox.showerror("Errore Caricamento", messaggio)

def main():
    root = tk.Tk()
    app = ApplicazioneGestioneChiavi(root)
    root.mainloop()

if __name__ == "__main__":
    main()
