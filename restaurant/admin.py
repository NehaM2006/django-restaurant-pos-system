from django.contrib import admin
from .models import Meal,OrderTransaction,Cart,Review
from .models import Coupon
@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = (
    'name',
    'category',
    'price',
    'stock',
    'available',
)

    search_fields = ('name', 'description', 'price')
# Register your models here.
#admin.site.register(Meal, MealAdmin)
@admin.register(OrderTransaction)
class OrderTransactionAdmin(admin.ModelAdmin):

    list_display = (
        "meal",
        "customer",
        "quantity",
        "amount",
        "payment_method",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "payment_method",
    )

    search_fields = (
        "meal__name",
        "customer__username",
    )
# Register your models here.
#admin.site.register(Meal, MealAdmin)
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('customer', 'meal', 'quantity', 'created_at')

    search_fields = ('customer__username', 'meal__name')
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = (
        "meal",
        "customer",
        "rating",
        "created_at",
    )

    search_fields = (
        "meal__name",
        "customer__username",
    )
@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):

    list_display = (
        "code",
        "discount",
        "active",
    )

    search_fields = (
        "code",
    )