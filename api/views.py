from django.db.models import QuerySet
from django.http import HttpRequest
from ninja import NinjaAPI
from ninja.pagination import paginate
 
from .models import Trial
from .schemas import TrialBrief
 
api = NinjaAPI(title="Dummy API for ANZCTR trial data")

@api.get("/hello")
def hello(request: HttpRequest, name: str ="world") -> str:
    print(name)
    return f"Hello {name}!"
 
@api.get("/trials", response=list[TrialBrief])
@paginate
def list_trials(request: HttpRequest) -> QuerySet[Trial]:
    return Trial.objects.all()
 
# @api.post("/books", response=BookOut)
# def create_book(request: HttpRequest, payload: BookIn) -> Book:
#     return Book.objects.create(**payload.model_dump())
 
# @api.get("/books/{book_id}", response=BookOut)
# def get_book(request: HttpRequest, book_id: int) -> Book:
#     return get_object_or_404(Book, pk=book_id)