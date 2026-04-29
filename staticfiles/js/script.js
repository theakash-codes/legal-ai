/* LegalAI Pro — FINAL FIXED JS (WORKING ALL FEATURES) */

document.addEventListener('DOMContentLoaded', () => {

const API = window.location.origin;

const S = {
    token: localStorage.getItem('authToken'),
    username: localStorage.getItem('username') || 'User',
    docId: null,
    docText: '',
    docData: null
};

const $ = s => document.querySelector(s);

/* ================= TOAST ================= */
function toast(msg,type=''){
    const t = $('#toast');
    if(!t) return;
    t.textContent = msg;
    t.className = 'toast show ' + type;
    setTimeout(()=>t.className='toast',3000);
}

/* ================= NAVIGATION (FIXED) ================= */
document.querySelectorAll('.nav-item').forEach(btn=>{
    btn.addEventListener('click', ()=>{

        document.querySelectorAll('.nav-item').forEach(b=>b.classList.remove('active'));
        btn.classList.add('active');

        const section = btn.getAttribute('data-section');

        document.querySelectorAll('.section').forEach(sec=>sec.classList.remove('active'));

        const target = document.getElementById(`sec-${section}`);
        if(target) target.classList.add('active');

        const title = document.getElementById('section-title');
        if(title) title.textContent = btn.innerText.trim();
    });
});

/* ================= AUTH ================= */
function showDash(){
    $('#login-page')?.classList.add('hidden');
    $('#dashboard-page')?.classList.remove('hidden');
    $('#top-username').textContent = S.username;
    $('#user-badge').textContent = S.username[0].toUpperCase();
}

if(S.token) showDash();

/* ================= LOGIN ================= */
$('#login-btn')?.addEventListener('click', async ()=>{
    const email = $('#login-email').value.trim();
    const password = $('#login-password').value.trim();

    if(!email || !password){
        return toast('Enter email & password','error');
    }

    try{
        const r = await fetch(`${API}/auth/login/`,{
            method:'POST',
            headers:{'Content-Type':'application/json'},
            body:JSON.stringify({email,password})
        });

        const d = await r.json();

        if(!r.ok) throw new Error(d.error || 'Login failed');

        S.token = d.token;
        S.username = d.username || email;

        localStorage.setItem('authToken',S.token);
        localStorage.setItem('username',S.username);

        showDash();
        toast('Welcome!','success');

    }catch(e){
        toast(e.message,'error');
    }
});

/* ================= FILE UPLOAD ================= */
const fileInput = $('#file-input');
const dropZone = $('#drop-zone');

dropZone && (dropZone.onclick = ()=>fileInput.click());

fileInput && (fileInput.onchange = ()=>{
    if(fileInput.files[0]) uploadFile(fileInput.files[0]);
});

dropZone && (dropZone.ondrop = e=>{
    e.preventDefault();
    uploadFile(e.dataTransfer.files[0]);
});

dropZone && (dropZone.ondragover = e=>e.preventDefault());

async function uploadFile(file){

    const progress = $('#upload-progress');
    const bar = $('#progress-fill');

    progress?.classList.remove('hidden');
    if(bar) bar.style.width = '20%';

    try{
        const fd = new FormData();
        fd.append('file',file);

        const headers = {};
        if(S.token) headers['Authorization'] = `Token ${S.token}`;

        const r = await fetch(`${API}/api/process-document/`, {
            method:'POST',
            headers,
            body:fd
        });

        if(!r.ok) throw new Error('Upload failed');

        const d = await r.json();

        if(bar) bar.style.width = '100%';

        S.docId = d.document_id;

        if(!S.docId){
            toast("Document ID missing","error");
            return;
        }

        S.docData = d;
        S.docText = d.content || '';

        showPreview(d);
        populateSummary(d);
        populateRisk(d.risk);
        populateFraud(d.fraud);
        populateCompliance(d.compliance);
        populateSimplify(d);
        populateAnalytics(d);

        toast('Document uploaded!','success');

    }catch(e){
        toast(e.message,'error');
    }
}

/* ================= PREVIEW ================= */
function showPreview(d){
    $('#preview-panel')?.classList.remove('hidden');
    $('#preview-body').textContent = d.content || 'No content';
    $('#doc-type-badge').textContent = d.doc_type || 'Document';
}

/* ================= SUMMARY ================= */
function populateSummary(d){
    const card = $('#doc-summary-card');
    if(!card) return;

    card.classList.remove('hidden');

    if(d.ai_summary?.summary_lines){
        $('#summary-lines').innerHTML =
            d.ai_summary.summary_lines.map(x=>`
                <div><b>${x.label}</b>: ${x.value}</div>
            `).join('');
    } else {
        $('#summary-lines').innerHTML =
            `<p>${d.summary || 'No summary available'}</p>`;
    }
}

/* ================= RISK ================= */
function populateRisk(r){
    const body = $('#risk-clauses-body');
    if(!body) return;

    if(!r?.clauses){
        body.innerHTML = '<p>No risk data</p>';
        return;
    }

    body.innerHTML = r.clauses.map(c=>`
        <div class="clause-item ${c.level}">
            <b>${c.level}</b><br>${c.text}
        </div>
    `).join('');
}

/* ================= FRAUD ================= */
function populateFraud(f){
    const body = $('#fraud-alerts-body');
    if(!body) return;

    if(!f?.alerts){
        body.innerHTML = '<p>No fraud detected</p>';
        return;
    }

    body.innerHTML = f.alerts.map(a=>`
        <div class="fraud-alert ${a.severity}">
            <b>${a.label}</b><br>${a.description}
        </div>
    `).join('');
}

/* ================= COMPLIANCE ================= */
function populateCompliance(c){
    const body = $('#compliance-list-body');
    if(!body) return;

    if(!c?.items){
        body.innerHTML = '<p>No compliance data</p>';
        return;
    }

    body.innerHTML = c.items.map(i=>`
        <div>${i.passed ? '✅' : '❌'} ${i.label}</div>
    `).join('');
}

/* ================= SIMPLIFY ================= */
function populateSimplify(d){
    $('#simplify-original') && ($('#simplify-original').textContent = d.content || '');
    $('#simplify-simple') && ($('#simplify-simple').textContent = d.simplified?.simplified_text || '');
}

/* ================= ANALYTICS ================= */
function populateAnalytics(d){
    $('#stat-risk') && ($('#stat-risk').textContent = (d.risk?.risk_score || 0) + '%');
    $('#stat-fraud') && ($('#stat-fraud').textContent = (d.fraud?.fraud_score || 0) + '%');
}

/* ================= CHAT ================= */
$('#chat-send-btn')?.addEventListener('click', async ()=>{
    const msg = $('#chat-input').value;

    if(!msg) return;
    if(!S.docId) return toast("Upload document first","error");

    addChat(msg,'user');

    try{
        const r = await fetch(`${API}/api/chat/`,{
            method:'POST',
            headers:{'Content-Type':'application/json'},
            body:JSON.stringify({
                document_id:S.docId,
                question:msg
            })
        });

        const d = await r.json();
        addChat(d.answer || 'No response','ai');

    }catch{
        addChat('Error','ai');
    }
});

function addChat(text,type){
    const div = document.createElement('div');
    div.className = `chat-bubble ${type}`;
    div.textContent = text;
    $('#chat-messages').appendChild(div);
}

/* ================= TRANSLATE (FIXED) ================= */
$('#translate-btn')?.addEventListener('click', async ()=>{

    if(!S.docId){
        toast("Upload document first","error");
        return;
    }

    try{
        const r = await fetch(`${API}/api/translate/`,{
            method:'POST',
            headers:{'Content-Type':'application/json'},
            body:JSON.stringify({
                document_id:S.docId,
                text:S.docText
            })
        });

        const d = await r.json();

        $('#translate-output')?.classList.remove('hidden');
        $('#translate-body').textContent = d.translated_text || 'No translation';

        toast("Translated successfully","success");

    }catch{
        toast("Translation failed","error");
    }
});

/* ================= LOGOUT ================= */
$('#sidebar-logout-btn')?.addEventListener('click', ()=>{
    localStorage.clear();
    location.reload();
});

});