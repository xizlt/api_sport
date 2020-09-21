from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    url = models.URLField(default='https://www.sportmaster.ru')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ('-name',)


class Brand(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, default='no brand')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    # image = models.ImageField(blank=True)
    image = models.TextField(blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True, default=None)
    link = models.TextField(max_length=2000)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    description = models.ManyToManyField('Description')
    specification = models.ManyToManyField('Specification')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} ({self.id})'

    class Meta:
        ordering = ('-created',)


class Description(models.Model):
    name = models.CharField(max_length=200)
    benefit = models.CharField(max_length=200)

    def __str__(self):
        return self.name + ' - ' + self.benefit


class Specification(models.Model):
    name = models.CharField(max_length=200)
    benefit = models.CharField(max_length=200)

    def __str__(self):
        return self.name + ' - ' + self.benefit
