from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Customer(models.Model):
    SEXE=(('Femme','Femme'),('Homme','Homme'))
    user=models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    Name=models.CharField(null=True,max_length=30)
    Email= models.EmailField(null=True, max_length=30)
    Age=models.CharField(null=True,max_length=2)
    Phone = models.CharField(null=True, max_length=8)
    Image = models.ImageField(null=True, blank=True, default="preson.png")
    Sexe = models.CharField(null=True, max_length=30,choices=SEXE)
    Country = models.CharField(null=True, max_length=30)
    
    def __str__(self):
        return self.Name
