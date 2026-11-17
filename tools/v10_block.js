/* ================= v10: live backend, legal duties, seller onboarding ================= */
/* Public site only (ON_SITE): accounts via Supabase, direct payment while no payment provider is
   connected, DSA notice-and-action, DAC7 / trader data, operator data from betreiber.json,
   Cardmarket stock import. Inside claude.ai none of this changes anything. */
let OPERATOR=null;
if(ON_SITE)fetch("betreiber.json",{cache:"no-cache"}).then(r=>r.ok?r.json():null).then(o=>{OPERATOR=o;if(["#impressum","#datenschutz","#agb","#hilfe","#ueber"].includes(location.hash))rerender()}).catch(()=>{});
const OPKEY={"Firmenname oder Vor- und Nachname":"name","Firmenname":"name","Rechtsform, z. B. Einzelunternehmen oder GmbH":"form","Straße und Hausnummer":"street","PLZ Ort":"city",
  "kontakt@deine-domain.at":"email","E-Mail":"email","support@deine-domain.at":"email","+43 …":"phone","ATU…":"uid","FN … , Landesgericht …":"fn",
  "Bezirkshauptmannschaft oder Magistrat":"authority","Fachgruppe":"wko","Gründer:innen, Standort und Geschichte von Foilio":"about"};
function opVal(label){
  if(!OPERATOR)return "";
  if(label==="Anschrift")return [OPERATOR.street,OPERATOR.city].filter(Boolean).join(", ");
  const k=OPKEY[label];return k&&OPERATOR[k]?String(OPERATOR[k]):"";
}
const opComplete=()=>!!(OPERATOR&&OPERATOR.name&&OPERATOR.street&&OPERATOR.city&&OPERATOR.email);
const opMail=()=>OPERATOR&&OPERATOR.email||"";

