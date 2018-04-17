
import db
import meds.db

import auth

from error import Error

import rx.interact as rxint

meds_with_cui_cmd = """
    SELECT id FROM user_meds
    WHERE user_id = %s AND rxcui = %s
"""

def find_med_with_cui(cui):
    conn = db.conn()
    cursor = conn.cursor(db.DictCursor)
    
    count = cursor.execute(meds_with_cui_cmd, [auth.uid(), cui])
    if count == 0:
        return None

    med = cursor.fetchall()[0]
    return med.get("id")

def check():
    user_meds = meds.db.for_user()
    cuis = [med.get("rxcui") for med in user_meds if med.get("rxcui") is not None]

    return check_list(cuis)

def check_with_id(med_id):
    conn = db.conn()
    cursor = conn.cursor(db.DictCursor)

    cursor.execute("""
        SELECT rxcui FROM user_meds
        WHERE id = %s
    """, [med_id])

    cui = cursor.fetchone()["rxcui"]
    return check_with(cui)

def check_with(cui):
    user_meds = meds.db.for_user()
    cuis = [med.get("rxcui") for med in user_meds if med.get("rxcui") is not None]
   
    cuis.append(cui)
    return check_list(cuis, against_cui=cui)

def check_list(cuis, against_cui=None):
    processed_interactions = []

    interactions = rxint.with_list(cuis) 
    for drugs, inters in interactions.items():
        if against_cui is not None:
            if drugs[0].cui != against_cui and drugs[1].cui != against_cui:
                continue

        drug1 = find_med_with_cui(drugs[0].cui)
        drug2 = find_med_with_cui(drugs[1].cui)

        info = [dict(
            desc=inter.desc,
            severity=inter.severity
        ) for inter in inters]

        processed_interactions.append(dict(drug1=drug1, drug2=drug2, info=info))

    return processed_interactions
