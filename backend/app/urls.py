from django.urls import path

from app.controllers.customer_controller import CustomerController

urlpatterns = [
    path('customers/', CustomerController.as_view(), name='customers'),
    path('customers/<int:id>/', CustomerController.as_view(), name='customer'),
]