/* ---------- legal pages for the public site ---------- */
const sec=(h,t)=>`<section><h2>${h}</h2><p>${t}</p></section>`;
const LEGAL_LIVE={
 agb:["Allgemeine Geschäftsbedingungen","Regeln für Kauf und Verkauf auf Foilio in der Startphase.",()=>`
  ${opComplete()?"":`<div class="banner"><p><b>Entwurf.</b> Vor dem Start rechtlich prüfen lassen und die Betreiberangaben in betreiber.json eintragen.</p></div>`}
  ${[["1. Betreiber und Geltungsbereich",`Foilio wird betrieben von ${PH("Firmenname")}, ${PH("Anschrift")}. Diese Bedingungen gelten für die Nutzung des Marktplatzes. Kaufverträge kommen ausschließlich zwischen Käufer:in und Verkäufer:in zustande. Foilio ist nicht Vertragspartei, sondern stellt die Plattform bereit.`],
    ["2. Konto","Zum Kaufen und Verkaufen ist ein Konto mit gültiger E-Mail-Adresse nötig. Kaufen und Verkaufen ist ab 18 Jahren erlaubt. Pro Person ist ein Konto zulässig. Zugangsdaten sind geheim zu halten."],
    ["3. Private und gewerbliche Verkäufer:innen","Wer gewerblich verkauft, muss das in den Verkäuferangaben angeben und Name, Anschrift, Kontaktdaten und gegebenenfalls Firmenbuch- und UID-Nummer hinterlegen. Diese Angaben werden Käufer:innen angezeigt (Art. 30 Digital Services Act). Bei gewerblichen Verkäufen gelten die Verbraucherrechte, insbesondere das 14-tägige Rücktrittsrecht nach dem FAGG."],
    ["4. Angebote","Angebote müssen die Karte wahrheitsgemäß beschreiben: Zustand (MT bis PO), Sprache, Foil, Grading samt Zertifikatsnummer. Fotos müssen die angebotene Karte zeigen. Fälschungen, Proxies, Nachdrucke und gestohlene Ware sind verboten."],
    ["5. Bestellung und Bezahlung","Mit „Verbindlich bestellen“ gibt die Käuferin oder der Käufer ein verbindliches Angebot ab. In der Startphase wird direkt zwischen den Beteiligten bezahlt: Die Verkäuferin oder der Verkäufer nennt im Chat die Zahlungsdaten. Wir empfehlen PayPal „Waren und Dienstleistungen“ wegen des Käuferschutzes. Foilio nimmt in der Startphase kein Geld entgegen und bietet keine Treuhand an."],
    ["6. Versand","Verkäufer:innen versenden innerhalb von 3 Werktagen nach Zahlungseingang, gut geschützt. Ab einem Warenwert von 25 € ist Versand mit Sendungsverfolgung Pflicht. Die Sendungsnummer wird im Chat mitgeteilt."],
    ["7. Gebühren","In der Startphase ist Foilio kostenlos: keine Einstellgebühr, keine Provision. Gebühren werden frühestens nach Ankündigung mit 30 Tagen Vorlauf eingeführt und gelten nur für danach eingestellte Angebote."],
    ["8. Bewertungen","Bewertungen müssen sich auf die konkrete Transaktion beziehen und sachlich sein. Gekaufte oder beleidigende Bewertungen werden entfernt."],
    ["9. Meldungen, Moderation und Beschwerden","Rechtswidrige Inhalte und Verstöße gegen diese Bedingungen können über „Melden“ auf jeder Kartenseite gemeldet werden, auch ohne Konto. Foilio prüft Meldungen zeitnah, sorgfältig und objektiv, informiert über die Entscheidung samt Begründung und bietet die Möglichkeit, dagegen Beschwerde einzulegen (Art. 16, 17 und 20 Digital Services Act). Kontaktstelle: "+PH("E-Mail")+"."],
    ["10. Sperren und Kündigung","Foilio kann Angebote entfernen und Konten sperren, wenn sie gegen Gesetze oder diese Bedingungen verstoßen. Die Entscheidung wird begründet. Nutzer:innen können ihr Konto jederzeit löschen."],
    ["11. Meldung an die Finanzverwaltung","Foilio ist nach dem Digitale-Plattformen-Meldepflichtgesetz (DAC7) verpflichtet, Verkäufer:innen ab 30 Verkäufen oder 2.000 € Umsatz im Kalenderjahr an das Finanzamt zu melden. Dafür sind die Verkäuferangaben nötig. Ohne sie können Angebote eingeschränkt werden."],
    ["12. Haftung","Foilio haftet für eigene Leistungen nach den gesetzlichen Bestimmungen. Für Erfüllung, Mängel und Zahlung der Kaufverträge zwischen Nutzer:innen haften die jeweiligen Vertragsparteien."],
    ["13. Schlussbestimmungen","Es gilt österreichisches Recht unter Ausschluss der Verweisungsnormen. Zwingende Verbraucherschutzvorschriften des Wohnsitzlandes bleiben unberührt."]].map(([h,t])=>sec(h,t)).join("")}`],
 datenschutz:["Datenschutzerklärung","Welche Daten Foilio verarbeitet, wofür und welche Rechte du hast.",()=>`
  ${opComplete()?"":`<div class="banner"><p><b>Entwurf.</b> Vor dem Start rechtlich prüfen lassen und die Betreiberangaben in betreiber.json eintragen.</p></div>`}
  ${[["Verantwortlich",`${PH("Firmenname")}, ${PH("Anschrift")}, ${PH("E-Mail")}.`],
    ["Ohne Konto",`Beim Aufruf der Website verarbeitet unser Hosting-Anbieter GitHub (GitHub Inc., USA; zertifiziert nach dem EU-US Data Privacy Framework) technisch notwendige Daten wie IP-Adresse und Zeitpunkt. Portfolio, Warenkorb, Wants-Liste und Einstellungen speichert die Seite nur in deinem Browser. Es gibt keine Tracking- oder Werbe-Cookies und keine Analyse-Dienste.`],
    ["Mit Konto",`E-Mail-Adresse und Name für die Anmeldung, deine Angebote samt Fotos, Bestellungen, Nachrichten, Preisvorschläge, Profil, Portfolio und Preisalarme. Gespeichert bei Supabase (Supabase Inc., Rechenzentrum in der EU) als Auftragsverarbeiter. Angebote, Profil und Tauschlisten sind öffentlich sichtbar. Nachrichten und Bestellungen sehen nur die Beteiligten. Verkäufe werden ohne Käuferdaten zur Preisberechnung verwendet.`],
    ["Verkäuferangaben",`Für Verkäufer:innen speichern wir Name, Anschrift, Geburtsdatum, Steuer- oder UID-Nummer und Bankverbindung, weil wir sie nach dem Digitale-Plattformen-Meldepflichtgesetz (DAC7) ab den gesetzlichen Schwellen an das Finanzamt melden müssen (Art. 6 Abs. 1 lit. c DSGVO). Bei gewerblichen Verkäufer:innen werden Name, Anschrift und Kontakt Käufer:innen angezeigt (Art. 30 DSA).`],
    ["Meldungen",`Wenn du einen Inhalt meldest, verarbeiten wir die Meldung und deine Kontaktdaten, um sie zu prüfen und dich über die Entscheidung zu informieren (Art. 16 DSA, Art. 6 Abs. 1 lit. c DSGVO).`],
    ["Zwecke und Rechtsgrundlagen",`Vertragserfüllung (Art. 6 Abs. 1 lit. b DSGVO) für Konto und Marktplatz, rechtliche Pflichten (lit. c) für Aufbewahrung und Meldungen, berechtigte Interessen (lit. f) für Betrugsprävention und Sicherheit.`],
    ["Kartenscanner",`Das Foto beim Scannen wird nur in deinem Browser verarbeitet und nicht hochgeladen, außer du verwendest es als Angebotsfoto.`],
    ["Speicherdauer",`Solange das Konto besteht. Daten zu Verkäufen und DAC7-Meldungen 10 Jahre (gesetzliche Aufbewahrungspflicht), Buchhaltungsdaten 7 Jahre.`],
    ["Deine Rechte",`Auskunft, Berichtigung, Löschung, Einschränkung, Datenübertragbarkeit und Widerspruch. Den Export deiner Daten findest du unter Konto. Kontakt: ${PH("E-Mail")}. Beschwerden kannst du bei der österreichischen Datenschutzbehörde einbringen (dsb.gv.at).`]].map(([h,t])=>sec(h,t)).join("")}`],
 gebuehren:["Gebühren","Foilio ist in der Startphase kostenlos.",()=>`
  <section><div class="banner"><p><b>Startphase: 0 % Provision.</b> Einstellen, Verkaufen und Kaufen kosten nichts. Änderungen kündigen wir mindestens 30 Tage vorher an.</p></div>
  <h2>Verkaufen</h2><div class="tbl-wrap"><table><tbody>
   <tr><td>Angebot einstellen</td><td class="num">0,00 €</td></tr><tr><td>Provision bei Verkauf</td><td class="num">0 %</td></tr>
   <tr><td>CSV- und Cardmarket-Import</td><td class="num">0,00 €</td></tr></tbody></table></div></section>
  <section><h2>Kaufen</h2><div class="tbl-wrap"><table><tbody>
   <tr><td>Kaufen über Foilio</td><td class="num">0,00 €</td></tr>
   <tr><td>Versand Standardbrief (Richtwert, bis 25 €)</td><td class="num">1,35 €</td></tr>
   <tr><td>Versand mit Sendungsverfolgung (Richtwert, ab 25 €)</td><td class="num">4,90 €</td></tr></tbody></table></div>
   <p class="muted" style="font-size:13px">Bezahlt wird in der Startphase direkt bei der Verkäuferin oder dem Verkäufer. Für Käuferschutz empfehlen wir PayPal „Waren und Dienstleistungen“.</p></section>`]
};
const HELP_LIVE=[["Bezahlung und Treuhand","Bezahlung"],
  ["Erst wenn du den Empfang bestätigst. Bis dahin liegt das Geld sicher bei Foilio.","In der Startphase zahlst du direkt an die Verkäuferin oder den Verkäufer, sobald du die Zahlungsdaten im Chat bekommen hast. Foilio nimmt kein Geld entgegen."],
  ["Foilio-Guthaben, Karte, Apple Pay und SEPA.","Das vereinbart ihr im Chat. Wir empfehlen PayPal „Waren und Dienstleistungen“ wegen des Käuferschutzes. Zahle nie per Geschenkkarte oder an Dritte."],
  ["Dein Geld bleibt in Treuhand, bis der Fall gelöst ist.","Schreib zuerst der Verkäuferin oder dem Verkäufer. Hast du mit PayPal „Waren und Dienstleistungen“ bezahlt, greift dort der Käuferschutz. Betrug meldest du über „Angebot oder Inhalt melden“."],
  ["Die Prüfung macht ein regulierter Zahlungsdienstleister.","Wir prüfen deine Verkäuferdaten und schalten danach das Abzeichen frei."]];
