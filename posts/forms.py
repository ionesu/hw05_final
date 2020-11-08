from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('group', 'text')
        labels = {'text': 'Введите текст', 'group': 'Выберите группу'}
        help_texts = {
                      'text': 'Введите здесь текст вашего поста',
                      'group': 'Выберите группу для вашего поста'
                     }

    def clean_text(self):
        data = self.cleaned_data['text']

        if "дурак" in data.lower():
            raise forms.ValidationError("Удалите плохое слово из текста!")

        return data
