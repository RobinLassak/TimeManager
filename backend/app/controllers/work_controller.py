from dataclasses import asdict
from datetime import datetime, date

from ninja import Router, Schema
from ninja.errors import HttpError

from app.dto.work_dto import WorkDTO
from app.services.work_service import WorkService

router = Router(tags=['works'])
service = WorkService()

class WorkIn(Schema):
    name: str
    project_id: int
    start_date: date
    end_date: date
    description: str = ""
    status: str = "active"

class WorkOut(Schema):
    id: int
    name: str
    project_id: int
    start_date: date
    end_date: date
    description: str
    status: str
    created_at: datetime
    updated_at: datetime

def _to_dto(payload: WorkIn, id: int | None = None) -> WorkDTO:
    return WorkDTO(**payload.dict(), id=id)

# Ziskani seznamu vsech praci
@router.get("/", response=list[WorkOut])
def get_all_works(request):
    works = service.get_all_works()
    return [asdict(work) for work in works]

# Ziskani jedne prace podle id
@router.get("/{id}", response=WorkOut)
def get_work_by_id(request, id: int):
    work = service.get_work_by_id(id)
    if work is None:
        raise HttpError(404, "Work not found")
    return asdict(work)

# Vytvoreni nove prace
@router.post("/", response={201: WorkOut})
def create_work(request, payload: WorkIn):
    work = service.create_work(_to_dto(payload))
    return 201, asdict(work)

# Aktualizace existujici prace
@router.put("/{id}", response=WorkOut)
def update_work(request, id: int, payload: WorkIn):
    work = service.update_work(_to_dto(payload, id))
    if work is None:
        raise HttpError(404, "Work not found")
    return asdict(work)

# Smazani prace
@router.delete("/{id}", response={204: None})
def delete_work(request, id: int):
    deleted = service.delete_work(id)
    if not deleted:
        raise HttpError(404, "Work not found")
    return 204, None