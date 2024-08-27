import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from easy_charge.users.models import CustomerProfile
from easy_charge.users.models import User
from easy_charge.users.tests.factories import UserFactory


@pytest.fixture()
def api_client():
    return APIClient()


@pytest.mark.django_db()
def test_vendor_signup(api_client):
    url = reverse("api:sign_up-vendor-signup")
    data = {
        "username": "testvendor",
        "name": "Test Vendor",
        "password": "strongpassword123",
    }
    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.filter(username="testvendor").exists()


@pytest.mark.django_db()
def test_customer_signup(api_client):
    url = reverse("api:sign_up-customer-signup")
    data = {
        "username": "testcustomer",
        "name": "Test Customer",
        "password": "strongpassword123",
        "phone_number": "09123456789",
    }
    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.filter(username="testcustomer").exists()
    customer = User.objects.get(username="testcustomer").customerprofile
    assert customer.phone_number == "09123456789"


@pytest.mark.django_db()
def test_me_view_customer(api_client):
    user = UserFactory(username="customeruser")
    CustomerProfile.objects.create(user=user, phone_number="09123456789", balance=100)
    api_client.force_authenticate(user=user)

    response = api_client.get(reverse("api:me"))

    assert response.status_code == status.HTTP_200_OK
    assert response.data["username"] == "customeruser"
    assert response.data["extra"]["phone_number"] == "09123456789"
    assert response.data["extra"]["balance"] == 100
