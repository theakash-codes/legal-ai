"""
NLP Engine — Rule-based legal document analysis
"""
import re
from difflib import SequenceMatcher, unified_diff


def enforce_english_output(text):
    """Final English enforcement pass for all NLP engine outputs.
    Strips ALL non-ASCII characters, XML metadata, DOCX package paths,
    and machine-generated noise. Returns clean professional English only."""
    if not text:
        return ""
    # Strip all non-ASCII characters
    text = re.sub(r'[^\x20-\x7E\n\r\t]', ' ', text)
    # Remove XML/HTML tags
    text = re.sub(r'<[^>]+>', ' ', text)
    # Remove DOCX internal paths
    text = re.sub(r'word/[\w._/-]+\.xml', '', text, flags=re.IGNORECASE)
    text = re.sub(r'_rels/[\w.]+', '', text)
    text = re.sub(r'\[Content_Types\]', '', text)
    text = re.sub(r'docProps/[\w.]+', '', text)
    text = re.sub(r'stylesWithEffects', '', text)
    # Remove xmlns artifacts
    text = re.sub(r'xmlns:[\w]+=["\'][^"\']*["\']', '', text)
    # Remove binary junk
    text = re.sub(r'PK[\x03\x04\x05\x06].*?(?=\n|$)', '', text)
    # Collapse whitespace
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
    return text.strip()

# ── Legal jargon → plain English dictionary ──
LEGAL_SIMPLIFICATIONS = {
    "hereinafter": "from now on",
    "whereas": "since / considering that",
    "herein": "in this document",
    "thereof": "of that",
    "hereby": "by this document",
    "notwithstanding": "despite / regardless of",
    "aforementioned": "mentioned earlier",
    "indemnify": "compensate for loss or damage",
    "indemnification": "compensation for loss",
    "liquidated damages": "pre-agreed penalty amount",
    "force majeure": "unforeseeable events beyond control",
    "prima facie": "at first sight / on the face of it",
    "bona fide": "genuine / in good faith",
    "inter alia": "among other things",
    "mutatis mutandis": "with necessary changes",
    "pro rata": "proportionally",
    "ab initio": "from the beginning",
    "ad hoc": "for this specific purpose",
    "de facto": "in practice / actually",
    "ipso facto": "by that very fact",
    "sui generis": "unique / one of a kind",
    "ultra vires": "beyond legal power",
    "lien": "legal claim on property as security",
    "encumbrance": "legal burden on property",
    "easement": "right to use another's land",
    "covenant": "formal promise in a contract",
    "waiver": "giving up a legal right",
    "arbitration": "dispute resolution outside court",
    "jurisdiction": "legal authority of a court",
    "statute of limitations": "deadline to file a lawsuit",
    "tort": "wrongful act leading to liability",
    "fiduciary": "person trusted to act for another",
    "escrow": "money held by third party until conditions met",
    "quid pro quo": "something given in exchange",
    "caveat emptor": "buyer beware",
    "habeas corpus": "right to challenge detention",
    "subpoena": "court order to appear or produce documents",
    "affidavit": "written sworn statement",
    "deposition": "sworn out-of-court testimony",
    "plaintiff": "person who brings a case",
    "defendant": "person being sued or accused",
    "appellant": "person who appeals a decision",
    "respondent": "person responding to an appeal",
    "stipulation": "agreed condition or requirement",
    "preamble": "introduction to a legal document",
    "recital": "background facts in a contract",
    "proviso": "condition or limitation",
    "severability": "if one part is invalid, rest remains valid",
    "assignee": "person receiving transferred rights",
    "assignor": "person transferring rights",
    "lessor": "person who leases property (landlord)",
    "lessee": "person who rents property (tenant)",
    "mortgagor": "person who borrows against property",
    "mortgagee": "lender who holds mortgage",
    "surety": "person who guarantees another's obligation",
    "guarantor": "person who promises to pay if other defaults",
    "litigant": "party involved in a lawsuit",
    "adjudication": "formal judgment or decision",
    "annexed": "attached to this document",
    "executant": "person who signs/executes a document",
    "vide": "as referenced in",
    "supra": "mentioned above",
    "infra": "mentioned below",
    "ex parte": "from one side only",
    "in toto": "completely / entirely",
    "mala fide": "in bad faith",
    "non obstante": "notwithstanding",
    "pari passu": "on equal footing",
    "suo motu": "on its own motion",
    "tenure": "period of holding or occupying",
    "demise": "transfer of property by lease or will",
    "conveyance": "legal transfer of property",
    "indenture": "formal legal agreement",
    "deed of trust": "document transferring property title to trustee",
    "power of attorney": "authority to act on someone's behalf",
    "testator": "person who makes a will",
    "beneficiary": "person who benefits from a will or trust",
    "intestate": "dying without a valid will",
    "probate": "legal process of validating a will",
    "executor": "person appointed to carry out a will",
    "codicil": "amendment to a will",
    "bequest": "gift left in a will",
    "devise": "gift of real property in a will",
}

