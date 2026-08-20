from ninja import NinjaAPI

from app.controllers.customer_controller import router as customer_router
from app.controllers.project_controller import router as project_router

api = NinjaAPI(title='TimeManager', version='1.0.0')

api.add_router('/customers', customer_router)
api.add_router('/projects', project_router)
