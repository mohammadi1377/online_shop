from django import forms
from customers.models import Comment


class CommentForm(forms.ModelForm):
    text = forms.CharField(label='متن', widget=forms.Textarea(attrs={'rows': 5}))

    class Meta:
        model = Comment
        fields = ('text',)

    def clean_text(self):
        text = self.cleaned_data['text']
        if not text:
            raise forms.ValidationError("متن نمی‌تواند خالی باشد.")
        return text