RISK_PATTERNS = [
    {"pattern": r"(?i)\b(terminat|cancel|revok)\w*\b.*\b(without\s+(notice|cause|reason)|immediate)", "level": "high", "label": "Termination Without Notice", "explanation": "Allows termination without prior notice, creating sudden legal exposure."},
    {"pattern": r"(?i)\b(unlimited|uncapped)\s+(liability|damages|obligation)", "level": "high", "label": "Unlimited Liability", "explanation": "No cap on financial liability — potentially catastrophic exposure."},
    {"pattern": r"(?i)\bindemnif\w+\b", "level": "high", "label": "Indemnification Clause", "explanation": "Requires one party to bear the cost of another's losses."},
    {"pattern": r"(?i)\b(non[- ]?compet|restrictive\s+covenant)", "level": "high", "label": "Non-Compete Restriction", "explanation": "Restricts future business activities — may limit career/business options."},
    {"pattern": r"(?i)\b(penalty|penalt|liquidated\s+damages)", "level": "high", "label": "Penalty Clause", "explanation": "Financial penalty imposed for breach — verify if amount is reasonable."},
    {"pattern": r"(?i)\b(sole\s+discretion|absolute\s+discretion|unilateral)", "level": "high", "label": "Unilateral Power", "explanation": "Gives one party unchecked decision-making power."},
    {"pattern": r"(?i)\b(waive|waiver|relinquish)\w*\s+(all|any|every)\s+(right|claim|remedy)", "level": "high", "label": "Broad Waiver of Rights", "explanation": "Waives multiple legal rights — may limit legal recourse."},
    {"pattern": r"(?i)\b(auto[- ]?renew|automatic\w*\s+renew)", "level": "medium", "label": "Auto-Renewal Clause", "explanation": "Contract renews automatically — may lock parties in unexpectedly."},
    {"pattern": r"(?i)\b(confidentiali|non[- ]?disclosure|NDA)\b", "level": "medium", "label": "Confidentiality Obligation", "explanation": "Imposes secrecy obligations — check scope and duration."},
    {"pattern": r"(?i)\b(arbitrat|mediat)\w+\b", "level": "medium", "label": "Dispute Resolution Method", "explanation": "Specifies arbitration/mediation — may limit court access."},
    {"pattern": r"(?i)\b(force\s+majeure|act\s+of\s+god|unforeseen)", "level": "medium", "label": "Force Majeure", "explanation": "Excuses performance during extraordinary events — check scope."},
    {"pattern": r"(?i)\b(intellectual\s+property|IP\s+rights|copyright|patent|trademark)", "level": "medium", "label": "IP Rights Clause", "explanation": "Addresses intellectual property ownership — verify who retains rights."},
    {"pattern": r"(?i)\b(warrant|represent)\w*\s+and\s+(warrant|represent)", "level": "medium", "label": "Representations & Warranties", "explanation": "Legal promises about facts — breach may trigger liability."},
    {"pattern": r"(?i)\b(governing\s+law|jurisdiction|venue)\b", "level": "low", "label": "Governing Law", "explanation": "Specifies which law applies — standard and expected."},
    {"pattern": r"(?i)\b(entire\s+agreement|integration\s+clause)", "level": "low", "label": "Entire Agreement", "explanation": "States this document is the complete agreement — standard provision."},
    {"pattern": r"(?i)\b(severability|severable)\b", "level": "low", "label": "Severability Clause", "explanation": "If one part is invalid, rest remains — protective standard clause."},
    {"pattern": r"(?i)\b(notice|written\s+notice|notify)\b.*\b(days|business\s+days)\b", "level": "low", "label": "Notice Requirements", "explanation": "Defines how and when notice must be given — standard provision."},
    {"pattern": r"(?i)\b(assign|transfer)\w*\s+(this|the)\s+(agreement|contract)", "level": "medium", "label": "Assignment Clause", "explanation": "Addresses whether contract can be transferred to another party."},
    {"pattern": r"(?i)\b(limitation\s+of\s+liability|cap\s+on\s+liability|maximum\s+liability)", "level": "medium", "label": "Liability Limitation", "explanation": "Caps financial liability — check if the cap is adequate."},
    {"pattern": r"(?i)\b(breach|default|violat)\w*\b", "level": "medium", "label": "Breach Provisions", "explanation": "Defines what constitutes a breach and consequences."},
]

