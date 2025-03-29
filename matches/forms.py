from django import forms

class NewsletterForm(forms.Form):
    message = forms.CharField(
        label='Mesaj', 
        widget=forms.Textarea(attrs={'placeholder': 'Mesajınızı buraya yazın...', 'rows': 3})
    )

