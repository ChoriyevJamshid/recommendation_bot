from django.db import models


class BaseModel(models.Model):
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        abstract = True


class Shop(BaseModel):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class ProductType(BaseModel):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Product(BaseModel):

    title = models.CharField(max_length=255)
    link = models.URLField(max_length=511)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    price_credit = models.DecimalField(max_digits=20, decimal_places=2,
                                       blank=True, null=True)

    def __str__(self):
        return self.title







