// Tactical Reload & Ballistics Hub - App Core JS (Multi-User Online Ready)

let unitaBalistica = 'ms';
let operatoreCorrente = null;
let tabAuthAttivo = 'login';

document.addEventListener('DOMContentLoaded', () => {
  verificaStatoAutenticazione();
  caricaTabelle();
  caricaRicette();
  calcolaCostoLive();
  calcolaBalisticaLive();
  calcolaSD();
});

// ==========================================
// GESTIONE AUTENTICAZIONE UTENTI (OPERATORI)
// ==========================================
async function verificaStatoAutenticazione() {
  try {
    const res = await fetch('/api/auth/me');
    const data = await res.json();
    
    if (data.authenticated && data.user) {
      operatoreCorrente = data.user;
      mostraStatoAutenticato(data.user);
      caricaPresetUtente();
    } else {
      operatoreCorrente = null;
      mostraStatoOspite();
    }
  } catch (err) {
    console.error("Errore verifica autenticazione:", err);
  }
}

function mostraStatoAutenticato(user) {
  const guestBox = document.getElementById('auth-guest-box');
  const userBox = document.getElementById('auth-user-box');
  const navUsername = document.getElementById('nav-username');
  const btnAdmin = document.getElementById('btn-nav-admin');
  
  const guestAlert = document.getElementById('logbook-guest-alert');
  const userAlert = document.getElementById('logbook-user-alert');
  const logbookUsername = document.getElementById('logbook-user-name');
  
  if (guestBox) guestBox.classList.add('hidden');
  if (userBox) {
    userBox.classList.remove('hidden');
    userBox.classList.add('flex');
  }
  if (navUsername) navUsername.textContent = user.username;
  
  if (btnAdmin) {
    if (user.is_admin) {
      btnAdmin.classList.remove('hidden');
      btnAdmin.classList.add('flex');
    } else {
      btnAdmin.classList.add('hidden');
      btnAdmin.classList.remove('flex');
    }
  }
  
  if (guestAlert) guestAlert.classList.add('hidden');
  if (userAlert) {
    userAlert.classList.remove('hidden');
    userAlert.classList.add('flex');
  }
  if (logbookUsername) logbookUsername.textContent = user.username;
  
  lucide.createIcons();
}

function mostraStatoOspite() {
  const guestBox = document.getElementById('auth-guest-box');
  const userBox = document.getElementById('auth-user-box');
  const btnAdmin = document.getElementById('btn-nav-admin');
  
  const guestAlert = document.getElementById('logbook-guest-alert');
  const userAlert = document.getElementById('logbook-user-alert');
  
  if (btnAdmin) {
    btnAdmin.classList.add('hidden');
    btnAdmin.classList.remove('flex');
  }
  if (userBox) {
    userBox.classList.add('hidden');
    userBox.classList.remove('flex');
  }
  if (guestBox) guestBox.classList.remove('hidden');
  
  if (userAlert) userAlert.classList.add('hidden');
  if (guestAlert) {
    guestAlert.classList.remove('hidden');
    guestAlert.classList.add('flex');
  }
  
  lucide.createIcons();
}

function apriModaleAuth(tab = 'login') {
  const modal = document.getElementById('modal-auth');
  modal.classList.remove('hidden');
  modal.classList.add('flex');
  impostaTabAuth(tab);
  document.getElementById('auth-error-banner').classList.add('hidden');
}

function chiudiModaleAuth() {
  const modal = document.getElementById('modal-auth');
  modal.classList.add('hidden');
  modal.classList.remove('flex');
  document.getElementById('form-auth').reset();
  document.getElementById('auth-error-banner').classList.add('hidden');
}

function impostaTabAuth(tab) {
  tabAuthAttivo = tab;
  const tabLogin = document.getElementById('tab-auth-login');
  const tabRegister = document.getElementById('tab-auth-register');
  const emailGroup = document.getElementById('auth-email-group');
  const btnLabel = document.getElementById('btn-auth-label');
  const errorBanner = document.getElementById('auth-error-banner');
  errorBanner.classList.add('hidden');
  
  if (tab === 'login') {
    tabLogin.className = "py-2 text-center font-bold rounded bg-tacgreen text-white transition";
    tabRegister.className = "py-2 text-center font-bold rounded text-gray-400 hover:text-white transition";
    emailGroup.classList.add('hidden');
    btnLabel.textContent = "AUTORIZZA ACCESSO";
  } else {
    tabRegister.className = "py-2 text-center font-bold rounded bg-tacgreen text-white transition";
    tabLogin.className = "py-2 text-center font-bold rounded text-gray-400 hover:text-white transition";
    emailGroup.classList.remove('hidden');
    btnLabel.textContent = "CREA ACCOUNT OPERATORE";
  }
}

async function inviaFormAuth(e) {
  e.preventDefault();
  const username = document.getElementById('auth-username').value.trim();
  const password = document.getElementById('auth-password').value.trim();
  const email = document.getElementById('auth-email').value.trim();
  const errorBanner = document.getElementById('auth-error-banner');
  errorBanner.classList.add('hidden');
  
  const endpoint = tabAuthAttivo === 'login' ? '/api/auth/login' : '/api/auth/register';
  const payload = { username, password, email };
  
  try {
    const res = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    
    if (data.success) {
      chiudiModaleAuth();
      await verificaStatoAutenticazione();
      await caricaRicette();
    } else {
      errorBanner.textContent = data.error || "Operazione non riuscita.";
      errorBanner.classList.remove('hidden');
    }
  } catch (err) {
    console.error("Errore autenticazione:", err);
    errorBanner.textContent = "Errore di connessione al server.";
    errorBanner.classList.remove('hidden');
  }
}

