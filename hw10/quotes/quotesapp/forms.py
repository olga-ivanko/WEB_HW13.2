from django.forms import ModelForm, CharField, TextInput, DateField
from .models import Tag, Author, Quote


class TagForm(ModelForm):
    name = CharField(min_length=3, max_length=25, required=True, widget=TextInput())

    class Meta:
        model = Tag
        fields = ["name"]


class AuthorForm(ModelForm):
    fullname = CharField(min_length=5, max_length=100, required=True, widget=TextInput())
    description = CharField(
        min_length=10, max_length=150, required=True, widget=TextInput()
    )
    born_date = DateField(required=True)
    born_location = CharField(min_length=3, max_length=100, required=True, widget=TextInput())

    class Meta:
        model = Author
        fields = ["fullname", "description", "born_date", "born_location"]

class QuoteForm(ModelForm):
    author = None
    quote = None
    tags = None

    class Meta:
        model = Quote
        fields = ['author', 'quote', 'tags']

