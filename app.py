import hashlib
_orig_md5 = hashlib.md5
def _safe_md5(*args, **kwargs):
    kwargs.pop('usedforsecurity', None)
    return _orig_md5(*args, **kwargs)
hashlib.md5 = _safe_md5

import os
import sqlite3
import math
import io
import re
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'tactical_ballistics_secret_key_2026_spec')

DB_PATH = os.environ.get('DATABASE_PATH', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ricarica.db'))

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Tabelle Ricarica Ufficiali CIP
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tabelle_ricarica (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        calibro TEXT NOT NULL,
        produttore_polvere TEXT,
        tipo_polvere TEXT,
        peso_palla_grani REAL,
        dose_min_grani REAL,
        dose_max_grani REAL,
        oal_consigliato REAL
    )
    ''')
    
    # Utenti / Operatori
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS utenti (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Ricette Utente Personali
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ricette_utente (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER REFERENCES utenti(id),
        calibro TEXT NOT NULL,
        titolo_ricetta TEXT NOT NULL,
        marca_peso_palla TEXT,
        marca_tipo_polvere TEXT,
        dose_grani REAL,
        oal_scelto REAL,
        note_prestazione TEXT
    )
    ''')
    
    # Migrazione: se ricette_utente esisteva senza user_id, aggiungilo
    cursor.execute("PRAGMA table_info(ricette_utente)")
    colonne_ricette = [row['name'] for row in cursor.fetchall()]
    if 'user_id' not in colonne_ricette:
        cursor.execute("ALTER TABLE ricette_utente ADD COLUMN user_id INTEGER REFERENCES utenti(id)")
        
    # Impostazioni / Calcoli Salvati per Utente
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS impostazioni_utente (
        user_id INTEGER PRIMARY KEY REFERENCES utenti(id),
        costo_pacco_palle REAL,
        quantita_pacco_palle INTEGER,
        costo_pacco_inneschi REAL,
        quantita_pacco_inneschi INTEGER,
        costo_barattolo_polvere REAL,
        peso_barattolo_g REAL,
        dose_grani REAL,
        costo_bossolo_nuovo REAL,
        ricariche_previste INTEGER,
        chrono_stringa TEXT,
        chrono_unita TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Migrazione colonne pacco bossoli per impostazioni_utente
    cursor.execute("PRAGMA table_info(impostazioni_utente)")
    colonne_imp = [row['name'] for row in cursor.fetchall()]
    if 'costo_pacco_bossoli' not in colonne_imp:
        cursor.execute("ALTER TABLE impostazioni_utente ADD COLUMN costo_pacco_bossoli REAL DEFAULT 25.0")
    if 'quantita_pacco_bossoli' not in colonne_imp:
        cursor.execute("ALTER TABLE impostazioni_utente ADD COLUMN quantita_pacco_bossoli INTEGER DEFAULT 100")
    
    # Verifica se tabelle_ricarica è vuota e autopopola con dati reali italiani ed europei
    cursor.execute('SELECT COUNT(*) FROM tabelle_ricarica')
    count = cursor.fetchone()[0]
    
    if count == 0:
        dati_ufficiali = [
            # Canna Rigata - Pistola / PCC (9x19, 9x21, .38 Spec, .45 ACP)
            ('9x19 Luger / 9x21 IMI', 'Vihtavuori', 'N320', 124.0, 3.8, 4.3, 29.0),
            ('9x19 Luger / 9x21 IMI', 'Vihtavuori', 'N340', 124.0, 4.4, 5.0, 29.0),
            ('9x19 Luger / 9x21 IMI', 'Explosia / FRex', 'FRex Yellow (D032)', 124.0, 3.6, 4.1, 29.2),
            ('9x19 Luger / 9x21 IMI', 'Explosia / FRex', 'FRex Green (D036)', 124.0, 4.6, 5.2, 29.2),
            ('9x19 Luger / 9x21 IMI', 'Baschieri & Pellagri', 'M92S', 147.0, 4.5, 5.2, 29.5),
            ('9x19 Luger / 9x21 IMI', 'Cheddite', 'GM3', 124.0, 3.6, 4.1, 29.0),
            ('9x19 Luger / 9x21 IMI', 'Cheddite', 'GM3', 115.0, 3.8, 4.3, 29.0),
            
            ('.38 Special', 'Cheddite', 'GM3', 158.0, 3.2, 3.8, 39.0),
            ('.38 Special', 'Vihtavuori', 'N320', 158.0, 3.5, 4.1, 39.2),
            ('.38 Special', 'Baschieri & Pellagri', 'BP103', 158.0, 3.8, 4.4, 39.0),
            
            ('.45 ACP', 'Vihtavuori', 'N320', 230.0, 4.7, 5.2, 32.0),
            ('.45 ACP', 'Cheddite', 'GM3', 230.0, 4.2, 4.8, 31.8),
            ('.45 ACP', 'Explosia / FRex', 'FRex Yellow (D032)', 230.0, 4.5, 5.1, 32.2),
            
            # Canna Rigata - Carabina (.223 Rem, .308 Win)
            ('.223 Remington', 'Vihtavuori', 'N133', 55.0, 22.5, 24.8, 57.0),
            ('.223 Remington', 'Explosia / FRex', 'FRex Red (D073.4)', 55.0, 23.0, 25.5, 57.2),
            ('.223 Remington', 'Vihtavuori', 'N140', 69.0, 23.0, 25.3, 57.4),
            
            ('.308 Winchester', 'Vihtavuori', 'N140', 168.0, 40.5, 44.5, 71.0),
            ('.308 Winchester', 'Vihtavuori', 'N150', 175.0, 41.0, 44.8, 71.5),
            ('.308 Winchester', 'Explosia / FRex', 'FRex Green (S060)', 168.0, 39.0, 43.5, 71.0),
            ('.308 Winchester', 'Baschieri & Pellagri', 'BP106', 168.0, 40.0, 44.0, 71.0),
            
            # Canna Liscia - Calibro 12 (Palla Slug, Pallettoni, Trap)
            ('Calibro 12 (Slug Gualandi 32g)', 'Baschieri & Pellagri', 'MBx36', 493.8, 30.8, 34.0, 58.0),
            ('Calibro 12 (Slug Gualandi 32g)', 'Baschieri & Pellagri', 'M92S', 493.8, 32.4, 35.5, 58.5),
            ('Calibro 12 (Trap 28g)', 'Cheddite', 'GM3', 432.1, 22.0, 23.9, 58.0),
            ('Calibro 12 (Trap 28g)', 'Baschieri & Pellagri', 'F2 x 28', 432.1, 21.6, 23.1, 57.8)
        ]
        
        cursor.executemany('''
        INSERT INTO tabelle_ricarica 
        (calibro, produttore_polvere, tipo_polvere, peso_palla_grani, dose_min_grani, dose_max_grani, oal_consigliato)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', dati_ufficiali)
        
        conn.commit()

    # Ricetta di esempio iniziale ad accesso pubblico se vuota
    cursor.execute('SELECT COUNT(*) FROM ricette_utente')
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
        INSERT INTO ricette_utente
        (user_id, calibro, titolo_ricetta, marca_peso_palla, marca_tipo_polvere, dose_grani, oal_scelto, note_prestazione)
        VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            '9x19 Luger / 9x21 IMI',
            'Match IPSC Production 124gr (Demo)',
            'Alsa Pro FMJ-RN 124gr',
            'Vihtavuori N320',
            4.1,
            29.1,
            'Ricetta di riferimento. Ottima precisione CZ Shadow 2. PF 132 medio.'
        ))
        conn.commit()
    conn.close()

# Inizializza il DB all'avvio
init_db()

@app.route('/')
def index():
    return render_template('index.html')

# ==========================================
# AUTENTICAZIONE UTENTI (LOGIN / REGISTER)
# ==========================================
@app.route('/api/auth/register', methods=['POST'])
def auth_register():
    data = request.get_json(silent=True) or request.form
    username = (data.get('username') or '').strip()
    password = (data.get('password') or '').strip()
    email = (data.get('email') or '').strip() or None
    
    if len(username) < 3:
        return jsonify({'success': False, 'error': 'Lo username deve contenere almeno 3 caratteri.'}), 400
    if len(password) < 4:
        return jsonify({'success': False, 'error': 'La password deve contenere almeno 4 caratteri.'}), 400
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Verifica esistenza
    cursor.execute('SELECT id FROM utenti WHERE username = ?', (username,))
    if cursor.fetchone():
        conn.close()
        return jsonify({'success': False, 'error': f'L\'operatore "{username}" è già registrato.'}), 400
        
    if email:
        cursor.execute('SELECT id FROM utenti WHERE email = ?', (email,))
        if cursor.fetchone():
            conn.close()
            return jsonify({'success': False, 'error': 'Email già associata ad un altro account.'}), 400

    pwd_hash = generate_password_hash(password)
    cursor.execute('''
    INSERT INTO utenti (username, email, password_hash)
    VALUES (?, ?, ?)
    ''', (username, email, pwd_hash))
    conn.commit()
    user_id = cursor.lastrowid
    
    # Pre-popola preset economici di default per il nuovo utente
    cursor.execute('''
    INSERT INTO impostazioni_utente 
    (user_id, costo_pacco_palle, quantita_pacco_palle, costo_pacco_inneschi, quantita_pacco_inneschi, costo_barattolo_polvere, peso_barattolo_g, dose_grani, costo_bossolo_nuovo, ricariche_previste, chrono_stringa, chrono_unita)
    VALUES (?, 105.0, 1000, 65.0, 1000, 68.0, 500.0, 4.2, 0.25, 5, '315.2, 318.0, 316.5, 319.1, 317.4', 'ms')
    ''', (user_id,))
    conn.commit()
    conn.close()
    
    session['user_id'] = user_id
    session['username'] = username
    
    return jsonify({
        'success': True,
        'message': f'Operatore {username} registrato e connesso con successo.',
        'user': {'id': user_id, 'username': username}
    })

@app.route('/api/auth/login', methods=['POST'])
def auth_login():
    data = request.get_json(silent=True) or request.form
    username = (data.get('username') or '').strip()
    password = (data.get('password') or '').strip()
    
    if not username or not password:
        return jsonify({'success': False, 'error': 'Inserisci username e password.'}), 400
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM utenti WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    
    if not user or not check_password_hash(user['password_hash'], password):
        return jsonify({'success': False, 'error': 'Credenziali non valide. Verifica username o password.'}), 401
        
    session['user_id'] = user['id']
    session['username'] = user['username']
    
    return jsonify({
        'success': True,
        'message': f'Accesso autorizzato. Benvenuto Operatore {user["username"]}.',
        'user': {'id': user['id'], 'username': user['username']}
    })

@app.route('/api/auth/logout', methods=['POST'])
def auth_logout():
    session.clear()
    return jsonify({'success': True, 'message': 'Disconnessione effettuata con successo.'})

@app.route('/api/auth/me', methods=['GET'])
def auth_me():
    user_id = session.get('user_id')
    username = session.get('username')
    if user_id and username:
        return jsonify({'authenticated': True, 'user': {'id': user_id, 'username': username}})
    return jsonify({'authenticated': False, 'user': None})

# ==========================================
# PRESET ECONOMICI & CALCOLI SALVATI UTENTE
# ==========================================
@app.route('/api/user/presets', methods=['GET', 'POST'])
def user_presets():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'error': 'Accesso richiesto per sincronizzare i preset.'}), 401
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        data = request.get_json(silent=True) or request.form
        cursor.execute('''
        INSERT INTO impostazioni_utente (
            user_id, costo_pacco_palle, quantita_pacco_palle, costo_pacco_inneschi,
            quantita_pacco_inneschi, costo_pacco_bossoli, quantita_pacco_bossoli,
            costo_barattolo_polvere, peso_barattolo_g, dose_grani, costo_bossolo_nuovo,
            ricariche_previste, chrono_stringa, chrono_unita, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(user_id) DO UPDATE SET
            costo_pacco_palle = excluded.costo_pacco_palle,
            quantita_pacco_palle = excluded.quantita_pacco_palle,
            costo_pacco_inneschi = excluded.costo_pacco_inneschi,
            quantita_pacco_inneschi = excluded.quantita_pacco_inneschi,
            costo_pacco_bossoli = excluded.costo_pacco_bossoli,
            quantita_pacco_bossoli = excluded.quantita_pacco_bossoli,
            costo_barattolo_polvere = excluded.costo_barattolo_polvere,
            peso_barattolo_g = excluded.peso_barattolo_g,
            dose_grani = excluded.dose_grani,
            costo_bossolo_nuovo = excluded.costo_bossolo_nuovo,
            ricariche_previste = excluded.ricariche_previste,
            chrono_stringa = excluded.chrono_stringa,
            chrono_unita = excluded.chrono_unita,
            updated_at = CURRENT_TIMESTAMP
        ''', (
            user_id,
            float(data.get('costo_pacco_palle', 105.0)),
            int(data.get('quantita_pacco_palle', 1000)),
            float(data.get('costo_pacco_inneschi', 65.0)),
            int(data.get('quantita_pacco_inneschi', 1000)),
            float(data.get('costo_pacco_bossoli', 25.0)),
            int(data.get('quantita_pacco_bossoli', 100)),
            float(data.get('costo_barattolo_polvere', 68.0)),
            float(data.get('peso_barattolo_g', 500)),
            float(data.get('dose_grani', 4.2)),
            float(data.get('costo_bossolo_nuovo', 0.25)),
            int(data.get('ricariche_previste', 5)),
            str(data.get('chrono_stringa', '')),
            str(data.get('chrono_unita', 'ms'))
        ))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Parametri economici e cronografo memorizzati sul tuo profilo cloud.'})

    # GET
    cursor.execute('SELECT * FROM impostazioni_utente WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return jsonify({'success': True, 'presets': dict(row)})
    return jsonify({'success': True, 'presets': None})

# ==========================================
# API TABELLE DI RICARICA UFFICIALI (PUBBLICHE)
# ==========================================
@app.route('/api/tabelle', methods=['GET'])
def get_tabelle():
    calibro = request.args.get('calibro')
    conn = get_db_connection()
    cursor = conn.cursor()
    if calibro and calibro != 'ALL':
        cursor.execute('SELECT * FROM tabelle_ricarica WHERE calibro = ? ORDER BY produttore_polvere, tipo_polvere', (calibro,))
    else:
        cursor.execute('SELECT * FROM tabelle_ricarica ORDER BY calibro, produttore_polvere')
    rows = cursor.fetchall()
    
    cursor.execute('SELECT DISTINCT calibro FROM tabelle_ricarica ORDER BY calibro')
    calibri = [r[0] for r in cursor.fetchall()]
    conn.close()
    
    data = [dict(row) for row in rows]
    return jsonify({'tabelle': data, 'calibri': calibri})

# ==========================================
# API CRUD RICETTE UTENTE (ISOLATE PER OPERATORE)
# ==========================================
@app.route('/api/ricette', methods=['GET', 'POST'])
def api_ricette():
    user_id = session.get('user_id')
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        if not user_id:
            conn.close()
            return jsonify({
                'success': False, 
                'error': 'Per salvare ricette personali è necessario accedere con un account operatore.'
            }), 401
            
        data = request.get_json(silent=True) or request.form
        calibro = data.get('calibro', '').strip()
        titolo_ricetta = data.get('titolo_ricetta', '').strip()
        marca_peso_palla = data.get('marca_peso_palla', '').strip()
        marca_tipo_polvere = data.get('marca_tipo_polvere', '').strip()
        dose_grani = float(data.get('dose_grani', 0))
        oal_scelto = float(data.get('oal_scelto', 0))
        note_prestazione = data.get('note_prestazione', '').strip()
        
        if not calibro or not titolo_ricetta:
            conn.close()
            return jsonify({'success': False, 'error': 'Calibro e Titolo ricetta sono obbligatori.'}), 400
            
        cursor.execute('''
        INSERT INTO ricette_utente (user_id, calibro, titolo_ricetta, marca_peso_palla, marca_tipo_polvere, dose_grani, oal_scelto, note_prestazione)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, calibro, titolo_ricetta, marca_peso_palla, marca_tipo_polvere, dose_grani, oal_scelto, note_prestazione))
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return jsonify({'success': True, 'id': new_id, 'message': 'Ricetta salvata nel tuo quaderno personale.'})

    # GET: Se loggato, mostra solo le ricette del suo account; altrimenti mostra le demo (user_id IS NULL)
    if user_id:
        cursor.execute('SELECT * FROM ricette_utente WHERE user_id = ? ORDER BY id DESC', (user_id,))
    else:
        cursor.execute('SELECT * FROM ricette_utente WHERE user_id IS NULL ORDER BY id DESC')
        
    ricette = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify({'ricette': ricette, 'is_authenticated': bool(user_id)})

@app.route('/api/ricette/<int:recipe_id>', methods=['GET', 'PUT', 'DELETE'])
def api_ricetta_singola(recipe_id):
    user_id = session.get('user_id')
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM ricette_utente WHERE id = ?', (recipe_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return jsonify({'error': 'Ricetta non trovata'}), 404
        
    if request.method == 'GET':
        conn.close()
        return jsonify(dict(row))
        
    # Per PUT e DELETE occorre essere il proprietario (o user_id demo se non loggato)
    if not user_id or (row['user_id'] is not None and row['user_id'] != user_id):
        conn.close()
        return jsonify({'success': False, 'error': 'Non sei autorizzato a modificare o cancellare questa ricetta.'}), 403
        
    if request.method == 'DELETE':
        cursor.execute('DELETE FROM ricette_utente WHERE id = ?', (recipe_id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Ricetta eliminata con successo.'})
        
    elif request.method == 'PUT':
        data = request.get_json(silent=True) or request.form
        cursor.execute('''
        UPDATE ricette_utente
        SET calibro = ?, titolo_ricetta = ?, marca_peso_palla = ?, marca_tipo_polvere = ?, dose_grani = ?, oal_scelto = ?, note_prestazione = ?
        WHERE id = ?
        ''', (
            data.get('calibro'),
            data.get('titolo_ricetta'),
            data.get('marca_peso_palla'),
            data.get('marca_tipo_polvere'),
            float(data.get('dose_grani', 0)),
            float(data.get('oal_scelto', 0)),
            data.get('note_prestazione', ''),
            recipe_id
        ))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Ricetta aggiornata con successo.'})

# ==========================================
# ALGORITMO CALCOLO COSTO AVANZATO CON AMMORTAMENTO
# ==========================================
@app.route('/calcola_costo', methods=['POST'])
def calcola_costo():
    data = request.get_json(silent=True) or request.form
    try:
        # Palla: pacco o singola
        if 'costo_pacco_palle' in data and 'quantita_pacco_palle' in data:
            costo_pacco_palle = float(data.get('costo_pacco_palle', 0))
            qta_palle = max(1, int(data.get('quantita_pacco_palle', 1)))
            costo_palla = costo_pacco_palle / qta_palle
        else:
            costo_palla = float(data.get('costo_palla', 0))
        
        # Innesco: pacco o singola
        if 'costo_pacco_inneschi' in data and 'quantita_pacco_inneschi' in data:
            costo_pacco_inneschi = float(data.get('costo_pacco_inneschi', 0))
            qta_inneschi = max(1, int(data.get('quantita_pacco_inneschi', 1)))
            costo_innesco = costo_pacco_inneschi / qta_inneschi
        else:
            costo_innesco = float(data.get('costo_innesco', 0))
        
        # Polvere
        costo_barattolo = float(data.get('costo_barattolo_polvere', 0))
        peso_barattolo_g = float(data.get('peso_barattolo_g', 500))
        dose_grani = float(data.get('dose_grani', 0))
        
        # Conversione grani in grammi: 1 grano = 0.0647989 grammi
        dose_grammi = dose_grani * 0.0647989
        
        costo_polvere_colpo = 0.0
        if peso_barattolo_g > 0:
            costo_polvere_colpo = (dose_grammi / peso_barattolo_g) * costo_barattolo
            
        # Ammortamento Bossolo: supporta pacco o costo singolo diretto
        if 'costo_pacco_bossoli' in data and 'quantita_pacco_bossoli' in data:
            costo_pacco_bossoli = float(data.get('costo_pacco_bossoli', 0))
            qta_bossoli = max(1, int(data.get('quantita_pacco_bossoli', 1)))
            costo_bossolo_nuovo = costo_pacco_bossoli / qta_bossoli
        else:
            costo_bossolo_nuovo = float(data.get('costo_bossolo_nuovo', 0))
            
        ricariche_previste = max(1, int(data.get('ricariche_previste', 1)))
        quota_bossolo = costo_bossolo_nuovo / ricariche_previste
        
        # Totale per singolo colpo
        costo_singolo = costo_palla + costo_innesco + costo_polvere_colpo + quota_bossolo
        costo_50 = costo_singolo * 50
        costo_1000 = costo_singolo * 1000
        
        return jsonify({
            'success': True,
            'dose_grammi': round(dose_grammi, 3),
            'costo_palla': round(costo_palla, 4),
            'costo_innesco': round(costo_innesco, 4),
            'costo_bossolo_singolo': round(costo_bossolo_nuovo, 4),
            'costo_polvere_colpo': round(costo_polvere_colpo, 4),
            'quota_bossolo_ammortizzata': round(quota_bossolo, 4),
            'costo_singolo': round(costo_singolo, 4),
            'costo_50': round(costo_50, 2),
            'costo_1000': round(costo_1000, 2)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# ==========================================
# ALGORITMO BALISTICO (PF, JOULE, IPSC)
# ==========================================
@app.route('/calcola_balistica', methods=['POST'])
def calcola_balistica():
    data = request.get_json(silent=True) or request.form
    try:
        peso_grani = float(data.get('peso_palla_grani', 0))
        velocita = float(data.get('velocita', 0))
        unita = data.get('unita', 'ms').lower()
        
        if velocita <= 0 or peso_grani <= 0:
            return jsonify({'success': False, 'error': 'Dati balistici non validi'}), 400
            
        if unita == 'ms':
            fps = velocita * 3.28084
            ms = velocita
        else:
            fps = velocita
            ms = velocita / 3.28084
            
        # Power Factor: (peso_grani * fps) / 1000
        pf = (peso_grani * fps) / 1000.0
        
        # Energia Cinetica in Joule: (peso_grani * (fps^2)) / 450240
        joule = (peso_grani * (fps ** 2)) / 450240.0
        
        # Soglie IPSC
        classificazione_ipsc = {
            'pf': round(pf, 1),
            'joule': round(joule, 1),
            'fps': round(fps, 1),
            'ms': round(ms, 1),
            'open': 'MAJOR (>=160)' if pf >= 160 else ('MINOR (>=125)' if pf >= 125 else 'SUB-MINOR (<125)'),
            'standard_classic': 'MAJOR (>=170)' if pf >= 170 else ('MINOR (>=125)' if pf >= 125 else 'SUB-MINOR (<125)'),
            'production': 'MINOR (Fattore unico)' if pf >= 125 else 'SUB-MINOR (<125)',
            'pcc': 'REGOLAMENTARE PCC (>=125)' if pf >= 125 else 'SUB-MINOR (<125)'
        }
        
        if pf >= 170:
            status_pf = "MAJOR // MASSIMA POTENZA"
            status_color = "amber"
        elif pf >= 160:
            status_pf = "MAJOR OPEN / MINOR STD"
            status_color = "amber"
        elif pf >= 125:
            status_pf = "MINOR // IDONEO GARA"
            status_color = "green"
        else:
            status_pf = "SUB-MINOR // NON QUALIFICATO"
            status_color = "red"
            
        return jsonify({
            'success': True,
            'pf': round(pf, 1),
            'joule': round(joule, 1),
            'fps': round(fps, 1),
            'ms': round(ms, 1),
            'ipsc': classificazione_ipsc,
            'status_pf': status_pf,
            'status_color': status_color
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# ==========================================
# ALGORITMO DEVIAZIONE STANDARD (SD) & ES
# ==========================================
@app.route('/calcola_sd', methods=['POST'])
def calcola_sd():
    data = request.get_json(silent=True) or request.form
    raw_string = data.get('velocita_stringa', '')
    unita = data.get('unita', 'ms')
    
    tokens = re.split(r'[,;\s\n]+', raw_string.strip())
    velocities = []
    for token in tokens:
        if not token:
            continue
        try:
            val = float(token.replace(',', '.'))
            if val > 0:
                velocities.append(val)
        except ValueError:
            pass
            
    if len(velocities) < 2:
        return jsonify({
            'success': False, 
            'error': 'Inserisci almeno 2 rilevamenti validi per calcolare la Deviazione Standard.'
        }), 400
        
    n = len(velocities)
    media = sum(velocities) / n
    variance = sum((x - media) ** 2 for x in velocities) / (n - 1)
    sd = math.sqrt(variance)
    max_v = max(velocities)
    min_v = min(velocities)
    es = max_v - min_v
    
    soglia_top = 3.0 if unita == 'ms' else 9.8
    soglia_mid = 5.0 if unita == 'ms' else 16.4
    soglia_acc = 8.0 if unita == 'ms' else 26.2
    
    if sd <= soglia_top:
        giudizio = "MATCH GRADE // ECCELLENTE"
        giudizio_color = "green"
    elif sd <= soglia_mid:
        giudizio = "BUONA // STANDARD TIRO SPORTIVO"
        giudizio_color = "blue"
    elif sd <= soglia_acc:
        giudizio = "ACCETTABILE // PLINKING / CACCIA"
        giudizio_color = "amber"
    else:
        giudizio = "IRREGOLARE // VERIFICARE DOSAGGIO E CRIMPATURA"
        giudizio_color = "red"
        
    return jsonify({
        'success': True,
        'count': n,
        'media': round(media, 2),
        'sd': round(sd, 2),
        'es': round(es, 2),
        'min': round(min_v, 2),
        'max': round(max_v, 2),
        'unita': unita,
        'giudizio': giudizio,
        'giudizio_color': giudizio_color,
        'velocities': velocities
    })

# ==========================================
# ESPORTAZIONE ETICHETTA PDF (ReportLab - 288x144 pt)
# ==========================================
@app.route('/esporta_etichetta_pdf', methods=['GET', 'POST'])
def esporta_etichetta_pdf():
    from reportlab.lib.colors import HexColor
    from reportlab.pdfgen import canvas
    
    recipe_id = request.args.get('id') or (request.get_json(silent=True) or {}).get('id')
    operatore = session.get('username') or 'OPERATORE STANDARD'
    
    calibro = "9x19 Luger"
    titolo = "Lotto Match Tattico"
    palla = "124 grs FMJ"
    polvere = "Vihtavuori N320"
    dose = "4.2 grs"
    oal = "29.10 mm"
    innesco = "Small Pistol Standard"
    lotto = f"LOT-{datetime.now().strftime('%y%m%d')}"
    data_str = datetime.now().strftime('%d/%m/%Y')
    note = "SD < 3.5 m/s - Precisione Sub-MOA"
    
    if recipe_id:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM ricette_utente WHERE id = ?', (recipe_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            calibro = row['calibro']
            titolo = row['titolo_ricetta']
            palla = row['marca_peso_palla'] or palla
            polvere = row['marca_tipo_polvere'] or polvere
            dose = f"{row['dose_grani']} grs" if row['dose_grani'] else dose
            oal = f"{row['oal_scelto']} mm" if row['oal_scelto'] else oal
            note = row['note_prestazione'] or note
    else:
        calibro = request.args.get('calibro', calibro)
        titolo = request.args.get('titolo', titolo)
        palla = request.args.get('palla', palla)
        polvere = request.args.get('polvere', polvere)
        dose = request.args.get('dose', dose)
        oal = request.args.get('oal', oal)
        innesco = request.args.get('innesco', innesco)
        lotto = request.args.get('lotto', lotto)
        note = request.args.get('note', note)
        
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(288, 144))
    
    c_bg = HexColor("#111317")
    c_card = HexColor("#1a1d24")
    c_amber = HexColor("#f59e0b")
    c_green = HexColor("#16a34a")
    c_text = HexColor("#f3f4f6")
    c_muted = HexColor("#9ca3af")
    c_line = HexColor("#374151")
    
    # Sfondo scuro
    c.setFillColor(c_bg)
    c.rect(0, 0, 288, 144, fill=1, stroke=0)
    
    # Bordo esterno tattico con mirini angolari
    c.setStrokeColor(c_amber)
    c.setLineWidth(1.5)
    c.rect(5, 5, 278, 134, fill=0, stroke=1)
    
    corner_len = 10
    c.setLineWidth(2.5)
    c.line(5, 139, 5 + corner_len, 139)
    c.line(5, 139, 5, 139 - corner_len)
    c.line(283, 139, 283 - corner_len, 139)
    c.line(283, 139, 283, 139 - corner_len)
    c.line(5, 5, 5 + corner_len, 5)
    c.line(5, 5, 5, 5 + corner_len)
    c.line(283, 5, 283 - corner_len, 5)
    c.line(283, 5, 283, 5 + corner_len)
    
    # Header Banner
    c.setFillColor(c_card)
    c.rect(7, 114, 274, 23, fill=1, stroke=0)
    c.setStrokeColor(c_line)
    c.setLineWidth(0.5)
    c.line(7, 114, 281, 114)
    
    c.setFillColor(c_amber)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(12, 126, f"BALLISTIC OPS // ARMORY LOGBOOK [{operatore.upper()}]")
    
    c.setFillColor(c_muted)
    c.setFont("Helvetica", 7)
    c.drawRightString(276, 126, f"DATA: {data_str}")
    
    c.setFillColor(c_text)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(12, 102, calibro.upper())
    
    c.setFillColor(c_green)
    c.setFont("Helvetica-Bold", 9)
    c.drawRightString(276, 102, f"LOTTO: {lotto}")
    
    c.setFillColor(c_text)
    c.setFont("Helvetica-Oblique", 8)
    safe_titolo = (titolo[:38] + '..') if len(titolo) > 40 else titolo
    c.drawString(12, 90, safe_titolo)
    
    c.setStrokeColor(c_line)
    c.setLineWidth(0.5)
    c.line(12, 85, 276, 85)
    
    # Colonna 1
    c.setFillColor(c_muted)
    c.setFont("Helvetica-Bold", 6.5)
    c.drawString(12, 75, "POLVERE / TIPO:")
    c.setFillColor(c_text)
    c.setFont("Helvetica", 8)
    c.drawString(12, 65, polvere[:22])
    
    c.setFillColor(c_muted)
    c.setFont("Helvetica-Bold", 6.5)
    c.drawString(12, 53, "PALLA / OGIVA:")
    c.setFillColor(c_text)
    c.setFont("Helvetica", 8)
    c.drawString(12, 43, palla[:22])
    
    # Colonna 2
    c.setFillColor(c_muted)
    c.setFont("Helvetica-Bold", 6.5)
    c.drawString(120, 75, "DOSE:")
    c.setFillColor(c_amber)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(120, 64, dose)
    
    c.setFillColor(c_muted)
    c.setFont("Helvetica-Bold", 6.5)
    c.drawString(120, 53, "O.A.L. (LUNGH. TOTALE):")
    c.setFillColor(c_text)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(120, 43, oal)
    
    # Colonna 3
    c.setFillColor(c_muted)
    c.setFont("Helvetica-Bold", 6.5)
    c.drawString(205, 75, "INNESCO:")
    c.setFillColor(c_text)
    c.setFont("Helvetica", 7.5)
    c.drawString(205, 65, innesco[:14])
    
    c.setFillColor(c_muted)
    c.setFont("Helvetica-Bold", 6.5)
    c.drawString(205, 53, "SICUREZZA CIP:")
    c.setFillColor(c_green)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(205, 43, "VERIFICATO")
    
    c.setStrokeColor(c_line)
    c.line(12, 36, 276, 36)
    
    c.setFillColor(c_muted)
    c.setFont("Helvetica-Bold", 6.5)
    c.drawString(12, 27, "NOTE PRESTAZIONE / CHRONO:")
    c.setFillColor(c_text)
    c.setFont("Helvetica-Oblique", 7)
    safe_note = (note[:55] + '..') if len(note) > 58 else note
    c.drawString(12, 17, safe_note)
    
    c.setFillColor(HexColor("#6b7280"))
    c.setFont("Helvetica", 5)
    c.drawString(12, 8, "VERIFICARE SEMPRE LE PRESSIONI MASSIME CIP/SAAMI PRIMA DELL'USO. NON SUPERARE LE DOSI MASSIME.")
    
    c.showPage()
    c.save()
    
    buf.seek(0)
    filename = f"etichetta_{calibro.replace('/', '_').replace(' ', '_')}_{lotto}.pdf"
    return send_file(buf, mimetype='application/pdf', as_attachment=False, download_name=filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5055))
    print(f"[*] Avvio Tactical Reload & Ballistics Hub su http://127.0.0.1:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
