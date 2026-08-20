from dataclasses import asdict
from datetime import datetime, date

from ninja import Router, Schema
from ninja.errors import HttpError

from app.dto.work_dto import WorkDTO
from app.services.work_service import WorkService

router = Router(tags=['works'])
service = WorkService()
