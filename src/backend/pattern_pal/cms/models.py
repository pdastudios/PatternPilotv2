from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    name = models.CharField(unique=True, max_length=255)
    author = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    proj_total_shapes = models.IntegerField(default=0)
    proj_total_rounds = models.IntegerField(default=0)
    proj_total_stitches = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update proj_total_shapes of the associated project
        if self.project:
            self.project.author = self.request.id
            self.project.save()

    def __str__(self):
        return self.name
    
class Shape(models.Model):
    name = models.CharField(max_length=255)
    project = models.ForeignKey(Project, blank=True, null=True, on_delete=models.CASCADE)
    total_rounds = models.IntegerField(default=0)
    total_stitches = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update proj_total_shapes of the associated project
        if self.project:
            self.project.proj_total_shapes = self.project.shape_set.count()
            self.project.save()

class Round(models.Model):
    number = models.IntegerField()
    formula = models.CharField(max_length=255)
    result = models.IntegerField()
    shape = models.ForeignKey(Shape, blank=True, null=True, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['number']

    def __str__(self):
        if self.shape:
            return self.shape.name + ": Round " + str(self.number)
        else:
            return "No Shape Assigned"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update proj_total_rounds and proj_total_stitches of the associated project
        shape = self.shape
        if shape:
            project = shape.project
            if project:
                project.proj_total_rounds = Round.objects.filter(shape__project=project).count()
                project.proj_total_stitches = Round.objects.filter(shape__project=project).aggregate(total_stitches=models.Sum('result'))['total_stitches']
                project.save()

    def delete(self, *args, **kwargs):
        shape = self.shape
        super().delete(*args, **kwargs)
        # Update proj_total_rounds and proj_total_stitches of the associated project after deletion
        if shape:
            project = shape.project
            if project:
                project.proj_total_rounds = Round.objects.filter(shape__project=project).count()
                project.proj_total_stitches = Round.objects.filter(shape__project=project).aggregate(total_stitches=models.Sum('result'))['total_stitches']
                project.save()
