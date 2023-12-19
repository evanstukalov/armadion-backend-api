import uuid

from django.db import models
from django.utils.text import slugify

FILTER_TYPE_CHOICES = [
    ('price_filter', 'Фильтр по цене'),
    ('category_filter', 'Фильтр по категории'),
    ('limitoffset_filter', 'Пагинация'),
]


class Feature(models.Model):
    """
    Model of features
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    value = models.CharField(max_length=200)
    name_slug = models.SlugField(max_length=255)
    value_slug = models.SlugField(max_length=255)
    door = models.ForeignKey("Door", on_delete=models.CASCADE, related_name='features')
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
    """
    Model of feature categories
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255)

    class Meta:
        verbose_name_plural = "Категории характеристик"

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


class Image(models.Model):
    """
    Model for images
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_added = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='mediafiles/doors/')
    mimetype = models.CharField(max_length=100)
    door = models.ForeignKey("Door", on_delete=models.CASCADE, related_name='images')

    class Meta:
        verbose_name_plural = "Фото"

    def __str__(self):
        """
        Returns a string representation of the object.
        :return: A string representation of the object.
        :rtype: str
        """
        return self.door.title


class Door(models.Model):
    """
    Model for doors
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    article = models.CharField(max_length=255, blank=True, null=True)
    click_counter = models.IntegerField(default=0)
    in_stock = models.BooleanField()
    slug = models.SlugField(max_length=255)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    delivery = models.TextField(blank=True, null=True)
    payment = models.TextField(blank=True, null=True)
    safeguards = models.TextField(blank=True, null=True)

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
    """
    Model for filter values
    """
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
    """
    Model for filters
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    type = models.CharField(max_length=255, choices=FILTER_TYPE_CHOICES, default=FILTER_TYPE_CHOICES[1][0])

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
