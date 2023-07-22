from django.db import models
from products.models import Product
from customers.models import Customer
from profiles.models import Profile
from django.utils import timezone
from .utils import generate_code
from django.shortcuts import reverse
# Create your models here.

# Type of Product(s) Sold, like TV etc. with its respective quantities
class Position(models.Model):

    # Product * Quantity
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField()
    price = models.FloatField(blank= True)      #Blanked, to perform custom price calculation
    created = models.DateTimeField(blank=True) # blanked, to enable editing in admin pannel

    def save(self, *args, **kwargs):
        self.price = self.quantity * self.product.price
        return super().save(*args, **kwargs)
    
    def get_sales_id(self):

        # Since there is NO Forward Relationship from Position -> Sale
        # There exist a Reverse Relation from Sale -> Position
        # We try to fetch that perticualr instance SALE ID
        # Reverse Relation without related name
        sale_obj = self.sale_set.first()
        return sale_obj.id

    def __str__(self):
        return f"ID: {self.id}, product: {self.product.name}, quantity: {self.quantity}"
    

class Sale(models.Model):
    transaction_id = models.CharField(max_length=12, blank=True)
    positions = models.ManyToManyField(Position)
    total_price = models.FloatField(blank = True, null = True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    salesman = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created  = models.DateTimeField(blank=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Sales for the amount of Rs.{self.total_price}"
    

    # To get a clickable URL for a particular ID
    # for Detail Page
    def get_absolute_url(self):
        # The URL/Class takes ID, hence Kwargs needs ID param
        return reverse("sales:detail", kwargs={"pk": self.pk})

    
    def save(self, *args, **kwargs):
        if self.transaction_id == "":
            self.transaction_id = generate_code()
        
        if self.created is None:
            self.created = timezone.now()
        
        # asking the Sale Class you call this overidden save method with new values
        return super().save(*args, **kwargs)

    def get_positions(self):
        return self.positions.all()



class CSV(models.Model):
    file_name = models.CharField(max_length=120, null=True)
    csv_file = models.FileField(upload_to='csvs', null=True)
    # activated = models.BooleanField(default=False) # File used or not already | Indicator
    created  = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return str(self.file_name)
