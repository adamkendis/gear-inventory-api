from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Item

from gear.serializers import ItemSerializer


ITEMS_URL = reverse('gear:item-list')


class PublicItemsApiTests(TestCase):
    """Test the publicly available items API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving items"""
        res = self.client.get(ITEMS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateItemsApiTests(TestCase):
    """Test the authorized user items API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@fake.com',
            'testpass'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_items(self):
        """Test retrieving items"""
        Item.objects.create(
            user=self.user,
            name='Tent',
            notes='4-season tent',
            weight=2505.51
        )
        Item.objects.create(
            user=self.user,
            name='Sleeping bag',
            notes='20* down sleeping bag',
            weight=1500.25
        )
        res = self.client.get(ITEMS_URL)

        items = Item.objects.all().order_by('-name')
        serializer = ItemSerializer(items, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_items_limited_to_user(self):
        """Test that items returned are for authenticated user"""
        user2 = get_user_model().objects.create_user(
            'other user',
            'testpassword'
        )
        Item.objects.create(
            user=user2,
            name='Titanium Pot',
            notes='900ml',
            weight=700
        )
        item = Item.objects.create(
            user=self.user,
            name='Bear bag',
            notes='stuff sack',
            weight=300.20
        )
        res = self.client.get(ITEMS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], item.name)

    def test_create_item_successful(self):
        """Test creating a new item"""
        payload = {'name': 'test backpack',
                   'notes': 'test notes',
                   'weight': 200.50}
        self.client.post(ITEMS_URL, payload)

        exists = Item.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()

        self.assertTrue(exists)

    def test_create_item_invalid(self):
        """Test creating a new item with invalid payload"""
        payload = {'name': '', 'notes': '', 'weight': 0}
        res = self.client.post(ITEMS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
