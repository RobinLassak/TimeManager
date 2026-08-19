import json
from dataclasses import asdict

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from app.dto.customer_dto import CustomerDTO
from app.services.customer_service import CustomerService

@method_decorator(csrf_exempt, name='dispatch')
class CustomerController(View):
    # Konstruktor
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.customer_service = CustomerService()

    # Bud ziska seznam vsech zakazniku nebo jednoho zakaznika podle id
    def get(self, request, id=None):
        if id is None:
            customers = self.customer_service.get_all_customers()
            return JsonResponse(
                [asdict(customer) for customer in customers],
                encoder=DjangoJSONEncoder,
                safe=False,
            )
        else:
            customer = self.customer_service.get_customer_by_id(id)
            if customer is None:
                return JsonResponse(
                    {"error": "Customer not found"},
                    status=404,
                )
            return JsonResponse(
                asdict(customer),
                encoder=DjangoJSONEncoder,
                safe=False,
            )
    
    # Vytvoreni noveho zakaznika
    def post(self, request):
        try:
            data = json.loads(request.body)
            dto = CustomerDTO(**data)
        except (json.JSONDecodeError, TypeError):
            return JsonResponse(
                {"error": "Invalid request body"},
                status=400,
            )
        customer = self.customer_service.create_customer(dto)
        return JsonResponse(
            asdict(customer),
            encoder=DjangoJSONEncoder,
            status=201,
        )
    
    # Aktualizace existujiciho zakaznika
    def put(self, request, id=None):
        if id is None:
            return JsonResponse(
                {"error": "Customer ID is required"},
                status=400,
            )
        try:
            data = json.loads(request.body)
            dto = CustomerDTO(**data)
        except (json.JSONDecodeError, TypeError):
            return JsonResponse(
                {"error": "Invalid request body"},
                status=400,
            )
        dto.id = id
        customer = self.customer_service.update_customer(dto)
        if customer is None:
            return JsonResponse(
                {"error": "Customer not found"},
                status=404,
            )
        return JsonResponse(
            asdict(customer),
            encoder=DjangoJSONEncoder,
            status=200,
        )

    # Smazani zakaznika
    def delete(self, request, id=None):
        if id is None:
            return JsonResponse(
                {"error": "Customer ID is required"},
                status=400,
            )
        deleted = self.customer_service.delete_customer(id)
        if not deleted:
            return JsonResponse(
                {"error": "Customer not found"},
                status=404,
            )
        return HttpResponse(status=204)
        