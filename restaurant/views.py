from http import HTTPStatus
from multiprocessing import context
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.conf import settings
from .models import Meal,OrderTransaction
from .forms import UserLoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.views.generic import ListView, DetailView

def error_404_view(request, exception):
    return redirect("index")
# Create your views here.
class IndexView(View):
    def get(self, request):
        meals =[]
        temp_list=[]
        all_meals = Meal.objects.all()
        for cnt in range(all_meals.count()):
            temp_list.append(all_meals[cnt])
            if (cnt + 1) % 3 == 0 and cnt + 1 > 2:
                meals.append(temp_list)
                temp_list= []   
        if  temp_list:
               meals.append(temp_list)
                                
        context = {
            "meals": meals,
        }
        return render(request=request, template_name="restaurant/index.html", context=context)
class OrderView(View):
    def get(self, request, pk=None):
            if pk:
                got_meal=Meal.objects.filter(id=pk).last()
                if got_meal and got_meal.stock > 0:
                    OrderTransaction.objects.create(meal=got_meal, customer=request.user,amount=got_meal.price)
                    got_meal.stock -= 1
                    got_meal.save()
                    return redirect("index")
            return HttpResponse(HTTPStatus.BAD_REQUEST)
class DetailsView(ListView):
    context_object_name = "transactions"
    def get_queryset(self):
        return OrderTransaction.objects.filter(customer=self.request.user)
class CustomLoginView(View):
    form_class = UserLoginForm
    template_name = 'restaurant/login.html'
    def get(self, request):
        form = self.form_class()
        form.fields['password'].widget.attrs["placeholder"] = "Your Password"
        form.fields['password'].widget.attrs["id"] = "password_id"
        context={
            "login_form": form,}
        return render(request=request, template_name=self.template_name, context=context)
    def post(self, request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            authenticateuser = authenticate(request, username=username, password=password)
            if authenticateuser is not None:
                login(request, authenticateuser)
                return redirect("details")
            form.add_error('username', "Invalid username and password!")
            form.add_error('password', "Invalid username and password!")
            context={
                "login_form": form,
            }
            return render(request=request, template_name=self.template_name, context=context)

def logout_user(request):
    logout(request)
    return redirect("index")
