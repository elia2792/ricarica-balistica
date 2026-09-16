import unittest
import json
import io
from app import app, init_db

class TacticalReloadTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        init_db()
        from app import get_db_connection
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("DELETE FROM utenti WHERE username LIKE 'operatore_%' OR username LIKE 'test_%' OR username LIKE 'tiratore_%'")
        c.execute("DELETE FROM ricette_utente WHERE titolo_ricetta LIKE '%Alfa%' OR titolo_ricetta LIKE '%Sniper%' OR titolo_ricetta LIKE '%Moderare%'")
        c.execute("DELETE FROM tabelle_ricarica WHERE calibro LIKE '%Test%' OR calibro LIKE '%Custom%'")
        c.execute("DELETE FROM log_visite")
        conn.commit()
        conn.close()

    def tearDown(self):
        from app import get_db_connection
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("DELETE FROM log_visite")
        conn.commit()
        conn.close()

    def test_home_page(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'BALLISTIC OPS', res.data)
        self.assertIn(b'AVVERTENZA LEGALE SULLA SICUREZZA', res.data)

    def test_get_tabelle(self):
        res = self.client.get('/api/tabelle')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(len(data['tabelle']) > 15)
        self.assertIn('calibri', data)
        res_filter = self.client.get('/api/tabelle?calibro=9x19 Luger / 9x21 IMI')
        data_filter = json.loads(res_filter.data)
        self.assertTrue(all('9x19' in row['calibro'] for row in data_filter['tabelle']))

    def test_auth_and_recipe_isolation(self):
        # 1. Registra Operatore Alfa
        res_reg = self.client.post('/api/auth/register', json={
            'username': 'operatore_alfa',
            'password': 'password123',
            'email': 'alfa@armory.it'
        })
        self.assertEqual(res_reg.status_code, 200)
        data_reg = json.loads(res_reg.data)
        self.assertTrue(data_reg['success'])
        self.assertEqual(data_reg['user']['username'], 'operatore_alfa')

        # 2. Crea ricetta per Operatore Alfa
        res_recipe_alfa = self.client.post('/api/ricette', json={
            'calibro': '9x19 Luger / 9x21 IMI',
            'titolo_ricetta': 'Alfa Special 9mm',
            'marca_peso_palla': 'Alsa Pro 124gr',
            'marca_tipo_polvere': 'Vihtavuori N320',
            'dose_grani': 4.2,
            'oal_scelto': 29.1,
            'note_prestazione': 'Solo per Alfa'
        })
        self.assertEqual(res_recipe_alfa.status_code, 200)
        alfa_recipe_id = json.loads(res_recipe_alfa.data)['id']

        # 3. Verifica che Alfa veda la sua ricetta
        res_list_alfa = self.client.get('/api/ricette')
        data_list_alfa = json.loads(res_list_alfa.data)
        self.assertTrue(any(r['titolo_ricetta'] == 'Alfa Special 9mm' for r in data_list_alfa['ricette']))

        # 4. Logout Alfa
        self.client.post('/api/auth/logout')

        # 5. Registra Operatore Bravo
        res_reg_b = self.client.post('/api/auth/register', json={
            'username': 'operatore_bravo',
            'password': 'password456',
            'email': 'bravo@armory.it'
        })
        self.assertEqual(res_reg_b.status_code, 200)

        # 6. Verifica che Bravo NON veda la ricetta di Alfa
        res_list_bravo = self.client.get('/api/ricette')
        data_list_bravo = json.loads(res_list_bravo.data)
        self.assertFalse(any(r['titolo_ricetta'] == 'Alfa Special 9mm' for r in data_list_bravo['ricette']))

        # 7. Verifica che Bravo non possa eliminare la ricetta di Alfa (Forbidden 403)
        res_del = self.client.delete(f'/api/ricette/{alfa_recipe_id}')
        self.assertEqual(res_del.status_code, 403)

    def test_user_presets(self):
        # Registra utente
        self.client.post('/api/auth/register', json={
            'username': 'operatore_test_presets',
            'password': 'password123'
        })
        
        # Salva preset custom
        preset_data = {
            'costo_pacco_palle': 120.0,
            'quantita_pacco_palle': 1000,
            'costo_pacco_inneschi': 70.0,
            'quantita_pacco_inneschi': 1000,
            'costo_pacco_bossoli': 30.0,
            'quantita_pacco_bossoli': 100,
            'costo_barattolo_polvere': 75.0,
            'peso_barattolo_g': 500.0,
            'dose_grani': 4.3,
            'costo_bossolo_nuovo': 0.30,
            'ricariche_previste': 8,
            'chrono_stringa': '319.5, 321.0, 320.2',
            'chrono_unita': 'ms'
        }
        res_save = self.client.post('/api/user/presets', json=preset_data)
        self.assertEqual(res_save.status_code, 200)

        # Recupera preset
        res_get = self.client.get('/api/user/presets')
        self.assertEqual(res_get.status_code, 200)
        data = json.loads(res_get.data)
        self.assertEqual(data['presets']['costo_pacco_palle'], 120.0)
        self.assertEqual(data['presets']['costo_pacco_bossoli'], 30.0)
        self.assertEqual(data['presets']['quantita_pacco_bossoli'], 100)
        self.assertEqual(data['presets']['ricariche_previste'], 8)

    def test_calcolo_costo(self):
        payload_pacco = {
            'costo_pacco_palle': 105.0,
            'quantita_pacco_palle': 1000,
            'costo_pacco_inneschi': 65.0,
            'quantita_pacco_inneschi': 1000,
            'costo_pacco_bossoli': 25.0,
            'quantita_pacco_bossoli': 100,
            'costo_barattolo_polvere': 68.0,
            'peso_barattolo_g': 500,
            'dose_grani': 4.2,
            'ricariche_previste': 5
        }
        res_pacco = self.client.post('/calcola_costo', json=payload_pacco)
        self.assertEqual(res_pacco.status_code, 200)
        data_pacco = json.loads(res_pacco.data)
        self.assertEqual(data_pacco['costo_palla'], 0.105)
        self.assertEqual(data_pacco['costo_innesco'], 0.065)
        self.assertEqual(data_pacco['costo_bossolo_singolo'], 0.25)
        self.assertEqual(data_pacco['quota_bossolo_ammortizzata'], 0.05)
        self.assertAlmostEqual(data_pacco['costo_singolo'], 0.105 + 0.065 + data_pacco['costo_polvere_colpo'] + 0.05, places=3)

    def test_calcolo_balistica(self):
        payload = {
            'peso_palla_grani': 124,
            'velocita': 320,
            'unita': 'ms'
        }
        res = self.client.post('/calcola_balistica', json=payload)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertAlmostEqual(data['pf'], 130.2, places=1)
        self.assertAlmostEqual(data['joule'], 303.6, places=0)
        self.assertIn('MINOR', data['status_pf'])

    def test_calcola_sd(self):
        payload = {
            'velocita_stringa': '315.0, 318.0, 316.0, 319.0, 317.0',
            'unita': 'ms'
        }
        res = self.client.post('/calcola_sd', json=payload)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['count'], 5)
        self.assertEqual(data['media'], 317.0)
        self.assertAlmostEqual(data['sd'], 1.58, places=1)
        self.assertEqual(data['es'], 4.0)
        self.assertIn('MATCH GRADE', data['giudizio'])

    def test_esporta_pdf(self):
        res = self.client.get('/esporta_etichetta_pdf?calibro=9x19+Luger&dose=4.2+grs&polvere=Vihtavuori+N320')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.mimetype, 'application/pdf')
        self.assertTrue(res.data.startswith(b'%PDF'))
        self.assertGreater(len(res.data), 1000)

    def test_custom_calibro_and_csv(self):
        # 1. Registra e autentica utente
        self.client.post('/api/auth/register', json={
            'username': 'operatore_ballistic_custom',
            'password': 'password123'
        })

        # 2. Inserimento manuale nuovo calibro personalizzato
        res_post = self.client.post('/api/tabelle', json={
            'calibro': '6.5 Creedmoor Custom',
            'produttore_polvere': 'Reload Swiss',
            'tipo_polvere': 'RS60 Test',
            'peso_palla_grani': 140.0,
            'dose_min_grani': 39.5,
            'dose_max_grani': 42.8,
            'oal_consigliato': 71.5,
            'note': 'Test Hornady ELD-M'
        })
        self.assertEqual(res_post.status_code, 200)
        data_post = json.loads(res_post.data)
        self.assertTrue(data_post['success'])
        custom_id = data_post['id']

        # 3. Verifica presenza nella lista tabelle e nel filtro calibri
        res_list = self.client.get('/api/tabelle')
        self.assertEqual(res_list.status_code, 200)
        data_list = json.loads(res_list.data)
        self.assertIn('6.5 Creedmoor Custom', data_list['calibri'])
        found = next((t for t in data_list['tabelle'] if t['id'] == custom_id), None)
        self.assertIsNotNone(found)
        self.assertTrue(found['is_custom'])
        self.assertTrue(found['can_delete'])

        # 4. Download template CSV
        res_tpl = self.client.get('/api/tabelle/template-csv')
        self.assertEqual(res_tpl.status_code, 200)
        self.assertIn(b'calibro,produttore_polvere', res_tpl.data)

        # 5. Upload CSV massivo
        csv_sample = (
            "calibro,produttore_polvere,tipo_polvere,peso_palla_grani,dose_min_grani,dose_max_grani,oal_consigliato,note\n"
            ".300 AAC Blackout Test,Vihtavuori,N110 Custom,125.0,17.0,19.2,54.0,Test Sub/Sup\n"
            "7.62x39 Soviet Test,Lovex,D073.4,123.0,24.0,26.5,56.0,Test AK\n"
        )
        res_csv = self.client.post('/api/tabelle/upload-csv', json={'csv_text': csv_sample})
        self.assertEqual(res_csv.status_code, 200)
        data_csv = json.loads(res_csv.data)
        self.assertTrue(data_csv['success'])
        self.assertEqual(data_csv['count'], 2)

        # 6. Verifica che i calibri CSV compaiano nel DB
        res_check = self.client.get('/api/tabelle?calibro=.300 AAC Blackout Test')
        data_check = json.loads(res_check.data)
        self.assertEqual(len(data_check['tabelle']), 1)
        self.assertEqual(data_check['tabelle'][0]['tipo_polvere'], 'N110 Custom')

        # 7. Cancellazione voce custom
        res_del = self.client.delete(f'/api/tabelle/{custom_id}')
        self.assertEqual(res_del.status_code, 200)
        self.assertTrue(json.loads(res_del.data)['success'])

        # 8. Verifica che non si possano cancellare le tabelle CIP ufficiali (id 1 ha user_id NULL)
        res_del_cip = self.client.delete('/api/tabelle/1')
        self.assertEqual(res_del_cip.status_code, 403)

    def test_admin_dashboard_and_visitor_stats(self):
        # 1. Simula visite con header di lingua e proxy
        self.client.get('/', headers={'Accept-Language': 'it-IT,it;q=0.9', 'User-Agent': 'TestBrowser/1.0'})
        self.client.get('/', headers={'CF-IPCountry': 'CH', 'User-Agent': 'TestBrowser/1.0'})
        self.client.get('/', headers={'CF-IPCountry': 'US', 'User-Agent': 'TestBrowser/1.0'})

        # 2. Accesso non autorizzato da ospite
        res_stats_guest = self.client.get('/api/admin/stats')
        self.assertEqual(res_stats_guest.status_code, 403)

        # 3. Accesso da utente normale (non admin)
        self.client.post('/api/auth/register', json={
            'username': 'tiratore_semplice',
            'password': 'password123'
        })
        res_stats_user = self.client.get('/api/admin/stats')
        self.assertEqual(res_stats_user.status_code, 403)

        # 4. Logout e Login come Superuser Admin con password ad alta sicurezza
        self.client.post('/api/auth/logout')
        res_admin_login = self.client.post('/api/auth/login', json={
            'username': 'admin',
            'password': 'Armory$Admin#2026!SecOps'
        })
        self.assertEqual(res_admin_login.status_code, 200)
        data_login = json.loads(res_admin_login.data)
        self.assertTrue(data_login['user']['is_admin'])

        # 5. Accesso alla pagina HTML Dashboard Admin
        res_dash = self.client.get('/admin')
        self.assertEqual(res_dash.status_code, 200)
        self.assertIn(b'HQ ADMIN COMMAND CENTER', res_dash.data)
        self.assertIn(b'Provenienza Geografica dei Visitatori', res_dash.data)

        # 6. Accesso API statistiche complete
        res_stats = self.client.get('/api/admin/stats')
        self.assertEqual(res_stats.status_code, 200)
        stats = json.loads(res_stats.data)
        self.assertTrue(stats['success'])

        # Verifica KPI visitatori e metriche
        kpi = stats['kpi']
        self.assertGreaterEqual(kpi['visitatori_totali'], 1)
        self.assertGreaterEqual(kpi['pageviews_totali'], 3)
        self.assertGreaterEqual(kpi['visitatori_oggi'], 1)
        self.assertGreaterEqual(kpi['totale_utenti'], 1)

        # Verifica nazioni rilevate
        nazioni = stats['nazioni']
        self.assertGreaterEqual(len(nazioni), 1)
        self.assertTrue(any(n['codice_paese'] in ('IT', 'CH', 'US') for n in nazioni))

        # 7. Test eliminazione ricetta da Admin
        # Crea ricetta con utente
        conn = self.client.application.view_functions  # check DB connection
        from app import get_db_connection
        conn_db = get_db_connection()
        cur = conn_db.cursor()
        cur.execute("INSERT INTO ricette_utente (calibro, titolo_ricetta) VALUES ('9x19 Luger', 'Ricetta da Moderare')")
        mod_id = cur.lastrowid
        conn_db.commit()
        conn_db.close()

        res_del_rec = self.client.delete(f'/api/admin/ricette/{mod_id}')
        self.assertEqual(res_del_rec.status_code, 200)
        self.assertTrue(json.loads(res_del_rec.data)['success'])

    def test_seo_endpoints(self):
        # 1. Test robots.txt
        res_robots = self.client.get('/robots.txt')
        self.assertEqual(res_robots.status_code, 200)
        self.assertEqual(res_robots.mimetype, 'text/plain')
        self.assertIn(b'User-agent: *', res_robots.data)
        self.assertIn(b'Allow: /', res_robots.data)
        self.assertIn(b'Disallow: /admin', res_robots.data)
        self.assertIn(b'Sitemap:', res_robots.data)

        # 2. Test sitemap.xml
        res_sitemap = self.client.get('/sitemap.xml')
        self.assertEqual(res_sitemap.status_code, 200)
        self.assertEqual(res_sitemap.mimetype, 'application/xml')
        self.assertIn(b'<urlset', res_sitemap.data)
        self.assertIn(b'https://ricarica-balistica.onrender.com/', res_sitemap.data)
        self.assertIn(b'<changefreq>daily</changefreq>', res_sitemap.data)

        # 3. Test favicon.ico
        res_fav = self.client.get('/favicon.ico')
        self.assertEqual(res_fav.status_code, 200)
        self.assertIn(b'<svg', res_fav.data)

        # 4. Test Home SEO tags & Schema.org JSON-LD
        res_home = self.client.get('/')
        self.assertEqual(res_home.status_code, 200)
        self.assertIn(b'<title>Ricarica Munizioni', res_home.data)
        self.assertIn(b'name="description"', res_home.data)
        self.assertIn(b'name="keywords"', res_home.data)
        self.assertIn(b'name="robots"', res_home.data)
        self.assertIn(b'rel="canonical"', res_home.data)
        self.assertIn(b'property="og:image"', res_home.data)
        self.assertIn(b'name="twitter:card"', res_home.data)
        self.assertIn(b'application/ld+json', res_home.data)
        self.assertIn(b'WebApplication', res_home.data)
        self.assertIn(b'FAQPage', res_home.data)
        self.assertIn(b'Guida alla Ricarica Munizioni', res_home.data)

if __name__ == '__main__':
    unittest.main()


