from django.db import models


class Widget(models.Model):
    key = models.CharField(max_length=200, unique=True)
    value = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.id=} {self.key=} {self.value=}"
