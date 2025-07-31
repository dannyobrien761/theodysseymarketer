from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(label="Name", max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Your full name',
        'id': 'fullname'
    }))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Your email address',
        'id': 'emailaddress'
    }))
    reason = forms.ChoiceField(label="Reason for Query", choices=[
        ("", "Select a reason"),
        ("Consultation Request", "Consultation Request"),
        ("Support Request", "Support Request"),
        ("Other", "Other"),
    ], widget=forms.Select(attrs={
        'class': 'form-control',
        'id': 'reason'
    }))
    message = forms.CharField(label="Message", widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'How can we help you?',
        'rows': 5,
        'id': 'message'
    }))
