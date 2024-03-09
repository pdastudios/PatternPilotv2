from django.contrib import admin
from cms.models import Project, Shape, Round 

# Register your models here.
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'created', 'modified', 'proj_total_shapes', 'proj_total_rounds', 'proj_total_stitches')
    readonly_fields = ('created', 'modified')

admin.site.register(Project, ProjectAdmin)
admin.site.register(Shape)
admin.site.register(Round)
