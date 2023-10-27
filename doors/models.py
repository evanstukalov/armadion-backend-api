from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class Characteristic(models.Model):
    name = models.CharField(max_length=200)
    value = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Характеристики"

    def __str__(self):
        """
        Returns a string representation of the object.
        :return: A string representation of the object.
        :rtype: str
        """
        return self.name


class CategoryCharacteristic(models.Model):
    name = models.CharField(max_length=200)
    characteristics = models.ManyToManyField(Characteristic, blank=True)


    class Meta:
        verbose_name_plural = "Категории характеристик"

    def __str__(self):
        """
        Returns a string representation of the object.
        :return: A string representation of the object.
        :rtype: str
        """
        return self.name


class Door(models.Model):
    title = models.CharField(max_length=255)
    article = models.CharField(max_length=255, blank=True, null=True)
    click_counter = models.IntegerField(default=0)
    in_stock = models.BooleanField()
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    image_one = models.ImageField(upload_to='door_photos/', blank=False, null=False)
    image_two = models.ImageField(upload_to='door_photos/', blank=True, null=True)
    image_three = models.ImageField(upload_to='door_photos/', blank=True, null=True)
    image_four = models.ImageField(upload_to='door_photos/', blank=True, null=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    delivery = models.TextField(blank=True, null=True)
    payment = models.TextField(blank=True, null=True)
    safeguards = models.TextField(blank=True, null=True)

    category_characteristics = models.ManyToManyField(CategoryCharacteristic, blank=True)


    class Meta:
        verbose_name_plural = "Двери"

    def __str__(self):
        """
        Returns a string representation of the object.
        :return: A string representation of the object.
        :rtype: str
        """
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
