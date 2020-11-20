from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['group', 'text', 'image']
        labels = {
            'text': 'Введите текст',
            'group': 'Выберите группу',
            'image': 'Загрузите картинку'
            }
        help_texts = {
                      'text': 'Введите здесь текст вашего поста',
                      'group': 'Выберите группу для вашего поста',
                      'image': 'Загрузите картинку для вашего поста'
                     }

    def clean_text(self):
        data = self.cleaned_data['text']

        if "дурак" in data.lower():
            raise forms.ValidationError("Удалите плохое слово из текста!")

        return data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("text",)
        widgets = {
            "text": forms.Textarea
        }
        labels = {
            "text": "Комментарий"
        }
        help_texts = {
            "text": "Ваш комментарий тут"
        }
