
import db
import meds.db

import auth

from error import Error

import rx.norm

def get_allergies():
    user = auth.user()
    allergies_str = user["allergies"]

    if allergies_str is None:
        return []

    allergies = allergies_str.split(",")
    return [allergy.strip() for allergy in allergies]

ingred_msg = "The '{}' ingredient in this medication conflicts with your '{}' allergy"
inactive_ingred_msg = "The '{}' inactive ingredient in this medication conflicts with your '{}' allergy"

def check(med_id):
    conflicts = []

    conn = db.conn()
    cursor = conn.cursor(db.DictCursor)

    allergies = get_allergies()

    cursor.execute("""
        SELECT * FROM user_meds
        WHERE id = %s
    """, [med_id])

    med = cursor.fetchone()
    cui = med["rxcui"]

    related_meds = rx.norm.related_by_types(cui, ["IN"])
    for related_med in related_meds:
        for allergy in allergies:
            if allergy.lower() in related.name.lower():
                conflicts.append(ingred_msg.format(related_med.name, allergy))

    # Check FDA inactive ingredients

    
    return conflicts
