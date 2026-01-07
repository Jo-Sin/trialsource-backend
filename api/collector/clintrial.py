
import requests
from anzctr import get_page

BASE_URL = "https://clinicaltrials.gov/api/v2/"

def safe_key(obj: dict, keys: list):
    temp_obj = obj
    for key in keys:
        if key in temp_obj:
            temp_obj = temp_obj[key]
        else:
            return None
    return temp_obj

def map_key(obj, checkKey, field):
    return list(map(lambda x: safe_key(x, [field]), obj[checkKey])) if checkKey in obj else None

def get_studies(next_page = None):
    fetch_url = BASE_URL + ("studies?filter.overallStatus=NOT_YET_RECRUITING%7CRECRUITING"
        "&sort=LastUpdatePostDate&pageSize=50")
    if next_page:
        fetch_url += f"&pageToken={next_page}"
    print(fetch_url)

    data = get_page(fetch_url).json()

    for study in data["studies"]:
        try:
            id_mod = study["protocolSection"]["identificationModule"]
            status_mod = study["protocolSection"]["statusModule"]
            sponsor_mod = study["protocolSection"]["sponsorCollaboratorsModule"]
            descript_mod = study["protocolSection"]["descriptionModule"]
            condition_mod = study["protocolSection"]["conditionsModule"]
            design_mod = study["protocolSection"]["designModule"]
            arm_mod = study["protocolSection"]["armsInterventionsModule"]
            outcome_mod = study["protocolSection"]["outcomesModule"]
            eligi_mod = study["protocolSection"]["eligibilityModule"]
            contact_mod = study["protocolSection"]["contactsLocationsModule"]

            print(id_mod["nctId"])
            check_response = get_page("http://127.0.0.1:8000/api/clin-trials/" + id_mod["nctId"])

            if check_response.status_code == 200:
                local_data = check_response.json()
                if local_data["last_update_post_date"] == status_mod["lastUpdatePostDateStruct"]["date"]:
                    print("last update point reached")
                    continue
                else:
                    # TO WRITE: update existing record
                    pass

            json_data = {
                "nct_id": id_mod["nctId"],
                "last_update_post_date": safe_key(
                    status_mod,
                    ["lastUpdatePostDateStruct", "date"]
                    ),
                "official_title": safe_key(id_mod, ["officialTitle"]),
                "brief_title": safe_key(id_mod, ["briefTitle"]),
                "organization": safe_key(id_mod, ["organization", "fullName"]),
                "overall_status": safe_key(status_mod, ["overallStatus"]),
                "start_date": safe_key(status_mod, ["startDateStruct", "date"]),
                "completion_date": safe_key(status_mod, ["completionDateStruct", "date"]),
                "lead_sponsor": safe_key(sponsor_mod, ["leadSponsor", "name"]),
                "collaborators": map_key(sponsor_mod, "collaborators", "name"),
                "brief_summary": safe_key(descript_mod, ["briefSummary"]),
                "detailed_description": safe_key(descript_mod, ["detailedDescription"]),
                "study_type": safe_key(design_mod, ["studyType"]),
                "conditions": safe_key(condition_mod, ["conditions"]),
                "condition_keywords": safe_key(condition_mod, ["keywords"]),
                "phases": safe_key(design_mod, ["phases"]),
                "target_duration": safe_key(design_mod, ["targetDuration"]),
                "allocation": safe_key(design_mod, ["designInfo", "allocation"]),
                "intervention_model": safe_key(design_mod, ["designInfo", "interventionModel"]),
                "intervention_model_description": safe_key(
                    design_mod,
                    ["designInfo", "interventionModelDescription"]
                    ),
                "primary_purpose": safe_key(design_mod, ["designInfo", "primaryPurpose"]),
                "observational_model": safe_key(design_mod, ["designInfo", "observationalModel"]),
                "time_perspective": safe_key(design_mod, ["designInfo", "timePerspective"]),
                "masking": safe_key(design_mod, ["designInfo", "maskingInfo", "masking"]),
                "masking_description": safe_key(
                    design_mod,
                    ["designInfo", "maskingInfo", "maskingDescription"]
                    ),
                "who_masked": safe_key(design_mod, ["designInfo", "maskingInfo", "whoMasked"]),
                "biospec_description": safe_key(design_mod, ["bioSpec", "description"]),
                "biospec_retention": safe_key(design_mod, ["bioSpec", "retention"]),
                "enrollment_count": safe_key(design_mod, ["enrollmentInfo", "count"]),
                "enrollment_type": safe_key(design_mod, ["enrollmentInfo", "type"]),
                "intervention_type": map_key(arm_mod, "interventions", "type"),
                "intervention_name": map_key(arm_mod, "interventions", "name"),
                "intervention_description": map_key(arm_mod, "interventions", "description"),
                "primary_outcome_measure": map_key(outcome_mod, "primaryOutcomes", "measure"),
                "primary_outcome_description": map_key(outcome_mod, "primaryOutcomes", "description"),
                "primary_outcome_timeframe": map_key(outcome_mod, "primaryOutcomes", "timeFrame"),
                "secondary_outcome_measure": map_key(outcome_mod, "secondaryOutcomes", "measure"),
                "secondary_outcome_description": map_key(
                    outcome_mod,
                    "secondaryOutcomes",
                    "description"
                    ),
                "secondary_outcome_timeframe": map_key(outcome_mod, "secondaryOutcomes", "timeFrame"),
                "other_outcome_measure": map_key(outcome_mod, "otherOutcomes", "measure"),
                "other_outcome_description": map_key(outcome_mod, "otherOutcomes", "description"),
                "other_outcome_timeframe": map_key(outcome_mod, "otherOutcomes", "timeFrame"),
                "eligibility_criteria": safe_key(eligi_mod, ["eligibilityCriteria"]),
                "eligibility_healthy_volunteers": safe_key(eligi_mod, ["healthyVolunteers"]),
                "eligibility_gender_based": safe_key(eligi_mod, ["genderBased"]),
                "eligibility_gender_description": safe_key(eligi_mod, ["genderDescription"]),
                "eligibility_sex": safe_key(eligi_mod, ["sex"]),
                "eligibility_minage": safe_key(eligi_mod, ["minimumAge"]),
                "eligibility_maxage": safe_key(eligi_mod, ["maximumAge"]),
                "eligibility_stdages": safe_key(eligi_mod, ["stdAges"]),
                "eligibility_study_population": safe_key(eligi_mod, ["studyPopulation"]),
                "eligibility_sampling_method": safe_key(eligi_mod, ["samplingMethod"]),
                "central_contact_name": safe_key(contact_mod, ["name"]),
                "central_contact_email": safe_key(contact_mod, ["email"]),
            }

            resp = requests.post("http://127.0.0.1:8000/api/clin-trials", json=json_data)
            if resp.status_code != 200:
                print(resp.content)
        except:
            print("Something went wrong")
        
    if data["nextPageToken"]:
        get_studies(data["nextPageToken"])

def main():
    get_studies(None)

if __name__ == "__main__":
    main()