from ninja import ModelSchema

from .models import Trial


class TrialBrief(ModelSchema):
    class Meta:
        model = Trial
        fields = [
            'registration_number',
            'public_title',
            'recruitment_status',
            'description',
            'date_last_updated'
            ]