function infoFor(k){
  if(!(ON_SITE&&PAYMENTS==="off"))return INFO[k];
  if(k==="hilfe"){const [t,d,body]=INFO.hilfe;return [t,d,()=>HELP_LIVE.reduce((h,[a,b])=>h.split(a).join(b),body())]}
  return LEGAL_LIVE[k]||INFO[k];
}

/* ---------- preview ribbon: public site without backend ---------- */
if(ON_SITE&&!LIVE_MODE){const r=document.createElement("div");r.className="pv-ribbon";r.innerHTML=`Vorschau: Angebote und Verkäufer:innen sind Beispiele. Echte Preise und Preisverlauf.`;document.body.prepend(r)}

/* ---------- logged-out visitors still see the live market ---------- */
function liveReadOnly(db,user){
  S.db=db;S.user=user;S.uid=null;
  db.collection("listings").onSnapshot(snap=>{const map={};snap.docs.forEach(d=>{const it=d.data()?.items;if(Array.isArray(it))map[d.id]=it.slice(0,MAXL)});S.shared=map;Object.values(map).flat().forEach(l=>l.card&&registerCustom(l.card));ensureNames(Object.keys(map)).then(softRefresh)},e=>console.warn(e));
  db.collection("orders").onSnapshot(snap=>{const sold=new Set(),all=[];snap.docs.forEach(d=>(d.data()?.items||[]).forEach(o=>{sold.add(o.lid);all.push({...o,buyer:d.id})}));S.sold=sold;S.allOrders=all;softRefresh()},e=>console.warn(e));
  db.collection("profiles").onSnapshot(snap=>{const map={};snap.docs.forEach(d=>{const v=d.data();if(v)map[d.id]=v});S.profiles=map;ensureNames(Object.keys(map))},e=>console.warn(e));
}
function traderTag(uid){if(!LIVE_MODE)return "Community";const p=S.profiles&&S.profiles[uid];return p&&p.trader?"Gewerblich":"Privat"}

