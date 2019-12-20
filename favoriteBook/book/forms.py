from django import forms
from .models import RecommendedBook
from .models import comment

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