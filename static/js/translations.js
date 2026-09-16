// Tactical Reload & Ballistics Hub - i18n Translations Dictionary
// Supported languages: it (Italiano), en (English), fr (Français), es (Español), pt (Português)

const TRANSLATIONS = {
  it: {
    lang_name: "Italiano",
    flag: "🇮🇹",
    nav_title: "BALLISTIC OPS // RICARICA MUNIZIONI & BALISTICA",
    nav_sub: "Tabelle CIP • Calcolo Costo Cartuccia • Quaderno di Ricarica • Etichette PDF",
    nav_cip_online: "CIP DATABASE: ONLINE",
    nav_login_btn: "ACCEDI // REGISTRATI",
    nav_operator: "OPERATORE:",
    nav_admin: "PANNELLO ADMIN",
    nav_test_pdf: "TEST PDF",
    nav_logout_title: "Disconnetti account",

    sec1_title: "1. Tabelle Ufficiali di Ricarica (CIP & Personalizzate)",
    sec1_add_btn: "+ Calibro / Polvere",
    sec1_select_cal: "Seleziona Calibro:",
    sec1_all_cal: "TUTTI I CALIBRI (Canna Rigata & Liscia)",
    th_cal_bullet: "Calibro / Palla",
    th_powder: "Polvere",
    th_min_charge: "Dose Min (grs)",
    th_max_charge: "Dose Max (grs)",
    th_oal: "OAL (mm)",
    th_action: "Azione",
    tb_init: "Inizializzazione database...",
    tb_custom_badge: "CUSTOM",
    tb_cip_badge: "CIP",
    tb_use_btn: "Usa",
    tb_delete_title: "Elimina riferimento personalizzato",
    tb_empty: "Nessun dato di ricarica trovato.",

    sec2_title: "2. Quaderno di Ricarica & Ricette Salvate",
    sec2_new_btn: "+ Nuova Ricetta",
    sec2_preset_btn: "Salva Come Predefinito",
    guest_alert: "Stai operando come Ospite. Le ricette sono salvate nella memoria locale di questa sessione. Accedi per sincronizzare in Cloud su tutti i tuoi dispositivi.",
    user_alert_prefix: "Connesso come",
    user_alert_suffix: "• Sincronizzazione automatica Cloud attiva",
    lbl_recipe_title: "Titolo Ricetta / Matricola Lotto",
    lbl_calibre: "Calibro",
    lbl_bullet: "Marca & Peso Palla (grani)",
    lbl_powder: "Tipo Polvere & Dose (grs)",
    lbl_primer: "Marca / Tipo Innesco",
    lbl_oal: "O.A.L. Complessivo (mm)",
    lbl_crimping: "Crimpatura",
    lbl_firearm: "Arma / Passo di Rigatura / Canna",
    lbl_notes: "Note Balistiche / Velocità Rilevata",
    btn_save_recipe: "SALVA NEL QUADERNO",
    btn_pdf_label: "STAMPA ETICHETTA PDF",
    th_rec_title: "Ricetta / Calibro",
    th_rec_details: "Palla & Polvere",
    th_rec_oal: "OAL",
    th_rec_date: "Data",
    th_rec_actions: "Azioni",
    btn_load: "Carica",
    btn_delete: "Elimina",
    no_recipes: "Nessuna ricetta salvata nel quaderno.",

    sec3_title: "3. Calcolatore Costo Cartuccia & Risparmio",
    sec3_badge: "ECONOMIC OPS",
    sec3_tab_cartridge: "[COSTO CARTUCCIA]",
    sec3_tab_amort: "[AMMORTAMENTO ATTREZZATURA]",
    c_powder_box: "Polvere da Sparo (Costo Barattolo + Dose Ricetta)",
    c_powder_label: "Costo Barattolo (€)",
    c_powder_weight: "Peso Barattolo (g)",
    c_pack_bullet: "Confezione Palle / Ogive",
    c_pack_primer: "Confezione Inneschi",
    c_pack_cost: "Costo Pacco (€)",
    c_pack_qty: "Quantità (pz)",
    c_brass_box: "Bossoli (Quota Ammortamento Riutilizzo)",
    c_brass_label: "Costo Singolo Bossolo (€)",
    c_brass_uses: "Riutilizzi Stimati",
    c_res_round_cost: "Costo Singolo Colpo",
    c_res_box50: "Costo Scatola 50 pz",
    c_res_factory_box: "Costo Commerciale Scatola (€)",
    c_res_saving: "Risparmio a Colpo",
    c_res_pct_saving: "Risparmio sul Commerciale",
    c_press_cost: "Costo Totale Attrezzatura (Pressa, Dies, Bilancina) (€)",
    c_amort_shots: "Colpi per Ammortizzare la Spesa",
    c_amort_boxes: "Scatole da 50 colpi necessarie",
    c_amort_desc: "Ogni colpo ricaricato ti fa risparmiare rispetto al prezzo di acquisto delle munizioni commerciali.",

    sec4_title: "4. Balistica Terminale & IPSC Power Factor",
    sec4_badge: "DYNAMIC SHOOTING",
    b_bullet_weight: "Peso Palla (grani - gn)",
    b_speed: "Velocità alla Volata",
    b_speed_unit: "Unità Velocità",
    b_res_pf: "Power Factor",
    b_res_joule: "Energia Cinetica",
    b_res_fps: "Velocità fps",
    b_res_ms: "Velocità m/s",
    b_comp_class: "Classificazione Competizione:",
    ipsc_minor: "MINOR // IDONEO GARA",
    ipsc_major: "MAJOR // POTENZA MASSIMA",
    ipsc_subminor: "NON IDONEO // SOTTOFATTORE (<125)",

    sec5_title: "5. Analizzatore Cronografo // SD & Extreme Spread",
    chrono_badge: "CHRONO STATS",
    chrono_string_lbl: "Stringa Velocità Cronografate (separate da virgola o spazio)",
    btn_calc_sd: "Calcola SD & Extreme Spread",
    sd_mean_speed: "Velocità Media",
    sd_dev: "Standard Dev (SD)",
    sd_es: "Extreme Spread (ES)",
    sd_shots_detected: "Colpi Rilevati",
    sd_consistency_lbl: "Qualità Costanza Balistica:",
    sd_grade_match: "MATCH GRADE // ECCELLENTE",
    sd_grade_good: "BUONA COSTANZA // STANDARD",
    sd_grade_check: "DISPERSIONE ELEVATA // VERIFICA DOSAGGIO",

    faq_title: "Guida alla Ricarica Munizioni, Tabelle CIP & Domande Frequenti (FAQ)",
    faq_sub: "Riferimenti tecnici su dosaggi polvere, standard C.I.P. e analisi economica del colpo ricaricato",
    faq1_q: "1. Come consultare le Tabelle di Ricarica CIP e determinare la Carica di Lancio?",
    faq1_a: "Le tabelle ufficiali CIP e dei produttori (Vihtavuori, Cheddite, Baschieri & Pellagri, Lovex, Reload Swiss, Hodgdon) stabiliscono la dose minima di partenza da cui avviare sempre i test, la dose massima da non superare mai, la quota O.A.L. (lunghezza complessiva cartuccia) e i pesi palla consigliati in grani.",
    faq2_q: "2. Come calcolare il Costo Reale per Cartuccia e l'Ammortamento della Pressa?",
    faq2_a: "Il costo del singolo colpo è dato da: Costo Palla + Costo Innesco + (Dose in Grani × Costo Polvere per Grano) + (Costo Bossolo / Riutilizzi). Confrontandolo con le cartucce commerciali si determina il risparmio netto e il punto di pareggio per ammortizzare pressa, dies e accessori.",
    faq3_q: "3. Fattore di Potenza IPSC (Power Factor) e Deviazione Standard al Cronografo",
    faq3_a: "Il Power Factor IPSC = [Peso Palla (grani) × Velocità (fps)] / 1000, dividendo le cariche tra Minor (≥125) e Major. L'analisi cronografica calcola Media, SD (Deviazione Standard) ed ES (Extreme Spread). Valori di SD inferiori a 3 m/s certificano una ricarica Match Grade.",
    faq4_q: "4. Quali sono i segnali di Sovrapressione e le Regole Fondamentali di Sicurezza?",
    faq4_a: "Iniziare sempre dalla dose minima (+10% di margine di sicurezza). Verificare segni di sovrapressione sui bossoli sparati: appiattimento innesco (flattening), craterizzazione attorno al percussore ed estrazione dura. Conservare propellenti e inneschi in luoghi freschi e asciutti.",
    faq5_q: "5. Come stampare le Etichette Tecniche PDF per le Scatole di Munizioni?",
    faq5_a: "Cliccando su 'STAMPA ETICHETTA PDF' dal quaderno o dal menu, si ottiene un foglio PDF vettoriale ad alta risoluzione con layout chiaro per scatole da 50 o 100 colpi, completo di calibro, dose, polvere, OAL, lotto e data.",

    disclaimer_collapsed: "AVVERTENZA LEGALE CIP / SAAMI & SICUREZZA PROPELLENTI",
    disclaimer_expand: "Espandi Avvertenze",
    disclaimer_collapse: "Riduci / Abbassa",
    disclaimer_title: "⚠️ AVVERTENZA LEGALE SULLA SICUREZZA E MANIPOLAZIONE DI PROPELLENTI ED ESPLODENTI:",
    disclaimer_text: "La ricarica domestica di munizioni richiede competenza, attrezzature adeguate e rispetto rigoroso delle normative di pubblica sicurezza. I propellenti, gli inneschi e le munizioni finite sono sostanze esplodenti o deflagranti che generano altissime pressioni. Le dosi e i parametri qui forniti hanno mero valore informativo, bibliografico e sperimentale. L'utente è l'unico responsabile del rispetto dei limiti pressori C.I.P. e SAAMI, della verifica dello stato dei bossoli e dell'assoluta conformità alle leggi vigenti. Gli autori della piattaforma declinano ogni responsabilità diretta o indiretta per incidenti, danni a persone, animali, cose o armi.",

    modal_tab_title: "CARICA NUOVO CALIBRO O POLVERE",
    modal_tab_sub: "Espandi il database con le tue dosi di ricarica e calibri inediti",
    tab_manual: "[INSERIMENTO RAPIDO]",
    tab_csv: "[IMPORTA DA CSV]",
    lbl_nt_calibre: "Calibro",
    lbl_nt_powder_mfg: "Produttore Polvere",
    lbl_nt_powder_type: "Tipo / Nome Polvere",
    lbl_nt_bullet_weight: "Peso Palla (grani)",
    lbl_nt_dose_min: "Dose Min (grs)",
    lbl_nt_dose_max: "Dose Max (grs)",
    lbl_nt_oal: "O.A.L. Consigliato (mm)",
    lbl_nt_notes: "Note Tecniche / Canna / Innesco",
    btn_save_db: "SALVA NEL DATABASE",
    csv_format_title: "FORMATO CSV SUPPORTATO:",
    btn_download_template: "SCARICA TEMPLATE CSV",
    lbl_csv_file: "Seleziona File CSV (.csv):",
    lbl_csv_paste: "Oppure incolla qui il testo CSV:",
    btn_import_csv: "IMPORTA TABELLE CSV",

    modal_auth_title: "AUTORIZZAZIONE OPERATORE",
    modal_auth_sub: "Gestione Account Personale & Sincronizzazione Cloud",
    tab_login: "[ACCESSO]",
    tab_register: "[REGISTRATI]",
    lbl_username: "Nome Operatore / Username",
    lbl_email: "Email (Facoltativa)",
    lbl_password: "Password di Sicurezza",
    btn_auth_login: "AUTORIZZA ACCESSO",
    btn_auth_register: "REGISTRA NUOVO OPERATORE"
  },

  en: {
    lang_name: "English",
    flag: "🇬🇧",
    nav_title: "BALLISTIC OPS // AMMO RELOADING & BALLISTICS",
    nav_sub: "CIP Load Data • Cartridge Cost Calculator • Reloading Logbook • PDF Labels",
    nav_cip_online: "CIP DATABASE: ONLINE",
    nav_login_btn: "LOGIN // REGISTER",
    nav_operator: "OPERATOR:",
    nav_admin: "ADMIN PANEL",
    nav_test_pdf: "TEST PDF",
    nav_logout_title: "Disconnect account",

    sec1_title: "1. Official Reloading Data (CIP & Custom Tables)",
    sec1_add_btn: "+ Caliber / Powder",
    sec1_select_cal: "Select Caliber:",
    sec1_all_cal: "ALL CALIBERS (Rifle & Pistol)",
    th_cal_bullet: "Caliber / Bullet",
    th_powder: "Powder",
    th_min_charge: "Min Charge (grs)",
    th_max_charge: "Max Charge (grs)",
    th_oal: "OAL (mm)",
    th_action: "Action",
    tb_init: "Initializing database...",
    tb_custom_badge: "CUSTOM",
    tb_cip_badge: "CIP",
    tb_use_btn: "Use",
    tb_delete_title: "Delete custom table",
    tb_empty: "No reloading data found.",

    sec2_title: "2. Reloading Logbook & Saved Recipes",
    sec2_new_btn: "+ New Recipe",
    sec2_preset_btn: "Save as Default",
    guest_alert: "You are currently operating as Guest. Recipes are stored locally in this session. Log in to sync your data in the Cloud across all your devices.",
    user_alert_prefix: "Connected as",
    user_alert_suffix: "• Cloud Auto-Sync active",
    lbl_recipe_title: "Recipe Title / Lot Number",
    lbl_calibre: "Caliber",
    lbl_bullet: "Bullet Brand & Weight (grains)",
    lbl_powder: "Powder Brand & Charge (grs)",
    lbl_primer: "Primer Brand / Type",
    lbl_oal: "Overall Length O.A.L. (mm)",
    lbl_crimping: "Crimping",
    lbl_firearm: "Firearm / Twist Rate / Barrel",
    lbl_notes: "Ballistic Notes / Chrono Velocity",
    btn_save_recipe: "SAVE TO LOGBOOK",
    btn_pdf_label: "PRINT PDF LABEL",
    th_rec_title: "Recipe / Caliber",
    th_rec_details: "Bullet & Powder",
    th_rec_oal: "OAL",
    th_rec_date: "Date",
    th_rec_actions: "Actions",
    btn_load: "Load",
    btn_delete: "Delete",
    no_recipes: "No recipes saved in logbook.",

    sec3_title: "3. Cartridge Cost Calculator & ROI Amortization",
    sec3_badge: "ECONOMIC OPS",
    sec3_tab_cartridge: "[CARTRIDGE COST]",
    sec3_tab_amort: "[EQUIPMENT AMORTIZATION]",
    c_powder_box: "Gunpowder (Canister Cost + Recipe Charge)",
    c_powder_label: "Canister Cost (€/$)",
    c_powder_weight: "Canister Weight (g)",
    c_pack_bullet: "Bullets / Projectiles Pack",
    c_pack_primer: "Primers Pack",
    c_pack_cost: "Pack Cost (€/$)",
    c_pack_qty: "Quantity (pcs)",
    c_brass_box: "Brass Cases (Amortization & Reuses)",
    c_brass_label: "Single Brass Cost (€/$)",
    c_brass_uses: "Estimated Reuses",
    c_res_round_cost: "Cost Per Single Round",
    c_res_box50: "Cost for 50-Round Box",
    c_res_factory_box: "Factory Ammo Box Cost (€/$)",
    c_res_saving: "Net Savings Per Round",
    c_res_pct_saving: "Savings vs Factory Ammo",
    c_press_cost: "Total Equipment Cost (Press, Dies, Scale) (€/$)",
    c_amort_shots: "Rounds Needed to Break Even",
    c_amort_boxes: "50-Round Boxes to Pay Off",
    c_amort_desc: "Every handloaded cartridge saves money compared to commercial store-bought ammunition.",

    sec4_title: "4. Terminal Ballistics & IPSC Power Factor",
    sec4_badge: "DYNAMIC SHOOTING",
    b_bullet_weight: "Bullet Weight (grains - gn)",
    b_speed: "Muzzle Velocity",
    b_speed_unit: "Speed Unit",
    b_res_pf: "Power Factor",
    b_res_joule: "Kinetic Energy",
    b_res_fps: "Velocity fps",
    b_res_ms: "Velocity m/s",
    b_comp_class: "Competition Classification:",
    ipsc_minor: "MINOR // MATCH LEGAL",
    ipsc_major: "MAJOR // MAX POWER",
    ipsc_subminor: "NOT ELIGIBLE // SUB-FACTOR (<125)",

    sec5_title: "5. Chronograph Analyzer // SD & Extreme Spread",
    chrono_badge: "CHRONO STATS",
    chrono_string_lbl: "Recorded Velocity String (comma or space separated)",
    btn_calc_sd: "Calculate SD & Extreme Spread",
    sd_mean_speed: "Average Velocity",
    sd_dev: "Standard Dev (SD)",
    sd_es: "Extreme Spread (ES)",
    sd_shots_detected: "Shots Recorded",
    sd_consistency_lbl: "Ballistic Consistency Rating:",
    sd_grade_match: "MATCH GRADE // EXCELLENT",
    sd_grade_good: "GOOD CONSISTENCY // STANDARD",
    sd_grade_check: "HIGH SPREAD // CHECK CHARGE WEIGHT",

    faq_title: "Reloading Guide, CIP Tables & Frequently Asked Questions (FAQ)",
    faq_sub: "Technical specifications on powder charges, CIP safety guidelines and reloading cost analysis",
    faq1_q: "1. How to read CIP Reloading Tables and determine start loads?",
    faq1_a: "Official CIP and manufacturer tables (Vihtavuori, Cheddite, Baschieri & Pellagri, Lovex, Reload Swiss, Hodgdon) define the safe starting charge to begin testing, the maximum safe charge that must never be exceeded, the recommended O.A.L. and bullet weights in grains.",
    faq2_q: "2. How to calculate real cost per round and reloading press ROI?",
    faq2_a: "Cost per round = Bullet Cost + Primer Cost + (Charge in Grains × Powder Cost per Grain) + (Brass Cost / Number of Reuses). Comparing this to factory ammo determines your net savings and the number of rounds required to pay off your press and dies.",
    faq3_q: "3. IPSC Power Factor and Standard Deviation (SD) at the Chronograph",
    faq3_a: "IPSC Power Factor = [Bullet Weight (grains) × Velocity (fps)] / 1000, separating charges into Minor (≥125) and Major. Chronograph statistical analysis computes Average, SD, and ES. An SD under 3 m/s (10 fps) certifies match-grade consistency.",
    faq4_q: "4. What are the signs of overpressure and core safety rules?",
    faq4_a: "Always start at the minimum starting charge. Inspect fired brass for overpressure signs: flattened primer cups, cratering around the firing pin indent, and sticky bolt lift. Always store powders and primers in a dry, cool location.",
    faq5_q: "5. How to print high-contrast PDF ammo box labels?",
    faq5_a: "Click 'PRINT PDF LABEL' from your logbook to download a vector PDF formatted for 50 or 100-round boxes (MTM, Plano) with toner-saving light background, showing caliber, charge, powder, OAL, lot and date.",

    disclaimer_collapsed: "LEGAL DISCLAIMER: CIP / SAAMI SAFETY & PROPELLANTS",
    disclaimer_expand: "Expand Safety Warning",
    disclaimer_collapse: "Minimize / Lower",
    disclaimer_title: "⚠️ LEGAL WARNING ON SAFETY AND PROPELLANT / EXPLOSIVE HANDLING:",
    disclaimer_text: "Handloading ammunition requires skill, appropriate tooling, and strict compliance with public safety laws. Powders, primers, and finished rounds generate extreme pressures. The charges and parameters provided here are for informational and experimental reference only. The user is solely responsible for observing CIP and SAAMI pressure limits. The authors disclaim all direct and indirect liability for accidents, injuries, or damage.",

    modal_tab_title: "ADD NEW CALIBER OR POWDER",
    modal_tab_sub: "Expand the database with your custom reloading recipes and calibers",
    tab_manual: "[MANUAL ENTRY]",
    tab_csv: "[IMPORT CSV]",
    lbl_nt_calibre: "Caliber",
    lbl_nt_powder_mfg: "Powder Manufacturer",
    lbl_nt_powder_type: "Powder Type / Name",
    lbl_nt_bullet_weight: "Bullet Weight (grains)",
    lbl_nt_dose_min: "Min Charge (grs)",
    lbl_nt_dose_max: "Max Charge (grs)",
    lbl_nt_oal: "Recommended O.A.L. (mm)",
    lbl_nt_notes: "Technical Notes / Barrel / Primer",
    btn_save_db: "SAVE TO DATABASE",
    csv_format_title: "SUPPORTED CSV FORMAT:",
    btn_download_template: "DOWNLOAD CSV TEMPLATE",
    lbl_csv_file: "Select CSV File (.csv):",
    lbl_csv_paste: "Or paste CSV text here:",
    btn_import_csv: "IMPORT CSV TABLES",

    modal_auth_title: "OPERATOR AUTHORIZATION",
    modal_auth_sub: "Personal Account Management & Cloud Synchronization",
    tab_login: "[LOGIN]",
    tab_register: "[REGISTER]",
    lbl_username: "Operator Username",
    lbl_email: "Email (Optional)",
    lbl_password: "Security Password",
    btn_auth_login: "AUTHORIZE ACCESS",
    btn_auth_register: "REGISTER NEW OPERATOR"
  },

  fr: {
    lang_name: "Français",
    flag: "🇫🇷",
    nav_title: "BALLISTIC OPS // RECHARGEMENT MUNITIONS & BALISTIQUE",
    nav_sub: "Tables CIP • Calculateur Coût Cartouche • Carnet de Tir • Étiquettes PDF",
    nav_cip_online: "CIP DATABASE: EN LIGNE",
    nav_login_btn: "CONNEXION // S'INSCRIRE",
    nav_operator: "OPÉRATEUR:",
    nav_admin: "PANNEAU ADMIN",
    nav_test_pdf: "TEST PDF",
    nav_logout_title: "Déconnecter le compte",

    sec1_title: "1. Tables Officielles de Rechargement (CIP & Personnalisées)",
    sec1_add_btn: "+ Calibre / Poudre",
    sec1_select_cal: "Sélectionner Calibre:",
    sec1_all_cal: "TOUS LES CALIBRES (Arme de poing & Carabine)",
    th_cal_bullet: "Calibre / Balle",
    th_powder: "Poudre",
    th_min_charge: "Charge Min (grs)",
    th_max_charge: "Charge Max (grs)",
    th_oal: "LHT / OAL (mm)",
    th_action: "Action",
    tb_init: "Initialisation base de données...",
    tb_custom_badge: "PERSO",
    tb_cip_badge: "CIP",
    tb_use_btn: "Utiliser",
    tb_delete_title: "Supprimer la table personnalisée",
    tb_empty: "Aucune donnée de rechargement trouvée.",

    sec2_title: "2. Carnet de Rechargement & Recettes Sauvegardées",
    sec2_new_btn: "+ Nouvelle Recette",
    sec2_preset_btn: "Enregistrer par Défaut",
    guest_alert: "Vous naviguez en mode Invité. Les recettes sont enregistrées localement pour cette session. Connectez-vous pour synchroniser dans le Cloud sur tous vos appareils.",
    user_alert_prefix: "Connecté en tant que",
    user_alert_suffix: "• Synchronisation Cloud active",
    lbl_recipe_title: "Titre Recette / Numéro de Lot",
    lbl_calibre: "Calibre",
    lbl_bullet: "Marque & Poids Balle (grains)",
    lbl_powder: "Type Poudre & Charge (grs)",
    lbl_primer: "Marque / Type Amorce",
    lbl_oal: "Longueur Totale O.A.L. (mm)",
    lbl_crimping: "Sertissage",
    lbl_firearm: "Arme / Pas de Rayure / Canon",
    lbl_notes: "Notes Balistiques / Vitesse Mesurée",
    btn_save_recipe: "ENREGISTRER DANS LE CARNET",
    btn_pdf_label: "IMPRIMER ÉTIQUETTE PDF",
    th_rec_title: "Recette / Calibre",
    th_rec_details: "Balle & Poudre",
    th_rec_oal: "OAL",
    th_rec_date: "Date",
    th_rec_actions: "Actions",
    btn_load: "Charger",
    btn_delete: "Supprimer",
    no_recipes: "Aucune recette enregistrée.",

    sec3_title: "3. Calculateur Coût Cartouche & Amortissement",
    sec3_badge: "ECONOMIC OPS",
    sec3_tab_cartridge: "[COÛT CARTOUCHE]",
    sec3_tab_amort: "[AMORTISSEMENT PRESSE]",
    c_powder_box: "Poudre (Prix Bidon + Charge Recette)",
    c_powder_label: "Prix du Bidon (€)",
    c_powder_weight: "Poids Bidon (g)",
    c_pack_bullet: "Boîte de Balles / Ogives",
    c_pack_primer: "Boîte d'Amorces",
    c_pack_cost: "Prix Boîte (€)",
    c_pack_qty: "Quantité (pcs)",
    c_brass_box: "Douilles (Amortissement & Réutilisations)",
    c_brass_label: "Prix Douille Unitaire (€)",
    c_brass_uses: "Réutilisations Estimées",
    c_res_round_cost: "Coût au Coup Simple",
    c_res_box50: "Coût Boîte de 50 coups",
    c_res_factory_box: "Prix Boîte Commerce (€)",
    c_res_saving: "Économie par Coup",
    c_res_pct_saving: "Économie vs Commerce",
    c_press_cost: "Coût Total Matériel (Presse, Outils, Balance) (€)",
    c_amort_shots: "Coups pour Rentabiliser l'Achat",
    c_amort_boxes: "Boîtes de 50 coups requises",
    c_amort_desc: "Chaque cartouche rechargée génère une économie nette par rapport aux munitions manufacturées.",

    sec4_title: "4. Balistique Terminale & Facteur IPSC",
    sec4_badge: "DYNAMIC SHOOTING",
    b_bullet_weight: "Poids Balle (grains - gn)",
    b_speed: "Vitesse Initiale",
    b_speed_unit: "Unité Vitesse",
    b_res_pf: "Power Factor",
    b_res_joule: "Énergie Cinétique",
    b_res_fps: "Vitesse fps",
    b_res_ms: "Vitesse m/s",
    b_comp_class: "Classification Compétition:",
    ipsc_minor: "MINOR // CONFORME MATCH",
    ipsc_major: "MAJOR // PUISSANCE MAX",
    ipsc_subminor: "NON HOMOLOGUÉ (<125)",

    sec5_title: "5. Analyseur Chronographe // Écart-Type (SD) & ES",
    chrono_badge: "CHRONO STATS",
    chrono_string_lbl: "Série de Vitesses (séparées par virgule ou espace)",
    btn_calc_sd: "Calculer SD & Extreme Spread",
    sd_mean_speed: "Vitesse Moyenne",
    sd_dev: "Écart-Type (SD)",
    sd_es: "Extreme Spread (ES)",
    sd_shots_detected: "Tirs Enregistrés",
    sd_consistency_lbl: "Qualité de Constance:",
    sd_grade_match: "MATCH GRADE // EXCELLENT",
    sd_grade_good: "BONNE CONSTANCE // STANDARD",
    sd_grade_check: "DISPERSION ÉLEVÉE // VÉRIFIER DOSAGE",

    faq_title: "Guide de Rechargement, Tables CIP & FAQ",
    faq_sub: "Directives techniques sur les charges de poudre, normes CIP et rentabilité du rechargement",
    faq1_q: "1. Comment lire les Tables CIP et choisir la charge de départ ?",
    faq1_a: "Les tables officielles CIP et des fabricants (Vihtavuori, Cheddite, Baschieri, Lovex, Reload Swiss, Hodgdon) définissent la charge minimale pour débuter, la charge maximale absolue à ne jamais dépasser, la longueur totale LHT/OAL et le poids de balle en grains.",
    faq2_q: "2. Comment calculer le coût réel par cartouche et amortir sa presse ?",
    faq2_a: "Coût cartouche = Balle + Amorce + (Charge en Grains × Coût Poudre par Grain) + (Douille / Nombre de Tirs). En comparant aux cartouches manufacturées, on calcule l'économie nette et le nombre de tirs pour rentabiliser la presse et les outils.",
    faq3_q: "3. Facteur de Puissance IPSC et Écart-Type (SD) au Chronographe",
    faq3_a: "Le facteur IPSC = [Poids Balle (grs) × Vitesse (fps)] / 1000 classe les munitions en Minor (≥125) ou Major. L'analyse chronographe calcule la Moyenne, le SD et l'ES. Un SD sous 3 m/s valide une régularité de niveau Match.",
    faq4_q: "4. Signes de surpression et consignes de sécurité essentielles",
    faq4_a: "Commencez toujours par la charge minimale. Examinez les douilles tirées : amorces aplaties (cratering), extraction difficile de la culasse. Stockez poudres et amorces à l'abri de la chaleur et de l'humidité.",
    faq5_q: "5. Comment imprimer les étiquettes PDF pour boîtes de munitions ?",
    faq5_a: "Cliquez sur 'IMPRIMER ÉTIQUETTE PDF' pour générer un PDF vectoriel prêt pour boîtes MTM/Plano de 50 ou 100 cartouches, avec fond clair économique en toner, calibre, charge, poudre, LHT et date.",

    disclaimer_collapsed: "AVERTISSEMENT LÉGAL CIP / SAAMI & SÉCURITÉ DES POUDRES",
    disclaimer_expand: "Développer l'Avertissement",
    disclaimer_collapse: "Réduire / Baisser",
    disclaimer_title: "⚠️ AVERTISSEMENT LÉGAL SUR LA SÉCURITÉ ET LA MANIPULATION D'EXPLOSIFS :",
    disclaimer_text: "Le rechargement d'armes requiert compétence et respect strict de la législation. Poudres et amorces génèrent des pressions extrêmes. Les données présentées sont à titre purement indicatif. L'utilisateur est seul responsable du respect des pressions CIP et SAAMI. Les auteurs déclinent toute responsabilité en cas d'accident.",

    modal_tab_title: "AJOUTER CALIBRE OU POUDRE",
    modal_tab_sub: "Enrichissez la base de données avec vos propres tables et calibres",
    tab_manual: "[SAISIE MANUELLE]",
    tab_csv: "[IMPORT FICHIER CSV]",
    lbl_nt_calibre: "Calibre",
    lbl_nt_powder_mfg: "Fabricant Poudre",
    lbl_nt_powder_type: "Nom / Type Poudre",
    lbl_nt_bullet_weight: "Poids Balle (grains)",
    lbl_nt_dose_min: "Charge Min (grs)",
    lbl_nt_dose_max: "Charge Max (grs)",
    lbl_nt_oal: "O.A.L. Conseillé (mm)",
    lbl_nt_notes: "Notes / Canon / Amorce",
    btn_save_db: "ENREGISTRER DANS LA BASE",
    csv_format_title: "FORMAT CSV ACCEPTÉ :",
    btn_download_template: "TÉLÉCHARGER MODÈLE CSV",
    lbl_csv_file: "Sélectionner Fichier CSV (.csv) :",
    lbl_csv_paste: "Ou collez le texte CSV ici :",
    btn_import_csv: "IMPORTER TABLES CSV",

    modal_auth_title: "AUTHENTIFICATION OPÉRATEUR",
    modal_auth_sub: "Compte Personnel & Synchronisation Cloud",
    tab_login: "[CONNEXION]",
    tab_register: "[INSCRIPTION]",
    lbl_username: "Nom Opérateur / Identifiant",
    lbl_email: "Email (Facultatif)",
    lbl_password: "Mot de Passe de Sécurité",
    btn_auth_login: "AUTORISER ACCÈS",
    btn_auth_register: "CRÉER NOUVEAU COMPTE"
  },

  es: {
    lang_name: "Español",
    flag: "🇪🇸",
    nav_title: "BALLISTIC OPS // RECARGA DE MUNICIÓN & BALÍSTICA",
    nav_sub: "Tablas CIP • Calculadora Coste Cartucho • Cuaderno de Tiro • Etiquetas PDF",
    nav_cip_online: "CIP DATABASE: EN LÍNEA",
    nav_login_btn: "ACCESO // REGISTRO",
    nav_operator: "OPERADOR:",
    nav_admin: "PANEL ADMIN",
    nav_test_pdf: "TEST PDF",
    nav_logout_title: "Desconectar cuenta",

    sec1_title: "1. Tablas Oficiales de Recarga (CIP & Personalizadas)",
    sec1_add_btn: "+ Calibre / Pólvora",
    sec1_select_cal: "Seleccionar Calibre:",
    sec1_all_cal: "TODOS LOS CALIBRES (Arma Corta & Rifle)",
    th_cal_bullet: "Calibre / Punta",
    th_powder: "Pólvora",
    th_min_charge: "Carga Mín (grs)",
    th_max_charge: "Carga Máx (grs)",
    th_oal: "LTC / OAL (mm)",
    th_action: "Acción",
    tb_init: "Inicializando base de datos...",
    tb_custom_badge: "CUSTOM",
    tb_cip_badge: "CIP",
    tb_use_btn: "Usar",
    tb_delete_title: "Eliminar tabla personalizada",
    tb_empty: "No se encontraron datos de recarga.",

    sec2_title: "2. Cuaderno de Recarga & Recetas Guardadas",
    sec2_new_btn: "+ Nueva Receta",
    sec2_preset_btn: "Guardar por Defecto",
    guest_alert: "Estás operando como Invitado. Las recetas se guardan localmente en esta sesión. Inicia sesión para sincronizar en la Nube en todos tus dispositivos.",
    user_alert_prefix: "Conectado como",
    user_alert_suffix: "• Sincronización en la Nube activa",
    lbl_recipe_title: "Título Receta / Número de Lote",
    lbl_calibre: "Calibre",
    lbl_bullet: "Marca & Peso Punta (granos)",
    lbl_powder: "Tipo Pólvora & Carga (grs)",
    lbl_primer: "Marca / Tipo Pistón",
    lbl_oal: "Longitud Total O.A.L. (mm)",
    lbl_crimping: "Crimpado",
    lbl_firearm: "Arma / Paso de Estría / Cañón",
    lbl_notes: "Notas Balísticas / Velocidad Medida",
    btn_save_recipe: "GUARDAR EN CUADERNO",
    btn_pdf_label: "IMPRIMIR ETIQUETA PDF",
    th_rec_title: "Receta / Calibre",
    th_rec_details: "Punta & Pólvora",
    th_rec_oal: "OAL",
    th_rec_date: "Fecha",
    th_rec_actions: "Acciones",
    btn_load: "Cargar",
    btn_delete: "Eliminar",
    no_recipes: "No hay recetas guardadas.",

    sec3_title: "3. Calculadora Coste de Cartucho & Amortización",
    sec3_badge: "ECONOMIC OPS",
    sec3_tab_cartridge: "[COSTE CARTUCHO]",
    sec3_tab_amort: "[AMORTIZACIÓN PRENSA]",
    c_powder_box: "Pólvora (Coste Bote + Carga de Receta)",
    c_powder_label: "Coste del Bote (€)",
    c_powder_weight: "Peso del Bote (g)",
    c_pack_bullet: "Caja de Puntas / Ojivas",
    c_pack_primer: "Caja de Pistones",
    c_pack_cost: "Coste Caja (€)",
    c_pack_qty: "Cantidad (uds)",
    c_brass_box: "Vainas (Amortización por Reutilización)",
    c_brass_label: "Coste Vaina Unitaria (€)",
    c_brass_uses: "Reutilizaciones Estimadas",
    c_res_round_cost: "Coste por Disparo Simple",
    c_res_box50: "Coste Caja de 50 disparos",
    c_res_factory_box: "Coste Caja Comercial (€)",
    c_res_saving: "Ahorro por Disparo",
    c_res_pct_saving: "Ahorro vs Munición Comercial",
    c_press_cost: "Coste Total Equipo (Prensa, Dies, Báscula) (€)",
    c_amort_shots: "Disparos para Amortizar el Equipo",
    c_amort_boxes: "Cajas de 50 necesarias",
    c_amort_desc: "Cada cartucho recargado ahorra dinero respecto a las cajas de munición comercial.",

    sec4_title: "4. Balística Terminal & Factor de Potencia IPSC",
    sec4_badge: "DYNAMIC SHOOTING",
    b_bullet_weight: "Peso Punta (granos - gn)",
    b_speed: "Velocidad en Boca",
    b_speed_unit: "Unidad Velocidad",
    b_res_pf: "Power Factor",
    b_res_joule: "Energía Cinética",
    b_res_fps: "Velocidad fps",
    b_res_ms: "Velocidad m/s",
    b_comp_class: "Clasificación Competición:",
    ipsc_minor: "MINOR // APTO COMPETICIÓN",
    ipsc_major: "MAJOR // POTENCIA MÁXIMA",
    ipsc_subminor: "NO APTO (<125)",

    sec5_title: "5. Analizador Cronógrafo // Desviación Típica (SD) & ES",
    chrono_badge: "CHRONO STATS",
    chrono_string_lbl: "Serie de Velocidades Medidas (separadas por coma o espacio)",
    btn_calc_sd: "Calcular SD & Extreme Spread",
    sd_mean_speed: "Velocidad Media",
    sd_dev: "Desviación Estándar (SD)",
    sd_es: "Extreme Spread (ES)",
    sd_shots_detected: "Disparos Registrados",
    sd_consistency_lbl: "Calidad de Consistencia:",
    sd_grade_match: "MATCH GRADE // EXCELENTE",
    sd_grade_good: "BUENA CONSTANCIA // ESTÁNDAR",
    sd_grade_check: "ALTA DISPERSIÓN // REVISAR DOSIS",

    faq_title: "Guía de Recarga, Tablas CIP & Preguntas Frecuentes (FAQ)",
    faq_sub: "Referencias técnicas sobre dosis de pólvora, normas de seguridad CIP y costes de recarga",
    faq1_q: "1. ¿Cómo consultar las Tablas CIP y elegir la carga inicial?",
    faq1_a: "Las tablas oficiales CIP y de fabricantes (Vihtavuori, Cheddite, Baschieri, Lovex, Reload Swiss, Hodgdon) fijan la carga mínima para comenzar las pruebas de tiro, la carga máxima que jamás debe superarse, la cota LTC/OAL y los pesos de punta recomendados en granos.",
    faq2_q: "2. ¿Cómo calcular el coste real por cartucho y amortizar la prensa?",
    faq2_a: "Coste cartucho = Punta + Pistón + (Carga en Granos × Coste Pólvora por Grano) + (Vaina / Reutilizaciones). Al compararlo con la munición comercial se calcula el ahorro neto y el número exacto de cartuchos para amortizar prensa y dies.",
    faq3_q: "3. Factor de Potencia IPSC y Desviación Estándar (SD) con cronógrafo",
    faq3_a: "Factor IPSC = [Peso Punta (granos) × Velocidad (fps)] / 1000, clasificando en Minor (≥125) o Major. El análisis cronográfico calcula Media, SD y ES. Un valor de SD inferior a 3 m/s certifica cartuchos Match Grade de precisión.",
    faq4_q: "4. ¿Cuáles son los signos de sobrepresión y normas básicas de seguridad?",
    faq4_a: "Comience siempre por la carga mínima. Inspeccione las vainas disparadas: pistones aplanados (flattening), cráteres en la aguja percutora y extracción dura del cerrojo. Conserve pólvoras y pistones en lugares secos y templados.",
    faq5_q: "5. ¿Cómo imprimir etiquetas técnicas en PDF para cajas de munición?",
    faq5_a: "Al pulsar 'IMPRIMIR ETIQUETA PDF' en el cuaderno o menú, se genera un archivo vectorial listo para imprimir sobre cajas MTM o Plano de 50 o 100 cartuchos, con fondo claro que ahorra tinta e información completa de lote, calibre, pólvora y fecha.",

    disclaimer_collapsed: "ADVERTENCIA LEGAL CIP / SAAMI & SEGURIDAD DE PÓLVORAS",
    disclaimer_expand: "Expandir Advertencia",
    disclaimer_collapse: "Minimizar / Bajar",
    disclaimer_title: "⚠️ ADVERTENCIA LEGAL SOBRE SEGURIDAD Y MANIPULACIÓN DE EXPLOSIVOS:",
    disclaimer_text: "La recarga casera de munición requiere destreza, equipo adecuado y estricto cumplimiento de la ley. Pólvoras y pistones generan presiones extremas. Los datos ofrecidos tienen valor puramente informativo. El usuario es el único responsable de respetar los límites CIP y SAAMI. Los autores declinan toda responsabilidad por daños o accidentes.",

    modal_tab_title: "CARGAR NUEVO CALIBRE O PÓLVORA",
    modal_tab_sub: "Amplía la base de datos con tus propias cargas y calibres",
    tab_manual: "[ENTRADA MANUAL]",
    tab_csv: "[IMPORTAR CSV]",
    lbl_nt_calibre: "Calibre",
    lbl_nt_powder_mfg: "Fabricante Pólvora",
    lbl_nt_powder_type: "Nombre / Tipo Pólvora",
    lbl_nt_bullet_weight: "Peso Punta (granos)",
    lbl_nt_dose_min: "Carga Mín (grs)",
    lbl_nt_dose_max: "Carga Máx (grs)",
    lbl_nt_oal: "O.A.L. Recomendado (mm)",
    lbl_nt_notes: "Notas / Cañón / Pistón",
    btn_save_db: "GUARDAR EN LA BASE DE DATOS",
    csv_format_title: "FORMATO CSV COMPATIBLE:",
    btn_download_template: "DESCARGAR PLANTILLA CSV",
    lbl_csv_file: "Seleccionar Archivo CSV (.csv):",
    lbl_csv_paste: "O pegar texto CSV aquí:",
    btn_import_csv: "IMPORTAR TABLAS CSV",

    modal_auth_title: "AUTORIZACIÓN DE OPERADOR",
    modal_auth_sub: "Gestión de Cuenta Personal & Sincronización Nube",
    tab_login: "[ACCEDER]",
    tab_register: "[REGISTRARSE]",
    lbl_username: "Nombre Operador / Usuario",
    lbl_email: "Email (Opcional)",
    lbl_password: "Contraseña de Seguridad",
    btn_auth_login: "AUTORIZAR ACCESO",
    btn_auth_register: "REGISTRAR NUEVO OPERADOR"
  },

  pt: {
    lang_name: "Português",
    flag: "🇵🇹",
    nav_title: "BALLISTIC OPS // RECARGA DE MUNIÇÕES & BALÍSTICA",
    nav_sub: "Tabelas CIP • Calculadora Custo Cartucho • Caderno de Tiro • Etiquetas PDF",
    nav_cip_online: "CIP DATABASE: ONLINE",
    nav_login_btn: "ENTRAR // REGISTAR",
    nav_operator: "OPERADOR:",
    nav_admin: "PAINEL ADMIN",
    nav_test_pdf: "TESTE PDF",
    nav_logout_title: "Terminar sessão",

    sec1_title: "1. Tabelas Oficiais de Recarga (CIP & Personalizadas)",
    sec1_add_btn: "+ Calibre / Pólvora",
    sec1_select_cal: "Selecionar Calibre:",
    sec1_all_cal: "TODOS OS CALIBRES (Arma Curta & Longa)",
    th_cal_bullet: "Calibre / Projétil",
    th_powder: "Pólvora",
    th_min_charge: "Carga Mín (grs)",
    th_max_charge: "Carga Máx (grs)",
    th_oal: "OAL (mm)",
    th_action: "Ação",
    tb_init: "A inicializar base de dados...",
    tb_custom_badge: "CUSTOM",
    tb_cip_badge: "CIP",
    tb_use_btn: "Usar",
    tb_delete_title: "Eliminar tabela personalizada",
    tb_empty: "Nenhum dado de recarga encontrado.",

    sec2_title: "2. Caderno de Recarga & Receitas Guardadas",
    sec2_new_btn: "+ Nova Receita",
    sec2_preset_btn: "Guardar por Defeito",
    guest_alert: "Está a operar como Convidado. As receitas são guardadas localmente nesta sessão. Inicie sessão para sincronizar na Nuvem em todos os seus dispositivos.",
    user_alert_prefix: "Ligado como",
    user_alert_suffix: "• Sincronização Cloud ativa",
    lbl_recipe_title: "Título da Receita / Lote",
    lbl_calibre: "Calibre",
    lbl_bullet: "Marca & Peso do Projétil (grãos)",
    lbl_powder: "Tipo de Pólvora & Carga (grs)",
    lbl_primer: "Marca / Tipo de Fulminante",
    lbl_oal: "Comprimento Total O.A.L. (mm)",
    lbl_crimping: "Crimpagem",
    lbl_firearm: "Arma / Passo de Estria / Cano",
    lbl_notes: "Notas Balísticas / Velocidade Medida",
    btn_save_recipe: "GUARDAR NO CADERNO",
    btn_pdf_label: "IMPRIMIR ETIQUETA PDF",
    th_rec_title: "Receita / Calibre",
    th_rec_details: "Projétil & Pólvora",
    th_rec_oal: "OAL",
    th_rec_date: "Data",
    th_rec_actions: "Ações",
    btn_load: "Carregar",
    btn_delete: "Eliminar",
    no_recipes: "Nenhuma receita guardada.",

    sec3_title: "3. Calculadora Custo por Cartucho & Amortização",
    sec3_badge: "ECONOMIC OPS",
    sec3_tab_cartridge: "[CUSTO CARTUCHO]",
    sec3_tab_amort: "[AMORTIZAÇÃO PRENSA]",
    c_powder_box: "Pólvora (Custo Embalagem + Carga da Receita)",
    c_powder_label: "Custo da Embalagem (€)",
    c_powder_weight: "Peso da Embalagem (g)",
    c_pack_bullet: "Caixa de Projéteis / Ogivas",
    c_pack_primer: "Caixa de Fulminantes",
    c_pack_cost: "Custo da Caixa (€)",
    c_pack_qty: "Quantidade (un)",
    c_brass_box: "Estojos (Amortização por Reutilização)",
    c_brass_label: "Custo do Estojo Unitário (€)",
    c_brass_uses: "Reutilizações Estimadas",
    c_res_round_cost: "Custo por Disparo Único",
    c_res_box50: "Custo Caixa de 50 un",
    c_res_factory_box: "Custo Caixa Comercial (€)",
    c_res_saving: "Poupança por Disparo",
    c_res_pct_saving: "Poupança vs Comercial",
    c_press_cost: "Custo Total Equipamento (Prensa, Dies, Balança) (€)",
    c_amort_shots: "Disparos para Amortizar o Investimento",
    c_amort_boxes: "Caixas de 50 necessárias",
    c_amort_desc: "Cada cartucho recarregado poupa dinheiro em relação às munições de fábrica comerciais.",

    sec4_title: "4. Balística Terminal & Fator de Potência IPSC",
    sec4_badge: "DYNAMIC SHOOTING",
    b_bullet_weight: "Peso do Projétil (grãos - gn)",
    b_speed: "Velocidade na Boca do Cano",
    b_speed_unit: "Unidade de Velocidade",
    b_res_pf: "Power Factor",
    b_res_joule: "Energia Cinética",
    b_res_fps: "Velocidade fps",
    b_res_ms: "Velocidade m/s",
    b_comp_class: "Classificação em Competição:",
    ipsc_minor: "MINOR // CONFORME REGULAMENTO",
    ipsc_major: "MAJOR // POTÊNCIA MÁXIMA",
    ipsc_subminor: "NÃO CONFORME (<125)",

    sec5_title: "5. Analisador Cronógrafo // Desvio Padrão (SD) & ES",
    chrono_badge: "CHRONO STATS",
    chrono_string_lbl: "Série de Velocidades Medidas (separadas por vírgula ou espaço)",
    btn_calc_sd: "Calcular SD & Extreme Spread",
    sd_mean_speed: "Velocidade Média",
    sd_dev: "Desvio Padrão (SD)",
    sd_es: "Extreme Spread (ES)",
    sd_shots_detected: "Disparos Registados",
    sd_consistency_lbl: "Qualidade de Constância:",
    sd_grade_match: "MATCH GRADE // EXCELENTE",
    sd_grade_good: "BOA CONSTÂNCIA // PADRÃO",
    sd_grade_check: "DISPERSÃO ELEVADA // VERIFICAR CARGA",

    faq_title: "Guia de Recarga, Tabelas CIP & Perguntas Frequentes (FAQ)",
    faq_sub: "Diretrizes técnicas sobre dosagens de pólvora, normas de segurança CIP e economia da recarga",
    faq1_q: "1. Como ler as Tabelas CIP e determinar a carga de partida?",
    faq1_a: "As tabelas oficiais CIP e dos fabricantes (Vihtavuori, Cheddite, Baschieri, Lovex, Reload Swiss, Hodgdon) estabelecem a carga mínima inicial recomendada para testes, a carga máxima que nunca deve ser excedida, a cota OAL e os pesos de projétil em grãos.",
    faq2_q: "2. Como calcular o custo real por cartucho e amortizar a prensa?",
    faq2_a: "Custo do cartucho = Projétil + Fulminante + (Carga em Grãos × Custo Pólvora por Grão) + (Estojo / Reutilizações). Em comparação com as munições comerciais, obtém-se a poupança líquida e o número de disparos necessários para pagar a prensa e dies.",
    faq3_q: "3. Fator de Potência IPSC e Desvio Padrão (SD) no Cronógrafo",
    faq3_a: "O Fator IPSC = [Peso Projétil (grãos) × Velocidade (fps)] / 1000 divide as cargas em Minor (≥125) e Major. O cronógrafo calcula Média, SD e ES. Um desvio padrão abaixo de 3 m/s indica munição Match Grade de alta precisão.",
    faq4_q: "4. Sinais de sobrepressão e regras essenciais de segurança",
    faq4_a: "Comece sempre pela carga mínima. Inspecione os estojos disparados para sinais de sobrepressão: fulminante espalmado (flattening), crateras no percutor e extração pesada do ferrolho. Guarde pólvoras e fulminantes em local seco e fresco.",
    faq5_q: "5. Como imprimir etiquetas técnicas em PDF para caixas de munição?",
    faq5_a: "Ao clicar em 'IMPRIMIR ETIQUETA PDF' no caderno ou menu, obtém um PDF vetorial pronto para imprimir e colar em caixas de 50 ou 100 unidades (MTM, Plano), com fundo claro que economiza tinta e todos os dados do lote.",

    disclaimer_collapsed: "AVISO LEGAL CIP / SAAMI & SEGURANÇA DE PÓLVORAS",
    disclaimer_expand: "Expandir Avisos",
    disclaimer_collapse: "Minimizar / Baixar",
    disclaimer_title: "⚠️ AVISO LEGAL SOBRE SEGURANÇA E MANIPULAÇÃO DE EXPLOSIVOS:",
    disclaimer_text: "A recarga caseira de munições exige formação e cumprimento estrito da legislação em vigor. Pólvoras e fulminantes geram pressões extremas. Os dados fornecidos são meramente informativos e experimentais. O utilizador é o único responsável pelo respeito aos limites de pressão CIP e SAAMI. Os autores declinam qualquer responsabilidade em caso de acidentes.",

    modal_tab_title: "CARREGAR NOVO CALIBRE OU PÓLVORA",
    modal_tab_sub: "Expanda a base de dados com as suas receitas e novos calibres",
    tab_manual: "[ENTRADA MANUAL]",
    tab_csv: "[IMPORTAR FICHEIRO CSV]",
    lbl_nt_calibre: "Calibre",
    lbl_nt_powder_mfg: "Fabricante de Pólvora",
    lbl_nt_powder_type: "Nome / Tipo de Pólvora",
    lbl_nt_bullet_weight: "Peso do Projétil (grãos)",
    lbl_nt_dose_min: "Carga Mín (grs)",
    lbl_nt_dose_max: "Carga Máx (grs)",
    lbl_nt_oal: "O.A.L. Recomendado (mm)",
    lbl_nt_notes: "Notas / Cano / Fulminante",
    btn_save_db: "GUARDAR NA BASE DE DADOS",
    csv_format_title: "FORMATO CSV SUPORTADO:",
    btn_download_template: "DESCARREGAR MODELO CSV",
    lbl_csv_file: "Selecionar Ficheiro CSV (.csv):",
    lbl_csv_paste: "Ou cole o texto CSV aqui:",
    btn_import_csv: "IMPORTAR TABELAS CSV",

    modal_auth_title: "AUTORIZAÇÃO DO OPERADOR",
    modal_auth_sub: "Gestão de Conta Pessoal & Sincronização Cloud",
    tab_login: "[INICIAR SESSÃO]",
    tab_register: "[REGISTAR]",
    lbl_username: "Nome de Operador / Utilizador",
    lbl_email: "Email (Opcional)",
    lbl_password: "Palavra-passe de Segurança",
    btn_auth_login: "AUTORIZAR ACESSO",
    btn_auth_register: "REGISTAR NOVO OPERADOR"
  }
};

