from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

DELIVERY_STATUS_CHOICES = (

    ("Pending", "Pending"),

    ("Preparing", "Preparing"),

    ("Out for Delivery", "Out for Delivery"),

    ("Delivered", "Delivered"),

)
PAYMENT_CHOICES = (
    ("COD", "Cash on Delivery"),
    ("UPI", "UPI"),
    ("CARD", "Card"),
)
CATEGORY_CHOICES = (
    ("Chinese", "Chinese"),
    ("Main Course", "Main Course"),
    ("South Indian", "South Indian"),
)
# Create your models here.
class Meal(models.Model):
    name = models.CharField( "Name of the Meal", max_length=100)
    description = models.TextField("Description of the Meal",blank=True, null=True)
    ingredients = models.TextField(blank=True, null=True)

    category = models.CharField(max_length=50, default="Main Course")
    category = models.CharField(
    max_length=20,
    choices=CATEGORY_CHOICES,
    default="Main Course"
)

    preparation_time = models.PositiveIntegerField(default=20)
    price = models.DecimalField("Price($)", max_digits=10, decimal_places=2)
    image = models.ImageField( upload_to="meal_images", default="meal_images/default_meal_image.jpg")
    available = models.BooleanField("Online Availability",default=False)
    stock = models.IntegerField("Stock",default=0)
    def __str__(self):
        return f'{self.description}'
class Cart(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)

    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.customer.username} - {self.meal.name}"
    @property
    def subtotal(self):
        return self.meal.price * self.quantity
RATING_CHOICES = (
    (1, "1 Star"),
    (2, "2 Stars"),
    (3, "3 Stars"),
    (4, "4 Stars"),
    (5, "5 Stars"),
)


class Review(models.Model):

    meal = models.ForeignKey(
        Meal,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    rating = models.IntegerField(
        choices=RATING_CHOICES
    )

    comment = models.TextField()

    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.customer.username} - {self.meal.name}"
class Coupon(models.Model):

    code = models.CharField(max_length=20, unique=True)

    discount = models.IntegerField(
        help_text="Discount Percentage"
    )

    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code
class OrderTransaction(models.Model):
    meal= models.ForeignKey(Meal,on_delete=models.CASCADE)
    customer=models.ForeignKey(User,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    amount = models.DecimalField("Amount paid(4)", max_digits=64, decimal_places=2, default=0)
    status = models.CharField("Delivery Status", max_length=20, choices=DELIVERY_STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField("Date Created", default=now)
    payment_method = models.CharField(
    max_length=10,
    choices=PAYMENT_CHOICES,
    default="COD"
)