import os
from datetime import datetime
from database import GestioneChiaviDB

def pulisci_schermo():
    """Pulisce lo schermo del terminale"""
    os.system('cls' if os.name == 'nt' else 'clear')

def pausa():
    """Mette in pausa il programma"""
    input("\nPremi INVIO per continuare...")

def stampa_intestazione(titolo):
    """Stampa un'intestazione formattata"""
    pulisci_schermo()
    print("=" * 60)
    print(f" {titolo.center(58)} ")
    print("=" * 60)
    print()

# ==================== MENU CASE ====================

def menu_gestione_case(db):
    """Menu per la gestione delle case"""
    while True:
        stampa_intestazione("GESTIONE CASE VACANZA")
        print("1. Aggiungi nuova casa")
        print("2. Visualizza tutte le case")
        print("3. Elimina casa")
        print("4. Visualizza movimenti per casa")
        print("0. Torna al menu principale")
        print()
        
        scelta = input("Scegli un'opzione: ").strip()
        
        if scelta == "1":
            aggiungi_casa(db)
        elif scelta == "2":
            visualizza_case(db)
        elif scelta == "3":
            elimina_casa(db)
        elif scelta == "4":
            visualizza_movimenti_casa(db)
        elif scelta == "0":
            break
        else:
            print("\n❌ Opzione non valida!")
            pausa()

def aggiungi_casa(db):
    """Aggiunge una nuova casa"""
    stampa_intestazione("AGGIUNGI NUOVA CASA")
    
    nome_casa = input("Nome della casa: ").strip()
    if not nome_casa:
        print("\n❌ Il nome della casa è obbligatorio!")
        pausa()
        return
    
    indirizzo = input("Indirizzo (opzionale): ").strip()
    note = input("Note (opzionale): ").strip()
    
    successo, messaggio = db.aggiungi_casa(nome_casa, indirizzo, note)
    
    if successo:
        print(f"\n✅ {messaggio}")
    else:
        print(f"\n❌ {messaggio}")
    
    pausa()

def visualizza_case(db):
    """Visualizza tutte le case"""
    stampa_intestazione("ELENCO CASE VACANZA")
    
    case = db.visualizza_case()
    
    if not case:
        print("Nessuna casa registrata nel sistema.")
    else:
        print(f"{'ID':<5} {'Nome Casa':<30} {'Indirizzo':<25}")
        print("-" * 60)
        for casa in case:
            print(f"{casa['id']:<5} {casa['nome_casa']:<30} {casa['indirizzo'] or '-':<25}")
    
    pausa()

def elimina_casa(db):
    """Elimina una casa"""
    visualizza_case(db)
    print()
    
    try:
        casa_id = int(input("Inserisci l'ID della casa da eliminare (0 per annullare): ").strip())
        if casa_id == 0:
            return
        
        conferma = input(f"Sei sicuro di voler eliminare la casa ID {casa_id}? (s/n): ").strip().lower()
        if conferma == 's':
            successo, messaggio = db.elimina_casa(casa_id)
            if successo:
                print(f"\n✅ {messaggio}")
            else:
                print(f"\n❌ {messaggio}")
        else:
            print("\n⚠️ Operazione annullata.")
    except ValueError:
        print("\n❌ ID non valido!")
    
    pausa()

def visualizza_movimenti_casa(db):
    """Visualizza i movimenti per una casa specifica"""
    visualizza_case(db)
    print()
    
    try:
        casa_id = int(input("Inserisci l'ID della casa (0 per annullare): ").strip())
        if casa_id == 0:
            return
        
        stampa_intestazione("MOVIMENTI CHIAVI PER CASA")
        movimenti = db.cerca_movimenti_per_casa(casa_id)
        
        if not movimenti:
            print("Nessun movimento registrato per questa casa.")
        else:
            for mov in movimenti:
                print(f"\nID Movimento: {mov['id']}")
                print(f"Casa: {mov['nome_casa']}")
                print(f"Collaboratore: {mov['collaboratore']}")
                print(f"Data consegna: {mov['data_consegna']}")
                print(f"Data restituzione: {mov['data_restituzione'] or 'NON RESTITUITA'}")
                if mov['note']:
                    print(f"Note: {mov['note']}")
                print("-" * 60)
    except ValueError:
        print("\n❌ ID non valido!")
    
    pausa()

# ==================== MENU COLLABORATORI ====================

def menu_gestione_collaboratori(db):
    """Menu per la gestione dei collaboratori"""
    while True:
        stampa_intestazione("GESTIONE COLLABORATORI")
        print("1. Aggiungi nuovo collaboratore")
        print("2. Visualizza tutti i collaboratori")
        print("3. Elimina collaboratore")
        print("4. Visualizza movimenti per collaboratore")
        print("0. Torna al menu principale")
        print()
        
        scelta = input("Scegli un'opzione: ").strip()
        
        if scelta == "1":
            aggiungi_collaboratore(db)
        elif scelta == "2":
            visualizza_collaboratori(db)
        elif scelta == "3":
            elimina_collaboratore(db)
        elif scelta == "4":
            visualizza_movimenti_collaboratore(db)
        elif scelta == "0":
            break
        else:
            print("\n❌ Opzione non valida!")
            pausa()