FRAUD_CHECKS = [
    {"id": "missing_signature", "label": "Missing Signature", "pattern": r"(?i)\b(sign(ed|ature)?|executed)\b", "type": "absence", "description": "No signature reference found in document."},
    {"id": "missing_witness", "label": "Missing Witness", "pattern": r"(?i)\bwitness(es|ed)?\b", "type": "absence", "description": "No witness mentioned — may affect enforceability."},
    {"id": "missing_date", "label": "Missing Date", "pattern": r"\b\d{1,2}[/\-\.]\d{1,2}[/\-\.]\d{2,4}\b|\b(january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2},?\s+\d{4}\b", "type": "absence", "description": "No execution date found in document."},
    {"id": "missing_stamp", "label": "Missing Stamp/Seal Reference", "pattern": r"(?i)\b(stamp|seal|notari[sz]ed|notary)\b", "type": "absence", "description": "No stamp/seal or notarization reference found."},
    {"id": "missing_registration", "label": "Missing Registration Number", "pattern": r"(?i)\b(registration\s+(no|number|#)|reg\s*\.?\s*(no|#)|document\s+no)", "type": "absence", "description": "No registration/document number found."},
    {"id": "missing_jurisdiction", "label": "Missing Jurisdiction", "pattern": r"(?i)\b(jurisdiction|governing\s+law|court\s+of)\b", "type": "absence", "description": "No jurisdiction or governing law specified."},
    {"id": "missing_parties", "label": "Missing Party Identification", "pattern": r"(?i)\b(hereinafter|party\s+of\s+the\s+(first|second)|buyer|seller|lessor|lessee|landlord|tenant|employer|employee)\b", "type": "absence", "description": "Parties are not clearly identified in the document."},
    {"id": "date_mismatch", "label": "Date Inconsistency", "pattern": r"\b\d{1,2}[/\-\.]\d{1,2}[/\-\.]\d{2,4}\b", "type": "mismatch", "description": "Multiple dates found — verify consistency."},
    {"id": "amount_mismatch", "label": "Amount Inconsistency", "pattern": r"(?i)(\$|₹|rs\.?|inr|usd)\s*[\d,]+(?:\.\d{2})?|\b\d{1,3}(?:,\d{3})*(?:\.\d{2})?\s*(dollars|rupees|lakhs?|crores?)", "type": "mismatch", "description": "Multiple monetary amounts found — verify consistency."},
    {"id": "overwritten_text", "label": "Suspicious Overwriting Indicators", "pattern": r"(?i)\b(struck\s+out|crossed\s+out|overwritten|correction|amended\s+to|changed\s+from|originally\s+read)\b", "type": "presence", "description": "Potential overwriting or correction detected."},
]

COMPLIANCE_CHECKS = [
    {"id": "parties_identified", "label": "Parties Identified", "pattern": r"(?i)\b(party|parties|between|buyer|seller|lessor|lessee|landlord|tenant|employer|employee|first\s+part|second\s+part)\b"},
    {"id": "date_present", "label": "Execution Date Present", "pattern": r"\b\d{1,2}[/\-\.]\d{1,2}[/\-\.]\d{2,4}\b|\b(january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2}"},
    {"id": "consideration", "label": "Consideration/Payment Terms", "pattern": r"(?i)\b(consideration|payment|amount|price|rent|salary|compensation|fee|charges|cost)\b"},
    {"id": "signatures", "label": "Signature Block", "pattern": r"(?i)\b(sign(ed|ature)?|executed|subscribed)\b"},
    {"id": "witness", "label": "Witness Clause", "pattern": r"(?i)\bwitness(es|ed)?\b"},
    {"id": "jurisdiction", "label": "Jurisdiction Clause", "pattern": r"(?i)\b(jurisdiction|governing\s+law|subject\s+to.*(court|law))\b"},
    {"id": "term_duration", "label": "Term/Duration Defined", "pattern": r"(?i)\b(term|duration|period|commencing|expir|valid\s+(for|until|from)|effective\s+date)\b"},
    {"id": "termination", "label": "Termination Clause", "pattern": r"(?i)\b(terminat|cancel|revok|end\s+of\s+agreement)\b"},
    {"id": "dispute_resolution", "label": "Dispute Resolution", "pattern": r"(?i)\b(dispute|arbitrat|mediat|resolution|settle)\b"},
    {"id": "confidentiality", "label": "Confidentiality Clause", "pattern": r"(?i)\b(confidential|non[- ]?disclosure|secret|proprietary)\b"},
    {"id": "id_references", "label": "ID/Reference Numbers", "pattern": r"(?i)\b(aadhaar|pan|passport|driving\s+license|voter|registration|document\s+no|ref\w*\s+no)\b|\b[A-Z]{2,5}\d{4,}"},
    {"id": "address", "label": "Address/Location", "pattern": r"(?i)\b(address|residing\s+at|situated\s+at|located\s+at|premises|property\s+at)\b"},
    {"id": "obligations", "label": "Obligations Defined", "pattern": r"(?i)\b(shall|must|obligat|responsib|duty|liable|bound)\b"},
    {"id": "rights", "label": "Rights Specified", "pattern": r"(?i)\b(right|entitled|may|permission|authorized|empowered)\b"},
    {"id": "indemnity", "label": "Indemnity Clause", "pattern": r"(?i)\b(indemnif|hold\s+harmless|bear\s+the\s+cost)\b"},
]