async function eseguiLogout() {
  if (!confirm("Confermi la disconnessione dall'account operatore?")) return;
  try {
    await fetch('/api/auth/logout', { method: 'POST' });
    operatoreCorrente = null;
    mostraStatoOspite();
    caricaRicette();
  } catch (err) {
    console.error("Errore logout:", err);
  }
}

// ==========================================
// PRESET ECONOMICI & CHRONO CLOUD
// ==========================================
async function caricaPresetUtente() {
  if (!operatoreCorrente) return;
  try {
    const res = await fetch('/api/user/presets');
    const data = await res.json();
    if (data.success && data.presets) {
      const p = data.presets;
      if (p.costo_pacco_palle) document.getElementById('c-pacco-palla-eur').value = p.costo_pacco_palle;
      if (p.quantita_pacco_palle) document.getElementById('c-pacco-palla-qta').value = p.quantita_pacco_palle;
      if (p.costo_pacco_inneschi) document.getElementById('c-pacco-innesco-eur').value = p.costo_pacco_inneschi;
      if (p.quantita_pacco_inneschi) document.getElementById('c-pacco-innesco-qta').value = p.quantita_pacco_inneschi;
      if (p.costo_pacco_bossoli) document.getElementById('c-pacco-bossolo-eur').value = p.costo_pacco_bossoli;
      if (p.quantita_pacco_bossoli) document.getElementById('c-pacco-bossolo-qta').value = p.quantita_pacco_bossoli;
      if (p.costo_barattolo_polvere) document.getElementById('c-barattolo-eur').value = p.costo_barattolo_polvere;
      if (p.peso_barattolo_g) document.getElementById('c-barattolo-g').value = p.peso_barattolo_g;
      if (p.dose_grani) document.getElementById('c-dose-grs').value = p.dose_grani;
      if (p.ricariche_previste) document.getElementById('c-bossolo-cicli').value = p.ricariche_previste;
      if (p.chrono_stringa) document.getElementById('chrono-stringa').value = p.chrono_stringa;
      if (p.chrono_unita) document.getElementById('chrono-unita').value = p.chrono_unita;
      
      calcolaCostoLive();
      calcolaSD();
    }
  } catch (err) {
    console.error("Errore caricamento preset:", err);
  }
}

