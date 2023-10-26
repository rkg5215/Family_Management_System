from django.test import TestCase, client
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from .views import *
from .models import *
import json

# Create your tests here.

# Urls Testing
class TestUrls(SimpleTestCase):

    def test_index_url_resolve(self):
        url= reverse('index')
        self.assertEquals(resolve(url).func, index)

    def test_login_url_resolve(self):
        url= reverse('login')
        self.assertEquals(resolve(url).func, login)

    def test_register_url_resolve(self):
        url= reverse('register')
        self.assertEquals(resolve(url).func, register)

    def test_logout_url_resolve(self):
        url= reverse('logout')
        self.assertEquals(resolve(url).func, logout)

    def test_family_url_resolve(self):
        url= reverse('family')
        self.assertEquals(resolve(url).func, family)


    def test_add_family_url_resolve(self):
        url= reverse('add_family')
        self.assertEquals(resolve(url).func, add_family)

    def test_update_family_url_resolve(self):
        url= reverse('update_family', args=[1])
        self.assertEquals(resolve(url).func, update_family)

    def test_delete_family_url_resolve(self):
        url= reverse('delete_family', args=[1])
        self.assertEquals(resolve(url).func, delete_family)

    def test_family_details_url_resolve(self):
        url = reverse('family_details', args=[1])
        self.assertEquals(resolve(url).func, family_details)

    def test_add_family_member_url_resolve(self):
        url = reverse('add_family_member' , args=[1])
        self.assertEquals(resolve(url).func, add_family_member)

    def test_update_family_member_url_resolve(self):
        url = reverse('update_family_member', args=[1,1])
        self.assertEquals(resolve(url).func, update_family_member)

    def test_delete_family_member_url_resolve(self):
        url = reverse('delete_family_member', args=[1,1])
        self.assertEquals(resolve(url).func, delete_family_member)

# Views Testing


# class TestViews(TestCase):
#
#     def setUp(self):
#         self.client = Family()
#         self.list_url = reverse('family')
#         self.list_url = reverse('family_details')
#
#     def test_family_GET(self):
#
#         response= self.client.get(self.list_url)
#         self.assertEquals(response.status_code, 200)
#         self.assertTemplateUsed(response, 'family.html')
#
#     def test_family_details_GET(self):
#
#         response= self.client.get(self.list_url)
#         self.assertEquals(response.status_code, 200)
#         self.assertTemplateUsed(response, 'family_details.html')