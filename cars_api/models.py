from django.db import models


class Car(models.Model):
    make = models.TextField(null=False)
    model = models.TextField(null=False)

    class Meta:
        unique_together = ('make', 'model')

    def __str__(self):
        return f'Car {self.pk}: {self.make} {self.model}'


class Rating(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name = 'ratings')
    rating = models.IntegerField(null=False)

    def __str__(self):
        return f'Rating of {self.rating}/5 for {self.car}'