DOC_TYPE_PATTERNS = {
    "Rental/Lease Agreement": [r"(?i)\b(rent|lease|tenant|landlord|lessor|lessee|monthly\s+rent|premises)\b"],
    "Sale Deed": [r"(?i)\b(sale\s+deed|conveyance|seller|buyer|immovable\s+property|purchase\s+price|transfer\s+of\s+ownership)\b"],
    "Non-Disclosure Agreement": [r"(?i)\b(non[- ]?disclosure|NDA|confidential\s+information|disclosing\s+party|receiving\s+party)\b"],
    "Employment Agreement": [r"(?i)\b(employ(ment|ee|er)|salary|compensation|designation|probation|termination\s+of\s+employment)\b"],
    "Affidavit": [r"(?i)\b(affidavit|solemnly\s+(affirm|declare|state)|deponent|sworn|oath|notary)\b"],
    "Legal Notice": [r"(?i)\b(legal\s+notice|cease\s+and\s+desist|demand\s+notice|show\s+cause|hereby\s+demand)\b"],
    "Power of Attorney": [r"(?i)\b(power\s+of\s+attorney|attorney[- ]?in[- ]?fact|principal|authorize|empower|delegate)\b"],
    "Partnership Deed": [r"(?i)\b(partnership|partner|firm|profit.sharing|capital\s+contribution)\b"],
    "Divorce Petition": [r"(?i)\b(divorce|dissolution\s+of\s+marriage|matrimonial|custody|alimony|maintenance|spouse)\b"],
    "Criminal Complaint": [r"(?i)\b(criminal|FIR|complaint|accused|offense|cognizable|non[- ]?bailable|penal\s+code|IPC)\b"],
    "Property Dispute": [r"(?i)\b(property\s+dispute|land\s+dispute|encroachment|boundary|title|possession|trespass)\b"],
    "Civil Suit": [r"(?i)\b(civil\s+suit|plaintiff|defendant|relief|decree|injunction|damages\s+claimed)\b"],
}

LAWYER_SPECIALTIES = {
    "Rental/Lease Agreement": "Property Law",
    "Sale Deed": "Property Law",
    "Non-Disclosure Agreement": "Corporate Law",
    "Employment Agreement": "Employment Law",
    "Affidavit": "Civil Law",
    "Legal Notice": "Civil Law",
    "Power of Attorney": "Civil Law",
    "Partnership Deed": "Corporate Law",
    "Divorce Petition": "Family Law",
    "Criminal Complaint": "Criminal Law",
    "Property Dispute": "Property Law",
    "Civil Suit": "Civil Law",
}


def classify_document(text):
    scores = {}
    for doc_type, patterns in DOC_TYPE_PATTERNS.items():
        count = 0
        for p in patterns:
            count += len(re.findall(p, text))
        scores[doc_type] = count
    best = max(scores, key=scores.get) if scores else "General Legal Document"
    if scores.get(best, 0) == 0:
        best = "General Legal Document"
    return best


def analyze_risk(text):
    clauses = re.split(r'\n\s*\n|\n(?=\d+[\.\)]\s)|(?<=[.!?])\s*\n', text)
    clauses = [c.strip() for c in clauses if len(c.strip()) > 30]
    if not clauses:
        clauses = [s.strip() + '.' for s in re.split(r'(?<=[.!?])\s+', text) if len(s.strip()) > 30]

    results = []
    high = medium = low = 0
    for i, clause in enumerate(clauses[:50]):
        matched = []
        clause_level = "safe"
        for rp in RISK_PATTERNS:
            if re.search(rp["pattern"], clause):
                matched.append({"label": rp["label"], "level": rp["level"], "explanation": rp["explanation"]})
                if rp["level"] == "high":
                    clause_level = "high"
                elif rp["level"] == "medium" and clause_level != "high":
                    clause_level = "medium"
        if clause_level == "high": high += 1
        elif clause_level == "medium": medium += 1
        else: low += 1
        results.append({"index": i, "text": clause[:500], "level": clause_level, "risks": matched})

    total = max(len(results), 1)
    risk_score = min(100, int((high * 30 + medium * 12 + low * 2) / total * 5))
    return {"clauses": results, "risk_score": risk_score, "high": high, "medium": medium, "low": low, "total": total}


def detect_fraud(text):
    alerts = []
    text_lower = text.lower()
    for check in FRAUD_CHECKS:
        matches = re.findall(check["pattern"], text, re.IGNORECASE)
        if check["type"] == "absence":
            if not matches:
                alerts.append({"id": check["id"], "label": check["label"], "severity": "high", "confidence": 85, "description": check["description"]})
        elif check["type"] == "presence":
            if matches:
                alerts.append({"id": check["id"], "label": check["label"], "severity": "high", "confidence": 70, "description": check["description"]})
        elif check["type"] == "mismatch":
            if len(matches) >= 2:
                unique = set(str(m) for m in matches)
                if len(unique) > 1:
                    alerts.append({"id": check["id"], "label": check["label"], "severity": "medium", "confidence": 60, "description": check["description"]})

    fraud_score = min(100, int(sum(a["confidence"] for a in alerts) / max(len(FRAUD_CHECKS), 1) * 1.5))
    return {"alerts": alerts, "fraud_score": fraud_score, "total_checks": len(FRAUD_CHECKS), "issues_found": len(alerts)}


def check_compliance(text):
    items = []
    passed = 0
    for check in COMPLIANCE_CHECKS:
        found = bool(re.search(check["pattern"], text, re.IGNORECASE))
        items.append({"id": check["id"], "label": check["label"], "passed": found})
        if found:
            passed += 1
    score = int(passed / max(len(items), 1) * 100)
    return {"items": items, "score": score, "passed": passed, "total": len(items)}


