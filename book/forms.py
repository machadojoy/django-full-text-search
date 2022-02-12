from django import forms


class PostSearchForm(forms.Form):

    search = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["search"].label = "Search For"
        self.fields["search"].widget.attrs.update({"class": "form-control"})
