from django import forms


class MessageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 40}))
    send_to_all = forms.BooleanField(required=False, widget=forms.HiddenInput)
