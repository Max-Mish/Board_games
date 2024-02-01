from django.contrib import admin

from django.utils.safestring import mark_safe

from .models import Choice, Question


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['question', 'choice_text', 'votes']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["question_text", "pub_date", "picture_image"]
    date_hierarchy = "pub_date"

    def picture_image(self, obj):
        return mark_safe(f'<img src="{obj.picture or ""}" width="150" height="150" /> ')
