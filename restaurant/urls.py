from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (
    IndexView,
    MealDetailView,
    OrderView,
    AddToCartView,
    DetailsView,
    CartView,
    RemoveCartItemView,
    CustomLoginView,
    IncreaseQuantityView,
    DecreaseQuantityView,
    CheckoutView,
    DashboardView,
    logout_user,
)
urlpatterns = [
    path('',IndexView.as_view(),name="index"),
    path("meal/<int:pk>/", MealDetailView.as_view(), name="meal_detail"),
    path(
    "cart/add/<int:pk>/",
    login_required(AddToCartView.as_view()),
    name="add_to_cart",
),
    path("order/<int:pk>/",login_required(OrderView.as_view()),name="order"),
      path("details/",login_required(DetailsView.as_view()),name="details"),
      path(
    "cart/",
    login_required(CartView.as_view()),
    name="cart",
),
      path(
    "cart/remove/<int:pk>/",
    login_required(RemoveCartItemView.as_view()),
    name="remove_cart",
),
      path(
    "cart/increase/<int:pk>/",
    login_required(IncreaseQuantityView.as_view()),
    name="increase_quantity",
),
      path(
    "cart/decrease/<int:pk>/",
    login_required(DecreaseQuantityView.as_view()),
    name="decrease_quantity",
),
      path(
    "checkout/",
    login_required(CheckoutView.as_view()),
    name="checkout",
),
        path(
        "meal/<int:pk>/",
        MealDetailView.as_view(),
        name="meal_detail",
),
        path(
    "dashboard/",
    login_required(DashboardView.as_view()),
    name="dashboard",
),
      path("login/",CustomLoginView.as_view(),name="login"),
      path("logout/",logout_user,name="logout"),
    
]
