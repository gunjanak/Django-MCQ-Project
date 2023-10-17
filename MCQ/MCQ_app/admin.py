from django.contrib import admin
from .models import Subject, MCQQuestion, UserScore

class MCQInline(admin.StackedInline):
    model = MCQQuestion
    extra = 1

class SubjectAdmin(admin.ModelAdmin):
    inlines = [MCQInline]
    list_display = ['name']
    search_fields = ['name']

class MCQAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'subject', 'correct_option']
    search_fields = ['question_text']

admin.site.register(Subject, SubjectAdmin)
admin.site.register(MCQQuestion, MCQAdmin)

admin.site.register(UserScore)
