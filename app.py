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
from flask import Flask, render_template, request, jsonify, send_file, session, Response
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
    
    # Tabelle Ricarica Ufficiali CIP e Personalizzate Utente
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tabelle_ricarica (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER REFERENCES utenti(id),
        calibro TEXT NOT NULL,
        produttore_polvere TEXT,
        tipo_polvere TEXT,
        peso_palla_grani REAL,
        dose_min_grani REAL,
        dose_max_grani REAL,
        oal_consigliato REAL,
        note TEXT
    )
    ''')
    
    # Migrazione per tabelle_ricarica (user_id e note)
    cursor.execute("PRAGMA table_info(tabelle_ricarica)")
    colonne_tabelle = [row['name'] for row in cursor.fetchall()]
    if 'user_id' not in colonne_tabelle:
        cursor.execute("ALTER TABLE tabelle_ricarica ADD COLUMN user_id INTEGER REFERENCES utenti(id)")
    if 'note' not in colonne_tabelle:
        cursor.execute("ALTER TABLE tabelle_ricarica ADD COLUMN note TEXT")

    
    # Utenti / Operatori
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS utenti (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE,
        password_hash TEXT NOT NULL,
        is_admin INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Migrazione colonna is_admin per tabella utenti
    cursor.execute("PRAGMA table_info(utenti)")
    colonne_utenti = [row['name'] for row in cursor.fetchall()]
    if 'is_admin' not in colonne_utenti:
        cursor.execute("ALTER TABLE utenti ADD COLUMN is_admin INTEGER DEFAULT 0")

    # Tabella Monitoraggio Visite & Geografica
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS log_visite (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip_hash TEXT NOT NULL,
        paese TEXT DEFAULT 'Italia',
        codice_paese TEXT DEFAULT 'IT',
        percorso TEXT,
        user_agent TEXT,
        giorno TEXT DEFAULT (DATE('now')),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_visite_giorno ON log_visite(giorno)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_visite_ip_giorno ON log_visite(ip_hash, giorno)")

    # Inizializzazione Superuser Admin con Password ad Alta Sicurezza (Militare)
    admin_user = os.environ.get('ADMIN_USERNAME', 'admin')
    admin_pass = os.environ.get('ADMIN_PASSWORD', 'Armory$Admin#2026!SecOps')
    admin_email = os.environ.get('ADMIN_EMAIL', 'admin@ricarica.it')

    cursor.execute('SELECT id FROM utenti WHERE username = ?', (admin_user,))
    admin_row = cursor.fetchone()
    if not admin_row:
        cursor.execute('''
        INSERT INTO utenti (username, email, password_hash, is_admin)
        VALUES (?, ?, ?, 1)
        ''', (admin_user, admin_email, generate_password_hash(admin_pass)))
    else:
        # Aggiorna credenziali superuser con password sicura e garantisce flag is_admin = 1
        cursor.execute('''
        UPDATE utenti SET password_hash = ?, is_admin = 1 WHERE username = ?
        ''', (generate_password_hash(admin_pass), admin_user))
    conn.commit()

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

# ==========================================
# GEOLOCALIZZAZIONE & TRACCIAMENTO VISITATORI
# ==========================================
GEO_CACHE = {}

COUNTRY_FLAGS = {
    'IT': '🇮🇹', 'US': '🇺🇸', 'DE': '🇩🇪', 'FR': '🇫🇷', 'ES': '🇪🇸',
    'CH': '🇨🇭', 'AT': '🇦🇹', 'GB': '🇬🇧', 'CA': '🇨🇦', 'AU': '🇦🇺',
    'NL': '🇳🇱', 'PL': '🇵🇱', 'CZ': '🇨🇿', 'SE': '🇸🇪', 'NO': '🇳🇴',
    'FI': '🇫🇮', 'BE': '🇧🇪', 'PT': '🇵🇹', 'GR': '🇬🇷', 'RO': '🇷🇴',
    'SM': '🇸🇲', 'VA': '🇻🇦', 'BR': '🇧🇷', 'JP': '🇯🇵', 'ZA': '🇿🇦',
    'IE': '🇮🇪', 'DK': '🇩🇰', 'HR': '🇭🇷', 'SI': '🇸🇮', 'HU': '🇭🇺'
}

COUNTRY_NAMES = {
    'IT': 'Italia', 'US': 'Stati Uniti', 'DE': 'Germania', 'FR': 'Francia',
    'ES': 'Spagna', 'CH': 'Svizzera', 'AT': 'Austria', 'GB': 'Regno Unito',
    'CA': 'Canada', 'AU': 'Australia', 'NL': 'Paesi Bassi', 'PL': 'Polonia',
    'CZ': 'Repubblica Ceca', 'SE': 'Svezia', 'NO': 'Norvegia', 'FI': 'Finlandia',
    'BE': 'Belgio', 'PT': 'Portogallo', 'GR': 'Grecia', 'RO': 'Romania',
    'SM': 'San Marino', 'VA': 'Città del Vaticano', 'BR': 'Brasile',
    'JP': 'Giappone', 'ZA': 'Sudafrica', 'IE': 'Irlanda', 'DK': 'Danimarca',
    'HR': 'Croazia', 'SI': 'Slovenia', 'HU': 'Ungheria'
}

def risolvi_paese_visitatore(ip):
    # 1. Header Proxy/Cloudflare
    cf_country = request.headers.get('CF-IPCountry') or request.headers.get('X-Country') or request.headers.get('X-Geo-Country')
    if cf_country and len(cf_country) == 2 and cf_country.upper() != 'XX':
        code = cf_country.upper()
        return COUNTRY_NAMES.get(code, code), code
        
    is_private = (
        ip.startswith('127.') or ip.startswith('192.168.') or 
        ip.startswith('10.') or ip.startswith('172.16.') or 
        ip in ('::1', 'localhost', '0.0.0.0')
    )
    
    # 2. Lookup IP se pubblico (con cache locale in memoria)
    if not is_private:
        if ip in GEO_CACHE:
            return GEO_CACHE[ip]
        try:
            import urllib.request
            req = urllib.request.Request(
                f"http://ip-api.com/json/{ip}?fields=status,country,countryCode",
                headers={'User-Agent': 'TacticalReloadHub/1.0'}
            )
            with urllib.request.urlopen(req, timeout=1.2) as resp:
                import json
                res_data = json.loads(resp.read().decode('utf-8'))
                if res_data.get('status') == 'success':
                    paese = res_data.get('country', 'Italia')
                    codice = res_data.get('countryCode', 'IT')
                    GEO_CACHE[ip] = (paese, codice)
                    return paese, codice
        except Exception:
            pass
            
    # 3. Fallback intelligente su Accept-Language
    lang_header = request.headers.get('Accept-Language', '').lower()
    for code in ('it', 'ch', 'de', 'fr', 'es', 'at', 'gb', 'us', 'nl', 'pl', 'cz'):
        if code in lang_header:
            codice = code.upper()
            if codice == 'GB':
                return 'Regno Unito', 'GB'
            return COUNTRY_NAMES.get(codice, codice), codice
            
    return 'Italia', 'IT'

@app.before_request
def traccia_visitatore():
    path = request.path
    if path.startswith('/static') or path in ('/favicon.ico', '/robots.txt') or path.startswith('/api/admin'):
        return
        
    try:
        forwarded = request.headers.get('X-Forwarded-For')
        if forwarded:
            ip = forwarded.split(',')[0].strip()
        else:
            ip = request.remote_addr or '127.0.0.1'
            
        ip_hash = hashlib.sha256(f"tactical_ops_{ip}".encode()).hexdigest()[:16]
        paese, codice_paese = risolvi_paese_visitatore(ip)
        user_agent = (request.headers.get('User-Agent') or '')[:120]
        today_str = datetime.now().strftime('%Y-%m-%d')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO log_visite (ip_hash, paese, codice_paese, percorso, user_agent, giorno)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (ip_hash, paese, codice_paese, path[:60], user_agent, today_str))
        conn.commit()
        conn.close()
    except Exception:
        pass

def admin_required():
    return bool(session.get('user_id') and session.get('is_admin'))

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
    INSERT INTO utenti (username, email, password_hash, is_admin)
    VALUES (?, ?, ?, 0)
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
    session['is_admin'] = False
    
    return jsonify({
        'success': True,
        'message': f'Operatore {username} registrato e connesso con successo.',
        'user': {'id': user_id, 'username': username, 'is_admin': False}
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
        
    is_admin = bool(user['is_admin']) if 'is_admin' in user.keys() else (username == 'admin')
    session['user_id'] = user['id']
    session['username'] = user['username']
    session['is_admin'] = is_admin
    
    return jsonify({
        'success': True,
        'message': f'Accesso autorizzato. Benvenuto Operatore {user["username"]}.',
        'user': {'id': user['id'], 'username': user['username'], 'is_admin': is_admin}
    })

@app.route('/api/auth/logout', methods=['POST'])
def auth_logout():
    session.clear()
    return jsonify({'success': True, 'message': 'Disconnessione effettuata con successo.'})

@app.route('/api/auth/me', methods=['GET'])
def auth_me():
    user_id = session.get('user_id')
    username = session.get('username')
    is_admin = session.get('is_admin', False)
    if user_id and username:
        return jsonify({'authenticated': True, 'user': {'id': user_id, 'username': username, 'is_admin': is_admin}})
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
# API TABELLE DI RICARICA (CIP + PERSONALIZZATE)
# ==========================================
@app.route('/api/tabelle', methods=['GET', 'POST'])
def handle_tabelle():
    user_id = session.get('user_id')
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        data = request.get_json(silent=True) or request.form
        calibro = (data.get('calibro') or '').strip()
        produttore = (data.get('produttore_polvere') or '').strip()
        tipo = (data.get('tipo_polvere') or '').strip()
        
        if not calibro or not tipo:
            conn.close()
            return jsonify({'success': False, 'error': 'Calibro e Tipo Polvere sono campi obbligatori.'}), 400
            
        try:
            peso_palla = float(data.get('peso_palla_grani') or 0)
            dose_min = float(data.get('dose_min_grani') or 0)
            dose_max = float(data.get('dose_max_grani') or 0)
            oal = float(data.get('oal_consigliato') or 0)
        except (ValueError, TypeError):
            conn.close()
            return jsonify({'success': False, 'error': 'I valori di peso palla, dosi e OAL devono essere numerici.'}), 400
            
        note = (data.get('note') or '').strip()
        
        cursor.execute('''
        INSERT INTO tabelle_ricarica 
        (user_id, calibro, produttore_polvere, tipo_polvere, peso_palla_grani, dose_min_grani, dose_max_grani, oal_consigliato, note)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, calibro, produttore, tipo, peso_palla, dose_min, dose_max, oal, note))
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        
        return jsonify({
            'success': True,
            'id': new_id,
            'message': f'Riferimento per {calibro} ({tipo}) registrato con successo!'
        })

    # GET
    calibro = request.args.get('calibro')
    query = '''
    SELECT t.*, u.username as operatore 
    FROM tabelle_ricarica t
    LEFT JOIN utenti u ON t.user_id = u.id
    '''
    params = []
    if calibro and calibro != 'ALL':
        query += ' WHERE t.calibro = ?'
        params.append(calibro)
        
    query += ' ORDER BY t.calibro, t.produttore_polvere, t.tipo_polvere'
    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    cursor.execute('SELECT DISTINCT calibro FROM tabelle_ricarica ORDER BY calibro')
    calibri = [r[0] for r in cursor.fetchall()]
    
    cursor.execute('SELECT DISTINCT tipo_polvere FROM tabelle_ricarica WHERE tipo_polvere IS NOT NULL AND tipo_polvere != "" ORDER BY tipo_polvere')
    polveri = [r[0] for r in cursor.fetchall()]
    
    cursor.execute('SELECT DISTINCT produttore_polvere FROM tabelle_ricarica WHERE produttore_polvere IS NOT NULL AND produttore_polvere != "" ORDER BY produttore_polvere')
    produttori = [r[0] for r in cursor.fetchall()]
    
    conn.close()
    
    data = []
    for r in rows:
        item = dict(r)
        item['is_custom'] = bool(r['user_id'])
        item['can_delete'] = bool(user_id and r['user_id'] == user_id)
        data.append(item)
        
    return jsonify({
        'tabelle': data, 
        'calibri': calibri,
        'polveri': polveri,
        'produttori': produttori,
        'current_user_id': user_id
    })

