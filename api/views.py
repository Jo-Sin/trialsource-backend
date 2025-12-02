from django.db.models import QuerySet
from django.http import HttpRequest
from ninja import NinjaAPI
from ninja.pagination import paginate
 
from .models import AnzctrTrial
from .schemas import AnzctrTrialFull, AnzctrTrialBrief
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
def get_book(request: HttpRequest, reg_no: str) -> AnzctrTrial:
    return AnzctrTrial.objects.filter(registration_number=reg_no).first()
 
@api.get("/test-worker", response=str)
def test_worker(request: HttpRequest) -> str:
    heartbeat.delay()
    return 'Success'

# @api.post("/books", response=str)
# def create_book(request: HttpRequest, payload: None) -> str:
#     heartbeat.delay()
#     return 'Success'
