from django import forms
from .models import RecommendedBook
from .models import comment
from django.contrib.admin import widgets
import os

CHOICE={
    ("0","新しいコメントを上"),
    ('1',"古いコメントを上"),
}


class RadioForm(forms.Form):
    select=forms.ChoiceField(label="コメントの出力順　(デフォルトで新しい順で表示されます)　", widget=forms.RadioSelect, choices=CHOICE,initial=0)


class BookForm(forms.ModelForm):
    class Meta:
        model=RecommendedBook
        fields=['author',"bookTitle","genre"]


class FindForm(forms.Form):
    find=forms.CharField(label="Find",required=False)


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model=comment
        fields=('handlename',"content")