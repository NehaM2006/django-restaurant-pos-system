from django.contrib import admin
from .models import Meal,OrderTransaction
@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'available',"image")

    search_fields = ('name', 'description', 'price')
# Register your models here.
#admin.site.register(Meal, MealAdmin)
@admin.register(OrderTransaction)
class MealAdmin(admin.ModelAdmin):
    list_display = ('meal','customer','amount','status','created_at')

    search_fields = ('meal','customer','amount','status')
# Register your models here.
#admin.site.register(Meal, MealAdmin)