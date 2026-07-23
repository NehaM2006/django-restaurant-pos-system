from http import HTTPStatus
from multiprocessing import context
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.conf import settings
from .models import Meal,OrderTransaction,Cart,Coupon
from .forms import UserLoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.views.generic import ListView, DetailView
from decimal import Decimal
from django.db.models import Avg
from .models import  Review
from .forms import ReviewForm
from django.db.models import Sum, Count, Avg
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages

def error_404_view(request, exception):
    return redirect("index")
# Create your views here.
class IndexView(View):

    def get(self, request):

        meals = []
        temp_list = []

        # Get search values from URL
        search_query = request.GET.get("search")
        category = request.GET.get("category")

        # Get all meals
        all_meals = Meal.objects.all()

        # Search by meal name
        if search_query:
            all_meals = all_meals.filter(
        Q(name__icontains=search_query) |
        Q(description__icontains=search_query)
    )

        # Filter by category
        if category:
            all_meals = all_meals.filter(category=category)

        # Arrange meals into rows of 3
        for meal in all_meals:

            temp_list.append(meal)

            if len(temp_list) == 3:
                meals.append(temp_list)
                temp_list = []

        if temp_list:
            meals.append(temp_list)

        # Get all categories for dropdown
        categories = Meal.objects.values_list(
            "category",
            flat=True
        ).distinct()

        context = {
            "meals": meals,
            "categories": categories,
            "search_query": search_query,
            "selected_category": category,
        }

        return render(
            request,
            "restaurant/index.html",
            context
        )
class MealDetailView(DetailView):

    model = Meal
    template_name = "restaurant/meal_detail.html"
    context_object_name = "meal"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        meal = self.object

        context["reviews"] = Review.objects.filter(
            meal=meal
        ).order_by("-created_at")

        context["average_rating"] = Review.objects.filter(
            meal=meal
        ).aggregate(
            Avg("rating")
        )["rating__avg"]

        context["form"] = ReviewForm()

        return context

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()

        form = ReviewForm(request.POST)

        if form.is_valid():

            existing_review = Review.objects.filter(
                meal=self.object,
                customer=request.user
            ).first()

            if not existing_review:

                review = form.save(commit=False)

                review.meal = self.object

                review.customer = request.user

                review.save()

        return redirect("meal_detail", pk=self.object.pk)
class AddToCartView(View):

    def get(self, request, pk):

        meal = Meal.objects.filter(id=pk).first()

        if not meal:
            return HttpResponse("Meal not found", status=404)

        cart_item = Cart.objects.filter(
            customer=request.user,
            meal=meal
        ).first()

        if cart_item:

            cart_item.quantity += 1
            cart_item.save()

        else:

            Cart.objects.create(
                customer=request.user,
                meal=meal,
                quantity=1
            )

        messages.success(
            request,
            f"{meal.name} added to cart successfully!"
        )

        return redirect("index")
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
class CartView(View):

    def get(self, request):

        cart_items = Cart.objects.filter(customer=request.user)

        total = 0

        for item in cart_items:
            total += item.meal.price * item.quantity

        context = {
            "cart_items": cart_items,
            "total": total,
        }

        return render(
            request,
            "restaurant/cart.html",
            context,
        )
class RemoveCartItemView(View):

    def get(self, request, pk):

        cart_item = Cart.objects.filter(
            id=pk,
            customer=request.user
        ).first()

        if cart_item:
            cart_item.delete()

        return redirect("cart")
class IncreaseQuantityView(View):

    def get(self, request, pk):

        item = Cart.objects.filter(
            id=pk,
            customer=request.user
        ).first()

        if item:
            item.quantity += 1
            item.save()

        return redirect("cart")
class DecreaseQuantityView(View):

    def get(self, request, pk):

        item = Cart.objects.filter(
            id=pk,
            customer=request.user
        ).first()

        if item:

            if item.quantity > 1:
                item.quantity -= 1
                item.save()
            else:
                item.delete()

        return redirect("cart")
