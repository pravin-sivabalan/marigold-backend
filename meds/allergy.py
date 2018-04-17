
import db
import meds.db

import auth

from error import Error

import rx.norm
import meds.fda as fda

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

    cursor.execute("""
        SELECT * FROM user_meds LEFT JOIN meds
        ON user_meds.medication_id = meds.id
        WHERE user_meds.id = %s
    """, [med_id])

    med = cursor.fetchone()
    return check_med(med)

def check_with(cui):
    conn = db.conn()
    cursor = conn.cursor(db.DictCursor)

    med = rx.norm.props(cui)
    med_id = fda.get_rx(cui)

    cursor.execute("""
        SELECT * FROM meds
        where id = %s
    """, [med_id])

    fda_med = cursor.fetchone()
    med.update(fda_med)

    med["id"] = None
    med["rxcui"] = cui

    return check_med(med)

def check_med(med):
    conflicts = []
    allergies = get_allergies()

    cui = med["rxcui"]
    med_id = med["id"]

    # Check active ingreidents via NIH
    related_meds = rx.norm.related_by_types(cui, ["IN"])
    for related_med in related_meds:
        for allergy in allergies:
            if allergy.lower() in related_med.name.lower():
                conflicts.append(dict(
                    drug = med_id,
                    allergy = allergy,
                    desc = ingred_msg.format(related_med.name, allergy),
                    type = "active_ingredient"
                ))

    # Check FDA inactive ingredients
    inactive_ingreds_str = med["inactive_ingredient"]
    if inactive_ingreds_str is not None:
        inactive_ingreds = [ingred.strip() for ingred in inactive_ingreds_str.split(",")]

        for ingred in inactive_ingreds:
            for allergy in allergies:
                if allergy.lower() in ingred.lower():
                    conflicts.append(dict(
                        drug = med_id,
                        allergy = allergy,
                        desc = inactive_ingred_msg.format(ingred, allergy),
                        type = "inactive_ingredient"
                    ))

    # Check for allergies in warning label
    warning_label = med["warnings"]
    if warning_label is not None:
        warning_label = warning_label.lower()
        
        for allergy in allergies:
            if allergy.lower() in warning_label:
                conflicts.append(dict(
                    drug = med_id,
                    allergy = allergy, 
                    desc = warning_label_msg.format(med["name"], allergy),
                    type = "warning_label"
                ))
    
    return conflicts
