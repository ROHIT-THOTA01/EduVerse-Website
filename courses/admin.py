from django.contrib import admin
from courses.models import Course,Lesson,Category
# Register your models here.

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'position', 'is_free_preview']
    list_filter = ['is_free_preview', 'course']
    search_fields = ['title', 'course__title']
    list_editable = ['is_free_preview', 'position']

admin.site.register(Course)
admin.site.register(Category)