class CheckoutView(View):

    def get(self, request):

        cart_items = Cart.objects.filter(customer=request.user)

        subtotal = Decimal("0")

        for item in cart_items:
            subtotal += item.meal.price * item.quantity

        discount = Decimal("0")
        coupon_message = ""
        coupon_code = request.GET.get("coupon")

        if coupon_code:

            coupon = Coupon.objects.filter(
                code=coupon_code,
                active=True
            ).first()

            if coupon:
                discount = subtotal * Decimal(coupon.discount) / Decimal("100")
                coupon_message = f"{coupon.discount}% discount applied!"
            else:
                coupon_message = "Invalid Coupon Code"

        subtotal_after_discount = subtotal - discount
        gst = subtotal_after_discount * Decimal("0.05")
        total = subtotal_after_discount + gst

        context = {
            "cart_items": cart_items,
            "subtotal": subtotal,
            "discount": discount,
            "gst": gst,
            "total": total,
            "coupon_code": coupon_code,
            "coupon_message": coupon_message,
        }

        return render(
            request,
            "restaurant/checkout.html",
            context
        )
    def post(self, request):

        payment = request.POST.get("payment_method")

        cart_items = Cart.objects.filter(
            customer=request.user
        )

        for item in cart_items:

            OrderTransaction.objects.create(
                meal=item.meal,
                customer=request.user,
                quantity=item.quantity,
                amount=item.meal.price * item.quantity,
                payment_method=payment,
                status="Pending",
            )

            item.meal.stock -= item.quantity
            item.meal.save()

        cart_items.delete()

        return redirect("details")
class DashboardView(View):

    def get(self, request):

        total_meals = Meal.objects.count()
        total_orders = OrderTransaction.objects.count()
        total_customers = User.objects.count()

        revenue = OrderTransaction.objects.aggregate(
            Sum("amount")
        )["amount__sum"] or 0

        average_rating = Review.objects.aggregate(
            Avg("rating")
        )["rating__avg"] or 0

        low_stock = Meal.objects.filter(stock__lt=5)

        most_ordered = (
            OrderTransaction.objects.values("meal__name")
            .annotate(total=Count("meal"))
            .order_by("-total")
            .first()
        )

        # ---------- Existing Bar Chart ----------
        chart_data = (
            OrderTransaction.objects
            .values("meal__name")
            .annotate(total=Count("meal"))
        )

        meal_names = []
        order_counts = []

        for item in chart_data:
            meal_names.append(item["meal__name"])
            order_counts.append(item["total"])

        # ---------- NEW Pie Chart ----------
        revenue_data = (
            OrderTransaction.objects
            .values("meal__name")
            .annotate(total_revenue=Sum("amount"))
        )

        revenue_labels = []
        revenue_values = []

        for item in revenue_data:
            revenue_labels.append(item["meal__name"])
            revenue_values.append(float(item["total_revenue"]))

        context = {
            "total_meals": total_meals,
            "total_orders": total_orders,
            "total_customers": total_customers,
            "revenue": revenue,
            "average_rating": average_rating,
            "low_stock": low_stock,
            "most_ordered": most_ordered,

            # Bar Chart
            "meal_names": meal_names,
            "order_counts": order_counts,

            # Pie Chart
            "revenue_labels": revenue_labels,
            "revenue_values": revenue_values,
        }

        return render(
            request,
            "restaurant/dashboard.html",
            context
        )
class CustomLoginView(View):
    form_class = UserLoginForm
    template_name = 'restaurant/login.html'

    def get(self, request):
        form = self.form_class()
        form.fields['username'].widget.attrs.update({
                "class":"form-control",
                "placeholder":"Enter Username"
            })

        form.fields['password'].widget.attrs.update({
                "class":"form-control",
                "placeholder":"Enter Password"
            })

        context = {
            "login_form": form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            authenticateuser = authenticate(
                request,
                username=username,
                password=password
            )

            if authenticateuser is not None:
                login(request, authenticateuser)
                return redirect("details")

            form.add_error('username', "Invalid username and password!")
            form.add_error('password', "Invalid username and password!")

        context = {
            "login_form": form,
        }

        return render(
            request,
            self.template_name,
            context
        )
def logout_user(request):
    logout(request)
    return redirect("index")