// Current active language
let currentLang = 'it';

function t(key) {
  if (TRANSLATIONS[currentLang] && TRANSLATIONS[currentLang][key]) {
    return TRANSLATIONS[currentLang][key];
  }
  if (TRANSLATIONS['it'] && TRANSLATIONS['it'][key]) {
    return TRANSLATIONS['it'][key];
  }
  return key;
}

function getInitialLanguage() {
  // 1. Check URL query param ?lang=...
  const urlParams = new URLSearchParams(window.location.search);
  const urlLang = urlParams.get('lang');
  if (urlLang && TRANSLATIONS[urlLang]) {
    return urlLang;
  }
  
  // 2. Check localStorage
  const storedLang = localStorage.getItem('preferred_language');
  if (storedLang && TRANSLATIONS[storedLang]) {
    return storedLang;
  }

  // 3. Check browser language navigator.language
  const browserLang = (navigator.language || navigator.userLanguage || '').slice(0, 2).toLowerCase();
  if (TRANSLATIONS[browserLang]) {
    return browserLang;
  }

  return 'it';
}

function applicaTraduzioni(lang) {
  if (!TRANSLATIONS[lang]) lang = 'it';
  currentLang = lang;
  localStorage.setItem('preferred_language', lang);
  document.documentElement.lang = lang;

  // Update navbar indicator
  const flagEl = document.getElementById('lang-flag');
  const codeEl = document.getElementById('lang-code');
  if (flagEl) flagEl.textContent = TRANSLATIONS[lang].flag;
  if (codeEl) codeEl.textContent = lang.toUpperCase();

  // 1. Text elements with data-i18n
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (TRANSLATIONS[lang][key]) {
      el.textContent = TRANSLATIONS[lang][key];
    }
  });

  // 2. HTML elements with data-i18n-html
  document.querySelectorAll('[data-i18n-html]').forEach(el => {
    const key = el.getAttribute('data-i18n-html');
    if (TRANSLATIONS[lang][key]) {
      el.innerHTML = TRANSLATIONS[lang][key];
    }
  });

  // 3. Inputs with data-i18n-placeholder
  document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
    const key = el.getAttribute('data-i18n-placeholder');
    if (TRANSLATIONS[lang][key]) {
      el.placeholder = TRANSLATIONS[lang][key];
    }
  });

  // 4. Elements with data-i18n-title
  document.querySelectorAll('[data-i18n-title]').forEach(el => {
    const key = el.getAttribute('data-i18n-title');
    if (TRANSLATIONS[lang][key]) {
      el.title = TRANSLATIONS[lang][key];
    }
  });

  // Refresh icons and tables/recipes with new translations if present
  if (window.lucide) {
    lucide.createIcons();
  }
}

function cambiaLingua(lang) {
  applicaTraduzioni(lang);
  chiudiLangDropdown();
  
  // Re-render table and cards if functions exist
  if (typeof caricaTabelle === 'function') caricaTabelle();
  if (typeof caricaRicette === 'function') caricaRicette();
  if (typeof calcolaCostoLive === 'function') calcolaCostoLive();
  if (typeof calcolaBalisticaLive === 'function') calcolaBalisticaLive();
  if (typeof calcolaSD === 'function') calcolaSD();
}

function toggleLangDropdown(event) {
  if (event) event.stopPropagation();
  const dropdown = document.getElementById('lang-dropdown');
  if (dropdown) {
    dropdown.classList.toggle('hidden');
  }
}

function chiudiLangDropdown() {
  const dropdown = document.getElementById('lang-dropdown');
  if (dropdown && !dropdown.classList.contains('hidden')) {
    dropdown.classList.add('hidden');
  }
}

// Close language dropdown on outside click
document.addEventListener('click', (e) => {
  const container = document.getElementById('lang-selector-container');
  if (container && !container.contains(e.target)) {
    chiudiLangDropdown();
  }
});
