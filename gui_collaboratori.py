import tkinter as tk
from tkinter import ttk, messagebox

class FrameGestioneCollaboratori(tk.Frame):
    def __init__(self, parent, db, colore_sfondo, colore_primario):
        super().__init__(parent, bg=colore_sfondo)
        self.db = db
        self.colore_sfondo = colore_sfondo
        self.colore_primario = colore_primario
        
        self.crea_interfaccia()
    
    def crea_interfaccia(self):
        """Crea l'interfaccia per la gestione dei collaboratori"""
        # Container principale
        container = tk.Frame(self, bg=self.colore_sfondo)
        container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Titolo
        tk.Label(container,
                text="Gestione Collaboratori",
                font=('Segoe UI', 24, 'bold'),
                bg=self.colore_sfondo,
                fg=self.colore_primario).pack(anchor="w", pady=(0, 15))
        
        # Frame pulsanti azioni (SPOSTATO IN ALTO)
        frame_azioni = tk.Frame(container, bg=self.colore_sfondo)
        frame_azioni.pack(fill=tk.X, pady=(0, 20))
        
        tk.Button(frame_azioni,
                 text="🔄 Aggiorna Elenco",
                 command=self.carica_collaboratori,
                 font=('Segoe UI', 9),
                 bg="#3498db",
                 fg="white",
                 cursor="hand2",
                 padx=15,
                 pady=8).pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame_azioni,
                 text="✏️ Modifica Collaboratore Selezionato",
                 command=self.prepara_modifica_collaboratore,
                 font=('Segoe UI', 9),
                 bg="#f39c12",
                 fg="white",
                 cursor="hand2",
                 padx=15,
                 pady=8).pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame_azioni,
                 text="🗑️ Elimina Collaboratore Selezionato",
                 command=self.elimina_collaboratore,
                 font=('Segoe UI', 9),
                 bg="#e74c3c",
                 fg="white",
                 cursor="hand2",
                 padx=15,
                 pady=8).pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame_azioni,
                 text="🔍 Mostra Chiavi in Affidamento",
                 command=self.mostra_chiavi_collaboratore,
                 font=('Segoe UI', 9),
                 bg="#9b59b6",
                 fg="white",
                 cursor="hand2",
                 padx=15,
                 pady=8).pack(side=tk.LEFT, padx=5)
        
        # Frame per il form
        frame_form = tk.LabelFrame(container,
                                   text="Aggiungi/Modifica Collaboratore",
                                   font=('Segoe UI', 12, 'bold'),
                                   bg="white",
                                   fg=self.colore_primario,
                                   padx=20,
                                   pady=20)
        frame_form.pack(fill=tk.X, pady=(0, 20))
        
        # ID collaboratore (nascosto, usato per modifiche)
        self.collaboratore_id_modifica = None
        
        # Campi del form - Prima riga
        tk.Label(frame_form, text="Nome:", font=('Segoe UI', 10), bg="white").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_nome = tk.Entry(frame_form, font=('Segoe UI', 10), width=25)
        self.entry_nome.grid(row=0, column=1, pady=5, padx=10)
        
        tk.Label(frame_form, text="Cognome:", font=('Segoe UI', 10), bg="white").grid(row=0, column=2, sticky="w", pady=5, padx=(20, 0))
        self.entry_cognome = tk.Entry(frame_form, font=('Segoe UI', 10), width=25)
        self.entry_cognome.grid(row=0, column=3, pady=5, padx=10)
        
        # Campi del form - Seconda riga
        tk.Label(frame_form, text="Telefono:", font=('Segoe UI', 10), bg="white").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_telefono = tk.Entry(frame_form, font=('Segoe UI', 10), width=25)
        self.entry_telefono.grid(row=1, column=1, pady=5, padx=10)
        
        tk.Label(frame_form, text="Email:", font=('Segoe UI', 10), bg="white").grid(row=1, column=2, sticky="w", pady=5, padx=(20, 0))
        self.entry_email = tk.Entry(frame_form, font=('Segoe UI', 10), width=25)
        self.entry_email.grid(row=1, column=3, pady=5, padx=10)
        
        # Frame per i pulsanti
        frame_buttons = tk.Frame(frame_form, bg="white")
        frame_buttons.grid(row=2, column=3, pady=15, sticky="e")
        
        # Pulsante aggiungi/salva
        self.btn_salva = tk.Button(frame_buttons,
                 text="➕ Aggiungi Collaboratore",
                 command=self.salva_collaboratore,
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
                                      text="Elenco Collaboratori",
                                      font=('Segoe UI', 12, 'bold'),
                                      bg="white",
                                      fg=self.colore_primario,
                                      padx=10,
                                      pady=10)
        frame_tabella.pack(fill=tk.BOTH, expand=True)
        
        # Tabella
        colonne = ("id", "cognome", "nome", "telefono", "email")
        self.tree = ttk.Treeview(frame_tabella, columns=colonne, show="headings", height=5)
        
        self.tree.heading("id", text="ID")
        self.tree.heading("cognome", text="Cognome")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("telefono", text="Telefono")
        self.tree.heading("email", text="Email")
        
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("cognome", width=200)
        self.tree.column("nome", width=200)
        self.tree.column("telefono", width=150)
        self.tree.column("email", width=250)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabella, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Carica i dati iniziali
        self.carica_collaboratori()
    
    def carica_collaboratori(self):
        """Carica i collaboratori nella tabella"""
        # Pulisci la tabella
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Carica i dati
        collaboratori = self.db.visualizza_collaboratori()
        for collab in collaboratori:
            self.tree.insert("", tk.END, values=(
                collab['id'],
                collab['cognome'],
                collab['nome'],
                collab['telefono'] or "-",
                collab['email'] or "-"
            ))
    
    def salva_collaboratore(self):
        """Aggiunge o modifica un collaboratore"""
        nome = self.entry_nome.get().strip()
        cognome = self.entry_cognome.get().strip()
        telefono = self.entry_telefono.get().strip()
        email = self.entry_email.get().strip()
        
        if not nome or not cognome:
            messagebox.showerror("Errore", "Nome e cognome sono obbligatori!")
            return
        
        if self.collaboratore_id_modifica:
            # Modifica
            successo, messaggio = self.db.modifica_collaboratore(
                self.collaboratore_id_modifica, nome, cognome, telefono, email
            )
        else:
            # Aggiunta
            successo, messaggio = self.db.aggiungi_collaboratore(nome, cognome, telefono, email)
        
        if successo:
            messagebox.showinfo("Successo", messaggio)
            self.pulisci_form()
            self.carica_collaboratori()
        else:
            messagebox.showerror("Errore", messaggio)
    
    def prepara_modifica_collaboratore(self):
        """Prepara il form per modificare il collaboratore selezionato"""
        selezione = self.tree.selection()
        if not selezione:
            messagebox.showwarning("Attenzione", "Seleziona un collaboratore da modificare!")
            return
        
        item = self.tree.item(selezione[0])
        self.collaboratore_id_modifica = item['values'][0]
        
        # Popola i campi del form
        self.entry_cognome.delete(0, tk.END)
        self.entry_cognome.insert(0, item['values'][1])
        
        self.entry_nome.delete(0, tk.END)
        self.entry_nome.insert(0, item['values'][2])
        
        self.entry_telefono.delete(0, tk.END)
        telefono = item['values'][3]
        if telefono != "-":
            self.entry_telefono.insert(0, telefono)
        
        self.entry_email.delete(0, tk.END)
        email = item['values'][4]
        if email != "-":
            self.entry_email.insert(0, email)
        
        # Cambia il pulsante in "Salva Modifiche"
        self.btn_salva.config(text="💾 Salva Modifiche", bg="#f39c12")
        self.btn_annulla.pack(side=tk.LEFT, padx=5)
    
    def annulla_modifica(self):
        """Annulla la modifica e pulisce il form"""
        self.pulisci_form()
    
    def pulisci_form(self):
        """Pulisce il form e resetta lo stato"""
        self.collaboratore_id_modifica = None
        self.entry_nome.delete(0, tk.END)
        self.entry_cognome.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.btn_salva.config(text="➕ Aggiungi Collaboratore", bg="#27ae60")
        self.btn_annulla.pack_forget()
    
    def aggiungi_collaboratore(self):
        """Metodo deprecato - ora usa salva_collaboratore"""
        self.salva_collaboratore()
    
    def elimina_collaboratore(self):
        """Elimina il collaboratore selezionato"""
        selezione = self.tree.selection()
        if not selezione:
            messagebox.showwarning("Attenzione", "Seleziona un collaboratore da eliminare!")
            return
        
        item = self.tree.item(selezione[0])
        collaboratore_id = item['values'][0]
        nome_completo = f"{item['values'][2]} {item['values'][1]}"
        
        if messagebox.askyesno("Conferma Eliminazione",
                              f"Sei sicuro di voler eliminare il collaboratore '{nome_completo}'?"):
            successo, messaggio = self.db.elimina_collaboratore(collaboratore_id)
            
            if successo:
                messagebox.showinfo("Successo", messaggio)
                self.carica_collaboratori()
            else:
                messagebox.showerror("Errore", messaggio)
    
    def mostra_chiavi_collaboratore(self):
        """Mostra finestra di ricerca per visualizzare chiavi in affidamento a collaboratore"""
        # Crea finestra di ricerca
        finestra_ricerca = tk.Toplevel(self.master)
        finestra_ricerca.title("Ricerca Chiavi per Collaboratore")
        finestra_ricerca.geometry("600x500")
        finestra_ricerca.transient(self.master)
        finestra_ricerca.grab_set()
        
        # Titolo
        tk.Label(finestra_ricerca,
                text="🔍 Ricerca Chiavi per Collaboratore",
                font=('Segoe UI', 18, 'bold'),
                bg="#9b59b6",
                fg="white",
                pady=15).pack(fill=tk.X)
        
        # Frame contenuto
        frame_contenuto = tk.Frame(finestra_ricerca, bg="white", padx=20, pady=20)
        frame_contenuto.pack(fill=tk.BOTH, expand=True)
        
        # Frame ricerca
        frame_ricerca = tk.LabelFrame(frame_contenuto,
                                      text="Seleziona Collaboratore",
                                      font=('Segoe UI', 11, 'bold'),
                                      bg="white",
                                      fg="#2c3e50",
                                      padx=15,
                                      pady=15)
        frame_ricerca.pack(fill=tk.X, pady=(0, 20))
        
        # Campo ricerca testuale
        tk.Label(frame_ricerca,
                text="Cerca per nome/cognome:",
                font=('Segoe UI', 10),
                bg="white").grid(row=0, column=0, sticky="w", pady=5)
        
        entry_ricerca = tk.Entry(frame_ricerca, font=('Segoe UI', 10), width=40)
        entry_ricerca.grid(row=0, column=1, pady=5, padx=10, sticky="ew")
        
        # Combobox collaboratori
        tk.Label(frame_ricerca,
                text="Oppure seleziona:",
                font=('Segoe UI', 10),
                bg="white").grid(row=1, column=0, sticky="w", pady=5)
        
        collaboratori = self.db.visualizza_collaboratori()
        collab_dict = {f"{c['cognome']} {c['nome']}": c['id'] for c in collaboratori}
        collab_nomi = sorted(collab_dict.keys())
        
        combo_collab = ttk.Combobox(frame_ricerca,
                                    values=collab_nomi,
                                    font=('Segoe UI', 10),
                                    width=37,
                                    state="readonly")
        combo_collab.grid(row=1, column=1, pady=5, padx=10, sticky="ew")
        
        if collab_nomi:
            combo_collab.current(0)
        
        frame_ricerca.grid_columnconfigure(1, weight=1)
        
        # Funzione per filtrare combobox in base alla ricerca
        def filtra_collaboratori(*args):
            testo = entry_ricerca.get().lower()
            if testo:
                filtrati = [nome for nome in collab_nomi if testo in nome.lower()]
                combo_collab['values'] = filtrati
                if filtrati:
                    combo_collab.current(0)
            else:
                combo_collab['values'] = collab_nomi
                if collab_nomi:
                    combo_collab.current(0)
        
        entry_ricerca.bind('<KeyRelease>', filtra_collaboratori)
        entry_ricerca.bind('<Return>', lambda e: cerca_chiavi())
        combo_collab.bind('<<ComboboxSelected>>', lambda e: None)
        
        # Funzione per aggiornare combo quando cambia il filtro
        def aggiorna_combo_e_cerca(event=None):
            filtra_collaboratori()
            # Se c'è solo un risultato, cerca automaticamente
            if len(combo_collab['values']) == 1:
                combo_collab.current(0)
        
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
        colonne = ("casa", "data_consegna", "note")
        tree_risultati = ttk.Treeview(frame_risultati, columns=colonne, show="headings", height=8)
        
        tree_risultati.heading("casa", text="Casa")
        tree_risultati.heading("data_consegna", text="Data Consegna")
        tree_risultati.heading("note", text="Note")
        
        tree_risultati.column("casa", width=200)
        tree_risultati.column("data_consegna", width=150)
        tree_risultati.column("note", width=200)
        
        scrollbar = ttk.Scrollbar(frame_risultati, orient=tk.VERTICAL, command=tree_risultati.yview)
        tree_risultati.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree_risultati.pack(fill=tk.BOTH, expand=True)
        
        # Label info
        label_info = tk.Label(frame_risultati,
                             text="Seleziona un collaboratore e clicca 'Cerca'",
                             font=('Segoe UI', 9, 'italic'),
                             bg="white",
                             fg="#7f8c8d")
        label_info.pack(pady=5)
        
        # Funzione cerca
        def cerca_chiavi():
            # Pulisci tabella
            for item in tree_risultati.get_children():
                tree_risultati.delete(item)
            
            collab_selezionato = combo_collab.get()
            if not collab_selezionato:
                label_info.config(text="⚠️ Seleziona un collaboratore", fg="#e74c3c")
                return
            
            collab_id = collab_dict[collab_selezionato]
            
            # Cerca movimenti
            movimenti = self.db.cerca_movimenti_per_collaboratore(collab_id)
            chiavi_attive = [m for m in movimenti if m['data_restituzione'] is None]
            
            if not chiavi_attive:
                label_info.config(
                    text=f"ℹ️ Nessuna chiave in affidamento a '{collab_selezionato}'",
                    fg="#f39c12"
                )
                return
            
            # Popola tabella
            for movimento in chiavi_attive:
                tree_risultati.insert("", tk.END, values=(
                    movimento['nome_casa'],
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
