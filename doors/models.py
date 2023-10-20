from django.db import models


class Door(models.Model):
    title = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='door_photos/')
    in_stock = models.BooleanField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    popular = models.BooleanField()
    article = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Двери"

    def __str__(self):
        """
        Returns a string representation of the object.
        :return: A string representation of the object.
        :rtype: str
        """
        return self.title

