from django.contrib import admin
from django.template.defaultfilters import truncatechars
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Question

# Register your models here.

class QuestionResource(resources.ModelResource):
    class Meta:
        model = Question

class QuestionAdmin(ImportExportModelAdmin):
    resource_class = QuestionResource

    list_display = ['id', 'question_body', 'isAccepted']
    search_fields = ['text',]

    def question_body(self, obj):
        return truncatechars(obj.text, 50)

admin.site.register(Question, QuestionAdmin)
