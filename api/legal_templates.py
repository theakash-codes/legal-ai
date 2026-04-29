"""
Legal clause templates for document drafting
"""

TEMPLATES = {
    "rental_agreement": {
        "title": "Rental/Lease Agreement",
        "template": """RENTAL AGREEMENT

This Rental Agreement ("Agreement") is entered into on {date} between:

LANDLORD: {landlord_name}, residing at {landlord_address} (hereinafter referred to as "Lessor")

AND

TENANT: {tenant_name}, residing at {tenant_address} (hereinafter referred to as "Lessee")

1. PROPERTY DESCRIPTION
The Lessor hereby agrees to lease the property situated at {property_address} ("Premises") to the Lessee for residential/commercial purposes.

2. TERM OF LEASE
This lease shall commence on {start_date} and shall remain in effect for a period of {duration} months, terminating on {end_date}, unless renewed by mutual written consent.

3. MONTHLY RENT
The Lessee agrees to pay a monthly rent of {rent_amount} (Rupees {rent_in_words} Only), payable on or before the {payment_day} of each calendar month.

4. SECURITY DEPOSIT
The Lessee shall deposit a sum of {deposit_amount} (Rupees {deposit_in_words} Only) as security deposit, refundable upon termination subject to deductions for damages if any.

5. MAINTENANCE
The Lessee shall maintain the premises in good condition and shall be responsible for minor repairs. Major structural repairs shall be the responsibility of the Lessor.

6. TERMINATION
Either party may terminate this agreement by providing {notice_period} days written notice to the other party.

7. GOVERNING LAW
This Agreement shall be governed by and construed in accordance with the laws of {jurisdiction}.

IN WITNESS WHEREOF, the parties have executed this Agreement on the date first written above.

LESSOR: ___________________          LESSEE: ___________________
Name: {landlord_name}                Name: {tenant_name}

WITNESS 1: ___________________       WITNESS 2: ___________________
"""
    },
    "nda": {
        "title": "Non-Disclosure Agreement",
        "template": """NON-DISCLOSURE AGREEMENT

This Non-Disclosure Agreement ("Agreement") is entered into on {date} between:

DISCLOSING PARTY: {disclosing_party}, {disclosing_address}
RECEIVING PARTY: {receiving_party}, {receiving_address}

1. DEFINITION OF CONFIDENTIAL INFORMATION
"Confidential Information" means any and all non-public information, including but not limited to technical, business, financial, and operational information disclosed by the Disclosing Party.

2. OBLIGATIONS
The Receiving Party agrees to:
(a) Hold all Confidential Information in strict confidence
(b) Not disclose Confidential Information to any third party without prior written consent
(c) Use Confidential Information solely for the purpose of {purpose}
(d) Take reasonable measures to protect the confidentiality of such information

3. EXCLUSIONS
This Agreement does not apply to information that:
(a) Is or becomes publicly available through no fault of the Receiving Party
(b) Was known to the Receiving Party prior to disclosure
(c) Is independently developed by the Receiving Party
(d) Is required to be disclosed by law or court order

4. TERM
This Agreement shall remain in effect for {duration} from the date of execution.

5. REMEDIES
The Receiving Party acknowledges that breach may cause irreparable harm, entitling the Disclosing Party to seek injunctive relief in addition to other remedies.

6. GOVERNING LAW
This Agreement shall be governed by the laws of {jurisdiction}.

DISCLOSING PARTY: ___________________    RECEIVING PARTY: ___________________
Name: {disclosing_party}                 Name: {receiving_party}
Date: {date}                              Date: {date}
"""
    },
    "sale_deed": {
        "title": "Sale Deed",
        "template": """SALE DEED

This Sale Deed is executed on {date} at {location}.

BETWEEN:

SELLER: {seller_name}, S/o/D/o {seller_parent}, aged {seller_age} years, residing at {seller_address}, holding {id_type} No. {id_number} (hereinafter called the "VENDOR")

AND

BUYER: {buyer_name}, S/o/D/o {buyer_parent}, aged {buyer_age} years, residing at {buyer_address} (hereinafter called the "PURCHASER")

WHEREAS the Vendor is the absolute owner of the property described herein and has agreed to sell the same to the Purchaser for a total consideration of {sale_amount} (Rupees {amount_in_words} Only).

PROPERTY DESCRIPTION:
{property_description}
Survey No: {survey_number}
Total Area: {area}
Bounded by: North - {north_boundary}, South - {south_boundary}, East - {east_boundary}, West - {west_boundary}

NOW THIS DEED WITNESSES AS FOLLOWS:

1. The Vendor hereby sells, conveys, transfers and assigns the above-described property to the Purchaser free from all encumbrances.

2. The Purchaser has paid the total consideration of {sale_amount} to the Vendor (receipt acknowledged).

3. The Vendor warrants that the property is free from all liens, charges, and encumbrances.

4. The Vendor shall execute all necessary documents for transfer of title.

IN WITNESS WHEREOF, the parties have signed this deed on the date mentioned above.

VENDOR: ___________________          PURCHASER: ___________________
Name: {seller_name}                   Name: {buyer_name}

WITNESS 1: ___________________       WITNESS 2: ___________________
"""
    },
    "affidavit": {
        "title": "Affidavit",
        "template": """AFFIDAVIT

I, {deponent_name}, S/o/D/o {parent_name}, aged {age} years, residing at {address}, do hereby solemnly affirm and state as follows:

1. That I am the deponent herein and am competent to swear this affidavit.

2. That {statement_1}

3. That {statement_2}

4. That {statement_3}

5. That the statements made above are true and correct to the best of my knowledge and belief and nothing material has been concealed.

VERIFICATION:
Verified at {location} on this {date} that the contents of this Affidavit are true and correct to my knowledge, no part of it is false and nothing material has been concealed.

DEPONENT: ___________________
({deponent_name})

Sworn before me on {date}

NOTARY PUBLIC / OATH COMMISSIONER: ___________________
"""
    },
    "legal_notice": {
        "title": "Legal Notice",
        "template": """LEGAL NOTICE

Date: {date}
Ref No: {reference_number}

To,
{recipient_name}
{recipient_address}

Subject: Legal Notice under {legal_section}

Dear Sir/Madam,

Under instructions from and on behalf of my client {sender_name}, residing at {sender_address}, I hereby serve upon you the following Legal Notice:

1. That {background_facts}

2. That despite repeated requests, you have failed to {grievance}

3. That your actions/inactions constitute a violation of {violated_provision}

4. That my client has suffered damages amounting to {damage_amount} on account of the above.

THEREFORE, you are hereby called upon to {demand} within {response_period} days of receipt of this notice, failing which my client shall be constrained to initiate appropriate legal proceedings against you, civil and/or criminal, at your risk, cost and consequences.

Please treat this notice as final and binding.

Yours faithfully,

{advocate_name}
Advocate
{bar_council_number}
On behalf of {sender_name}
"""
    },
    "employment_agreement": {
        "title": "Employment Agreement",
        "template": """EMPLOYMENT AGREEMENT

This Employment Agreement ("Agreement") is made on {date} between:

EMPLOYER: {company_name}, a company registered under the laws of {jurisdiction}, having its registered office at {company_address} (hereinafter referred to as "Company")

AND

EMPLOYEE: {employee_name}, residing at {employee_address} (hereinafter referred to as "Employee")

1. POSITION AND DUTIES
The Company hereby employs the Employee as {designation} in the {department} department. The Employee shall perform duties as assigned and report to {reporting_manager}.

2. COMMENCEMENT AND PROBATION
Employment commences on {start_date} with a probation period of {probation_period} months.

3. COMPENSATION
(a) Basic Salary: {salary_amount} per month
(b) Benefits: As per company policy
(c) Payment: On or before the last working day of each month

4. WORKING HOURS
The Employee shall work {working_hours} hours per week, {work_days} per week.

5. CONFIDENTIALITY
The Employee agrees to maintain strict confidentiality of all proprietary information during and after employment.

6. NON-COMPETE
For a period of {non_compete_period} months after termination, the Employee shall not engage in competing business within {geographic_scope}.

7. TERMINATION
Either party may terminate this agreement with {notice_period} days written notice.

8. GOVERNING LAW
This Agreement shall be governed by the laws of {jurisdiction}.

EMPLOYER: ___________________          EMPLOYEE: ___________________
Name: {company_name}                   Name: {employee_name}
Date: {date}                            Date: {date}
"""
    },
}


def get_template_fields(template_type):
    import re
    tpl = TEMPLATES.get(template_type)
    if not tpl:
        return []
    fields = re.findall(r'\{(\w+)\}', tpl["template"])
    return list(dict.fromkeys(fields))


def generate_clause(template_type, fields_dict):
    tpl = TEMPLATES.get(template_type)
    if not tpl:
        return {"error": "Unknown template type"}
    text = tpl["template"]
    for key, value in fields_dict.items():
        text = text.replace("{" + key + "}", value)
    import re
    remaining = re.findall(r'\{(\w+)\}', text)
    for r in remaining:
        text = text.replace("{" + r + "}", f"[{r.replace('_', ' ').title()}]")
    return {"title": tpl["title"], "content": text, "template_type": template_type}
