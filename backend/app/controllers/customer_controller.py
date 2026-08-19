from dataclasses import asdict
from datetime import datetime

from ninja import Router, Schema
from ninja.errors import HttpError

from app.dto.customer_dto import CustomerDTO
from app.services.customer_service import CustomerService

router = Router(tags=['customers'])
service = CustomerService()

class CustomerIn(Schema):
    first_name: str
    last_name: str
    ico: str
    dic: str
    street: str
    city: str
    zip: str
    country: str
    email: str
    phone: str
    website: str

class CustomerOut(Schema):
    id: int
    first_name: str
    last_name: str
    ico: str
    dic: str
    street: str
    city: str
    zip: str
    country: str
    email: str
    phone: str
    website: str
    created_at: datetime
    updated_at: datetime

def _to_dto(payload: CustomerIn, id: int | None = None) -> CustomerDTO:
    return CustomerDTO(**payload.dict(), id=id)

# Ziskani seznamu vsech zakazniku
@router.get("/", response=list[CustomerOut])
def get_all_customers(request):
    customers = service.get_all_customers()
    return [asdict(customer) for customer in customers]

# Ziskani jednoho zakaznika podle id
@router.get("/{id}", response=CustomerOut)
def get_customer_by_id(request, id: int):
    customer = service.get_customer_by_id(id)
    if customer is None:
        raise HttpError(404, "Customer not found")
    return asdict(customer)

# Vytvoreni noveho zakaznika
@router.post("/", response={201: CustomerOut})
def create_customer(request, payload: CustomerIn):
    customer = service.create_customer(_to_dto(payload))
    return 201, asdict(customer)

# Aktualizace existujiciho zakaznika
@router.put("/{id}", response=CustomerOut)
def update_customer(request, id: int, payload: CustomerIn):
    customer = service.update_customer(_to_dto(payload, id))
    if customer is None:
        raise HttpError(404, "Customer not found")
    return asdict(customer)

# Smazani zakaznika
@router.delete("/{id}", response={204: None})
def delete_customer(request, id: int):
    deleted = service.delete_customer(id)
    if not deleted:
        raise HttpError(404, "Customer not found")
    return 204, None

        