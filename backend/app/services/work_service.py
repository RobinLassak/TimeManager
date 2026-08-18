from app.entities.work import Work
from app.dto.work_dto import WorkDTO

class WorkService:
    # Metoda pro získání všech pracovních úkolů
    def get_all_works(self) -> list[WorkDTO]:
        works = Work.objects.all()
        return [self._to_dto(work) for work in works]
    
    # Metoda pro získání pracovního úkolu podle jeho ID
    def get_work_by_id(self, id: int) -> WorkDTO:
        try:
            work = Work.objects.get(id=id)
            return self._to_dto(work)
        except Work.DoesNotExist:
            return None
        
    # Metoda pro vytvoření nového pracovního úkolu
    def create_work(self, workDTO: WorkDTO) -> WorkDTO | None:
        work = self._to_entity(workDTO)
        work.save()
        return self._to_dto(work)

    # Metoda pro aktualizaci existujícího pracovního úkolu
    def update_work(self, workDTO: WorkDTO) -> WorkDTO | None:
        if workDTO.id is None:
            return None
        if not Work.objects.filter(id=workDTO.id).exists():
            return None
        work = self._to_entity(workDTO)
        work.save()
        return self._to_dto(work)

    # Metoda pro smazání pracovního úkolu
    def delete_work(self, id: int) -> bool:
        if not Work.objects.filter(id=id).exists():
            return False
        Work.objects.filter(id=id).delete()
        return True
    
    # Pomocné metody pro převod entity na DTO a DTO na entity
    def _to_dto(self, work: Work) -> WorkDTO:
        return WorkDTO(
            name = work.name,
            project_id = work.project_id,
            start_date = work.start_date,
            end_date = work.end_date,
            description = work.description,
            status = work.status,
            id = work.id,
            created_at = work.created_at,
            updated_at = work.updated_at,
        )

    def _to_entity(self, workDTO: WorkDTO) -> Work:
        return Work(
            name = workDTO.name,
            project_id = workDTO.project_id,
            start_date = workDTO.start_date,
            end_date = workDTO.end_date,
            description = workDTO.description,
            status = workDTO.status,
            id = workDTO.id,
        )