from django import forms

from core.models import Member, Answer

TRUE_FALSE_CHOICES = (
    (True, 'Да'),
    (False, 'Нет')
)


class MemberForm(forms.ModelForm):
    """Форма создания участника"""

    class Meta:
        model = Member
        fields = '__all__'


class AnswerForm(forms.ModelForm):
    """Форма ответа"""
    answer = forms.ChoiceField(choices=TRUE_FALSE_CHOICES, label="Была ли такая таблица?",
                               initial='', widget=forms.Select(), required=True)
    class Meta:
        model = Answer
        fields = '__all__'
        exclude = ('member', 'table', 'was_shown')
