from django.db import models

class Door(models.Model):
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='door_photos/')
    in_stock = models.BooleanField()
    door_type = models.ForeignKey('DoorType', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    popular = models.BooleanField()
    series = models.ForeignKey('Series', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Двери"

    def __str__(self):
        """
        Returns a string representation of the object.
        :return: A string representation of the object.
        :rtype: str
        """
        return self.name


class Series(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    photo = models.ImageField(upload_to='series_photos/')
    price_from = models.DecimalField(max_digits=10, decimal_places=2)
    door_type = models.ForeignKey('DoorType', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Серии"

    def __str__(self):
        """
        Returns a string representation of the object.

        :return: A string representation of the object.
        :rtype: str
        """
        return self.name

class DoorType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        verbose_name_plural = "Типы дверей"

    def __str__(self):
        """
        Returns a string representation of the object.
        :return: A string representation of the object.
        :rtype: str
        """

        return self.name