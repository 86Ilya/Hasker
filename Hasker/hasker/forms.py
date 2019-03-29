from django import forms

from Hasker.hasker.models import Question, Tag, Answer


# TODO при начальной иницализации происходит косяк
tags = Tag.objects.all()
if len(tags) == 0:
    tag_names_list = ['c++', 'scala', 'python', 'java', 'javascript', 'django', 'css']
    for tag in tag_names_list:
        Tag(tag_name=tag).save()

TAG_CHOICES = [[tag.id, tag.tag_name] for tag in tags]
# TAG_CHOICES = [[1, 'c++'], [2, 'scala']]


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
