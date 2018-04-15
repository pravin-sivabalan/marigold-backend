
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
warning_label_msg = "The warning label for '{}' references your '{}' allergy"

def check(med_id):
    conflicts = []

    conn = db.conn()
    cursor = conn.cursor(db.DictCursor)

    allergies = get_allergies()

    cursor.execute("""
        SELECT * FROM user_meds LEFT JOIN meds
        ON user_meds.medication_id = meds.id
        WHERE user_meds.id = %s
    """, [med_id])

    med = cursor.fetchone()
    cui = med["rxcui"]

    # Check active ingreidents via NIH
    related_meds = rx.norm.related_by_types(cui, ["IN"])
    for related_med in related_meds:
        for allergy in allergies:
            if allergy.lower() in related_med.name.lower():
                conflicts.append(ingred_msg.format(related_med.name, allergy))

    # Check FDA inactive ingredients
    inactive_ingreds_str = med["inactive_ingredient"]
    if inactive_ingreds_str is not None:
        inactive_ingreds = [ingred.strip() for ingred in inactive_ingreds_str.split(",")]

        for ingred in inactive_ingreds:
            for allergy in allergies:
                if allergy.lower() in ingred.lower():
                    conflicts.append(inactive_ingred_msg.format(ingred, allergy))

    # Check for allergies in warning label
    warning_label = med["warnings"]
    if warning_label is not None:
        warning_label = warning_label.lower()
        
        for allergy in allergies:
            if allergy.lower() in warning_label:
                conflicts.append(warning_label_msg.format(med["name"], allergy))
    
    return conflicts
