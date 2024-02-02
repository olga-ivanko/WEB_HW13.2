from django.forms import ModelForm, CharField, TextInput, DateField, ModelMultipleChoiceField
from .models import Tag, Author, Quote


class TagForm(ModelForm):
    name = CharField(min_length=3, max_length=25, required=True, widget=TextInput())

    class Meta:
        model = Tag
        fields = ["name"]


class AuthorForm(ModelForm):

    class Meta:
        model = Author
        fields = ["fullname", "description", "born_date", "born_location"]


class QuoteForm(ModelForm):

    class Meta:
        model = Quote
        fields = ["author", "quote", "tags"]