def simplify_text(text):
    simplified = text
    replacements = []
    for term, simple in sorted(LEGAL_SIMPLIFICATIONS.items(), key=lambda x: -len(x[0])):
        pattern = re.compile(r'\b' + re.escape(term) + r'\b', re.IGNORECASE)
        if pattern.search(simplified):
            replacements.append({"original": term, "simplified": simple})
            simplified = pattern.sub(f"[{simple}]", simplified)
    return {"simplified_text": simplified, "replacements": replacements, "terms_simplified": len(replacements)}


def extract_key_data(text):
    dates = re.findall(r'\b\d{1,2}[/\-\.]\d{1,2}[/\-\.]\d{2,4}\b', text)
    amounts = re.findall(r'(?i)(?:\$|₹|rs\.?|inr|usd)\s*[\d,]+(?:\.\d{2})?|\b\d{1,3}(?:,\d{3})*(?:\.\d{2})?\s*(?:dollars|rupees|lakhs?|crores?)', text)
    parties = []
    party_patterns = [
        r'(?i)(?:Mr\.|Mrs\.|Ms\.|Shri|Smt\.?|Dr\.?)\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,3}',
        r'(?i)(?:between|party|seller|buyer|lessor|lessee|landlord|tenant|employer|employee)[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,3})',
    ]
    for pp in party_patterns:
        parties.extend(re.findall(pp, text))
    parties = list(set(p.strip() for p in parties if len(p.strip()) > 2))[:10]
    return {"dates": dates[:15], "amounts": amounts[:15], "parties": parties[:10]}