/* ---------- account: sign in ---------- */
function vLogin(){
  const st={sent:false,email:""};
  const draw=()=>{view.innerHTML=`<div class="pf-head"><span class="eyebrow">Konto</span><h1>${st.sent?"Schau in dein Postfach":"Anmelden oder registrieren"}</h1><p class="muted">${st.sent?`Wir haben einen Anmeldelink an <b>${esc(st.email)}</b> geschickt. Öffne ihn in diesem Browser.`:"Ohne Passwort: Du bekommst einen Anmeldelink per E-Mail. Neue Konten werden dabei automatisch angelegt."}</p></div>
  ${st.sent?`<section class="panel" style="display:grid;gap:10px;max-width:520px;padding:18px"><p>Keine E-Mail bekommen? Prüfe den Spam-Ordner oder versuche es in einer Minute noch einmal.</p><button class="btn" id="lgBack">Andere E-Mail-Adresse</button></section>`:
  `<section class="panel" style="display:grid;gap:12px;max-width:520px;padding:18px">
    <div class="field"><label for="lgName">Name auf Foilio <span class="muted">(nur bei neuem Konto, öffentlich sichtbar)</span></label><input class="input" id="lgName" maxlength="40" autocomplete="nickname" placeholder="z. B. Kartenfuchs_Linz"></div>
    <div class="field"><label for="lgMail">E-Mail-Adresse</label><input class="input" id="lgMail" type="email" autocomplete="email" inputmode="email" value="${esc(st.email)}" placeholder="du@beispiel.at"></div>
    <label style="display:flex;gap:10px;align-items:flex-start;font-size:14px"><input type="checkbox" id="lgAgb" style="margin-top:3px"> <span>Ich bin mindestens 18 Jahre alt und akzeptiere die <a href="#agb">AGB</a>. Die <a href="#datenschutz">Datenschutzerklärung</a> habe ich gelesen.</span></label>
    <button class="btn primary lg block" id="lgGo">${ICON.send} Anmeldelink senden</button></section>`}
  <section class="feat" style="margin-top:8px"><div><b>Angebote für alle sichtbar</b><p>Deine Karten erscheinen sofort im Marktplatz.</p></div><div><b>Überall synchron</b><p>Portfolio, Wants und Preisalarme auf allen Geräten.</p></div><div><b>Kostenlos</b><p>In der Startphase 0 % Provision.</p></div></section>`;
    const b=$("#lgBack");if(b)b.onclick=()=>{st.sent=false;draw()};
    const g=$("#lgGo");if(!g)return;
    g.onclick=async()=>{
      const email=$("#lgMail").value.trim(),name=$("#lgName").value.trim();
      if(!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)){toast("Bitte eine gültige E-Mail-Adresse eingeben.");$("#lgMail").focus();return}
      if(!$("#lgAgb").checked){toast("Bitte bestätige Alter und AGB.");return}
      g.disabled=true;g.textContent="Sende …";
      try{await FolioBackend.signIn(email,name);st.sent=true;st.email=email;buzz(10);draw()}
      catch(e){g.disabled=false;g.innerHTML=`${ICON.send} Anmeldelink senden`;toast(/rate|security purposes/i.test(e&&e.message||"")?"Zu viele Versuche. Bitte warte eine Minute.":"Senden hat nicht geklappt. Bitte später erneut versuchen.")}
    };
  };
  draw();
}
function vKonto(){
  if(LIVE_MODE&&!S.uid)return vLogin();
  vKontoBase();
  if(!LIVE_MODE)return;
  const head=$("#balVal")&&$("#balVal").closest("section");
  if(head){head.outerHTML=`<section class="pf-head stage"><span class="eyebrow">Mein Konto</span><div class="pf-value" style="font-size:clamp(26px,5vw,40px)">${esc(S.myName||"Sammler:in")}</div><p class="muted" id="accMail" style="margin:0"></p>
    <div class="hero-cta" style="flex-wrap:wrap"><button class="btn white" data-act="sellerdata">${ICON.shield} Verkäuferdaten</button><button class="btn glass" data-act="rename">Name ändern</button><button class="btn glass" data-act="logout">Abmelden</button></div></section>`;
    FolioBackend.email().then(m=>{const e=$("#accMail");if(e)e.textContent=m})}
  $$("#view section").forEach(s=>{const h=s.querySelector(".sec-h h2");if(h&&/Guthaben/.test(h.textContent))s.remove()});
  $$("#view .qgrid > *").forEach(t=>{if(/Freunde einladen/.test(t.textContent))t.remove()});
  const ban=$("#view .banner");if(ban&&/Konto bestätigen/.test(ban.textContent))ban.remove();
  dac7Check();
}
/* ---------- DAC7: sellers above the reporting thresholds need their data on file ---------- */
function mySalesThisYear(){const y=new Date().getFullYear();return (S.allOrders||[]).filter(o=>o.seller===S.uid&&new Date(o.at).getFullYear()===y&&!refundOf(o))}
function dac7Check(){
  if(!S.db||!S.uid)return;
  if(S.taxDone===undefined){S.taxDone=null;S.db.doc("data/users/"+S.uid+"/tax").onSnapshot(s=>{const was=S.taxDone;S.taxDone=!!s.exists;if(was===null&&location.hash==="#konto")softRefresh()},()=>{})}
  const sales=mySalesThisYear(),sum=sales.reduce((a,o)=>a+o.price,0);
  if(S.taxDone===false&&(sales.length>=25||sum>=1500)){const v=$("#view");v&&v.insertAdjacentHTML("afterbegin",`<div class="banner"><p><b>Verkäuferangaben nötig:</b> Du hast dieses Jahr ${sales.length} Verkäufe (${eur(sum)}). Ab 30 Verkäufen oder 2.000 € müssen wir dich nach DAC7 dem Finanzamt melden.</p><button class="btn sm dark" data-act="sellerdata">${ICON.shield} Angaben ergänzen</button></div>`)}
}
function openSellerData(reason){
  if(!S.uid){toast("Bitte melde dich zuerst an.");location.hash="#konto";return}
  const st={trader:!!S.myProfile.trader,name:"",birth:"",street:"",city:"",country:S.myProfile.country||"AT",tin:"",vat:"",fn:"",iban:""};
  const draw=()=>{
    $("#sheetIn").innerHTML=`<div class="rowline"><div><span class="eyebrow">Sicherheit und Pflichtangaben</span><h2>Verkäuferangaben</h2></div><button class="iconbtn" data-act="close" aria-label="Schließen">${ICON.x}</button></div>
    ${reason?`<div class="banner"><p>${esc(reason)}</p></div>`:""}
    <div class="seg"><button class="${st.trader?"":"on"}" data-sdt="0">Privat</button><button class="${st.trader?"on":""}" data-sdt="1">Gewerblich</button></div>
    ${st.trader?`<p class="muted" style="font-size:13px">Gewerblich: Name, Anschrift und E-Mail werden Käufer:innen angezeigt (Art. 30 DSA). Es gilt das 14-tägige Rücktrittsrecht.</p>`:""}
    ${[["sdName","name",st.trader?"Firmenname oder Vor- und Nachname":"Vor- und Nachname","text"],["sdBirth","birth","Geburtsdatum","date"],["sdStreet","street","Straße und Hausnummer","text"],["sdCity","city","PLZ und Ort","text"],
       ["sdTin","tin","Steuernummer oder Steuer-ID (für DAC7)","text"],...(st.trader?[["sdVat","vat","UID-Nummer (falls vorhanden)","text"],["sdFn","fn","Firmenbuchnummer (falls eingetragen)","text"]]:[]),["sdIban","iban","IBAN (für die Meldung, keine Abbuchung)","text"]]
      .map(([id,k,l,t])=>`<div class="field"><label for="${id}">${l}</label><input class="input" id="${id}" type="${t}" data-sdk="${k}" value="${esc(st[k])}"></div>`).join("")}
    <p class="muted" style="font-size:12.5px">Diese Angaben sind privat und nur für Foilio sichtbar (außer bei Gewerblich: Name, Anschrift, E-Mail). Wir prüfen sie und schalten danach das Verifiziert-Abzeichen frei.</p>
    <button class="btn primary lg block" id="sdGo">${ICON.shield} Speichern</button>`;
    $$("[data-sdt]").forEach(b=>b.onclick=()=>{st.trader=b.dataset.sdt==="1";draw()});
    $$("[data-sdk]").forEach(i=>i.oninput=()=>st[i.dataset.sdk]=i.value);
    $("#sdGo").onclick=async e=>{
      if(!st.name.trim()||!st.street.trim()||!st.city.trim()||!st.birth){toast("Bitte Name, Geburtsdatum und Anschrift ausfüllen.");return}
      if(st.iban&&!/^[A-Z]{2}\d{2}[A-Z0-9]{11,30}$/.test(st.iban.replace(/\s/g,"").toUpperCase())){toast("Die IBAN sieht nicht richtig aus.");return}
      e.currentTarget.disabled=true;
      try{
        await S.db.doc("data/users/"+S.uid+"/tax").set({...st,iban:st.iban.replace(/\s/g,"").toUpperCase(),email:await FolioBackend.email(),at:Date.now()});
        S.myProfile={...S.myProfile,trader:st.trader?{name:st.name.trim(),address:st.street.trim()+", "+st.city.trim(),email:await FolioBackend.email(),vat:st.vat.trim(),fn:st.fn.trim()}:false};
        saveProfile();S.taxDone=true;closeSheet();buzz([10,30,20]);toast("Gespeichert. Wir prüfen deine Angaben und schalten das Abzeichen frei.");setTimeout(rerender,300);
      }catch(err){console.warn(err);e.currentTarget.disabled=false;toast("Speichern hat nicht geklappt.")}
    };
  };
  openSheet();draw();
  S.db.doc("data/users/"+S.uid+"/tax").onSnapshot(s=>{if(s.exists&&!st.name){Object.assign(st,s.data());draw()}},()=>{});
}

