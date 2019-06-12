from import_export.admin import ImportExportMixin
from import_export.resources import ModelResource
from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import ugettext_lazy as _

from .models import Quiz, Category, SubCategory, Progress, Question
from multichoice.models import MCQuestion, Answer
from true_false.models import TF_Question
from essay.models import Essay_Question


class AnswerInline(admin.TabularInline):
    model = Answer


class QuizAdminForm(forms.ModelForm):
    """
    below is from
    http://stackoverflow.com/questions/11657682/
    django-admin-interface-using-horizontal-filter-with-
    inline-manytomany-field
    """

    class Meta:
        model = Quiz
        exclude = []

    questions = forms.ModelMultipleChoiceField(
        queryset=Question.objects.all().select_subclasses(),
        required=False,
        label=_("Questions"),
        widget=FilteredSelectMultiple(
            verbose_name=_("Questions"),
            is_stacked=False))

    def __init__(self, *args, **kwargs):
        super(QuizAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['questions'].initial =\
                self.instance.question_set.all().select_subclasses()

    def save(self, commit=True):
        quiz = super(QuizAdminForm, self).save(commit=False)
        quiz.save()
        quiz.question_set.set(self.cleaned_data['questions'])
        self.save_m2m()
        return quiz


class QuizResource(ModelResource):

    class Meta:
        model = Quiz


class QuizAdmin(ImportExportMixin, admin.ModelAdmin):
    form = QuizAdminForm

    list_display = ('title', 'category', )
    list_filter = ('category',)
    search_fields = ('description', 'category', )
    resource_class = QuizResource


class CategoryResource(ModelResource):

    class Meta:
        model = MCQuestion


class CategoryAdmin(ImportExportMixin, admin.ModelAdmin):
    search_fields = ('category', )
    resource_class = CategoryResource


class SubCategoryResource(ModelResource):

    class Meta:
        model = SubCategory


class SubCategoryAdmin(ImportExportMixin, admin.ModelAdmin):
    search_fields = ('sub_category', )
    list_display = ('sub_category', 'category',)
    list_filter = ('category',)
    resource_class = SubCategoryResource


class MCResource(ModelResource):

    class Meta:
        model = MCQuestion


class MCQuestionAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('content', 'category', )
    list_filter = ('category',)
    fields = ('content', 'category', 'sub_category',
              'figure', 'quiz', 'explanation', 'answer_order')

    search_fields = ('content', 'explanation')
    filter_horizontal = ('quiz',)

    inlines = [AnswerInline]
    resource_class = MCResource


class ProgressResource(ModelResource):

    class Meta:
        model = Progress


class ProgressAdmin(ImportExportMixin, admin.ModelAdmin):
    """
    to do:
            create a user section
    """
    resource_class = ProgressResource
    search_fields = ('user', 'score', )


class TFResource(ModelResource):

    class Meta:
        model = TF_Question


class TFQuestionAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('content', 'category', )
    list_filter = ('category',)
    fields = ('content', 'category', 'sub_category',
              'figure', 'quiz', 'explanation', 'correct',)

    search_fields = ('content', 'explanation')
    filter_horizontal = ('quiz',)
    resource_class = TFResource


class EssayResource(ModelResource):

    class Meta:
        model = Essay_Question


class EssayQuestionAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('content', 'category', )
    list_filter = ('category',)
    fields = ('content', 'category', 'sub_category', 'quiz', 'explanation', )
    search_fields = ('content', 'explanation')
    filter_horizontal = ('quiz',)
    resource_class = EssayResource


admin.site.register(Quiz, QuizAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(MCQuestion, MCQuestionAdmin)
admin.site.register(Progress, ProgressAdmin)
admin.site.register(TF_Question, TFQuestionAdmin)
admin.site.register(Essay_Question, EssayQuestionAdmin)
