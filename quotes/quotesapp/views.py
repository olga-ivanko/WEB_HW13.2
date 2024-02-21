from django.shortcuts import render, redirect, get_object_or_404
from .forms import TagForm, AuthorForm, QuoteForm
from .models import Tag, Author, Quote
from collections import Counter

from django.core.paginator import Paginator


def main(request):
    quote_list = Quote.objects.all()

    tag_counter = Counter()
    for quote in quote_list:
        for tag in quote.tags.all():
            tag_counter[tag.name] += 1
    top_ten_tags = tag_counter.most_common(10)
    
    paginator = Paginator(quote_list, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "quotesapp/index.html", {"page_obj": page_obj, "top_ten_tags": top_ten_tags})


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


def tags_list(request, tag_name):
    quotes_with_tag = Quote.objects.filter(tags__name__in=[tag_name])
    paginator = Paginator(quotes_with_tag, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "quotesapp/tags_list.html", {"page_obj": page_obj, "tag_name": tag_name})




    