/* ---------- checkout while no payment provider is connected: honest direct payment ---------- */
function vCart(){
  vCartBase();
  if(!(LIVE_MODE&&PAYMENTS==="off"))return;
  const b=$('#view [data-act="checkout"]');if(b)b.innerHTML=`${ICON.send} Bestellen`;
  const n=b&&b.closest("aside")&&[...b.closest("aside").querySelectorAll("p.muted")].pop();
  if(n)n.textContent="Bezahlt wird direkt bei der Verkäuferin oder dem Verkäufer. Für Käuferschutz empfehlen wir PayPal „Waren und Dienstleistungen“.";
}
function openCheckoutDirect(){
  const groups={};S.cart.forEach(i=>(groups[i.sellerUid||i.seller]=groups[i.sellerUid||i.seller]||[]).push(i));
  const st={addr:ls.get("addr","")};
  $("#sheetIn").innerHTML=`<div class="rowline"><div><span class="eyebrow">Bestellen</span><h2>Verbindlich bestellen</h2></div><button class="iconbtn" data-act="close" aria-label="Schließen">${ICON.x}</button></div>
  <div class="escrow"><div><i>1</i>Du bestellst verbindlich</div><div><i>2</i>Du bekommst die Zahlungsdaten im Chat und zahlst direkt</div><div><i>3</i>Die Karte kommt per Post, du bestätigst den Empfang</div></div>
  <div class="panel" style="padding:4px 14px">${Object.entries(groups).map(([k,g])=>{const s=g.reduce((a,i)=>a+i.price,0),sh=groupShip(g[0].seller,s);return `<div class="tx"><span><b>${esc(g[0].seller)}</b><br><small class="muted">${g.length} Karte${g.length>1?"n":""} · Versand ca. ${eur(sh)}</small></span><b class="num">${eur(s+sh)}</b></div>`}).join("")}</div>
  <div class="field"><label for="coAddr">Lieferadresse <span class="muted">(geht nur an die Verkäufer:innen dieser Bestellung)</span></label><textarea class="input" id="coAddr" rows="3" autocomplete="shipping street-address" placeholder="Vor- und Nachname&#10;Straße und Hausnummer&#10;PLZ Ort">${esc(st.addr)}</textarea></div>
  <p class="muted" style="font-size:12.5px">Foilio nimmt in der Startphase kein Geld entgegen. Zahle nie per Geschenkkarte oder an Dritte. Für Käuferschutz: PayPal „Waren und Dienstleistungen“.</p>
  <button class="btn primary lg block" id="coGo">${ICON.send} Verbindlich bestellen · ${eur(cartTotal(S.cart))}</button>`;
  openSheet();
  $("#coGo").onclick=async e=>{
    const addr=$("#coAddr").value.trim();if(addr.length<12||addr.split("\n").length<2){toast("Bitte die vollständige Lieferadresse eingeben.");$("#coAddr").focus();return}
    e.currentTarget.disabled=true;ls.set("addr",addr);
    const now=Date.now();
    Object.entries(groups).forEach(([k,g])=>{const ship=groupShip(g[0].seller,g.reduce((a,i)=>a+i.price,0));
      g.forEach((i,n)=>S.myOrders.push({oid:uidGen(),lid:i.offerId,cardId:i.cardId,price:i.price,shipShare:n===0?ship:0,ins:0,sellerName:i.seller,seller:i.sellerUid,graded:i.graded||null,cond:i.cond,at:now,pay:"direct",...(i.bid?{bid:i.bid}:{})}));
      if(i0(g).sellerUid){const list=g.map(i=>`• ${fullName(getCard(i.cardId)||{name:i.cardId})} (${i.graded?gradeLabel(i.graded):i.cond}) ${eur(i.price)}`).join("\n");
        S.msgs.push({id:uidGen(),to:i0(g).sellerUid,text:`Neue Bestellung:\n${list}\nVersand: ${eur(ship)} · Gesamt: ${eur(g.reduce((a,i)=>a+i.price,0)+ship)}\n\nLieferadresse:\n${addr}\n\nBitte schick mir die Zahlungsdaten.`,at:now,order:true})}});
    S.cart.forEach(i=>S.sold.add(i.offerId));
    try{await saveOrders();saveMsgs()}catch(err){console.warn(err);toast("Bestellung konnte nicht gespeichert werden.");e.currentTarget.disabled=false;return}
    S.cart=[];saveCart();
    $("#sheetIn").innerHTML=`<div class="success"><div class="check">${ICON.check}</div><h2>Bestellung gesendet</h2><p class="muted">Die Verkäufer:innen haben deine Bestellung und Adresse im Chat. Sie schicken dir dort die Zahlungsdaten. Nach dem Erhalt bestätigst du unter Konto den Empfang.</p><a class="btn primary block" href="#konto">Zu Bestellungen und Nachrichten</a></div>`;
    confetti(innerWidth/2,innerHeight*.45);buzz([10,30,10,30,20]);
    if(location.hash==="#warenkorb")setTimeout(()=>{view.innerHTML="";vCart()},50);
  };
}
const i0=g=>g[0];

