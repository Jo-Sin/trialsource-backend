from ninja import ModelSchema

from .models import AnzctrTrial


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