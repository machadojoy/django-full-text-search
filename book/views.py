from django.shortcuts import render
from book.forms import PostSearchForm
from book.models import Book
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank


# Standard textual (case-sensitive) queries
def contains(search_query):
    return Book.objects.filter(title__icontains=search_query)


# Full text postgres search
def search(search_query):
    return Book.objects.filter(title__search=search_query)


# Postgres search vector against multiple fields
def search_vector(search_query):
    return Book.objects.annotate(search=SearchVector("title", "authors"),).filter(search=search_query)


# Postgres search ranking
def search_rank(search_query):
    vector = SearchVector("title")
    query = SearchQuery(search_query)
    return Book.objects.annotate(rank=SearchRank(vector, query)).order_by("-rank")


def post_search(request):
    form = PostSearchForm

    results = []
    if "search" in request.GET:
        form = PostSearchForm(request.GET)
        if form.is_valid():
            search_query = form.cleaned_data["search"]
            results = search_rank(search_query)
    return render(request, "index.html", {"form": form, "results": results, "search_query": search_query})
