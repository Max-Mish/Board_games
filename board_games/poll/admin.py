from django.contrib import admin

from django.utils.safestring import mark_safe

from .models import Choice, Question

admin.site.register(Choice)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["question_text", "pub_date", "picture_image"]
    date_hierarchy = "pub_date"

    def picture_image(self, obj):
        return mark_safe(f'<img src="{obj.picture or ""}" width="150" height="150" /> ')
