from django.db.models import QuerySet
from django.http import HttpRequest
from ninja import NinjaAPI
from ninja.pagination import paginate

from .models import AnzctrTrial, ClinicalTrialsStudy, GenTrial
from .schemas import AnzctrTrialBrief, AnzctrTrialFull, ClinTrialBrief, ClinTrialFull, GenTrialBrief, GenTrialFull, TrialFilterSchema
from .tasks import heartbeat

api = NinjaAPI(title="Dummy API for ANZCTR trial data")

@api.get("/hello")
def hello(request: HttpRequest, name: str ="world") -> str:
    print(name)
    return f"Hello {name}!"
 
@api.get("/anzctr-trials", response=list[AnzctrTrialBrief])
@paginate
def list_anzctr_trials(request: HttpRequest) -> QuerySet[AnzctrTrial]:
    return AnzctrTrial.objects.all()

@api.get("/anzctr-trials/{reg_no}", response=AnzctrTrialFull)
def get_anzctr_trial(request: HttpRequest, reg_no: str) -> AnzctrTrial:
    return AnzctrTrial.objects.filter(registration_number=reg_no).first()
 
@api.get("/test-worker", response=str)
def test_worker(request: HttpRequest) -> str:
    heartbeat.delay()
    return 'Success'

@api.get("/clin-trials", response=list[ClinTrialBrief])
@paginate
def list_clin_trials(request: HttpRequest) -> QuerySet[ClinicalTrialsStudy]:
    return ClinicalTrialsStudy.objects.all()

@api.get("/clin-trials/{nct_id}", response=ClinTrialFull)
def get_clin_trial(request: HttpRequest, nct_id: str) -> ClinicalTrialsStudy:
    return ClinicalTrialsStudy.objects.filter(nct_id=nct_id).first()

@api.post("/clin-trials", response=ClinTrialFull)
def create_clin_trial(request: HttpRequest, payload: ClinTrialFull) -> ClinicalTrialsStudy:
    return ClinicalTrialsStudy.objects.create(**payload.model_dump())

@api.get("/trials", response=list[GenTrialBrief])
@paginate
def list_gen_trials(request: HttpRequest) -> QuerySet[GenTrial]:
    return GenTrial.objects.all()

@api.get("/trials/{id}", response=GenTrialFull)
def get_gen_trial(request: HttpRequest, id: str) -> GenTrial:
    return GenTrial.objects.filter(tid=id).first()

@api.post("/find-trials", response=list[GenTrialBrief])
@paginate
def find_trials(request: HttpRequest, filters: TrialFilterSchema) -> QuerySet[GenTrial]:
    trials = GenTrial.objects.all()
    trials = filters.filter(trials)
    return trials

# @api.post("/books", response=str)
# def create_book(request: HttpRequest, payload: None) -> str:
#     heartbeat.delay()
#     return 'Success'
