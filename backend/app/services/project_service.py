from app.entities.project import Project
from app.dto.project_dto import ProjectDTO

class ProjectService:
    # Metoda pro získání všech projektů
    def get_all_projects(self) -> list[ProjectDTO]:
        projects = Project.objects.all()
        return [self._to_dto(project) for project in projects]

    # Metoda pro získání projektu podle jeho ID
    def get_project_by_id(self, id: int) -> ProjectDTO:
        try:
            project = Project.objects.get(id=id)
            return self._to_dto(project)
        except Project.DoesNotExist:
            return None
        
    # Metoda pro vytvoření nového projektu
    def create_project(self, projectDTO: ProjectDTO) -> ProjectDTO | None:
        project = self._to_entity(projectDTO)
        project.save()
        return self._to_dto(project)
    
    # Metoda pro aktualizaci existujícího projektu
    def update_project(self, projectDTO: ProjectDTO) -> ProjectDTO | None:
        if projectDTO.id is None:
            return None
        if not Project.objects.filter(id=projectDTO.id).exists():
            return None
        project = self._to_entity(projectDTO)
        project.save()
        return self._to_dto(project)
    
    # Metoda pro smazání projektu
    def delete_project(self, id: int) -> bool:
        if not Project.objects.filter(id=id).exists():
            return False
        Project.objects.filter(id=id).delete()
        return True
    
    # Pomocné metody pro převod entity na DTO a DTO na entity
    def _to_dto(self, project: Project) -> ProjectDTO:
        return ProjectDTO(
            name = project.name,
            customer_id = project.customer_id,
            start_date = project.start_date,
            end_date = project.end_date,
            description = project.description,
            status = project.status,
            id = project.id,
            created_at = project.created_at,
            updated_at = project.updated_at,
        )

    def _to_entity(self, projectDTO: ProjectDTO) -> Project:
        return Project(
            name = projectDTO.name,
            customer_id = projectDTO.customer_id,
            start_date = projectDTO.start_date,
            end_date = projectDTO.end_date,
            description = projectDTO.description,
            status = projectDTO.status,
            id = projectDTO.id,
        )