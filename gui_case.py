import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class FrameGestioneCase(tk.Frame):
    def __init__(self, parent, db, colore_sfondo, colore_primario):
        super().__init__(parent, bg=colore_sfondo)
        self.db = db
        self.colore_sfondo = colore_sfondo
        self.colore_primario = colore_primario
        
        self.crea_interfaccia()
    
    def crea_interfaccia(self):
        """Crea l'interfaccia per la gestione delle case"""
        # Container principale
        container = tk.Frame(self, bg=self.colore_sfondo)
        container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Titolo
        tk.Label(container,
                text="Gestione Case Vacanza",
                font=('Segoe UI', 24, 'bold'),
                bg=self.colore_sfondo,
                fg=self.colore_primario).pack(anchor="w", pady=(0, 15))
        
        # Frame pulsanti azioni (SPOSTATO IN ALTO)
        frame_azioni = tk.Frame(container, bg=self.colore_sfondo)
        frame_azioni.pack(fill=tk.X, pady=(0, 20))
        
        tk.Button(frame_azioni,
                 text="🔄 Aggiorna Elenco",
                 command=self.carica_case,
                 font=('Segoe UI', 9),
                 bg="#3498db",
                 fg="white",
                 cursor="hand2",
                 padx=15,
                 pady=8).pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame_azioni,
                 text="✏️ Modifica Casa Selezionata",
                 command=self.prepara_modifica_casa,
                 font=('Segoe UI', 9),
                 bg="#f39c12",
                 fg="white",
                 cursor="hand2",
                 padx=15,
                 pady=8).pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame_azioni,
                 text="🗑️ Elimina Casa Selezionata",
                 command=self.elimina_casa,
                 font=('Segoe UI', 9),
                 bg="#e74c3c",
                 fg="white",
                 cursor="hand2",
                 padx=15,
                 pady=8).pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame_azioni,
                 text="🔍 Mostra Chiavi in Affidamento",
                 command=self.mostra_chiavi_casa,
                 font=('Segoe UI', 9),
                 bg="#9b59b6",
                 fg="white",
                 cursor="hand2",
                 padx=15,
                 pady=8).pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame_azioni,
                 text="📥 Importa da Excel",
                 command=self.importa_da_excel,
                 font=('Segoe UI', 9),
                 bg="#16a085",
                 fg="white",
                 cursor="hand2",
                 padx=15,
                 pady=8).pack(side=tk.LEFT, padx=5)
        
        # Frame per il form
        frame_form = tk.LabelFrame(container,
                                   text="Aggiungi/Modifica Casa",
                                   font=('Segoe UI', 12, 'bold'),
                                   bg="white",
                                   fg=self.colore_primario,
                                   padx=20,
                                   pady=20)
        frame_form.pack(fill=tk.X, pady=(0, 20))
        
        # ID casa (nascosto, usato per modifiche)
        self.casa_id_modifica = None
        
        # Campi del form
        tk.Label(frame_form, text="Nome Casa:", font=('Segoe UI', 10), bg="white").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_nome = tk.Entry(frame_form, font=('Segoe UI', 10), width=40)
        self.entry_nome.grid(row=0, column=1, pady=5, padx=10)
        
        tk.Label(frame_form, text="Indirizzo:", font=('Segoe UI', 10), bg="white").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_indirizzo = tk.Entry(frame_form, font=('Segoe UI', 10), width=40)
        self.entry_indirizzo.grid(row=1, column=1, pady=5, padx=10)
        
        tk.Label(frame_form, text="Note:", font=('Segoe UI', 10), bg="white").grid(row=2, column=0, sticky="w", pady=5)
        self.entry_note = tk.Entry(frame_form, font=('Segoe UI', 10), width=40)
        self.entry_note.grid(row=2, column=1, pady=5, padx=10)
        
        tk.Label(frame_form, text="Numero Chiavi:", font=('Segoe UI', 10), bg="white").grid(row=3, column=0, sticky="w", pady=5)
        self.entry_numero_chiavi = tk.Entry(frame_form, font=('Segoe UI', 10), width=10)
        self.entry_numero_chiavi.insert(0, "1")
        self.entry_numero_chiavi.grid(row=3, column=1, pady=5, padx=10, sticky="w")
        
        # Frame per i pulsanti
        frame_buttons = tk.Frame(frame_form, bg="white")
        frame_buttons.grid(row=4, column=1, pady=15, sticky="e")
        
        # Pulsante aggiungi/salva
        self.btn_salva = tk.Button(frame_buttons,
                 text="➕ Aggiungi Casa",
                 command=self.salva_casa,
                 font=('Segoe UI', 10, 'bold'),
                 bg="#27ae60",
                 fg="white",
                 cursor="hand2",
                 padx=20,
                 pady=10)
        self.btn_salva.pack(side=tk.LEFT, padx=5)
        
        # Pulsante annulla modifica (inizialmente nascosto)
        self.btn_annulla = tk.Button(frame_buttons,
                 text="✖ Annulla",
                 command=self.annulla_modifica,
                 font=('Segoe UI', 10, 'bold'),
                 bg="#95a5a6",
                 fg="white",
                 cursor="hand2",
                 padx=20,
                 pady=10)
        # Non mostrare il pulsante annulla inizialmente
        
        # Frame per la tabella
        frame_tabella = tk.LabelFrame(container,
                                      text="Elenco Case",
                                      font=('Segoe UI', 12, 'bold'),
                                      bg="white",
                                      fg=self.colore_primario,
                                      padx=10,
                                      pady=10)
        frame_tabella.pack(fill=tk.BOTH, expand=True)
        
        # Tabella
        colonne = ("id", "nome", "indirizzo", "note", "totale_chiavi", "affidate", "disponibili")
        self.tree = ttk.Treeview(frame_tabella, columns=colonne, show="headings", height=5)
        
        self.tree.heading("id", text="ID")
        self.tree.heading("nome", text="Nome Casa")
        self.tree.heading("indirizzo", text="Indirizzo")
        self.tree.heading("note", text="Note")
        self.tree.heading("totale_chiavi", text="Tot. Chiavi")
        self.tree.heading("affidate", text="Affidate")
        self.tree.heading("disponibili", text="Disponibili")
        
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("nome", width=200)
        self.tree.column("indirizzo", width=250)
        self.tree.column("note", width=200)
        self.tree.column("totale_chiavi", width=80, anchor="center")
        self.tree.column("affidate", width=80, anchor="center")
        self.tree.column("disponibili", width=90, anchor="center")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabella, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Carica i dati iniziali
        self.carica_case()
    
    def carica_case(self):
        """Carica le case nella tabella"""
        # Pulisci la tabella
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Carica i dati
        case = self.db.visualizza_case()
        for casa in case:
            # Colora la riga se non ci sono chiavi disponibili
            tag = 'disponibili' if casa['chiavi_disponibili'] > 0 else 'esaurite'
            self.tree.insert("", tk.END, values=(
                casa['id'],
                casa['nome_casa'],
                casa['indirizzo'] or "-",
                casa['note'] or "-",
                casa['totale_chiavi'],
                casa['chiavi_affidate'],
                casa['chiavi_disponibili']
            ), tags=(tag,))
        
        # Configura i colori
        self.tree.tag_configure('esaurite', background='#ffcccc')
        self.tree.tag_configure('disponibili', background='white')
    
    def salva_casa(self):
        """Aggiunge o modifica una casa"""
        nome = self.entry_nome.get().strip()
        indirizzo = self.entry_indirizzo.get().strip()
        note = self.entry_note.get().strip()
        
        try:
            numero_chiavi = int(self.entry_numero_chiavi.get().strip())
            if numero_chiavi < 1:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Errore", "Il numero di chiavi deve essere un numero positivo!")
            return
        
        if not nome:
            messagebox.showerror("Errore", "Il nome della casa è obbligatorio!")
            return
        
        if self.casa_id_modifica:
            # Modifica
            successo, messaggio = self.db.modifica_casa(self.casa_id_modifica, nome, indirizzo, note, numero_chiavi)
        else:
            # Aggiunta
            successo, messaggio = self.db.aggiungi_casa(nome, indirizzo, note, numero_chiavi)
        
        if successo:
            messagebox.showinfo("Successo", messaggio)
            self.pulisci_form()
            self.carica_case()
        else:
            messagebox.showerror("Errore", messaggio)
    
    def prepara_modifica_casa(self):
        """Prepara il form per modificare la casa selezionata"""
        selezione = self.tree.selection()
        if not selezione:
            messagebox.showwarning("Attenzione", "Seleziona una casa da modificare!")
            return
        
        item = self.tree.item(selezione[0])
        self.casa_id_modifica = item['values'][0]
        
        # Popola i campi del form
        self.entry_nome.delete(0, tk.END)
        self.entry_nome.insert(0, item['values'][1])
        
        self.entry_indirizzo.delete(0, tk.END)
        indirizzo = item['values'][2]
        if indirizzo != "-":
            self.entry_indirizzo.insert(0, indirizzo)
        
        self.entry_note.delete(0, tk.END)
        note = item['values'][3]
        if note != "-":
            self.entry_note.insert(0, note)
        
        self.entry_numero_chiavi.delete(0, tk.END)
        self.entry_numero_chiavi.insert(0, str(item['values'][4]))
        
        # Cambia il pulsante in "Salva Modifiche"
        self.btn_salva.config(text="💾 Salva Modifiche", bg="#f39c12")
        self.btn_annulla.pack(side=tk.LEFT, padx=5)
    
    def annulla_modifica(self):
        """Annulla la modifica e pulisce il form"""
        self.pulisci_form()
    
    def pulisci_form(self):
        """Pulisce il form e resetta lo stato"""
        self.casa_id_modifica = None
        self.entry_nome.delete(0, tk.END)
        self.entry_indirizzo.delete(0, tk.END)
        self.entry_note.delete(0, tk.END)
        self.entry_numero_chiavi.delete(0, tk.END)
        self.entry_numero_chiavi.insert(0, "1")
        self.btn_salva.config(text="➕ Aggiungi Casa", bg="#27ae60")
        self.btn_annulla.pack_forget()
    
    def aggiungi_casa(self):
        """Metodo deprecato - ora usa salva_casa"""
        self.salva_casa()
    
    def elimina_casa(self):
        """Elimina la casa selezionata"""
        selezione = self.tree.selection()
        if not selezione:
            messagebox.showwarning("Attenzione", "Seleziona una casa da eliminare!")
            return
        
        item = self.tree.item(selezione[0])
        casa_id = item['values'][0]
        nome_casa = item['values'][1]
        
        if messagebox.askyesno("Conferma Eliminazione",
                              f"Sei sicuro di voler eliminare la casa '{nome_casa}'?"):
            successo, messaggio = self.db.elimina_casa(casa_id)
            
            if successo:
                messagebox.showinfo("Successo", messaggio)
                self.carica_case()
            else:
                messagebox.showerror("Errore", messaggio)
    
    def mostra_chiavi_casa(self):
        """Mostra finestra di ricerca per visualizzare chiavi in affidamento"""
        # Crea finestra di ricerca
        finestra_ricerca = tk.Toplevel(self.master)
        finestra_ricerca.title("Ricerca Chiavi in Affidamento")
        finestra_ricerca.geometry("600x500")
        finestra_ricerca.transient(self.master)
        finestra_ricerca.grab_set()
        
        # Titolo
        tk.Label(finestra_ricerca,
                text="🔍 Ricerca Chiavi per Casa",
                font=('Segoe UI', 18, 'bold'),
                bg="#9b59b6",
                fg="white",
                pady=15).pack(fill=tk.X)
        
        # Frame contenuto
        frame_contenuto = tk.Frame(finestra_ricerca, bg="white", padx=20, pady=20)
        frame_contenuto.pack(fill=tk.BOTH, expand=True)
        
        # Frame ricerca
        frame_ricerca = tk.LabelFrame(frame_contenuto,
                                      text="Seleziona Casa",
                                      font=('Segoe UI', 11, 'bold'),
                                      bg="white",
                                      fg="#2c3e50",
                                      padx=15,
                                      pady=15)
        frame_ricerca.pack(fill=tk.X, pady=(0, 20))
        
        # Campo ricerca testuale
        tk.Label(frame_ricerca,
                text="Cerca per nome:",
                font=('Segoe UI', 10),
                bg="white").grid(row=0, column=0, sticky="w", pady=5)
        
        entry_ricerca = tk.Entry(frame_ricerca, font=('Segoe UI', 10), width=40)
        entry_ricerca.grid(row=0, column=1, pady=5, padx=10, sticky="ew")
        
        # Combobox case
        tk.Label(frame_ricerca,
                text="Oppure seleziona:",
                font=('Segoe UI', 10),
                bg="white").grid(row=1, column=0, sticky="w", pady=5)
        
        case = self.db.visualizza_case()
        case_dict = {f"{c['nome_casa']}": c['id'] for c in case}
        case_nomi = sorted(case_dict.keys())
        
        combo_case = ttk.Combobox(frame_ricerca,
                                  values=case_nomi,
                                  font=('Segoe UI', 10),
                                  width=37,
                                  state="readonly")
        combo_case.grid(row=1, column=1, pady=5, padx=10, sticky="ew")
        
        if case_nomi:
            combo_case.current(0)
        
        frame_ricerca.grid_columnconfigure(1, weight=1)
        
        # Funzione per filtrare combobox in base alla ricerca
        def filtra_case(*args):
            testo = entry_ricerca.get().lower()
            if testo:
                filtrate = [nome for nome in case_nomi if testo in nome.lower()]
                combo_case['values'] = filtrate
                if filtrate:
                    combo_case.current(0)
            else:
                combo_case['values'] = case_nomi
                if case_nomi:
                    combo_case.current(0)
        
        entry_ricerca.bind('<KeyRelease>', filtra_case)
        entry_ricerca.bind('<Return>', lambda e: cerca_chiavi())
        combo_case.bind('<<ComboboxSelected>>', lambda e: None)  # Permette selezione manuale
        
        # Funzione per aggiornare combo quando cambia il filtro
        def aggiorna_combo_e_cerca(event=None):
            filtra_case()
            # Se c'è solo un risultato, cerca automaticamente
            if len(combo_case['values']) == 1:
                combo_case.current(0)
        
        entry_ricerca.bind('<KeyRelease>', aggiorna_combo_e_cerca)
        
        # Frame risultati
        frame_risultati = tk.LabelFrame(frame_contenuto,
                                        text="Chiavi in Affidamento",
                                        font=('Segoe UI', 11, 'bold'),
                                        bg="white",
                                        fg="#2c3e50",
                                        padx=10,
                                        pady=10)
        frame_risultati.pack(fill=tk.BOTH, expand=True)
        
        # Tabella risultati
        colonne = ("collaboratore", "data_consegna", "note")
        tree_risultati = ttk.Treeview(frame_risultati, columns=colonne, show="headings", height=8)
        
        tree_risultati.heading("collaboratore", text="Collaboratore")
        tree_risultati.heading("data_consegna", text="Data Consegna")
        tree_risultati.heading("note", text="Note")
        
        tree_risultati.column("collaboratore", width=200)
        tree_risultati.column("data_consegna", width=150)
        tree_risultati.column("note", width=200)
        
        scrollbar = ttk.Scrollbar(frame_risultati, orient=tk.VERTICAL, command=tree_risultati.yview)
        tree_risultati.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree_risultati.pack(fill=tk.BOTH, expand=True)
        
        # Label info
        label_info = tk.Label(frame_risultati,
                             text="Seleziona una casa e clicca 'Cerca'",
                             font=('Segoe UI', 9, 'italic'),
                             bg="white",
                             fg="#7f8c8d")
        label_info.pack(pady=5)
        
        # Funzione cerca
        def cerca_chiavi():
            # Pulisci tabella
            for item in tree_risultati.get_children():
                tree_risultati.delete(item)
            
            casa_selezionata = combo_case.get()
            if not casa_selezionata:
                label_info.config(text="⚠️ Seleziona una casa", fg="#e74c3c")
                return
            
            casa_id = case_dict[casa_selezionata]
            
            # Cerca movimenti
            movimenti = self.db.cerca_movimenti_per_casa(casa_id)
            chiavi_attive = [m for m in movimenti if m['data_restituzione'] is None]
            
            if not chiavi_attive:
                label_info.config(
                    text=f"ℹ️ Nessuna chiave in affidamento per '{casa_selezionata}'",
                    fg="#f39c12"
                )
                return
            
            # Popola tabella
            for movimento in chiavi_attive:
                tree_risultati.insert("", tk.END, values=(
                    movimento['collaboratore'],
                    movimento['data_consegna'],
                    movimento['note'] or "-"
                ))
            
            label_info.config(
                text=f"✅ Trovate {len(chiavi_attive)} chiavi in affidamento",
                fg="#27ae60"
            )
        
        # Frame pulsanti
        frame_pulsanti = tk.Frame(frame_contenuto, bg="white")
        frame_pulsanti.pack(fill=tk.X, pady=(10, 0))
        
        btn_cerca = tk.Button(frame_pulsanti,
                 text="🔍 Cerca",
                 command=cerca_chiavi,
                 font=('Segoe UI', 10, 'bold'),
                 bg="#9b59b6",
                 fg="white",
                 cursor="hand2",
                 padx=30,
                 pady=10)
        btn_cerca.pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame_pulsanti,
                 text="Chiudi",
                 command=finestra_ricerca.destroy,
                 font=('Segoe UI', 10, 'bold'),
                 bg="#95a5a6",
                 fg="white",
                 cursor="hand2",
                 padx=30,
                 pady=10).pack(side=tk.LEFT, padx=5)
        
        # Info tasti rapidi
        tk.Label(frame_pulsanti,
                text="💡 Premi Invio per cercare",
                font=('Segoe UI', 8, 'italic'),
                bg="white",
                fg="#7f8c8d").pack(side=tk.LEFT, padx=15)
    
    def importa_da_excel(self):
        """Importa case da file Excel"""
        file_path = filedialog.askopenfilename(
            title="Seleziona file Excel",
            filetypes=[
                ("File Excel", "*.xlsx *.xls"),
                ("Tutti i file", "*.*")
            ]
        )
        
        if not file_path:
            return
        
        # Mostra finestra con istruzioni
        info_msg = (
            "Formato file Excel richiesto:\n\n"
            "Colonna A: Nome Casa (obbligatorio)\n"
            "Colonna B: Indirizzo (facoltativo)\n"
            "Colonna C: Numero Chiavi (facoltativo, default 1)\n\n"
            "La prima riga può contenere intestazioni e verrà saltata.\n\n"
            "Procedere con l'importazione?"
        )
        
        if not messagebox.askyesno("Importazione Excel", info_msg):
            return
        
        # Importa
        successo, messaggio = self.db.importa_case_da_excel(file_path)
        
        if successo:
            messagebox.showinfo("Importazione Completata", messaggio)
            self.carica_case()
        else:
            messagebox.showerror("Errore Importazione", messaggio)

