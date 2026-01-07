import os
import sys
import django
from json import dumps

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
sys.path.append('D:\\cser\\josin\\trialsource-backend')
django.setup()

from api.models import GenTrial, AnzctrTrial, ClinicalTrialsStudy

def main():
    anztrials = AnzctrTrial.objects.all()[:200]
    for item in anztrials:
        try:
            GenTrial.objects.create(**{
                "tid": item.registration_number,
                "last_update_date": item.date_last_updated,
                "source_table": "api_anzctrtrial",
                "brief_title": item.public_title,
                "scientific_title": item.scientific_title,
                "status": item.recruitment_status,
                "summary": item.summary,
                "description": item.description,
                "study_type": item.study_type,
                "conditions": item.condition_code,
                "purpose": item.purpose,
                "enrollment_procedure": item.enrolling_procedure,
                "intervention_code": item.intervention_code,
                "intervention_description": item.intervention_allocation,
                "primary_outcome_measure": item.primary_assessment_method,
                "primary_outcome_description": item.primary_outcome,
                "primary_outcome_timeframe": item.primary_timepoint,
                "secondary_outcome_measure": item.secondary_assessment_method,
                "secondary_outcome_description": item.secondary_outcome,
                "secondary_outcome_timeframe": item.secondary_timepoint,
                "eligibility_criteria": f"Inclusion criteria: {item.inclusion_criteria}\nExclusion criteria: {item.exclusion_criteria}",
                "healthy_volunteers": item.healthy_volunteers,
                "sex": item.sex,
                "minage": item.min_age,
                "maxage": item.max_age
            })
        except Exception as e:
            print(e)
            print(f"Error: {dumps(item)}")
            return
        
    clintrials = ClinicalTrialsStudy.objects.all()[:200]
    for item in clintrials:
        try:
            GenTrial.objects.create(**{
                "tid": item.nct_id,
                "last_update_date": item.last_update_post_date,
                "source_table": "api_clinicaltrialsstudy",
                "brief_title": item.brief_title,
                "scientific_title": item.official_title,
                "status": item.overall_status,
                "summary": item.brief_summary,
                "description": item.detailed_description,
                "study_type": item.study_type,
                "conditions": item.conditions,
                "purpose": item.primary_purpose,
                "enrollment_procedure": item.enrollment_type,
                "intervention_code": item.intervention_name,
                "intervention_description": item.intervention_description[0] if item.intervention_description else None,
                "primary_outcome_measure": item.primary_outcome_measure,
                "primary_outcome_description": item.primary_outcome_description,
                "primary_outcome_timeframe": item.primary_outcome_timeframe,
                "secondary_outcome_measure": item.secondary_outcome_measure,
                "secondary_outcome_description": item.secondary_outcome_description,
                "secondary_outcome_timeframe": item.secondary_outcome_timeframe,
                "eligibility_criteria": item.eligibility_criteria,
                "healthy_volunteers": item.eligibility_healthy_volunteers,
                "sex": item.eligibility_sex,
                "minage": item.eligibility_minage,
                "maxage": item.eligibility_maxage
            })
        except:
            print(f"Error: {item}")

if __name__ == '__main__':
    main()