import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class FrameGestioneMovimenti(tk.Frame):
    def __init__(self, parent, db, colore_sfondo, colore_primario):
        super().__init__(parent, bg=colore_sfondo)
        self.db = db
        self.colore_sfondo = colore_sfondo
        self.colore_primario = colore_primario
        
        self.crea_interfaccia()
    
    def crea_interfaccia(self):
        """Crea l'interfaccia per la gestione dei movimenti"""
        # Container principale
        container = tk.Frame(self, bg=self.colore_sfondo)
        container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Titolo
        tk.Label(container,
                text="Gestione Movimenti Chiavi",
                font=('Segoe UI', 24, 'bold'),
                bg=self.colore_sfondo,
                fg=self.colore_primario).pack(anchor="w", pady=(0, 20))
        
        # Frame principale con due colonne
        frame_principale = tk.Frame(container, bg=self.colore_sfondo)
        frame_principale.pack(fill=tk.BOTH, expand=True)
        
        # Colonna sinistra - Consegna
        frame_sinistra = tk.Frame(frame_principale, bg=self.colore_sfondo)
        frame_sinistra.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Colonna destra - Restituzione
        frame_destra = tk.Frame(frame_principale, bg=self.colore_sfondo)
        frame_destra.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # ==================== CONSEGNA ====================
        frame_consegna = tk.LabelFrame(frame_sinistra,
                                       text="Registra Consegna Chiave",
                                       font=('Segoe UI', 12, 'bold'),
                                       bg="white",
                                       fg=self.colore_primario,
                                       padx=20,
                                       pady=20)
        frame_consegna.pack(fill=tk.BOTH, expand=True)
        
        # Casa
        tk.Label(frame_consegna, text="Casa:", font=('Segoe UI', 10), bg="white").grid(row=0, column=0, sticky="w", pady=10)
        self.combo_casa = ttk.Combobox(frame_consegna, font=('Segoe UI', 10), width=30, state="readonly")
        self.combo_casa.grid(row=0, column=1, pady=10, padx=10)
        self.combo_casa.bind('<<ComboboxSelected>>', self.aggiorna_info_chiavi)
        
        # Info chiavi disponibili
        self.label_chiavi_disponibili = tk.Label(frame_consegna, 
                                                  text="", 
                                                  font=('Segoe UI', 9, 'bold'), 
                                                  bg="white", 
                                                  fg="#27ae60")
        self.label_chiavi_disponibili.grid(row=0, column=2, pady=10, padx=10)
        
        # Collaboratore
        tk.Label(frame_consegna, text="Collaboratore:", font=('Segoe UI', 10), bg="white").grid(row=1, column=0, sticky="w", pady=10)
        self.combo_collaboratore = ttk.Combobox(frame_consegna, font=('Segoe UI', 10), width=30, state="readonly")
        self.combo_collaboratore.grid(row=1, column=1, pady=10, padx=10)
        
        # Note
        tk.Label(frame_consegna, text="Note:", font=('Segoe UI', 10), bg="white").grid(row=2, column=0, sticky="w", pady=10)
        self.entry_note_consegna = tk.Entry(frame_consegna, font=('Segoe UI', 10), width=32)
        self.entry_note_consegna.grid(row=2, column=1, pady=10, padx=10)
        
        # Pulsante registra consegna
        tk.Button(frame_consegna,
                 text="🔑 Registra Consegna",
                 command=self.registra_consegna,
                 font=('Segoe UI', 11, 'bold'),
                 bg="#27ae60",
                 fg="white",
                 cursor="hand2",
                 padx=20,
                 pady=15).grid(row=3, column=0, columnspan=2, pady=20)
        
        # ==================== RESTITUZIONE ====================
        frame_restituzione = tk.LabelFrame(frame_destra,
                                          text="Registra Restituzione Chiave",
                                          font=('Segoe UI', 12, 'bold'),
                                          bg="white",
                                          fg=self.colore_primario,
                                          padx=20,
                                          pady=20)
        frame_restituzione.pack(fill=tk.BOTH, expand=True)
        
        # Informazioni
        tk.Label(frame_restituzione,
                text="Seleziona la consegna da chiudere dalla lista sottostante",
                font=('Segoe UI', 9, 'italic'),
                bg="white",
                fg="#7f8c8d").pack(pady=10)
        
        # Pulsante registra restituzione
        tk.Button(frame_restituzione,
                 text="✅ Registra Restituzione",
                 command=self.registra_restituzione,
                 font=('Segoe UI', 11, 'bold'),
                 bg="#3498db",
                 fg="white",
                 cursor="hand2",
                 padx=20,
                 pady=15).pack(pady=20)
        
        # ==================== TABELLA CHIAVI CONSEGNATE ====================
        frame_tabella = tk.LabelFrame(container,
                                      text="Chiavi Attualmente Consegnate",
                                      font=('Segoe UI', 12, 'bold'),
                                      bg="white",
                                      fg=self.colore_primario,
                                      padx=10,
                                      pady=10)
        frame_tabella.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        # Tabella
        colonne = ("id", "casa", "collaboratore", "data_consegna", "note")
        self.tree = ttk.Treeview(frame_tabella, columns=colonne, show="headings", height=8)
        
        self.tree.heading("id", text="ID")
        self.tree.heading("casa", text="Casa")
        self.tree.heading("collaboratore", text="Collaboratore")
        self.tree.heading("data_consegna", text="Data Consegna")
        self.tree.heading("note", text="Note")
        
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("casa", width=250)
        self.tree.column("collaboratore", width=200)
        self.tree.column("data_consegna", width=150, anchor="center")
        self.tree.column("note", width=200)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabella, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Frame pulsanti azioni
        frame_azioni = tk.Frame(frame_tabella, bg="white")
        frame_azioni.pack(fill=tk.X, pady=(10, 0))
        
        tk.Button(frame_azioni,
                 text="🔄 Aggiorna Elenco",
                 command=self.carica_dati,
                 font=('Segoe UI', 9),
                 bg="#3498db",
                 fg="white",
                 cursor="hand2",
                 padx=15,
                 pady=8).pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame_azioni,
                 text="📋 Visualizza Storico Completo",
                 command=self.mostra_storico,
                 font=('Segoe UI', 9),
                 bg="#9b59b6",
                 fg="white",
                 cursor="hand2",
                 padx=15,
                 pady=8).pack(side=tk.LEFT, padx=5)
        
        # Carica i dati iniziali
        self.carica_dati()
    
    def carica_dati(self):
        """Carica case, collaboratori e chiavi consegnate"""
        # Carica case
        case = self.db.visualizza_case()
        self.case_dict = {f"{c['id']} - {c['nome_casa']}": c['id'] for c in case}
        self.case_info = {c['id']: c for c in case}  # Salva info complete
        self.combo_casa['values'] = list(self.case_dict.keys())
        if self.case_dict:
            self.combo_casa.current(0)
            self.aggiorna_info_chiavi(None)
        
        # Carica collaboratori
        collaboratori = self.db.visualizza_collaboratori()
        self.collaboratori_dict = {f"{c['id']} - {c['nome']} {c['cognome']}": c['id'] for c in collaboratori}
        self.combo_collaboratore['values'] = list(self.collaboratori_dict.keys())
        if self.collaboratori_dict:
            self.combo_collaboratore.current(0)
        
        # Carica chiavi consegnate
        self.carica_chiavi_consegnate()
    
    def aggiorna_info_chiavi(self, event):
        """Aggiorna le informazioni sulle chiavi disponibili"""
        casa_selezionata = self.combo_casa.get()
        if casa_selezionata:
            casa_id = self.case_dict[casa_selezionata]
            info = self.case_info.get(casa_id)
            if info:
                disponibili = info['chiavi_disponibili']
                totale = info['totale_chiavi']
                
                if disponibili > 0:
                    self.label_chiavi_disponibili.config(
                        text=f"✓ {disponibili}/{totale} disponibili",
                        fg="#27ae60"
                    )
                else:
                    self.label_chiavi_disponibili.config(
                        text=f"✗ 0/{totale} disponibili",
                        fg="#e74c3c"
                    )
    
    def carica_chiavi_consegnate(self):
        """Carica le chiavi attualmente consegnate nella tabella"""
        # Pulisci la tabella
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Carica i dati
        chiavi = self.db.visualizza_chiavi_consegnate()
        for chiave in chiavi:
            self.tree.insert("", tk.END, values=(
                chiave['id'],
                chiave['nome_casa'],
                chiave['collaboratore'],
                chiave['data_consegna'],
                chiave['note'] or "-"
            ))
    
    def registra_consegna(self):
        """Registra una nuova consegna di chiave"""
        if not self.case_dict or not self.collaboratori_dict:
            messagebox.showerror("Errore", "Aggiungi prima almeno una casa e un collaboratore!")
            return
        
        casa_selezionata = self.combo_casa.get()
        collaboratore_selezionato = self.combo_collaboratore.get()
        note = self.entry_note_consegna.get().strip()
        
        id_casa = self.case_dict[casa_selezionata]
        id_collaboratore = self.collaboratori_dict[collaboratore_selezionato]
        
        successo, messaggio = self.db.registra_consegna(id_casa, id_collaboratore, None, note)
        
        if successo:
            messagebox.showinfo("Successo", messaggio)
            self.entry_note_consegna.delete(0, tk.END)
            self.carica_dati()  # Ricarica tutto per aggiornare contatore chiavi
        else:
            messagebox.showerror("Errore", messaggio)
    
    def registra_restituzione(self):
        """Registra la restituzione di una chiave"""
        selezione = self.tree.selection()
        if not selezione:
            messagebox.showwarning("Attenzione", "Seleziona una consegna da chiudere!")
            return
        
        item = self.tree.item(selezione[0])
        movimento_id = item['values'][0]
        casa = item['values'][1]
        collaboratore = item['values'][2]
        
        if messagebox.askyesno("Conferma Restituzione",
                              f"Registrare la restituzione della chiave?\n\nCasa: {casa}\nCollaboratore: {collaboratore}"):
            successo, messaggio = self.db.registra_restituzione(movimento_id)
            
            if successo:
                messagebox.showinfo("Successo", messaggio)
                self.carica_dati()  # Ricarica tutto per aggiornare contatore chiavi
            else:
                messagebox.showerror("Errore", messaggio)
    
    def mostra_storico(self):
        """Mostra lo storico completo dei movimenti in una nuova finestra"""
        # Crea una nuova finestra
        finestra_storico = tk.Toplevel(self)
        finestra_storico.title("Storico Movimenti Chiavi")
        finestra_storico.geometry("1000x600")
        
        # Titolo
        tk.Label(finestra_storico,
                text="Storico Completo Movimenti",
                font=('Segoe UI', 16, 'bold'),
                bg=self.colore_sfondo,
                fg=self.colore_primario).pack(pady=20)
        
        # Frame per la tabella
        frame = tk.Frame(finestra_storico, bg="white", padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Tabella
        colonne = ("id", "casa", "collaboratore", "data_consegna", "data_restituzione", "stato")
        tree = ttk.Treeview(frame, columns=colonne, show="headings", height=20)
        
        tree.heading("id", text="ID")
        tree.heading("casa", text="Casa")
        tree.heading("collaboratore", text="Collaboratore")
        tree.heading("data_consegna", text="Data Consegna")
        tree.heading("data_restituzione", text="Data Restituzione")
        tree.heading("stato", text="Stato")
        
        tree.column("id", width=50, anchor="center")
        tree.column("casa", width=200)
        tree.column("collaboratore", width=200)
        tree.column("data_consegna", width=150, anchor="center")
        tree.column("data_restituzione", width=150, anchor="center")
        tree.column("stato", width=100, anchor="center")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)
        
        # Carica i dati
        movimenti = self.db.visualizza_storico_movimenti(100)
        for mov in movimenti:
            stato = "CONSEGNATA" if not mov['data_restituzione'] else "RESTITUITA"
            tree.insert("", tk.END, values=(
                mov['id'],
                mov['nome_casa'],
                mov['collaboratore'],
                mov['data_consegna'],
                mov['data_restituzione'] or "-",
                stato
            ))
        
        # Pulsante chiudi
        tk.Button(finestra_storico,
                 text="Chiudi",
                 command=finestra_storico.destroy,
                 font=('Segoe UI', 10),
                 bg="#95a5a6",
                 fg="white",
                 cursor="hand2",
                 padx=30,
                 pady=10).pack(pady=20)
