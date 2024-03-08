from django.contrib import admin
from .models import *
from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib import admin
from .models import Quiz

class MyModelAdminForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = '__all__'
        widgets = {
            'content': CKEditorWidget(),
        }

class MyModelAdmin(admin.ModelAdmin):
    form = MyModelAdminForm

admin.site.register(Quiz, MyModelAdmin)

admin.site.register(Question)
admin.site.register(Option)
admin.site.register(QuizTaker)
admin.site.register(Answer)
admin.site.register(Result)
