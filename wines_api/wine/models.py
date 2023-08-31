from django.db import models

class Wine(models.Model):
    WHITE_WINE = 'WH'
    RED_WINE = 'RE'
    WINE_TYPES = [
        (WHITE_WINE, 'Белое вино'),
        (RED_WINE, 'Красное вино'),
    ]
    category = models.CharField(
        max_length=2,
        choices=WINE_TYPES,
    )
    title = models.CharField(max_length=40)
    sort_of_grape = models.CharField(max_length=40)
    price = models.PositiveSmallIntegerField()
    by_stock = models.BooleanField()

    def __str__(self):
        return self.title