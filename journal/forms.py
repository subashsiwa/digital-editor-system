from django import forms
from .models import Article, Comment

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите заголовок'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Введите содержание статьи'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = "Выберите рубрику"

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'target_text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Введите комментарий'}),
            'target_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Укажите комментируемый текст (опционально)'}),
        }