/* ---------- DSA notice and action: report on every card page, also without an account ---------- */
function vCard(id){
  vCardBase(id);
  const c=getCard(id);if(!ON_SITE||!c)return;
  const offers=allOffers(c).filter(o=>o.type!=="Beispiel"&&!o.demo);
  const traders=[...new Set(offers.map(o=>o.sellerUid))].map(u=>[u,S.profiles&&S.profiles[u]&&S.profiles[u].trader]).filter(([,t])=>t);
  $("#view").insertAdjacentHTML("beforeend",`${traders.length?`<section><div class="sec-h"><h2>Angaben gewerblicher Verkäufer:innen</h2></div><div class="panel" style="padding:4px 16px">${traders.map(([u,t])=>`<div class="tx"><span><b>${esc(t.name)}</b><br><small class="muted">${esc(t.address)} · ${esc(t.email)}${t.vat?" · UID "+esc(t.vat):""}${t.fn?" · "+esc(t.fn):""}</small></span></div>`).join("")}</div></section>`:""}
  <p class="muted" style="font-size:13px;margin-top:18px">Stimmt mit einem Angebot etwas nicht? <button class="linkbtn" data-act="report" data-card="${esc(c.id)}" style="background:none;border:0;padding:0;color:var(--accent);font:inherit;text-decoration:underline;cursor:pointer">Angebot oder Inhalt melden</button></p>`);
}
function openReport(cardId){
  const c=getCard(cardId), offers=c?allOffers(c).filter(o=>!o.demo):[];
  const reasons=["Fälschung oder Nachdruck","Falsche Beschreibung oder fremde Fotos","Betrugsverdacht","Verletzt Urheber- oder Markenrechte","Sonstiger rechtswidriger Inhalt"];
  $("#sheetIn").innerHTML=`<div class="rowline"><div><span class="eyebrow">Meldung nach dem Digital Services Act</span><h2>Inhalt melden</h2></div><button class="iconbtn" data-act="close" aria-label="Schließen">${ICON.x}</button></div>
  <div class="field"><label for="rpWhat">Was meldest du?</label><select class="input" id="rpWhat">${offers.map(o=>`<option value="${esc(o.id)}">Angebot von ${esc(o.seller)} · ${eur(o.price)}</option>`).join("")}<option value="page">Die Kartenseite selbst</option></select></div>
  <div class="field"><label for="rpWhy">Grund</label><select class="input" id="rpWhy">${reasons.map(r=>`<option>${r}</option>`).join("")}</select></div>
  <div class="field"><label for="rpText">Begründung <span class="muted">(warum ist der Inhalt rechtswidrig oder regelwidrig?)</span></label><textarea class="input" id="rpText" rows="4" maxlength="2000"></textarea></div>
  <div class="field"><label for="rpName">Dein Name</label><input class="input" id="rpName" autocomplete="name"></div>
  <div class="field"><label for="rpMail">Deine E-Mail-Adresse <span class="muted">(für die Rückmeldung zur Entscheidung)</span></label><input class="input" id="rpMail" type="email" autocomplete="email"></div>
  <label style="display:flex;gap:10px;align-items:flex-start;font-size:14px"><input type="checkbox" id="rpGood" style="margin-top:3px"> <span>Ich bin in gutem Glauben davon überzeugt, dass die Angaben in dieser Meldung richtig und vollständig sind.</span></label>
  <button class="btn primary lg block" id="rpGo">Meldung absenden</button>`;
  openSheet();
  $("#rpGo").onclick=async e=>{
    const r={id:uidGen(),at:Date.now(),url:location.href,cardId,target:$("#rpWhat").value,reason:$("#rpWhy").value,text:$("#rpText").value.trim(),name:$("#rpName").value.trim(),email:$("#rpMail").value.trim()};
    if(r.text.length<10){toast("Bitte begründe die Meldung kurz.");return}
    if(!$("#rpGood").checked){toast("Bitte bestätige die Richtigkeit der Angaben.");return}
    e.currentTarget.disabled=true;
    if(S.db&&S.uid){
      try{const mine=ls.get("reports",[]);mine.push(r);await S.db.doc("reports/"+S.uid).set({items:mine.slice(-100),updatedAt:Date.now()});ls.set("reports",mine);closeSheet();toast("Danke. Wir prüfen die Meldung und melden uns per E-Mail.");return}
      catch(err){console.warn(err)}
    }
    const to=opMail();
    if(!to){toast("Meldungen sind erst möglich, wenn der Betreiber seine Kontaktdaten hinterlegt hat.");e.currentTarget.disabled=false;return}
    location.href=`mailto:${encodeURIComponent(to)}?subject=${encodeURIComponent("DSA-Meldung: "+r.reason)}&body=${encodeURIComponent(`Inhalt: ${r.url} (${r.target})\nGrund: ${r.reason}\n\n${r.text}\n\nName: ${r.name}\nE-Mail: ${r.email}\nIch bestätige, dass die Angaben in gutem Glauben richtig und vollständig sind.`)}`;
    closeSheet();
  };
}

