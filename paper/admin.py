from django.contrib import admin
from .models import Paper, Question


class PaperAdmin(admin.ModelAdmin):
    list_display = ['paper_id', 'paper_name', 'teacher', 'created_at', 'updated_at']


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_id', 'paper_id', 'question', 'answer']


admin.site.register(Paper, PaperAdmin)
admin.site.register(Question, QuestionAdmin)