async function salvaPresetEconomico() {
  if (!operatoreCorrente) {
    alert("Accedi o registrati come Operatore per memorizzare i tuoi costi predefiniti su cloud.");
    apriModaleAuth('login');
    return;
  }
  
  const payload = {
    costo_pacco_palle: parseFloat(document.getElementById('c-pacco-palla-eur').value) || 105.0,
    quantita_pacco_palle: parseInt(document.getElementById('c-pacco-palla-qta').value) || 1000,
    costo_pacco_inneschi: parseFloat(document.getElementById('c-pacco-innesco-eur').value) || 65.0,
    quantita_pacco_inneschi: parseInt(document.getElementById('c-pacco-innesco-qta').value) || 1000,
    costo_pacco_bossoli: parseFloat(document.getElementById('c-pacco-bossolo-eur').value) || 25.0,
    quantita_pacco_bossoli: parseInt(document.getElementById('c-pacco-bossolo-qta').value) || 100,
    costo_barattolo_polvere: parseFloat(document.getElementById('c-barattolo-eur').value) || 68.0,
    peso_barattolo_g: parseFloat(document.getElementById('c-barattolo-g').value) || 500,
    dose_grani: parseFloat(document.getElementById('c-dose-grs').value) || 4.2,
    ricariche_previste: parseInt(document.getElementById('c-bossolo-cicli').value) || 5,
    chrono_stringa: document.getElementById('chrono-stringa').value.trim(),
    chrono_unita: document.getElementById('chrono-unita').value
  };
  
  try {
    const res = await fetch('/api/user/presets', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (data.success) {
      const label = document.getElementById('btn-save-presets-text');
      const orig = label.textContent;
      label.textContent = "Preset Sincronizzati su Cloud!";
      label.classList.add('text-tacgreen', 'font-bold');
      setTimeout(() => {
        label.textContent = orig;
        label.classList.remove('text-tacgreen', 'font-bold');
      }, 2000);
    }
  } catch (err) {
    console.error("Errore salvataggio preset:", err);
  }
}

// ==========================================
// TABELLE DI RICARICA (CIP + PERSONALIZZATE)
// ==========================================
let tabNuovaTabellaAttivo = 'manuale';

async function caricaTabelle() {
  const calibroSelect = document.getElementById('filtro-calibro');
  const calibroSelezionato = calibroSelect.value;
  const tbody = document.getElementById('tabelle-tbody');
  const countSpan = document.getElementById('tot-tabelle-count');
  
  try {
    const url = calibroSelezionato && calibroSelezionato !== 'ALL' 
      ? `/api/tabelle?calibro=${encodeURIComponent(calibroSelezionato)}` 
      : '/api/tabelle';
      
    const res = await fetch(url);
    const data = await res.json();
    
    // Popola dropdown filtro calibri
    if (data.calibri) {
      const prevVal = calibroSelect.value;
      calibroSelect.innerHTML = '<option value="ALL">TUTTI I CALIBRI (Canna Rigata & Liscia)</option>';
      data.calibri.forEach(cal => {
        const opt = document.createElement('option');
        opt.value = cal;
        opt.textContent = cal;
        calibroSelect.appendChild(opt);
      });
      if (prevVal && Array.from(calibroSelect.options).some(o => o.value === prevVal)) {
        calibroSelect.value = prevVal;
      }
    }

    // Popola datalist calibri per autocompletamento
    const dlCalibri = document.getElementById('datalist-calibri');
    if (dlCalibri && data.calibri) {
      dlCalibri.innerHTML = data.calibri.map(c => `<option value="${escapeHtml(c)}">`).join('');
    }

    // Popola datalist polveri
    const dlPolveri = document.getElementById('datalist-polveri');
    if (dlPolveri && data.polveri) {
      dlPolveri.innerHTML = data.polveri.map(p => `<option value="${escapeHtml(p)}">`).join('');
    }

    // Popola datalist produttori
    const dlProduttori = document.getElementById('datalist-produttori');
    if (dlProduttori && data.produttori) {
      dlProduttori.innerHTML = data.produttori.map(pr => `<option value="${escapeHtml(pr)}">`).join('');
    }
    
    countSpan.textContent = `${data.tabelle.length} Riferimenti nel Database`;
    
    if (data.tabelle.length === 0) {
      tbody.innerHTML = `<tr><td colspan="6" class="p-4 text-center text-gray-500 font-mono">Nessun dato per questo calibro. Usa il pulsante "+ Calibro / Polvere" per aggiungerlo!</td></tr>`;
      return;
    }
    
    tbody.innerHTML = data.tabelle.map(row => {
      const badge = row.is_custom 
        ? `<span class="px-1.5 py-0.5 rounded bg-tacamber/20 text-tacamber border border-tacamber/40 text-[9px] font-bold">CUSTOM</span>` 
        : `<span class="px-1.5 py-0.5 rounded bg-tacblue/20 text-tacblue border border-tacblue/40 text-[9px] font-bold">CIP</span>`;
      
      const opInfo = row.operatore ? `<span class="text-[9px] text-gray-500 font-mono block">By ${escapeHtml(row.operatore)}</span>` : '';
      const noteBadge = row.note ? `<span class="text-[10px] text-gray-400 italic block mt-0.5" title="${escapeHtml(row.note)}">📝 ${escapeHtml(row.note)}</span>` : '';
      
      const btnDelete = row.can_delete 
        ? `<button onclick="eliminaDatoTabella(${row.id})" title="Elimina dato ricarica" class="px-2 py-1 bg-red-950/40 hover:bg-red-800 text-red-400 hover:text-white border border-red-800/60 text-[10px] font-bold rounded uppercase transition ml-1">
             <i data-lucide="trash-2" class="w-3 h-3"></i>
           </button>` 
        : '';

      return `
        <tr class="hover:bg-tacpanel/80 transition-colors">
          <td class="p-2.5">
            <div class="flex items-center gap-1.5 flex-wrap">
              <span class="font-bold text-white">${escapeHtml(row.calibro)}</span>
              ${badge}
            </div>
            <span class="text-[10px] text-gray-400 font-mono">${row.peso_palla_grani ? row.peso_palla_grani + ' grs' : '-'}</span>
            ${opInfo}
            ${noteBadge}
          </td>
          <td class="p-2.5">
            <span class="text-white block font-medium">${escapeHtml(row.tipo_polvere)}</span>
            <span class="text-[10px] text-gray-400 font-mono">${escapeHtml(row.produttore_polvere || '-')}</span>
          </td>
          <td class="p-2.5 text-center font-bold text-gray-300">
            ${row.dose_min_grani ? row.dose_min_grani.toFixed(1) : '-'}
          </td>
          <td class="p-2.5 text-center font-bold text-tacamber">
            ${row.dose_max_grani ? row.dose_max_grani.toFixed(1) : '-'}
          </td>
          <td class="p-2.5 text-center text-gray-300">
            ${row.oal_consigliato ? row.oal_consigliato.toFixed(1) : '-'}
          </td>
          <td class="p-2.5 text-right whitespace-nowrap">
            <button onclick="usaInRicetta('${escapeHtml(row.calibro)}', '${escapeHtml(row.produttore_polvere || '')} ${escapeHtml(row.tipo_polvere)}'.trim(), ${row.dose_max_grani || 0}, ${row.dose_min_grani || 0}, ${row.peso_palla_grani || 0}, ${row.oal_consigliato || 0})" 
                    class="px-2.5 py-1 bg-tacblue/20 hover:bg-tacblue text-tacblue hover:text-white border border-tacblue/50 text-[10px] font-bold rounded uppercase transition">
              Usa
            </button>
            ${btnDelete}
          </td>
        </tr>
      `;
    }).join('');
    
    lucide.createIcons();
    
  } catch (err) {
    console.error("Errore tabelle:", err);
    tbody.innerHTML = `<tr><td colspan="6" class="p-4 text-center text-red-400 font-mono">Errore nel caricamento delle tabelle.</td></tr>`;
  }
}

function apriModaleNuovaTabella(tab = 'manuale') {
  const modal = document.getElementById('modal-nuova-tabella');
  modal.classList.remove('hidden');
  modal.classList.add('flex');
  impostaTabNuovaTabella(tab);
  document.getElementById('tabella-error-banner').classList.add('hidden');
  document.getElementById('tabella-success-banner').classList.add('hidden');
  lucide.createIcons();
}

function chiudiModaleNuovaTabella() {
  const modal = document.getElementById('modal-nuova-tabella');
  modal.classList.add('hidden');
  modal.classList.remove('flex');
  document.getElementById('form-nuova-tabella').reset();
  const csvArea = document.getElementById('csv-text-area');
  if (csvArea) csvArea.value = '';
  const csvFile = document.getElementById('csv-file-input');
  if (csvFile) csvFile.value = '';
  document.getElementById('tabella-error-banner').classList.add('hidden');
  document.getElementById('tabella-success-banner').classList.add('hidden');
}

function impostaTabNuovaTabella(tab) {
  tabNuovaTabellaAttivo = tab;
  const tabManuale = document.getElementById('tab-tabella-manuale');
  const tabCsv = document.getElementById('tab-tabella-csv');
  const formManuale = document.getElementById('form-nuova-tabella');
  const formCsv = document.getElementById('form-nuova-tabella-csv');
  
  if (tab === 'manuale') {
    tabManuale.className = "py-2 text-center font-bold rounded bg-tacblue text-white transition";
    tabCsv.className = "py-2 text-center font-bold rounded text-gray-400 hover:text-white transition";
    formManuale.classList.remove('hidden');
    formCsv.classList.add('hidden');
  } else {
    tabCsv.className = "py-2 text-center font-bold rounded bg-tacblue text-white transition";
    tabManuale.className = "py-2 text-center font-bold rounded text-gray-400 hover:text-white transition";
    formCsv.classList.remove('hidden');
    formManuale.classList.add('hidden');
  }
}

async function salvaNuovaTabella(e) {
  e.preventDefault();
  const errBanner = document.getElementById('tabella-error-banner');
  const succBanner = document.getElementById('tabella-success-banner');
  errBanner.classList.add('hidden');
  succBanner.classList.add('hidden');
  
  const payload = {
    calibro: document.getElementById('nt-calibro').value.trim(),
    produttore_polvere: document.getElementById('nt-produttore').value.trim(),
    tipo_polvere: document.getElementById('nt-tipo-polvere').value.trim(),
    peso_palla_grani: parseFloat(document.getElementById('nt-peso-palla').value) || 0,
    dose_min_grani: parseFloat(document.getElementById('nt-dose-min').value) || 0,
    dose_max_grani: parseFloat(document.getElementById('nt-dose-max').value) || 0,
    oal_consigliato: parseFloat(document.getElementById('nt-oal').value) || 0,
    note: document.getElementById('nt-note').value.trim()
  };
  
  try {
    const res = await fetch('/api/tabelle', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (data.success) {
      succBanner.textContent = data.message || "Riferimento salvato con successo!";
      succBanner.classList.remove('hidden');
      document.getElementById('form-nuova-tabella').reset();
      await caricaTabelle();
      setTimeout(() => {
        chiudiModaleNuovaTabella();
      }, 1400);
    } else {
      errBanner.textContent = data.error || "Errore durante il salvataggio.";
      errBanner.classList.remove('hidden');
    }
  } catch (err) {
    console.error("Errore salvataggio tabella:", err);
    errBanner.textContent = "Errore di connessione al server.";
    errBanner.classList.remove('hidden');
  }
}

async function caricaFileCSV() {
  const errBanner = document.getElementById('tabella-error-banner');
  const succBanner = document.getElementById('tabella-success-banner');
  errBanner.classList.add('hidden');
  succBanner.classList.add('hidden');
  
  const fileInput = document.getElementById('csv-file-input');
  const textArea = document.getElementById('csv-text-area');
  
  let formData = null;
  let jsonBody = null;
  
  if (fileInput.files && fileInput.files[0]) {
    formData = new FormData();
    formData.append('file', fileInput.files[0]);
  } else if (textArea.value.trim()) {
    jsonBody = JSON.stringify({ csv_text: textArea.value.trim() });
  } else {
    errBanner.textContent = "Seleziona un file .csv oppure incolla del testo CSV.";
    errBanner.classList.remove('hidden');
    return;
  }
  
  try {
    const options = formData 
      ? { method: 'POST', body: formData }
      : { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: jsonBody };
      
    const res = await fetch('/api/tabelle/upload-csv', options);
    const data = await res.json();
    
    if (data.success) {
      succBanner.textContent = data.message || `${data.count} righe importate con successo!`;
      succBanner.classList.remove('hidden');
      textArea.value = '';
      fileInput.value = '';
      await caricaTabelle();
      setTimeout(() => {
        chiudiModaleNuovaTabella();
      }, 1600);
    } else {
      errBanner.textContent = data.error || "Errore durante l'importazione CSV.";
      errBanner.classList.remove('hidden');
    }
  } catch (err) {
    console.error("Errore upload CSV:", err);
    errBanner.textContent = "Errore di connessione durante l'upload CSV.";
    errBanner.classList.remove('hidden');
  }
}

async function eliminaDatoTabella(id) {
  if (!confirm("Confermi l'eliminazione di questo riferimento balistico dal database?")) return;
  try {
    const res = await fetch(`/api/tabelle/${id}`, { method: 'DELETE' });
    const data = await res.json();
    if (data.success) {
      await caricaTabelle();
    } else {
      alert(data.error || "Impossibile eliminare il dato.");
    }
  } catch (err) {
    console.error("Errore cancellazione tabella:", err);
    alert("Errore di connessione durante la cancellazione.");
  }
}

function usaInRicetta(calibro, polvere, doseMax, doseMin, pesoPalla, oal) {
  document.getElementById('r-calibro').value = calibro;
  document.getElementById('r-polvere').value = polvere;
  
  let doseConsigliata = doseMax;
  if (doseMin && doseMax) {
    doseConsigliata = ((doseMin + doseMax) / 2);
  }
  document.getElementById('r-dose').value = doseConsigliata.toFixed(1);
  aggiornaDoseGrammiRealtime();
  
  if (pesoPalla) {
    document.getElementById('r-palla').value = `${pesoPalla} grs`;
    document.getElementById('b-peso-grs').value = pesoPalla;
    calcolaBalisticaLive();
  }
  
  if (oal) {
    document.getElementById('r-oal').value = oal.toFixed(2);
  }
  
  document.getElementById('c-dose-grs').value = doseConsigliata.toFixed(1);
  calcolaCostoLive();
  
  const formSection = document.getElementById('form-ricetta');
  formSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
  formSection.classList.add('ring-2', 'ring-tacgreen');
  setTimeout(() => formSection.classList.remove('ring-2', 'ring-tacgreen'), 1200);
}

// ==========================================
// QUADERNO DIGITALE RICETTE (CRUD)
// ==========================================
async function caricaRicette() {
  const container = document.getElementById('lista-ricette');
  const countLabel = document.getElementById('ricette-count');
  
  try {
    const res = await fetch('/api/ricette');
    const data = await res.json();
    
    countLabel.textContent = `${data.ricette.length} Ricette ${data.is_authenticated ? '(Account Privato)' : '(Demo)'}`;
    
    if (data.ricette.length === 0) {
      container.innerHTML = `
        <div class="text-center py-6 text-gray-500 font-mono text-xs border border-dashed border-tacborder rounded p-4">
          Nessuna ricetta presente. Compila il modulo per creare il tuo primo lotto di ricarica.
        </div>
      `;
      return;
    }
    
    container.innerHTML = data.ricette.map(r => {
      const isDemo = !r.user_id;
      return `
        <div class="p-3 bg-black/60 border border-tacborder hover:border-tacgreen/60 rounded transition group">
          <div class="flex items-start justify-between gap-2">
            <div>
              <div class="flex items-center gap-2">
                <span class="font-bold text-white text-xs font-mono">${escapeHtml(r.titolo_ricetta)}</span>
                <span class="text-[9px] px-1.5 py-0.5 rounded bg-tacblue/20 text-tacblue border border-tacblue/30 uppercase font-bold font-mono">
                  ${escapeHtml(r.calibro)}
                </span>
                ${isDemo ? '<span class="text-[9px] px-1 py-0.2 rounded bg-gray-800 text-gray-400 font-mono">Demo</span>' : ''}
              </div>
              <div class="text-[11px] text-gray-300 font-mono mt-1">
                <span class="text-tacamber font-bold">${r.dose_grani ? r.dose_grani.toFixed(1) + ' grs' : '-'}</span>
                <span class="text-gray-400">di</span> ${escapeHtml(r.marca_tipo_polvere || 'Polvere')} 
                • <span class="text-gray-400">Palla:</span> ${escapeHtml(r.marca_peso_palla || '-')} 
                • <span class="text-gray-400">OAL:</span> ${r.oal_scelto ? r.oal_scelto.toFixed(2) + ' mm' : '-'}
              </div>
              ${r.note_prestazione ? `<p class="text-[10px] text-gray-400 font-mono mt-1 italic">${escapeHtml(r.note_prestazione)}</p>` : ''}
            </div>

            <!-- Azioni Rapide -->
            <div class="flex items-center gap-1.5 flex-shrink-0">
              <button onclick="stampaEtichetta(${r.id})" title="Esporta Etichetta PDF" class="p-1.5 rounded bg-tacamber/20 hover:bg-tacamber text-tacamber hover:text-black border border-tacamber/40 transition">
                <i data-lucide="printer" class="w-3.5 h-3.5"></i>
              </button>
              <button onclick="caricaRicettaInForm(${r.id})" title="Carica / Modifica" class="p-1.5 rounded bg-tacborder hover:bg-gray-700 text-gray-300 transition">
                <i data-lucide="edit-3" class="w-3.5 h-3.5"></i>
              </button>
              <button onclick="eliminaRicetta(${r.id})" title="Elimina" class="p-1.5 rounded bg-red-950/40 hover:bg-red-900 text-red-400 border border-red-800/40 transition">
                <i data-lucide="trash-2" class="w-3.5 h-3.5"></i>
              </button>
            </div>
          </div>
        </div>
      `;
    }).join('');
    
    lucide.createIcons();
  } catch (err) {
    console.error("Errore ricette:", err);
    container.innerHTML = `<div class="text-red-400 text-xs font-mono text-center">Errore nel caricamento ricette.</div>`;
  }
}

async function salvaRicetta(e) {
  e.preventDefault();
  
  if (!operatoreCorrente) {
    alert("⚠️ È necessario accedere o creare un account per salvare le ricette nel tuo quaderno personale.");
    apriModaleAuth('login');
    return;
  }
  
  const id = document.getElementById('edit-ricetta-id').value;
  const payload = {
    calibro: document.getElementById('r-calibro').value.trim(),
    titolo_ricetta: document.getElementById('r-titolo').value.trim(),
    marca_peso_palla: document.getElementById('r-palla').value.trim(),
    marca_tipo_polvere: document.getElementById('r-polvere').value.trim(),
    dose_grani: parseFloat(document.getElementById('r-dose').value) || 0,
    oal_scelto: parseFloat(document.getElementById('r-oal').value) || 0,
    note_prestazione: document.getElementById('r-note').value.trim()
  };
  
  const url = id ? `/api/ricette/${id}` : '/api/ricette';
  const method = id ? 'PUT' : 'POST';
  
  try {
    const res = await fetch(url, {
      method: method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const result = await res.json();
    
    if (result.success) {
      resetFormRicetta();
      caricaRicette();
      
      const btn = document.getElementById('btn-salva-ricetta');
      const originalText = btn.innerHTML;
      btn.innerHTML = `<i data-lucide="check" class="w-4 h-4 text-white"></i><span>Salvato!</span>`;
      lucide.createIcons();
      setTimeout(() => { btn.innerHTML = originalText; lucide.createIcons(); }, 1500);
    } else {
      alert("Errore salvataggio: " + (result.error || "Operazione non riuscita"));
    }
  } catch (err) {
    console.error("Errore salvataggio:", err);
    alert("Errore di rete durante il salvataggio.");
  }
}

async function caricaRicettaInForm(id) {
  try {
    const res = await fetch(`/api/ricette/${id}`);
    const r = await res.json();
    
    document.getElementById('edit-ricetta-id').value = r.id;
    document.getElementById('r-calibro').value = r.calibro || '';
    document.getElementById('r-titolo').value = r.titolo_ricetta || '';
    document.getElementById('r-palla').value = r.marca_peso_palla || '';
    document.getElementById('r-polvere').value = r.marca_tipo_polvere || '';
    document.getElementById('r-dose').value = r.dose_grani || '';
    document.getElementById('r-oal').value = r.oal_scelto || '';
    document.getElementById('r-note').value = r.note_prestazione || '';
    
    aggiornaDoseGrammiRealtime();
    
    document.getElementById('btn-salva-ricetta').innerHTML = `
      <i data-lucide="refresh-cw" class="w-4 h-4"></i><span>Aggiorna Ricetta #${r.id}</span>
    `;
    lucide.createIcons();
    
    if (r.dose_grani) {
      document.getElementById('c-dose-grs').value = r.dose_grani;
      calcolaCostoLive();
    }
    
    document.getElementById('form-ricetta').scrollIntoView({ behavior: 'smooth', block: 'center' });
  } catch (err) {
    console.error("Errore caricamento ricetta:", err);
  }
}

function resetFormRicetta() {
  document.getElementById('edit-ricetta-id').value = '';
  document.getElementById('form-ricetta').reset();
  aggiornaDoseGrammiRealtime();
  document.getElementById('btn-salva-ricetta').innerHTML = `
    <i data-lucide="save" class="w-4 h-4"></i><span>Salva nel Quaderno</span>
  `;
  lucide.createIcons();
}

async function eliminaRicetta(id) {
  if (!confirm("Confermi l'eliminazione di questa ricetta dal tuo quaderno personale?")) return;
  
  try {
    const res = await fetch(`/api/ricette/${id}`, { method: 'DELETE' });
    const data = await res.json();
    if (data.success) {
      caricaRicette();
    } else {
      alert(data.error || "Impossibile eliminare questa ricetta.");
    }
  } catch (err) {
    console.error("Errore eliminazione:", err);
  }
}

function aggiornaDoseGrammiRealtime() {
  const grani = parseFloat(document.getElementById('r-dose').value) || 0;
  const grammi = grani * 0.0647989;
  document.getElementById('r-dose-grammi-tag').textContent = `≈ ${grammi.toFixed(3)} g`;
}

// ==========================================
// ESPORTAZIONE ETICHETTA PDF (ReportLab)
// ==========================================
function stampaEtichetta(id) {
  window.open(`/esporta_etichetta_pdf?id=${id}`, '_blank');
}

function stampaEtichettaDaForm() {
  const calibro = encodeURIComponent(document.getElementById('r-calibro').value || 'Calibro N.D.');
  const titolo = encodeURIComponent(document.getElementById('r-titolo').value || 'Lotto Personale');
  const palla = encodeURIComponent(document.getElementById('r-palla').value || 'Standard');
  const polvere = encodeURIComponent(document.getElementById('r-polvere').value || 'Standard');
  const dose = encodeURIComponent((document.getElementById('r-dose').value || '0') + ' grs');
  const oal = encodeURIComponent((document.getElementById('r-oal').value || '0') + ' mm');
  const innesco = encodeURIComponent(document.getElementById('r-innesco').value || 'Standard');
  const note = encodeURIComponent(document.getElementById('r-note').value || 'Verificato al poligono');
  
  const url = `/esporta_etichetta_pdf?calibro=${calibro}&titolo=${titolo}&palla=${palla}&polvere=${polvere}&dose=${dose}&oal=${oal}&innesco=${innesco}&note=${note}`;
  window.open(url, '_blank');
}

function stampaEtichettaRapida() {
  window.open('/esporta_etichetta_pdf', '_blank');
}

// ==========================================
// CALCOLATORE ECONOMICO AVANZATO
// ==========================================
function calcolaCostoLive() {
  const paccoPallaEur = parseFloat(document.getElementById('c-pacco-palla-eur')?.value) || 0;
  const paccoPallaQta = Math.max(1, parseInt(document.getElementById('c-pacco-palla-qta')?.value) || 1);
  const costoPalla = paccoPallaEur / paccoPallaQta;
  const pallaDisp = document.getElementById('c-singola-palla-display');
  if (pallaDisp) {
    pallaDisp.textContent = `€ ${costoPalla.toFixed(4)} / pz`;
  }

  const paccoInnescoEur = parseFloat(document.getElementById('c-pacco-innesco-eur')?.value) || 0;
  const paccoInnescoQta = Math.max(1, parseInt(document.getElementById('c-pacco-innesco-qta')?.value) || 1);
  const costoInnesco = paccoInnescoEur / paccoInnescoQta;
  const innescoDisp = document.getElementById('c-singolo-innesco-display');
  if (innescoDisp) {
    innescoDisp.textContent = `€ ${costoInnesco.toFixed(4)} / pz`;
  }

  const costoBarattolo = parseFloat(document.getElementById('c-barattolo-eur').value) || 0;
  const pesoBarattoloG = parseFloat(document.getElementById('c-barattolo-g').value) || 500;
  const doseGrani = parseFloat(document.getElementById('c-dose-grs').value) || 0;
  
  // Bossoli: calcolo da pacco e quantità
  const paccoBossoloEur = parseFloat(document.getElementById('c-pacco-bossolo-eur')?.value) || 0;
  const paccoBossoloQta = Math.max(1, parseInt(document.getElementById('c-pacco-bossolo-qta')?.value) || 1);
  const costoBossoloNuovo = paccoBossoloEur / paccoBossoloQta;
  const bossoloDisp = document.getElementById('c-singolo-bossolo-display');
  if (bossoloDisp) {
    bossoloDisp.textContent = `€ ${costoBossoloNuovo.toFixed(4)} / pz`;
  }
  const unitarioDisp = document.getElementById('c-costo-unitario-bossolo');
  if (unitarioDisp) {
    unitarioDisp.textContent = `Costo bossolo nuovo: €${costoBossoloNuovo.toFixed(4)}`;
  }
  
  const cicliBossolo = Math.max(1, parseInt(document.getElementById('c-bossolo-cicli').value) || 1);
  
  const doseGrammi = doseGrani * 0.0647989;
  document.getElementById('c-dose-g-display').textContent = `Grammi: ${doseGrammi.toFixed(3)} g`;
  
  let costoPolvereColpo = 0;
  if (pesoBarattoloG > 0) {
    costoPolvereColpo = (doseGrammi / pesoBarattoloG) * costoBarattolo;
  }
  document.getElementById('c-polvere-colpo-display').textContent = `Costo polvere: €${costoPolvereColpo.toFixed(4)}`;
  
  const quotaBossolo = costoBossoloNuovo / cicliBossolo;
  document.getElementById('c-quota-bossolo-display').textContent = `Quota ammortizzata: €${quotaBossolo.toFixed(4)} / colpo (${cicliBossolo} cicli)`;
  
  const costoSingolo = costoPalla + costoInnesco + costoPolvereColpo + quotaBossolo;
  const costo50 = costoSingolo * 50;
  const costo1000 = costoSingolo * 1000;
  
  document.getElementById('display-costo-singolo').textContent = `€ ${costoSingolo.toFixed(3)}`;
  document.getElementById('display-costo-50').textContent = `€ ${costo50.toFixed(2)}`;
  document.getElementById('display-costo-1000').textContent = `€ ${costo1000.toFixed(2)}`;
  
  const refCommerciale = 0.38;
  if (costoSingolo < refCommerciale) {
    const perc = ((refCommerciale - costoSingolo) / refCommerciale) * 100;
    document.getElementById('display-risparmio').textContent = `Risparmio: ~${perc.toFixed(0)}% vs factory`;
  } else {
    document.getElementById('display-risparmio').textContent = `Munizione Match Precision`;
  }
}

// ==========================================
// MODULO BALISTICO: PF & JOULE
// ==========================================
function setUnitaBalistica(u) {
  unitaBalistica = u;
  const btnMs = document.getElementById('btn-unita-ms');
  const btnFps = document.getElementById('btn-unita-fps');
  const label = document.getElementById('b-unita-label');
  const inputVel = document.getElementById('b-velocita');
  const curVal = parseFloat(inputVel.value) || 0;
  
  if (u === 'ms') {
    btnMs.className = 'py-1 text-xs font-mono font-bold rounded bg-tacamber text-black';
    btnFps.className = 'py-1 text-xs font-mono font-bold rounded text-gray-400 hover:text-white';
    label.textContent = 'M/S';
    if (curVal > 500) {
      inputVel.value = (curVal / 3.28084).toFixed(1);
    }
  } else {
    btnFps.className = 'py-1 text-xs font-mono font-bold rounded bg-tacamber text-black';
    btnMs.className = 'py-1 text-xs font-mono font-bold rounded text-gray-400 hover:text-white';
    label.textContent = 'FPS';
    if (curVal < 500 && curVal > 0) {
      inputVel.value = (curVal * 3.28084).toFixed(1);
    }
  }
  
  calcolaBalisticaLive();
}

function calcolaBalisticaLive() {
  const pesoGrani = parseFloat(document.getElementById('b-peso-grs').value) || 0;
  const velocita = parseFloat(document.getElementById('b-velocita').value) || 0;
  
  if (pesoGrani <= 0 || velocita <= 0) return;
  
  let fps = velocita;
  let ms = velocita;
  if (unitaBalistica === 'ms') {
    fps = velocita * 3.28084;
    ms = velocita;
  } else {
    fps = velocita;
    ms = velocita / 3.28084;
  }
  
  const pf = (pesoGrani * fps) / 1000.0;
  const joule = (pesoGrani * Math.pow(fps, 2)) / 450240.0;
  
  document.getElementById('b-res-pf').textContent = pf.toFixed(1);
  document.getElementById('b-res-joule').textContent = `${joule.toFixed(1)} J`;
  document.getElementById('b-res-fps').textContent = fps.toFixed(1);
  document.getElementById('b-res-ms').textContent = ms.toFixed(1);
  
  const badge = document.getElementById('b-status-badge');
  if (pf >= 170) {
    badge.textContent = "MAJOR // MASSIMA POTENZA";
    badge.className = "font-bold px-2 py-0.5 rounded bg-tacamber/20 text-tacamber border border-tacamber/40";
  } else if (pf >= 160) {
    badge.textContent = "MAJOR OPEN / MINOR STD";
    badge.className = "font-bold px-2 py-0.5 rounded bg-tacamber/20 text-tacamber border border-tacamber/40";
  } else if (pf >= 125) {
    badge.textContent = "MINOR // IDONEO GARA";
    badge.className = "font-bold px-2 py-0.5 rounded bg-tacgreen/20 text-tacgreen border border-tacgreen/40";
  } else {
    badge.textContent = "SUB-MINOR // NON QUALIFICATO";
    badge.className = "font-bold px-2 py-0.5 rounded bg-red-950/40 text-red-400 border border-red-800/40";
  }
  
  document.getElementById('ipsc-open').textContent = pf >= 160 ? 'MAJOR (>=160)' : (pf >= 125 ? 'MINOR' : 'SUB-MINOR');
  document.getElementById('ipsc-standard').textContent = pf >= 170 ? 'MAJOR (>=170)' : (pf >= 125 ? 'MINOR' : 'SUB-MINOR');
  document.getElementById('ipsc-production').textContent = pf >= 125 ? 'MINOR (Idoneo)' : 'SUB-MINOR';
  document.getElementById('ipsc-pcc').textContent = pf >= 125 ? 'REGOLAMENTARE (>=125)' : 'SUB-MINOR';
}

// ==========================================
// CRONOGRAFO: SD & EXTREME SPREAD
// ==========================================
async function calcolaSD() {
  const stringa = document.getElementById('chrono-stringa').value.trim();
  const unita = document.getElementById('chrono-unita').value;
  const errBox = document.getElementById('chrono-error');
  errBox.classList.add('hidden');
  
  try {
    const res = await fetch('/calcola_sd', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ velocita_stringa: stringa, unita: unita })
    });
    const data = await res.json();
    
    if (data.success) {
      document.getElementById('sd-media').textContent = data.media.toFixed(2);
      document.getElementById('sd-media-unit').textContent = data.unita;
      
      document.getElementById('sd-val').textContent = data.sd.toFixed(2);
      document.getElementById('sd-val-unit').textContent = data.unita;
      
      document.getElementById('sd-es').textContent = data.es.toFixed(2);
      document.getElementById('sd-es-unit').textContent = data.unita;
      
      document.getElementById('sd-count').textContent = `${data.count} colpi`;
      document.getElementById('sd-minmax').textContent = `Min: ${data.min} | Max: ${data.max}`;
      
      const giudizioLabel = document.getElementById('sd-giudizio');
      const box = document.getElementById('chrono-giudizio-box');
      giudizioLabel.textContent = data.giudizio;
      
      if (data.giudizio_color === 'green') {
        giudizioLabel.className = 'font-bold text-tacgreen';
        box.className = 'p-2.5 bg-black/50 border border-tacgreen/50 rounded flex items-center justify-between text-xs font-mono';
      } else if (data.giudizio_color === 'blue') {
        giudizioLabel.className = 'font-bold text-tacblue';
        box.className = 'p-2.5 bg-black/50 border border-tacblue/50 rounded flex items-center justify-between text-xs font-mono';
      } else if (data.giudizio_color === 'amber') {
        giudizioLabel.className = 'font-bold text-tacamber';
        box.className = 'p-2.5 bg-black/50 border border-tacamber/50 rounded flex items-center justify-between text-xs font-mono';
      } else {
        giudizioLabel.className = 'font-bold text-red-400';
        box.className = 'p-2.5 bg-black/50 border border-red-800/50 rounded flex items-center justify-between text-xs font-mono';
      }
    } else {
      errBox.textContent = data.error || 'Errore nei dati inseriti';
      errBox.classList.remove('hidden');
    }
  } catch (err) {
    console.error("Errore SD:", err);
    errBox.textContent = 'Errore di connessione con il modulo balistico.';
    errBox.classList.remove('hidden');
  }
}

function escapeHtml(text) {
  if (!text) return '';
  return String(text)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