/* ---------- Cardmarket stock export → Foilio offers ---------- */
const CM_LANG={"1":"EN","2":"FR","3":"DE","4":"ES","5":"IT","6":"ZH","7":"JP","8":"PT","9":"RU","10":"KO","11":"ZH",english:"EN",german:"DE",deutsch:"DE",french:"FR",spanish:"ES",italian:"IT",japanese:"JP",portuguese:"PT",korean:"KO"};
async function importCSV(text){
  const rows=parseCSV(text.replace(/^﻿/,""));if(!rows.length){toast("Die Datei ist leer.");return}
  const head=rows[0].map(h=>h.trim().toLowerCase().replace(/[^a-z]/g,""));
  const isCM=head.includes("expansion")||head.includes("idproduct")||(head.includes("count")&&head.includes("price"));
  if(!isCM)return importCSVBase(text);
  toast("Cardmarket-Datei erkannt. Katalog wird geladen …");
  try{await Promise.all(ALLG.map(loadGame))}catch(e){console.warn(e)}
  const col=k=>head.indexOf(k), at=(r,k)=>{const i=col(k);return i>=0?(r[i]||"").trim():""};
  const norm=s=>String(s||"").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g,"").replace(/[^a-z0-9]+/g," ").trim();
  const bySet={};pool().forEach(c=>{const k=norm(c.name)+"|"+norm(c.set);(bySet[k]=bySet[k]||[]).push(c);const ka=c.alias?norm(c.alias)+"|"+norm(c.set):null;if(ka)(bySet[ka]=bySet[ka]||[]).push(c)});
  const out=[["cardId","name","set","zustand","sprache","foil","grading","menge","preis","kommentar"]];let miss=0;
  rows.slice(1).forEach(r=>{
    const name=at(r,"name")||at(r,"enname")||at(r,"localname"),exp=at(r,"expansion")||at(r,"expansionname")||at(r,"set");
    const c=(bySet[norm(name)+"|"+norm(exp)]||[])[0];
    if(!c){miss++;return}
    const lang=CM_LANG[(at(r,"language")||at(r,"idlanguage")).toLowerCase()]||"EN";
    out.push([c.id,c.name,c.set,(at(r,"condition")||"NM").toUpperCase(),lang,/^(1|true|yes|x|foil)$/i.test(at(r,"isfoil")||at(r,"foil"))?"ja":"",
      "",at(r,"count")||at(r,"amount")||"1",at(r,"price"),at(r,"comments")||at(r,"comment")]);
  });
  if(miss)toast(`${miss} Zeile${miss>1?"n":""} nicht im Katalog gefunden (Name und Set müssen auf Englisch übereinstimmen).`);
  importCSVBase(out.map(r=>r.map(v=>/[",\n;]/.test(v)?`"${String(v).replace(/"/g,'""')}"`:v).join(",")).join("\n"));
}

/* ---------- extra actions ---------- */
document.addEventListener("click",async e=>{
  const a=e.target.closest("[data-act]");if(!a)return;const act=a.dataset.act;
  if(act==="logout")FolioBackend.signOut();
  if(act==="sellerdata")openSellerData();
  if(act==="report")openReport(a.dataset.card);
  if(act==="rename"){const n=prompt("Neuer Name auf Foilio (öffentlich sichtbar):",S.myName||"");if(n&&n.trim()){try{await FolioBackend.setName(n.trim().slice(0,40));S.myName=n.trim().slice(0,40);saveProfile();rerender();toast("Name geändert.")}catch{toast("Ändern hat nicht geklappt.")}}}
});
