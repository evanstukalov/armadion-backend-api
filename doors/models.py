import uuid

from django.db import models
from django.utils.text import slugify


class Feature(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    value = models.CharField(max_length=200)
    name_slug = models.SlugField(max_length=255)
    value_slug = models.SlugField(max_length=255)
    feature_category = models.ForeignKey("FeatureCategory", on_delete=models.CASCADE, related_name="features")

    class Meta:
        verbose_name_plural = "Характеристики"

    def __str__(self):
        """
        Returns a string representation of the object.
        :return: A string representation of the object.
        :rtype: str
        """
        return self.name

    def save(self, *args, **kwargs):
        if not self.name_slug:
            self.slug = slugify(self.name)
        if not self.value_slug:
            self.slug = slugify(self.value)
        super().save(*args, **kwargs)


class FeatureCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255)
    door = models.ForeignKey("Door", on_delete=models.CASCADE, related_name='feature_categories')

    class Meta:
        verbose_name_plural = "Характеристики: категории"

    def __str__(self):
        """
        Returns a string representation of the object.
        :return: A string representation of the object.
        :rtype: str
        """
        return f'{self.name} - {self.door.title}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Door(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    article = models.CharField(max_length=255, blank=True, null=True)
    click_counter = models.IntegerField(default=0)
    in_stock = models.BooleanField()
    slug = models.SlugField(max_length=255)

    image_one = models.ImageField(upload_to='door_photos/', blank=False, null=False)
    image_two = models.ImageField(upload_to='door_photos/', blank=True, null=True)
    image_three = models.ImageField(upload_to='door_photos/', blank=True, null=True)
    image_four = models.ImageField(upload_to='door_photos/', blank=True, null=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    delivery = models.TextField(blank=True, null=True)
    payment = models.TextField(blank=True, null=True)
    safeguards = models.TextField(blank=True, null=True)

    for_test_purposes = models.TextField(blank=True, null=True)

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


class FilterValue(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    filter = models.ForeignKey("Filter", on_delete=models.CASCADE, related_name='filter_values')

    class Meta:
        verbose_name_plural = "Фильтры: значения"

    def __str__(self):
        """
        Returns a string representation of the object.
        :return: A string representation of the object.
        :rtype: str
        """
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.value = slugify(self.name)
        super().save(*args, **kwargs)


class Filter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)

    class Meta:
        verbose_name_plural = "Фильтры"

    def __str__(self):
        """
        Returns a string representation of the object.
        :return: A string representation of the object.
        :rtype: str
        """
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
