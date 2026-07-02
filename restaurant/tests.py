from django.test import TestCase,Client
from django.urls import reverse
from .models import Meal
from django.contrib.auth.models import User
from django.contrib.auth import get_user
from .forms import UserLoginForm

# Create your tests here.
class MealModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Meal.objects.create(name="Test Meal", description="This is a test meal.", price=20.23, available=True, stock=3)
    def test_meal_name(self):
        meal = Meal.objects.get(id=1)
        self.assertEqual(meal.name, "Test Meal")
    def test_stock_count(self):
        meal = Meal.objects.get(id=1)
        self.assertEqual(meal.stock, 3)

class ViewsTestCase(TestCase):
    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
    def test_order_view(self):
        user = User.objects.create_user(username="neham")
        user.set_password("password")
        user.save()
        response = self.client.login(username="neham", password="password")
        self.assertTrue(response)
    def test_details_view_fails(self):
        user = User.objects.create_user(username="neham")
        user.set_password("password")
        user.save()
        response = self.client.login(username="neham", password="password2")
        self.assertFalse(response)
class FormsTest(TestCase):
    def test_login_form_user_name_is_required(self):
        form = UserLoginForm()
        self.assertTrue(form.fields['username'].required)
    def test_valid_login_form(self):
        User.objects.create_user(username="neham", password="password2")
        form = UserLoginForm(data={'username': 'neham', 'password': 'password2'})
        self.assertTrue(form.is_valid())
class ClientTest(TestCase):
    def test_login_view(self):
        user = User.objects.create_user(username="neham")
        user.set_password("password")
        user.save()
        c = Client()
        c.post('/login/', {'username': 'neham', 'password': 'password'})
       # self.assertTrue(get_user(c).is_authenticated)
        response = c.get(reverse('details'))
        self.assertEqual(response.status_code, 200)