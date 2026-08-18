from app.entities.customer import Customer
from app.dto.customer_dto import CustomerDTO

class CustomerService:
    # Metoda pro získání všech zákazníků
    def get_all_customers(self) -> list[CustomerDTO]:
        customers = Customer.objects.all()
        return [self._to_dto(customer) for customer in customers]

    # Metoda pro získání zákazníka podle jeho ID
    def get_customer_by_id(self, id: int) -> CustomerDTO:
        try:
            customer = Customer.objects.get(id=id)
            return self._to_dto(customer)
        except Customer.DoesNotExist:
            return None

    # Metoda pro vytvoření nového zákazníka
    def create_customer(self, customerDTO: CustomerDTO) -> CustomerDTO | None:
        customer = self._to_entity(customerDTO)
        customer.save()
        return self._to_dto(customer)

    # Metoda pro aktualizaci existujícího zákazníka
    def update_customer(self, customerDTO: CustomerDTO) -> CustomerDTO | None:
        if customerDTO.id is None:
            return None
        if not Customer.objects.filter(id=customerDTO.id).exists():
            return None
        customer = self._to_entity(customerDTO)
        customer.save()
        return self._to_dto(customer)

    # Metoda pro smazání zákazníka
    def delete_customer(self, id: int) -> bool:
        if not Customer.objects.filter(id=id).exists():
            return False
        Customer.objects.filter(id=id).delete()
        return True

    # Pomocné metody pro převod entit na DTO a DTO na entity
    def _to_dto(self, customer: Customer) -> CustomerDTO:
        return CustomerDTO(
            first_name = customer.first_name,
            last_name = customer.last_name,
            ico = customer.ico,
            dic = customer.dic,
            street = customer.street,
            city = customer.city,
            zip = customer.zip,
            country = customer.country,
            email = customer.email,
            phone = customer.phone,
            website = customer.website,
            id = customer.id,
            created_at = customer.created_at,
            updated_at = customer.updated_at,
        )

    def _to_entity(self, customerDTO: CustomerDTO) -> Customer:
        return Customer(
            first_name = customerDTO.first_name,
            last_name = customerDTO.last_name,
            ico = customerDTO.ico,
            dic = customerDTO.dic,
            street = customerDTO.street,
            city = customerDTO.city,
            zip = customerDTO.zip,
            country = customerDTO.country,
            email = customerDTO.email,
            phone = customerDTO.phone,
            website = customerDTO.website,
            id = customerDTO.id,
        )