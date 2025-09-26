from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100,unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image= models.ImageField(upload_to='product_images',null=True,blank=True)

    def __str__(self):
        return self.name
    

class Cart(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    def __str__(self):
        return f"{self.id} - {self.user.username}"
    
class CartItem(models.Model):
    order = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.order.user.username}-{self.product.name}-{self.quantity}"
    
class OrderHistory(models.Model):
    STATUS_CHOICES = [
        ("requested", "Requested"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
        ("paid", "Paid"),
    ]

    order_id = models.CharField(max_length=20, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="requested")
    created_at = models.DateTimeField(auto_now_add=True)
    def save(self, *args, **kwargs):
        if not self.order_id:
            today = timezone.now().strftime("%Y%m%d") 
            last_order = OrderHistory.objects.filter(order_id__startswith=f"ORD{today}").order_by("id").last()
            if last_order:
                last_number = int(last_order.order_id[-4:])
                new_number = last_number + 1
            else:
                new_number = 1
            self.order_id = f"ORD{today}{new_number:04d}"
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.order_id}- {self.user.username}"