import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from easy_charge.reseller.models import CreditRequest
from easy_charge.reseller.models import SellHistory
from easy_charge.reseller.models import Vendor
from easy_charge.users.models import CustomerProfile
from easy_charge.users.models import VendorProfile
from easy_charge.users.tests.factories import UserFactory


@pytest.fixture()
def api_client():
    return APIClient()


@pytest.mark.django_db()
def test_create_vendor(api_client):
    user = UserFactory(username="vendoruser")
    VendorProfile.objects.create(user=user)
    api_client.force_authenticate(user=user)

    url = reverse("api:vendor-list")
    data = {"name": "Test Vendor"}

    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert Vendor.objects.filter(name="Test Vendor").exists()


@pytest.mark.django_db()
def test_get_vendors_for_customer(api_client):
    v1 = UserFactory(username="vo1")
    v2 = UserFactory(username="vo2")

    vendor_owner1 = VendorProfile.objects.create(user=v1)
    vendor_owner2 = VendorProfile.objects.create(user=v2)

    user = UserFactory(username="customeruser")
    api_client.force_authenticate(user=user)

    Vendor.objects.create(owner=vendor_owner1, name="Vendor 1", is_verify=True)
    Vendor.objects.create(owner=vendor_owner2, name="Vendor 2", is_verify=False)

    url = reverse("api:vendor-list")
    response = api_client.get(url, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["name"] == "Vendor 1"


@pytest.mark.django_db()
def test_create_credit_request(api_client):
    user = UserFactory(username="vendoruser")
    vendor_profile = VendorProfile.objects.create(user=user)
    Vendor.objects.create(owner=vendor_profile, is_verify=True, name="test vendor")

    api_client.force_authenticate(user=user)

    url = reverse("api:credit_request-list")
    data = {"amount": 100}

    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert CreditRequest.objects.filter(
        amount=100,
        vendor=vendor_profile.vendor,
    ).exists()


@pytest.mark.django_db()
def test_get_credit_requests(api_client):
    user = UserFactory(username="vendoruser")
    vendor_profile = VendorProfile.objects.create(user=user)
    Vendor.objects.create(owner=vendor_profile, is_verify=True, name="test vendor")
    api_client.force_authenticate(user=user)

    CreditRequest.objects.create(amount=100, vendor=vendor_profile.vendor)
    CreditRequest.objects.create(amount=200, vendor=vendor_profile.vendor)

    url = reverse("api:credit_request-list")
    response = api_client.get(url, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2


@pytest.mark.django_db()
def test_charge_phone_number(api_client):
    user = UserFactory(username="customeruser")
    customer_profile = CustomerProfile.objects.create(user=user, balance=0)
    vendor = Vendor.objects.create(name="Test Vendor", balance=100, is_verify=True)
    api_client.force_authenticate(user=user)

    url = f"/api/reseller/charge-phone/{vendor.id}/"
    data = {"amount": 50, "phone_number": "09123456789"}

    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert vendor.balance == 50
    assert customer_profile.balance == 0
    assert SellHistory.objects.filter(
        vendor=vendor,
        amount=50,
        phone_number="09123456789",
    ).exists()


@pytest.mark.django_db()
def test_charge_customer_balance(api_client):
    user = UserFactory(username="customeruser")
    customer_profile = CustomerProfile.objects.create(user=user, balance=0)
    vendor = Vendor.objects.create(name="Test Vendor", balance=100, is_verify=True)
    api_client.force_authenticate(user=user)

    url = f"/api/reseller/charge-phone/{vendor.id}/"
    data = {"amount": 50}

    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert vendor.balance == 50
    assert customer_profile.balance == 50
    assert SellHistory.objects.filter(
        vendor=vendor,
        amount=50,
        customer=customer_profile,
    ).exists()
