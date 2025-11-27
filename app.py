from flask import Flask, render_template, request, jsonify, redirect, url_for
from database import GestioneChiaviDB
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chiave-segreta-gestione-chiavi-2025'
db = GestioneChiaviDB()

# ==================== ROUTES PAGINE ====================

@app.route('/')
def index():
    """Pagina principale - Dashboard"""
    return render_template('index.html')

@app.route('/case')
def case():
    """Pagina gestione case"""
    return render_template('case.html')

@app.route('/collaboratori')
def collaboratori():
    """Pagina gestione collaboratori"""
    return render_template('collaboratori.html')

@app.route('/movimenti')
def movimenti():
    """Pagina gestione movimenti"""
    return render_template('movimenti.html')

# ==================== API DASHBOARD ====================

@app.route('/api/dashboard')
def api_dashboard():
    """API per i dati della dashboard"""
    try:
        num_case = len(db.visualizza_case())
        num_collaboratori = len(db.visualizza_collaboratori())
        chiavi_consegnate = db.visualizza_chiavi_consegnate()
        num_chiavi_consegnate = len(chiavi_consegnate)
        
        # Converti chiavi consegnate in formato JSON-serializable
        chiavi_list = []
        for chiave in chiavi_consegnate:
            chiavi_list.append({
                'id': chiave['id'],
                'nome_casa': chiave['nome_casa'],
                'collaboratore': chiave['collaboratore'],
                'data_consegna': chiave['data_consegna'],
                'note': chiave['note'] if chiave['note'] else ''
            })
        
        return jsonify({
            'success': True,
            'data': {
                'num_case': num_case,
                'num_collaboratori': num_collaboratori,
                'num_chiavi_consegnate': num_chiavi_consegnate,
                'chiavi_consegnate': chiavi_list
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# ==================== API CASE ====================

@app.route('/api/case', methods=['GET'])
def api_get_case():
    """Ottiene tutte le case"""
    try:
        case = db.visualizza_case()
        case_list = []
        for casa in case:
            case_list.append({
                'id': casa['id'],
                'nome_casa': casa['nome_casa'],
                'indirizzo': casa['indirizzo'] if casa['indirizzo'] else '',
                'note': casa['note'] if casa['note'] else '',
                'totale_chiavi': casa['totale_chiavi'],
                'chiavi_affidate': casa['chiavi_affidate'],
                'chiavi_disponibili': casa['chiavi_disponibili'],
                'data_creazione': casa['data_creazione']
            })
        return jsonify({'success': True, 'data': case_list})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/case', methods=['POST'])
def api_add_casa():
    """Aggiunge una nuova casa"""
    try:
        data = request.get_json()
        nome_casa = data.get('nome_casa', '').strip()
        indirizzo = data.get('indirizzo', '').strip()
        note = data.get('note', '').strip()
        numero_chiavi = int(data.get('numero_chiavi', 1))
        
        if not nome_casa:
            return jsonify({'success': False, 'message': 'Il nome della casa è obbligatorio'}), 400
        
        successo, messaggio = db.aggiungi_casa(nome_casa, indirizzo, note, numero_chiavi)
        return jsonify({'success': successo, 'message': messaggio})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/case/<int:casa_id>', methods=['PUT'])
def api_update_casa(casa_id):
    """Modifica una casa esistente"""
    try:
        data = request.get_json()
        nome_casa = data.get('nome_casa', '').strip()
        indirizzo = data.get('indirizzo', '').strip()
        note = data.get('note', '').strip()
        numero_chiavi = int(data.get('numero_chiavi', 1))
        
        if not nome_casa:
            return jsonify({'success': False, 'message': 'Il nome della casa è obbligatorio'}), 400
        
        successo, messaggio = db.modifica_casa(casa_id, nome_casa, indirizzo, note, numero_chiavi)
        return jsonify({'success': successo, 'message': messaggio})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/case/<int:casa_id>', methods=['DELETE'])
def api_delete_casa(casa_id):
    """Elimina una casa"""
    try:
        successo, messaggio = db.elimina_casa(casa_id)
        return jsonify({'success': successo, 'message': messaggio})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/case/<int:casa_id>/movimenti', methods=['GET'])
def api_get_movimenti_casa(casa_id):
    """Ottiene i movimenti di una casa"""
    try:
        movimenti = db.cerca_movimenti_per_casa(casa_id)
        movimenti_list = []
        for mov in movimenti:
            movimenti_list.append({
                'id': mov['id'],
                'nome_casa': mov['nome_casa'],
                'collaboratore': mov['collaboratore'],
                'data_consegna': mov['data_consegna'],
                'data_restituzione': mov['data_restituzione'] if mov['data_restituzione'] else None,
                'note': mov['note'] if mov['note'] else ''
            })
        return jsonify({'success': True, 'data': movimenti_list})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# ==================== API COLLABORATORI ====================

@app.route('/api/collaboratori', methods=['GET'])
def api_get_collaboratori():
    """Ottiene tutti i collaboratori"""
    try:
        collaboratori = db.visualizza_collaboratori()
        collaboratori_list = []
        for collab in collaboratori:
            collaboratori_list.append({
                'id': collab['id'],
                'nome': collab['nome'],
                'cognome': collab['cognome'],
                'telefono': collab['telefono'] if collab['telefono'] else '',
                'email': collab['email'] if collab['email'] else '',
                'data_creazione': collab['data_creazione']
            })
        return jsonify({'success': True, 'data': collaboratori_list})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/collaboratori', methods=['POST'])
def api_add_collaboratore():
    """Aggiunge un nuovo collaboratore"""
    try:
        data = request.get_json()
        nome = data.get('nome', '').strip()
        cognome = data.get('cognome', '').strip()
        telefono = data.get('telefono', '').strip()
        email = data.get('email', '').strip()
        
        if not nome or not cognome:
            return jsonify({'success': False, 'message': 'Nome e cognome sono obbligatori'}), 400
        
        successo, messaggio = db.aggiungi_collaboratore(nome, cognome, telefono, email)
        return jsonify({'success': successo, 'message': messaggio})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/collaboratori/<int:collaboratore_id>', methods=['PUT'])
def api_update_collaboratore(collaboratore_id):
    """Modifica un collaboratore esistente"""
    try:
        data = request.get_json()
        nome = data.get('nome', '').strip()
        cognome = data.get('cognome', '').strip()
        telefono = data.get('telefono', '').strip()
        email = data.get('email', '').strip()
        
        if not nome or not cognome:
            return jsonify({'success': False, 'message': 'Nome e cognome sono obbligatori'}), 400
        
        successo, messaggio = db.modifica_collaboratore(collaboratore_id, nome, cognome, telefono, email)
        return jsonify({'success': successo, 'message': messaggio})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/collaboratori/<int:collaboratore_id>', methods=['DELETE'])
def api_delete_collaboratore(collaboratore_id):
    """Elimina un collaboratore"""
    try:
        successo, messaggio = db.elimina_collaboratore(collaboratore_id)
        return jsonify({'success': successo, 'message': messaggio})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/collaboratori/<int:collaboratore_id>/movimenti', methods=['GET'])
def api_get_movimenti_collaboratore(collaboratore_id):
    """Ottiene i movimenti di un collaboratore"""
    try:
        movimenti = db.cerca_movimenti_per_collaboratore(collaboratore_id)
        movimenti_list = []
        for mov in movimenti:
            movimenti_list.append({
                'id': mov['id'],
                'nome_casa': mov['nome_casa'],
                'collaboratore': mov['collaboratore'],
                'data_consegna': mov['data_consegna'],
                'data_restituzione': mov['data_restituzione'] if mov['data_restituzione'] else None,
                'note': mov['note'] if mov['note'] else ''
            })
        return jsonify({'success': True, 'data': movimenti_list})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# ==================== API MOVIMENTI ====================

@app.route('/api/movimenti/consegnate', methods=['GET'])
def api_get_chiavi_consegnate():
    """Ottiene tutte le chiavi consegnate"""
    try:
        chiavi = db.visualizza_chiavi_consegnate()
        chiavi_list = []
        for chiave in chiavi:
            chiavi_list.append({
                'id': chiave['id'],
                'nome_casa': chiave['nome_casa'],
                'collaboratore': chiave['collaboratore'],
                'data_consegna': chiave['data_consegna'],
                'note': chiave['note'] if chiave['note'] else ''
            })
        return jsonify({'success': True, 'data': chiavi_list})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/movimenti/storico', methods=['GET'])
def api_get_storico():
    """Ottiene lo storico dei movimenti"""
    try:
        limite = request.args.get('limite', 50, type=int)
        movimenti = db.visualizza_storico_movimenti(limite)
        movimenti_list = []
        for mov in movimenti:
            movimenti_list.append({
                'id': mov['id'],
                'nome_casa': mov['nome_casa'],
                'collaboratore': mov['collaboratore'],
                'data_consegna': mov['data_consegna'],
                'data_restituzione': mov['data_restituzione'] if mov['data_restituzione'] else None,
                'note': mov['note'] if mov['note'] else ''
            })
        return jsonify({'success': True, 'data': movimenti_list})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/movimenti/consegna', methods=['POST'])
def api_registra_consegna():
    """Registra una consegna di chiave"""
    try:
        data = request.get_json()
        id_casa = int(data.get('id_casa'))
        id_collaboratore = int(data.get('id_collaboratore'))
        note = data.get('note', '').strip()
        data_consegna = data.get('data_consegna', None)
        
        successo, messaggio = db.registra_consegna(id_casa, id_collaboratore, data_consegna, note)
        return jsonify({'success': successo, 'message': messaggio})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/movimenti/<int:movimento_id>/restituzione', methods=['POST'])
def api_registra_restituzione(movimento_id):
    """Registra una restituzione di chiave"""
    try:
        data = request.get_json() if request.is_json else {}
        data_restituzione = data.get('data_restituzione', None)
        
        successo, messaggio = db.registra_restituzione(movimento_id, data_restituzione)
        return jsonify({'success': successo, 'message': messaggio})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# ==================== API BACKUP ====================

@app.route('/api/backup/save', methods=['POST'])
def api_save_backup():
    """Salva un backup manuale"""
    try:
        successo, messaggio = db.salva_backup_automatico()
        return jsonify({'success': successo, 'message': messaggio})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    # Crea cartella templates se non esiste
    if not os.path.exists('templates'):
        os.makedirs('templates')
    if not os.path.exists('static'):
        os.makedirs('static')
    
    # Avvia il server
    print("=" * 60)
    print(" 🔑 GESTIONE CHIAVI CASE VACANZA - WEB APP ")
    print("=" * 60)
    print("\n✅ Server avviato con successo!")
    print("\n🌐 Apri il browser e vai a: http://localhost:5000")
    print("\n⚠️  Per fermare il server premi CTRL+C")
    print("=" * 60 + "\n")
    
    # Usa porta da variabile ambiente per compatibilità cloud
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
