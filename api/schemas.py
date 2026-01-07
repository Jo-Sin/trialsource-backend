from ninja import ModelSchema

from .models import AnzctrTrial, ClinicalTrialsStudy, GenTrial


class AnzctrTrialBrief(ModelSchema):
    class Meta:
        model = AnzctrTrial
        fields = [
            'registration_number',
            'public_title',
            'recruitment_status',
            'description',
            'date_last_updated'
            ]
        
class AnzctrTrialFull(ModelSchema):
    class Meta:
        model = AnzctrTrial
        fields = '__all__'


class ClinTrialBrief(ModelSchema):
    class Meta:
        model = ClinicalTrialsStudy
        fields = [
            'nct_id',
            'official_title',
            'overall_status',
            'brief_summary',
            'last_update_post_date'
            ]

class ClinTrialFull(ModelSchema):
    class Meta:
        model = ClinicalTrialsStudy
        fields = '__all__'
        


class GenTrialBrief(ModelSchema):
    class Meta:
        model = GenTrial
        fields = [
            'tid',
            'brief_title',
            'status',
            'summary',
            'last_update_date'
            ]

class GenTrialFull(ModelSchema):
    class Meta:
        model = GenTrial
        fields = '__all__'