@app.route('/api/tabelle/<int:item_id>', methods=['DELETE'])
def delete_tabella(item_id):
    user_id = session.get('user_id')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tabelle_ricarica WHERE id = ?', (item_id,))
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        return jsonify({'success': False, 'error': 'Dato non trovato nel database.'}), 404
        
    if row['user_id'] is None:
        conn.close()
        return jsonify({'success': False, 'error': 'Le tabelle ufficiali CIP di sistema sono protette e non possono essere eliminate.'}), 403
        
    if not user_id or row['user_id'] != user_id:
        conn.close()
        return jsonify({'success': False, 'error': 'Non sei autorizzato a eliminare questa voce.'}), 403
        
    cursor.execute('DELETE FROM tabelle_ricarica WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Riferimento balistico eliminato dal database.'})

@app.route('/api/tabelle/upload-csv', methods=['POST'])
def upload_csv_tabelle():
    user_id = session.get('user_id')
    file = request.files.get('file')
    csv_text = ''
    
    if file:
        csv_text = file.read().decode('utf-8', errors='ignore')
    else:
        data = request.get_json(silent=True) or request.form
        csv_text = data.get('csv_text', '')
        
    if not csv_text.strip():
        return jsonify({'success': False, 'error': 'Nessun file o testo CSV fornito.'}), 400
        
    import csv
    lines = csv_text.strip().splitlines()
    first_line = lines[0] if lines else ''
    delimiter = ';' if ';' in first_line and ',' not in first_line else ','
    
    reader = csv.reader(lines, delimiter=delimiter)
    header = next(reader, None)
    if not header:
        return jsonify({'success': False, 'error': 'File CSV vuoto.'}), 400
        
    header_map = {}
    for idx, col in enumerate(header):
        cleaned = col.strip().lower().replace(' ', '_').replace('"', '').replace("'", "")
        header_map[cleaned] = idx
        
    inserted_count = 0
    conn = get_db_connection()
    cursor = conn.cursor()
    
    for row in reader:
        if not row or len(row) < 2:
            continue
            
        def get_val(key, default=''):
            if key in header_map and header_map[key] < len(row):
                return row[header_map[key]].strip()
            return default
            
        calibro = get_val('calibro') or (row[0].strip() if len(row) > 0 else '')
        produttore = get_val('produttore_polvere') or get_val('produttore') or (row[1].strip() if len(row) > 1 else '')
        tipo = get_val('tipo_polvere') or get_val('polvere') or (row[2].strip() if len(row) > 2 else '')
        
        if not calibro or not tipo:
            continue
            
        try:
            peso_palla = float(get_val('peso_palla_grani') or get_val('peso_palla') or (row[3] if len(row) > 3 else 0) or 0)
        except (ValueError, TypeError):
            peso_palla = 0.0
            
        try:
            dose_min = float(get_val('dose_min_grani') or get_val('dose_min') or (row[4] if len(row) > 4 else 0) or 0)
        except (ValueError, TypeError):
            dose_min = 0.0
            
        try:
            dose_max = float(get_val('dose_max_grani') or get_val('dose_max') or (row[5] if len(row) > 5 else 0) or 0)
        except (ValueError, TypeError):
            dose_max = 0.0
            
        try:
            oal = float(get_val('oal_consigliato') or get_val('oal') or (row[6] if len(row) > 6 else 0) or 0)
        except (ValueError, TypeError):
            oal = 0.0
            
        note = get_val('note') or (row[7].strip() if len(row) > 7 else '')
        
        cursor.execute('''
        INSERT INTO tabelle_ricarica 
        (user_id, calibro, produttore_polvere, tipo_polvere, peso_palla_grani, dose_min_grani, dose_max_grani, oal_consigliato, note)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, calibro, produttore, tipo, peso_palla, dose_min, dose_max, oal, note))
        inserted_count += 1
        
    conn.commit()
    conn.close()
    
    return jsonify({
        'success': True,
        'count': inserted_count,
        'message': f'{inserted_count} nuovi riferimenti di ricarica importati con successo nel database.'
    })

@app.route('/api/tabelle/template-csv', methods=['GET'])
def download_csv_template():
    csv_content = "calibro,produttore_polvere,tipo_polvere,peso_palla_grani,dose_min_grani,dose_max_grani,oal_consigliato,note\n"
    csv_content += "6.5 Creedmoor,Reload Swiss,RS60,140.0,40.0,43.5,71.5,Palla Hornady ELD-M\n"
    csv_content += ".300 AAC Blackout,Vihtavuori,N110,125.0,17.0,19.2,54.0,Carabina AR-15\n"
    csv_content += ".357 Magnum,Vihtavuori,N340,158.0,7.0,8.2,40.0,Revolver canna 6 pollici\n"
    
    buf = io.BytesIO(csv_content.encode('utf-8'))
    return send_file(buf, mimetype='text/csv', as_attachment=True, download_name='template_ricarica_balistica.csv')


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
    
    # Palette Tattica a Sfondo Grigio Chiaro (ottimizzata per stampa nitida ed etichette adesive)
    c_bg = HexColor("#f1f5f9")        # Grigio chiaro / Light slate
    c_card = HexColor("#e2e8f0")      # Header banner grigio chiaro accentuato
    c_amber = HexColor("#b45309")     # Ambra scuro / ad alto contrasto
    c_green = HexColor("#15803d")     # Verde scuro certificato CIP
    c_text = HexColor("#0f172a")      # Testo scuro primario
    c_muted = HexColor("#475569")     # Testo secondario ed etichette
    c_line = HexColor("#cbd5e1")      # Linee divisorie
    c_border = HexColor("#b45309")    # Bordo esterno e angoli tattici
    
    # Sfondo grigio chiaro
    c.setFillColor(c_bg)
    c.rect(0, 0, 288, 144, fill=1, stroke=0)
    
    # Bordo esterno tattico con mirini angolari
    c.setStrokeColor(c_border)
    c.setLineWidth(1.2)
    c.rect(5, 5, 278, 134, fill=0, stroke=1)
    
    corner_len = 10
    c.setLineWidth(2.2)
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
    
    # Note / Chrono
    c.setFillColor(c_muted)
    c.setFont("Helvetica-Bold", 6.5)
    c.drawString(12, 27, "NOTE PRESTAZIONE / CHRONO:")
    c.setFillColor(c_text)
    c.setFont("Helvetica-Oblique", 7)
    safe_note = (note[:55] + '..') if len(note) > 58 else note
    c.drawString(12, 17, safe_note)
    
    c.setFillColor(HexColor("#64748b"))
    c.setFont("Helvetica", 5)
    c.drawString(12, 8, "VERIFICARE SEMPRE LE PRESSIONI MASSIME CIP/SAAMI PRIMA DELL'USO. NON SUPERARE LE DOSI MASSIME.")
    
    c.showPage()
    c.save()
    
    buf.seek(0)
    filename = f"etichetta_{calibro.replace('/', '_').replace(' ', '_')}_{lotto}.pdf"
    return send_file(buf, mimetype='application/pdf', as_attachment=False, download_name=filename)

# ==========================================
# AREA RISERVATA ADMIN & DASHBOARD STATISTICHE
# ==========================================
@app.route('/admin')
def admin_dashboard():
    if not admin_required():
        # Se non autorizzato, reindirizza con avviso o apri login
        return render_template('index.html', admin_required=True)
    return render_template('admin_dashboard.html')

@app.route('/api/admin/stats', methods=['GET'])
def api_admin_stats():
    if not admin_required():
        return jsonify({'success': False, 'error': 'Accesso riservato esclusivamente al superuser amministratore.'}), 403
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    today_str = datetime.now().strftime('%Y-%m-%d')
    
    # 1. Metriche Visitatori & Traffico
    cursor.execute('SELECT COUNT(DISTINCT ip_hash) FROM log_visite')
    visitatori_unici_totali = cursor.fetchone()[0] or 0
    
    cursor.execute('SELECT COUNT(*) FROM log_visite')
    pageviews_totali = cursor.fetchone()[0] or 0
    
    cursor.execute('SELECT COUNT(DISTINCT ip_hash) FROM log_visite WHERE giorno = ?', (today_str,))
    visitatori_oggi = cursor.fetchone()[0] or 0
    
    cursor.execute('SELECT COUNT(*) FROM log_visite WHERE giorno = ?', (today_str,))
    pageviews_oggi = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT COUNT(DISTINCT ip_hash) FROM log_visite WHERE giorno >= DATE('now', '-7 days')")
    visitatori_7gg = cursor.fetchone()[0] or 0
    
    # Trend giornaliero ultimi 7 giorni
    cursor.execute('''
    SELECT giorno, COUNT(DISTINCT ip_hash) as visitatori, COUNT(*) as pageviews
    FROM log_visite
    WHERE giorno >= DATE('now', '-7 days')
    GROUP BY giorno
    ORDER BY giorno ASC
    ''')
    trend_giornaliero = [dict(r) for r in cursor.fetchall()]
    
    # Rilevamento e distribuzione Nazioni visitatori
    cursor.execute('''
    SELECT codice_paese, paese, COUNT(DISTINCT ip_hash) as visitatori, COUNT(*) as pageviews
    FROM log_visite
    GROUP BY codice_paese
    ORDER BY visitatori DESC, pageviews DESC
    LIMIT 20
    ''')
    nazioni_raw = cursor.fetchall()
    distribuzione_nazioni = []
    for r in nazioni_raw:
        item = dict(r)
        code = item['codice_paese'] or 'IT'
        item['bandiera'] = COUNTRY_FLAGS.get(code, '🌐')
        item['paese'] = COUNTRY_NAMES.get(code, item['paese'] or code)
        item['percentuale'] = round((item['visitatori'] / max(1, visitatori_unici_totali)) * 100, 1)
        distribuzione_nazioni.append(item)
        
    # 2. Metriche Tiratori / Utenti
    cursor.execute('SELECT COUNT(*) FROM utenti')
    totale_utenti = cursor.fetchone()[0] or 0
    
    cursor.execute('''
    SELECT u.id, u.username, u.email, u.is_admin, u.created_at,
           COUNT(r.id) as ricette_count
    FROM utenti u
    LEFT JOIN ricette_utente r ON u.id = r.user_id
    GROUP BY u.id
    ORDER BY u.id DESC
    LIMIT 25
    ''')
    utenti_recenti = [dict(r) for r in cursor.fetchall()]
    
    # 3. Metriche Ricette Personali
    cursor.execute('SELECT COUNT(*) FROM ricette_utente')
    totale_ricette = cursor.fetchone()[0] or 0
    
    cursor.execute('''
    SELECT r.*, u.username as operatore
    FROM ricette_utente r
    LEFT JOIN utenti u ON r.user_id = u.id
    ORDER BY r.id DESC
    LIMIT 20
    ''')
    ultime_ricette = [dict(r) for r in cursor.fetchall()]
    
    # 4. Metriche Tabelle e Ricarica
    cursor.execute('SELECT COUNT(*) FROM tabelle_ricarica')
    totale_tabelle = cursor.fetchone()[0] or 0
    
    cursor.execute('SELECT COUNT(*) FROM tabelle_ricarica WHERE user_id IS NULL')
    tabelle_cip = cursor.fetchone()[0] or 0
    
    cursor.execute('SELECT COUNT(*) FROM tabelle_ricarica WHERE user_id IS NOT NULL')
    tabelle_custom = cursor.fetchone()[0] or 0
    
    cursor.execute('SELECT COUNT(*) FROM impostazioni_utente')
    totale_preset = cursor.fetchone()[0] or 0
    
    # 5. Top Calibri Più Popolari
    cursor.execute('''
    SELECT calibro, COUNT(*) as count 
    FROM (
        SELECT calibro FROM ricette_utente
        UNION ALL
        SELECT calibro FROM tabelle_ricarica
    )
    WHERE calibro IS NOT NULL AND calibro != ''
    GROUP BY calibro
    ORDER BY count DESC
    LIMIT 8
    ''')
    top_calibri = [dict(r) for r in cursor.fetchall()]
    
    # 6. Top Polveri Più Utilizzate
    cursor.execute('''
    SELECT tipo_polvere as polvere, COUNT(*) as count
    FROM tabelle_ricarica
    WHERE tipo_polvere IS NOT NULL AND tipo_polvere != ''
    GROUP BY tipo_polvere
    ORDER BY count DESC
    LIMIT 8
    ''')
    top_polveri = [dict(r) for r in cursor.fetchall()]
    
    conn.close()
    
    return jsonify({
        'success': True,
        'kpi': {
            'visitatori_totali': visitatori_unici_totali,
            'pageviews_totali': pageviews_totali,
            'visitatori_oggi': visitatori_oggi,
            'pageviews_oggi': pageviews_oggi,
            'visitatori_7gg': visitatori_7gg,
            'totale_utenti': totale_utenti,
            'totale_ricette': totale_ricette,
            'totale_tabelle': totale_tabelle,
            'tabelle_cip': tabelle_cip,
            'tabelle_custom': tabelle_custom,
            'totale_preset': totale_preset
        },
        'trend_giornaliero': trend_giornaliero,
        'nazioni': distribuzione_nazioni,
        'utenti_recenti': utenti_recenti,
        'ultime_ricette': ultime_ricette,
        'top_calibri': top_calibri,
        'top_polveri': top_polveri,
        'timestamp': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    })

@app.route('/api/admin/ricette/<int:recipe_id>', methods=['DELETE'])
def admin_delete_ricetta(recipe_id):
    if not admin_required():
        return jsonify({'success': False, 'error': 'Non autorizzato'}), 403
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM ricette_utente WHERE id = ?', (recipe_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Ricetta rimossa dal moderatore.'})

@app.route('/api/admin/tabelle/<int:table_id>', methods=['DELETE'])
def admin_delete_tabella(table_id):
    if not admin_required():
        return jsonify({'success': False, 'error': 'Non autorizzato'}), 403
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tabelle_ricarica WHERE id = ?', (table_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Riferimento eliminato dal database.'})

@app.route('/api/admin/utenti/<int:target_user_id>', methods=['DELETE'])
def admin_delete_utente(target_user_id):
    if not admin_required():
        return jsonify({'success': False, 'error': 'Non autorizzato'}), 403
    if target_user_id == session.get('user_id'):
        return jsonify({'success': False, 'error': 'Non puoi eliminare il tuo stesso account superuser.'}), 400
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM ricette_utente WHERE user_id = ?', (target_user_id,))
    cursor.execute('DELETE FROM impostazioni_utente WHERE user_id = ?', (target_user_id,))
    cursor.execute('DELETE FROM tabelle_ricarica WHERE user_id = ?', (target_user_id,))
    cursor.execute('DELETE FROM utenti WHERE id = ?', (target_user_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Account operatore e dati associati eliminati con successo.'})

# ============================================================
# SEO & CRAWLER ENDPOINTS: ROBOTS.TXT, SITEMAP.XML, FAVICON
# ============================================================
@app.route('/robots.txt')
def robots_txt():
    """Direttive di crawling per motori di ricerca (Googlebot, Bingbot, ecc.)"""
    base_url = request.host_url.rstrip('/')
    # Fallback to production URL if behind proxy or localhost
    if '127.0.0.1' in base_url or 'localhost' in base_url:
        site_url = 'https://ricarica-balistica.onrender.com'
    else:
        site_url = base_url
        
    content = f"""User-agent: *
Allow: /
Disallow: /admin
Disallow: /api/admin/

Sitemap: {site_url}/sitemap.xml
"""
    return Response(content, mimetype='text/plain')

@app.route('/sitemap.xml')
def sitemap_xml():
    """Mappa del sito XML per indicizzazione istantanea delle pagine e strumenti"""
    today = datetime.utcnow().strftime('%Y-%m-%d')
    base_url = request.host_url.rstrip('/')
    if '127.0.0.1' in base_url or 'localhost' in base_url:
        site_url = 'https://ricarica-balistica.onrender.com'
    else:
        site_url = base_url

    content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9
        http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">
  <url>
    <loc>{site_url}/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>"""
    return Response(content, mimetype='application/xml')

@app.route('/favicon.ico')
def favicon():
    """Icona standard del sito per browser e crawler"""
    icon_path = os.path.join(app.root_path, 'static', 'img', 'favicon.svg')
    if os.path.exists(icon_path):
        return send_file(icon_path, mimetype='image/svg+xml')
    return ('', 204)

@app.route('/googlec4d8d72365b0f7d7.html')
def google_search_console_verification():
    """Verifica di proprietà per Google Search Console"""
    return Response('google-site-verification: googlec4d8d72365b0f7d7.html', mimetype='text/html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5055))
    print(f"[*] Avvio Tactical Reload & Ballistics Hub su http://127.0.0.1:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
