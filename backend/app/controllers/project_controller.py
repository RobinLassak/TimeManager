from dataclasses import asdict
from datetime import datetime, date

from ninja import Router, Schema
from ninja.errors import HttpError

from app.dto.project_dto import ProjectDTO
from app.services.project_service import ProjectService

router = Router(tags=['projects'])
service = ProjectService()

class ProjectIn(Schema):
    name: str
    start_date: date
    end_date: date
    customer_id: int
    description: str = ""
    status: str = "active"

class ProjectOut(Schema):
    id: int
    name: str
    start_date: date
    end_date: date
    customer_id: int
    description: str
    status: str
    created_at: datetime
    updated_at: datetime

def _to_dto(payload: ProjectIn, id: int | None = None) -> ProjectDTO:
    return ProjectDTO(**payload.dict(), id=id)

# Ziskani seznamu vsech projektu
@router.get("/", response=list[ProjectOut])
def get_all_projects(request):
    projects = service.get_all_projects()
    return [asdict(project) for project in projects]

# Ziskani jednoho projektu podle id
@router.get("/{id}", response=ProjectOut)
def get_project_by_id(request, id: int):
    project = service.get_project_by_id(id)
    if project is None:
        raise HttpError(404, "Project not found")
    return asdict(project)

# Vytvoreni noveho projektu
@router.post("/", response={201: ProjectOut})
def create_project(request, payload: ProjectIn):
    project = service.create_project(_to_dto(payload))
    return 201, asdict(project)

# Aktualizace existujiciho projektu
@router.put("/{id}", response=ProjectOut)
def update_project(request, id: int, payload: ProjectIn):
    project = service.update_project(_to_dto(payload, id))
    if project is None:
        raise HttpError(404, "Project not found")
    return asdict(project)

# Smazani projektu
@router.delete("/{id}", response={204: None})
def delete_project(request, id: int):
    deleted = service.delete_project(id)
    if not deleted:
        raise HttpError(404, "Project not found")
    return 204, None