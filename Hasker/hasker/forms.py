from django import forms

from Hasker.hasker.models import Question, Tag, Answer
from Hasker.settings import DEBUG

if DEBUG:
    tag_names_list = ['c++', 'scala', 'python', 'java', 'javascript', 'django', 'css']
    TAG_CHOICES = [[i + 1, name] for i, name in enumerate(tag_names_list)]
else:
    TAG_CHOICES = [[tag.id, tag.tag_name] for tag in Tag.objects.all()]


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
