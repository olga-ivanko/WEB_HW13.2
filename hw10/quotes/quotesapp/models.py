from django.db import models


# Create your models here.
class Author(models.Model):

    fullname = models.CharField(null=False, blank=False, unique=True)
    born_date = models.DateField(null=False, blank=False)
    born_location = models.CharField(null=False, blank=False)
    description = models.TextField(null=False, blank=False)

    def __str__(self) -> str:
        return f"{self.fullname}"


class Tag(models.Model):
    name = models.CharField(unique=True)

    def __str__(self) -> str:
        return f"{self.name}"


class Quote(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    quote = models.TextField(null=False, blank=False, unique=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self) -> str:
        return f"{self.quote}"
