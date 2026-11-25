from django.db import models

class Skill(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/')
    url = models.URLField(blank=True)
    repository = models.URLField(blank=True)
    year = models.PositiveIntegerField()
    skills = models.ManyToManyField("Skill")

    def __str__(self):
        return self.title