def aggiungi_collaboratore(db):
    """Aggiunge un nuovo collaboratore"""
    stampa_intestazione("AGGIUNGI NUOVO COLLABORATORE")
    
    nome = input("Nome: ").strip()
    cognome = input("Cognome: ").strip()
    
    if not nome or not cognome:
        print("\n❌ Nome e cognome sono obbligatori!")
        pausa()
        return
    
    telefono = input("Telefono (opzionale): ").strip()
    email = input("Email (opzionale): ").strip()
    
    successo, messaggio = db.aggiungi_collaboratore(nome, cognome, telefono, email)
    
    if successo:
        print(f"\n✅ {messaggio}")
    else:
        print(f"\n❌ {messaggio}")
    
    pausa()

def visualizza_collaboratori(db):
    """Visualizza tutti i collaboratori"""
    stampa_intestazione("ELENCO COLLABORATORI")
    
    collaboratori = db.visualizza_collaboratori()
    
    if not collaboratori:
        print("Nessun collaboratore registrato nel sistema.")
    else:
        print(f"{'ID':<5} {'Cognome':<20} {'Nome':<20} {'Telefono':<15}")
        print("-" * 60)
        for collab in collaboratori:
            print(f"{collab['id']:<5} {collab['cognome']:<20} {collab['nome']:<20} {collab['telefono'] or '-':<15}")
    
    pausa()

def elimina_collaboratore(db):
    """Elimina un collaboratore"""
    visualizza_collaboratori(db)
    print()
    
    try:
        collaboratore_id = int(input("Inserisci l'ID del collaboratore da eliminare (0 per annullare): ").strip())
        if collaboratore_id == 0:
            return
        
        conferma = input(f"Sei sicuro di voler eliminare il collaboratore ID {collaboratore_id}? (s/n): ").strip().lower()
        if conferma == 's':
            successo, messaggio = db.elimina_collaboratore(collaboratore_id)
            if successo:
                print(f"\n✅ {messaggio}")
            else:
                print(f"\n❌ {messaggio}")
        else:
            print("\n⚠️ Operazione annullata.")
    except ValueError:
        print("\n❌ ID non valido!")
    
    pausa()

def visualizza_movimenti_collaboratore(db):
    """Visualizza i movimenti per un collaboratore specifico"""
    visualizza_collaboratori(db)
    print()
    
    try:
        collaboratore_id = int(input("Inserisci l'ID del collaboratore (0 per annullare): ").strip())
        if collaboratore_id == 0:
            return
        
        stampa_intestazione("MOVIMENTI CHIAVI PER COLLABORATORE")
        movimenti = db.cerca_movimenti_per_collaboratore(collaboratore_id)
        
        if not movimenti:
            print("Nessun movimento registrato per questo collaboratore.")
        else:
            for mov in movimenti:
                print(f"\nID Movimento: {mov['id']}")
                print(f"Casa: {mov['nome_casa']}")
                print(f"Collaboratore: {mov['collaboratore']}")
                print(f"Data consegna: {mov['data_consegna']}")
                print(f"Data restituzione: {mov['data_restituzione'] or 'NON RESTITUITA'}")
                if mov['note']:
                    print(f"Note: {mov['note']}")
                print("-" * 60)
    except ValueError:
        print("\n❌ ID non valido!")
    
    pausa()

# ==================== MENU MOVIMENTI ====================

def menu_gestione_movimenti(db):
    """Menu per la gestione dei movimenti chiavi"""
    while True:
        stampa_intestazione("GESTIONE MOVIMENTI CHIAVI")
        print("1. Registra consegna chiave")
        print("2. Registra restituzione chiave")
        print("3. Visualizza chiavi attualmente consegnate")
        print("4. Visualizza storico movimenti")
        print("0. Torna al menu principale")
        print()
        
        scelta = input("Scegli un'opzione: ").strip()
        
        if scelta == "1":
            registra_consegna(db)
        elif scelta == "2":
            registra_restituzione(db)
        elif scelta == "3":
            visualizza_chiavi_consegnate(db)
        elif scelta == "4":
            visualizza_storico(db)
        elif scelta == "0":
            break
        else:
            print("\n❌ Opzione non valida!")
            pausa()

