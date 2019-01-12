from django import forms

class ContactForm(forms.Form):
    code = forms.CharField(
        max_length=20000,
        widget=forms.Textarea(),
    )


    def clean(self):
        cleaned_data = super(ContactForm, self).clean()
        code = cleaned_data.get('code')
        if not code:
            raise forms.ValidationError('You have to write something!')
