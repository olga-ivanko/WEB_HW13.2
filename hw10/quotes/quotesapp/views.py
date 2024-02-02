from django.shortcuts import render, redirect, get_object_or_404
from .forms import TagForm, AuthorForm, QuoteForm
from .models import Tag, Author, Quote

from django.core.paginator import Paginator

# Create your views here.
def main(request):
    quote_list = Quote.objects.all()
    paginator = Paginator(quote_list, 10)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)


    return render(request, "quotesapp/index.html", {"page_obj": page_obj})


def tag(request):
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="quotesapp:main")
        else:
            return render(request, "quotesapp/tag.html", {"form": form})

    return render(request, "quotesapp/tag.html", {"form": TagForm()})


def author(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="quotesapp:main")
        else:
            return render(request, "quotesapp/n_author.html", {"form": form})

    return render(request, "quotesapp/n_author.html", {"form": AuthorForm()})


def quote(request):
    tags = Tag.objects.all()
    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            author_name = form.cleaned_data["author"]
            author = get_object_or_404(Author, fullname=author_name)
            quote.author = author
            quote.save()
            chosen_tags = form.cleaned_data["tags"]
            quote.tags.set(chosen_tags)
            return redirect(to="quotesapp:main")
        else:
            return render(
                request, "quotesapp/n_quote.html", {"tags": tags, "form": form}
            )
    return render(
        request, "quotesapp/n_quote.html", {"tags": tags, "form": QuoteForm()}
    )


def about_author(request, author_name):
    author = get_object_or_404(Author, fullname=author_name)
    return render(request, "quotesapp/author.html", {"author": author})


def quote_detail(request, quote_id):
    quote = get_object_or_404(Quote, id=quote_id)
    return render(request, "quotesapp/quote.html", {"quote": quote})
