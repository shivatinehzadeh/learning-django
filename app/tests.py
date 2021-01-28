from django.test import TestCase,RequestFactory
from .models import Category
# Create your tests here.
from rest_framework import status
import pytest
from . import views
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.test.client import Client


class Unit_test(TestCase):

    def test_home_page(self):
        get_home=self.client.get('/')
        self.assertTemplateUsed(get_home,'base.html')

    def setUp(self):
         Category.objects.create(name = 'کتاب',description = 'Category object (1)')


    def test_list(self):
           factory=RequestFactory()
           url=factory.get('list/کتاب')
           name='کتاب'
           query = Category.objects.filter(name=name)
           self.assertTrue(query.exists())

    def test_form(self):
        data={'username':'shiva4345','email':'sh@as.vd','password1':123,'password2':123,'phone':'0912092'}
        User.objects.create(username='shiva4345',email='sh@as.vd',password=123)
        form = RegisterForm(data)
        response=self.client.get('/register',data,True)
        password=data['password1']
        username=data['username']
        user=authenticate(username=username,password=password)
        myUser=User.objects.filter(username='shiva4345',password=password)
        self.assertTrue(form.is_valid)
        self.assertEqual(myUser.count(),1)
        self.assertEqual(response.status_code,200)


    def test_ajax(self):
         data={'name':'shiva4345','email':'sh@as.vd','description':'qwqwqwqwq'}
         response=self.client.post("/suggest", data, **{'HTTP_X_REQUESTED_WITH':
         'XMLHttpRequest'})
         self.assertEqual(response.status_code, 301) # this is OK.
         





class Unit_test_API(APITestCase):
 def test_api(self):
    data= {"url": "http://127.0.0.1:8000/api/books/8/",
    "name": 'مدادرنگی 24 رنگ',
    "description": "<p style=\"text-align:center\">مدادرنگی 24 رنگ</p>"}
    response =self.client.get('/api',data,True)

    self.assertEqual(response.status_code,200)
    # self.assertTrue(status.is_success(response.status_code))
