from django import forms
from django.db import ProgrammingError

from Hasker.hasker.models import Question, Tag, Answer

# Workaround for initial migration
try:
    TAG_CHOICES = [[tag.id, tag.tag_name] for tag in Tag.objects.all()]
except ProgrammingError as error:
    if 'LINE 1: ...T "hasker_tag"."id", "hasker_tag"."tag_name" FROM "hasker_ta...' in str(error):
        TAG_CHOICES = [[1, '1'], ]
    else:
        raise


class AskForm(forms.ModelForm):

    tags = forms.MultipleChoiceField(choices=TAG_CHOICES)

    class Meta:
        model = Question
        fields = ['header', 'content', 'tags']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['header'].widget.attrs.update({'class': 'form-control'})

        self.fields['content'].widget = forms.widgets.Textarea()
        self.fields['content'].widget.attrs.update({'class': 'form-control', 'rows': '5'})

        self.fields['tags'].widget.attrs.update({
            'class': 'form-control d-none'
        })


class AnswerForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ['content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget = forms.widgets.Textarea()
        self.fields['content'].widget.attrs.update({'class': 'form-control w-100', 'rows': '5'})