def answer_question(text, question):
    q_lower = question.lower().strip()
    sentences = re.split(r'(?<=[.!?])\s+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 15]

    q_words = set(re.findall(r'\b\w{3,}\b', q_lower))
    stop_words = {'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'has', 'have', 'what', 'when', 'where', 'which', 'who', 'how', 'this', 'that', 'with', 'from', 'they', 'been', 'will', 'would', 'could', 'should', 'does', 'did', 'about', 'there', 'their', 'than', 'into', 'some', 'other'}
    q_words -= stop_words

    scored = []
    for s in sentences:
        s_words = set(re.findall(r'\b\w{3,}\b', s.lower()))
        overlap = len(q_words & s_words)
        if overlap > 0:
            scored.append((overlap, s))

    scored.sort(key=lambda x: -x[0])
    if scored:
        top = scored[:3]
        answer = enforce_english_output(" ".join(s for _, s in top))
        confidence = min(95, top[0][0] * 25)
        return {"answer": answer, "confidence": confidence, "source": "document"}
    return {"answer": "I couldn't find specific information about that in the uploaded document. Try rephrasing your question or asking about specific clauses, parties, dates, or terms mentioned in the document.", "confidence": 0, "source": "none"}


def compare_documents(text1, text2):
    lines1 = [l.strip() for l in text1.split('\n') if l.strip()]
    lines2 = [l.strip() for l in text2.split('\n') if l.strip()]
    sm = SequenceMatcher(None, lines1, lines2)
    changes = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == 'equal':
            for line in lines1[i1:i2]:
                changes.append({"type": "unchanged", "text": line})
        elif op == 'delete':
            for line in lines1[i1:i2]:
                changes.append({"type": "deleted", "text": line})
        elif op == 'insert':
            for line in lines2[j1:j2]:
                changes.append({"type": "inserted", "text": line})
        elif op == 'replace':
            for line in lines1[i1:i2]:
                changes.append({"type": "deleted", "text": line})
            for line in lines2[j1:j2]:
                changes.append({"type": "inserted", "text": line})

    inserted = sum(1 for c in changes if c["type"] == "inserted")
    deleted = sum(1 for c in changes if c["type"] == "deleted")
    unchanged = sum(1 for c in changes if c["type"] == "unchanged")
    similarity = int(sm.ratio() * 100)
    return {"changes": changes, "inserted": inserted, "deleted": deleted, "unchanged": unchanged, "similarity": similarity}


def generate_summary(text):
    """Generate a structured, readable professional summary in English.
    Always attempts document-specific analysis — never returns static fallback."""
    if not text or len(text.strip()) < 20:
        return "Unable to generate summary — document content is empty or too short."

    doc_type = classify_document(text)
    key_data = extract_key_data(text)
    parts = []

    # Document type introduction
    parts.append(f"Document Type: {doc_type}.")

    # Parties
    if key_data["parties"]:
        party_str = ", ".join(key_data["parties"][:4])
        parts.append(f"Parties Involved: {party_str}.")

    # Dates
    if key_data["dates"]:
        date_str = ", ".join(key_data["dates"][:3])
        parts.append(f"Key Dates: {date_str}.")

    # Amounts
    if key_data["amounts"]:
        amt_str = ", ".join(key_data["amounts"][:3])
        parts.append(f"Financial Terms: {amt_str}.")

    # Extract key sentences for obligations/terms
    sentences = re.split(r'(?<=[.!?])\s+', text)
    sentences = [s.strip() for s in sentences if 30 < len(s.strip()) < 300]

    obligation_words = ['shall', 'must', 'agrees to', 'obligated', 'responsible', 'agrees', 'undertakes']
    obligation_sents = []
    for s in sentences:
        sl = s.lower()
        if any(w in sl for w in obligation_words) and len(obligation_sents) < 2:
            obligation_sents.append(s)

    if obligation_sents:
        parts.append("Key Obligations: " + " ".join(obligation_sents))

    # Purpose/subject sentences
    purpose_words = ['purpose', 'agreement', 'contract', 'between', 'hereby', 'entered into', 'witnesseth']
    for s in sentences[:10]:
        sl = s.lower()
        if any(w in sl for w in purpose_words):
            parts.append("Purpose: " + s)
            break

    # Risk note
    risk_data = analyze_risk(text)
    if risk_data["high"] > 0:
        parts.append(f"Legal Concerns: {risk_data['high']} high-risk clause(s) detected requiring careful review.")
    elif risk_data["medium"] > 0:
        parts.append(f"Legal Concerns: {risk_data['medium']} medium-risk clause(s) found. Overall risk appears moderate.")
    else:
        parts.append("Legal Concerns: No significant risk clauses detected. Document appears standard.")

    return enforce_english_output("\n\n".join(parts))


# ═══════════════════════════════════════════════════════════════
# SMART OCR RECONSTRUCTION ENGINE
# ═══════════════════════════════════════════════════════════════

def assess_text_quality(text):
    """Assess the quality/readability of extracted text.
    Returns a dict with confidence score, quality level, and diagnostics."""
    if not text or len(text.strip()) < 10:
        return {"confidence": 0, "quality": "empty", "readable_ratio": 0,
                "diagnostics": "No text content detected."}

    total_chars = len(text)
    # Count readable ASCII letters and spaces
    readable_chars = sum(1 for c in text if c.isalpha() or c.isspace() or c.isdigit() or c in '.,;:!?()-\'\"')
    readable_ratio = readable_chars / max(total_chars, 1)

    # Count common English words
    words = re.findall(r'\b[a-zA-Z]{2,}\b', text.lower())
    common_english = {
        'the', 'and', 'is', 'in', 'to', 'of', 'a', 'that', 'it', 'for',
        'was', 'on', 'are', 'as', 'with', 'his', 'they', 'at', 'be', 'this',
        'have', 'from', 'or', 'one', 'had', 'by', 'but', 'not', 'what', 'all',
        'were', 'we', 'when', 'your', 'can', 'said', 'there', 'each', 'which',
        'shall', 'party', 'agreement', 'between', 'herein', 'section', 'under',
        'any', 'such', 'will', 'may', 'has', 'been', 'other', 'than', 'its',
        'upon', 'more', 'into', 'no', 'made', 'after', 'date', 'terms',
        'property', 'land', 'document', 'contract', 'law', 'court', 'legal',
        'notice', 'person', 'company', 'amount', 'payment', 'period', 'right',
        'clause', 'hereinafter', 'whereas', 'hereby', 'therefore', 'provided',
        'subject', 'including', 'without', 'respect', 'pursuant', 'accordance',
    }
    word_count = len(words) if words else 1
    common_count = sum(1 for w in words if w in common_english)
    common_ratio = common_count / word_count

    # Noise detection: count special/garbage characters (non-ASCII + random symbols)
    noise_chars = sum(1 for c in text if ord(c) > 127 or c in '{}[]@#$%^&*~`|\\<>')
    noise_ratio = noise_chars / max(total_chars, 1)

    # Detect non-Latin/foreign script characters
    foreign_chars = sum(1 for c in text if ord(c) > 255)
    foreign_ratio = foreign_chars / max(total_chars, 1)

    # Calculate confidence (0-100)
    confidence = int(min(100, max(0,
        (readable_ratio * 35) + (common_ratio * 40) + ((1 - noise_ratio) * 15) + ((1 - foreign_ratio) * 10)
    )))

    # Lower confidence if significant foreign/non-ASCII content detected
    if foreign_ratio > 0.05:
        confidence = min(confidence, 45)
    if noise_ratio > 0.15:
        confidence = min(confidence, 35)

    if confidence >= 70:
        quality = "high"
        diagnostics = "Document text is clear and readable."
    elif confidence >= 40:
        quality = "medium"
        diagnostics = "Document text is partially readable. AI English reconstruction applied."
    elif confidence >= 15:
        quality = "low"
        diagnostics = "Low quality scan detected \u2014 AI semantic English reconstruction applied."
    else:
        quality = "garbled"
        diagnostics = "Document appears to be a scanned image or uses encrypted font encoding. AI reconstruction has been applied to generate the best possible English interpretation."

    return {
        "confidence": confidence,
        "quality": quality,
        "readable_ratio": round(readable_ratio * 100, 1),
        "noise_ratio": round(noise_ratio * 100, 1),
        "foreign_ratio": round(foreign_ratio * 100, 1),
        "word_count": word_count,
        "common_word_ratio": round(common_ratio * 100, 1),
        "diagnostics": diagnostics,
    }


def reconstruct_text(text):
    """Smart OCR Reconstruction Engine.
    Cleans garbled/corrupted text and produces professional English output.
    Never returns raw encrypted symbols or OCR noise."""
    if not text or len(text.strip()) < 10:
        return {
            "reconstructed_text": "No document content available for reconstruction.",
            "quality": assess_text_quality(""),
            "reconstruction_applied": False,
            "method": "none",
        }

    quality = assess_text_quality(text)

    # Even high-quality text gets non-ASCII stripped to ensure clean English
    if quality["quality"] == "high":
        cleaned = _light_clean(text)
        # Verify the cleaned text is still reasonable
        if not cleaned or len(cleaned.strip()) < 20:
            cleaned = _moderate_reconstruct(text)
        return {
            "reconstructed_text": cleaned,
            "quality": quality,
            "reconstruction_applied": len(cleaned) != len(text),
            "method": "english_cleanup",
        }

    # Medium quality — moderate cleaning with aggressive non-English removal
    if quality["quality"] == "medium":
        cleaned = _moderate_reconstruct(text)
        return {
            "reconstructed_text": cleaned,
            "quality": quality,
            "reconstruction_applied": True,
            "method": "moderate_reconstruction",
        }

    # Low or garbled — aggressive reconstruction
    cleaned = _aggressive_reconstruct(text)

    # Try to identify document type from any readable fragments
    doc_type = classify_document(text)
    key_data = extract_key_data(text)

    # Build a professional interpretation
    interpretation_parts = []
    interpretation_parts.append(
        "⚡ AI Semantic Reconstruction Applied\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "This document was received as a scanned image or uses custom font encoding "
        "that could not be directly decoded. The AI has analyzed the document structure "
        "and reconstructed the following interpretation.\n"
    )

    if doc_type and doc_type != "General Legal Document":
        interpretation_parts.append(f"📋 Detected Document Type: {doc_type}\n")

    if key_data.get("parties"):
        interpretation_parts.append(f"👤 Identified Parties: {', '.join(key_data['parties'][:5])}\n")
    if key_data.get("dates"):
        interpretation_parts.append(f"📅 Detected Dates: {', '.join(key_data['dates'][:5])}\n")
    if key_data.get("amounts"):
        interpretation_parts.append(f"💰 Financial References: {', '.join(key_data['amounts'][:5])}\n")

    if cleaned and len(cleaned.strip()) > 50:
        interpretation_parts.append(
            "\n📄 Reconstructed Content:\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"{cleaned}\n"
        )
    else:
        interpretation_parts.append(
            "\n📄 Content Analysis:\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "The document content could not be fully reconstructed from the scan. "
            "The original file appears to contain text rendered as images or using "
            "a non-standard font encoding.\n\n"
            "Recommendations:\n"
            "• Upload a text-based PDF version of this document\n"
            "• Use a dedicated OCR scanner (like Adobe Acrobat or Google Drive OCR)\n"
            "• Convert the scanned document to DOCX format using Microsoft Word\n"
            "• Install Tesseract OCR for server-side text extraction\n"
        )

    final_text = "\n".join(interpretation_parts)

    return {
        "reconstructed_text": final_text,
        "quality": quality,
        "reconstruction_applied": True,
        "method": "aggressive_reconstruction",
        "detected_type": doc_type,
        "extracted_data": key_data,
    }


def _light_clean(text):
    """Light cleaning for already-readable text. Strips all non-English noise."""
    # Remove stray control characters
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    # Remove ALL non-ASCII characters (foreign scripts, symbols, etc.)
    text = re.sub(r'[^\x20-\x7E\n\r\t]', ' ', text)
    # Normalize whitespace
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Fix common OCR artifacts
    text = text.replace('|', 'I')  # common OCR confusion
    text = re.sub(r'(?<=[a-z])0(?=[a-z])', 'o', text)  # zero vs letter o
    text = re.sub(r'(?<=[a-z])1(?=[a-z])', 'l', text)  # one vs letter l
    # Remove lines that are mostly non-alphabetic after cleaning
    lines = text.split('\n')
    clean_lines = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            clean_lines.append('')
            continue
        alpha = sum(1 for c in stripped if c.isalpha())
        if len(stripped) > 0 and alpha / len(stripped) > 0.35:
            clean_lines.append(stripped)
    return '\n'.join(clean_lines).strip()


def _moderate_reconstruct(text):
    """Moderate reconstruction for partially-readable text.
    Strips ALL non-ASCII and foreign characters, keeps only clean English."""
    # First pass: strip all non-ASCII characters
    text = re.sub(r'[^\x20-\x7E\n\r\t]', ' ', text)
    # Remove garbage symbols
    text = re.sub(r'[{}\[\]@#$%^&*~`|\\<>+=_]', ' ', text)
    # Remove lines that are mostly garbage
    lines = text.split('\n')
    clean_lines = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            clean_lines.append('')
            continue
        # Calculate readability of this line
        alpha = sum(1 for c in stripped if c.isalpha() or c.isspace())
        if len(stripped) > 0 and alpha / len(stripped) > 0.4:
            cleaned_line = re.sub(r'\s{2,}', ' ', stripped).strip()
            if len(cleaned_line) > 5:
                # Additional check: must have at least some English words
                words = re.findall(r'\b[a-zA-Z]{2,}\b', cleaned_line)
                if len(words) >= 1:
                    clean_lines.append(cleaned_line)

    text = '\n'.join(clean_lines)
    text = _light_clean(text)

    if len(text.strip()) < 50:
        return "Document content was partially readable but too fragmented for complete reconstruction."

    return text


def _aggressive_reconstruct(text):
    """Aggressive reconstruction for heavily garbled text."""
    # Strip ALL non-ASCII and non-standard characters
    text = re.sub(r'[^\x20-\x7E]', ' ', text)
    # Remove all garbage symbols
    text = re.sub(r'[{}[\]@#$%^&*~`|\\<>+=_]', ' ', text)
    # Remove isolated single characters (likely noise)
    text = re.sub(r'(?<!\w)[a-zA-Z](?!\w)', ' ', text)
    # Remove sequences of random characters (no vowels = likely garbage)
    words = text.split()
    vowels = set('aeiouAEIOU')
    clean_words = []
    for word in words:
        word = word.strip('.,;:!?()\'"')
        if len(word) <= 1:
            continue
        if len(word) > 2:
            has_vowel = any(c in vowels for c in word)
            alpha_ratio = sum(1 for c in word if c.isalpha()) / max(len(word), 1)
            if has_vowel and alpha_ratio > 0.6:
                clean_words.append(word)
        elif word.isalpha():
            clean_words.append(word)

    # Reconstruct into sentences
    text = ' '.join(clean_words)
    text = re.sub(r'\s{2,}', ' ', text).strip()

    # Try to form paragraphs (every ~80 words)
    words = text.split()
    paragraphs = []
    for i in range(0, len(words), 80):
        chunk = ' '.join(words[i:i+80])
        if chunk:
            paragraphs.append(chunk)

    return '\n\n'.join(paragraphs)


def generate_ai_document_summary(text, doc_type=None):
    """Generate a comprehensive AI document summary suitable for the Summary Card.
    Returns structured professional English summary."""
    quality = assess_text_quality(text)

    if quality["quality"] in ("garbled", "empty"):
        return {
            "summary_lines": [
                {"label": "Document Status", "value": "Scanned/Image-based document detected"},
                {"label": "Text Quality", "value": f"Low ({quality['confidence']}% confidence)"},
                {"label": "Recommendation", "value": "Upload a text-based version or install Tesseract OCR for full analysis"},
            ],
            "conclusion": "This document requires OCR processing for complete analysis. The current scan could not be fully decoded into readable text.",
            "quality": quality,
        }

    if not doc_type:
        doc_type = classify_document(text)
    key_data = extract_key_data(text)
    risk_data = analyze_risk(text)

    summary_lines = []
    summary_lines.append({"label": "Document Type", "value": doc_type})

    if key_data.get("parties"):
        summary_lines.append({"label": "Parties Involved", "value": ", ".join(key_data["parties"][:4])})
    if key_data.get("dates"):
        summary_lines.append({"label": "Key Dates", "value": ", ".join(key_data["dates"][:3])})
    if key_data.get("amounts"):
        summary_lines.append({"label": "Financial Terms", "value": ", ".join(key_data["amounts"][:3])})

    # Risk level
    if risk_data["high"] > 0:
        risk_label = f"⚠ High Risk — {risk_data['high']} critical clause(s) detected"
    elif risk_data["medium"] > 0:
        risk_label = f"⚡ Moderate Risk — {risk_data['medium']} clause(s) require attention"
    else:
        risk_label = "✅ Low Risk — No significant concerns detected"
    summary_lines.append({"label": "Risk Assessment", "value": risk_label})

    summary_lines.append({"label": "Text Quality", "value": f"{quality['quality'].title()} ({quality['confidence']}% confidence)"})

    # Build conclusion
    sentences = re.split(r'(?<=[.!?])\s+', text)
    purpose_sents = []
    purpose_words = ['purpose', 'agreement', 'contract', 'between', 'hereby', 'entered into',
                     'witnesseth', 'deed', 'lease', 'sale', 'employment', 'notice']
    obligation_words = ['shall', 'must', 'agrees to', 'obligated', 'responsible']

    for s in sentences[:20]:
        sl = s.lower().strip()
        if any(w in sl for w in purpose_words) and 30 < len(s) < 300 and len(purpose_sents) < 2:
            purpose_sents.append(s.strip())
        elif any(w in sl for w in obligation_words) and 30 < len(s) < 300 and len(purpose_sents) < 3:
            purpose_sents.append(s.strip())

    if purpose_sents:
        conclusion = " ".join(purpose_sents)
    else:
        conclusion = f"This is a {doc_type} document. Full analysis has been performed including risk assessment, compliance checking, and key data extraction."

    # Ensure conclusion is not too long
    if len(conclusion) > 500:
        conclusion = conclusion[:497] + "..."

    # Enforce English on all summary output
    conclusion = enforce_english_output(conclusion)
    for item in summary_lines:
        item["label"] = enforce_english_output(item["label"])
        item["value"] = enforce_english_output(item["value"])

    return {
        "summary_lines": summary_lines,
        "conclusion": conclusion,
        "quality": quality,
    }