def registra_consegna(db):
    """Registra la consegna di una chiave"""
    stampa_intestazione("REGISTRA CONSEGNA CHIAVE")
    
    # Mostra le case disponibili
    print("CASE DISPONIBILI:")
    case = db.visualizza_case()
    if not case:
        print("Nessuna casa registrata. Aggiungi prima una casa.")
        pausa()
        return
    
    for casa in case:
        print(f"  {casa['id']}. {casa['nome_casa']}")
    print()
    
    # Mostra i collaboratori disponibili
    print("COLLABORATORI DISPONIBILI:")
    collaboratori = db.visualizza_collaboratori()
    if not collaboratori:
        print("Nessun collaboratore registrato. Aggiungi prima un collaboratore.")
        pausa()
        return
    
    for collab in collaboratori:
        print(f"  {collab['id']}. {collab['nome']} {collab['cognome']}")
    print()
    
    try:
        id_casa = int(input("ID Casa: ").strip())
        id_collaboratore = int(input("ID Collaboratore: ").strip())
        
        # Data consegna (opzionale, default = adesso)
        data_input = input("Data consegna (YYYY-MM-DD HH:MM, lascia vuoto per adesso): ").strip()
        data_consegna = data_input if data_input else None
        
        note = input("Note (opzionale): ").strip()
        
        successo, messaggio = db.registra_consegna(id_casa, id_collaboratore, data_consegna, note)
        
        if successo:
            print(f"\n✅ {messaggio}")
        else:
            print(f"\n❌ {messaggio}")
    except ValueError:
        print("\n❌ Dati non validi!")
    
    pausa()

def registra_restituzione(db):
    """Registra la restituzione di una chiave"""
    stampa_intestazione("REGISTRA RESTITUZIONE CHIAVE")
    
    # Mostra le chiavi attualmente consegnate
    chiavi = db.visualizza_chiavi_consegnate()
    
    if not chiavi:
        print("Nessuna chiave attualmente consegnata.")
        pausa()
        return
    
    print("CHIAVI ATTUALMENTE CONSEGNATE:")
    print(f"{'ID':<5} {'Casa':<25} {'Collaboratore':<25} {'Data Consegna':<20}")
    print("-" * 75)
    for chiave in chiavi:
        print(f"{chiave['id']:<5} {chiave['nome_casa']:<25} {chiave['collaboratore']:<25} {chiave['data_consegna']:<20}")
    print()
    
    try:
        movimento_id = int(input("ID Movimento da chiudere (0 per annullare): ").strip())
        if movimento_id == 0:
            return
        
        # Data restituzione (opzionale, default = adesso)
        data_input = input("Data restituzione (YYYY-MM-DD HH:MM, lascia vuoto per adesso): ").strip()
        data_restituzione = data_input if data_input else None
        
        successo, messaggio = db.registra_restituzione(movimento_id, data_restituzione)
        
        if successo:
            print(f"\n✅ {messaggio}")
        else:
            print(f"\n❌ {messaggio}")
    except ValueError:
        print("\n❌ ID non valido!")
    
    pausa()

def visualizza_chiavi_consegnate(db):
    """Visualizza le chiavi attualmente consegnate"""
    stampa_intestazione("CHIAVI ATTUALMENTE CONSEGNATE")
    
    chiavi = db.visualizza_chiavi_consegnate()
    
    if not chiavi:
        print("Nessuna chiave attualmente consegnata.")
    else:
        for chiave in chiavi:
            print(f"\nID Movimento: {chiave['id']}")
            print(f"Casa: {chiave['nome_casa']}")
            print(f"Collaboratore: {chiave['collaboratore']}")
            print(f"Data consegna: {chiave['data_consegna']}")
            if chiave['note']:
                print(f"Note: {chiave['note']}")
            print("-" * 60)
    
    pausa()

def visualizza_storico(db):
    """Visualizza lo storico di tutti i movimenti"""
    stampa_intestazione("STORICO MOVIMENTI CHIAVI")
    
    try:
        limite = input("Numero di movimenti da visualizzare (default 50): ").strip()
        limite = int(limite) if limite else 50
    except ValueError:
        limite = 50
    
    movimenti = db.visualizza_storico_movimenti(limite)
    
    if not movimenti:
        print("Nessun movimento registrato.")
    else:
        for mov in movimenti:
            stato = "🔴 CONSEGNATA" if not mov['data_restituzione'] else "🟢 RESTITUITA"
            print(f"\n{stato}")
            print(f"ID: {mov['id']} | Casa: {mov['nome_casa']} | Collaboratore: {mov['collaboratore']}")
            print(f"Consegna: {mov['data_consegna']}")
            print(f"Restituzione: {mov['data_restituzione'] or 'N/A'}")
            if mov['note']:
                print(f"Note: {mov['note']}")
            print("-" * 60)
    
    pausa()

# ==================== MENU PRINCIPALE ====================

def menu_principale():
    """Menu principale dell'applicazione"""
    db = GestioneChiaviDB()
    
    while True:
        stampa_intestazione("GESTIONE CHIAVI CASE VACANZA")
        print("1. Gestione Case")
        print("2. Gestione Collaboratori")
        print("3. Gestione Movimenti Chiavi")
        print("0. Esci")
        print()
        
        scelta = input("Scegli un'opzione: ").strip()
        
        if scelta == "1":
            menu_gestione_case(db)
        elif scelta == "2":
            menu_gestione_collaboratori(db)
        elif scelta == "3":
            menu_gestione_movimenti(db)
        elif scelta == "0":
            stampa_intestazione("ARRIVEDERCI!")
            print("Grazie per aver utilizzato il sistema di gestione chiavi.")
            print()
            break
        else:
            print("\n❌ Opzione non valida!")
            pausa()

if __name__ == "__main__":
    menu_principale()
