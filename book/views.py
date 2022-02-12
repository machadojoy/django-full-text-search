from django.shortcuts import render
from book.forms import PostSearchForm
from book.models import Book
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, \
    TrigramSimilarity, TrigramDistance, SearchHeadline


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


# Search ranking weights
def search_weights(search_query):
    vector = SearchVector("title", weight="A") + SearchVector("authors", weight="B")
    query = search_query
    return Book.objects.annotate(rank=SearchRank(vector, query)).order_by("-rank")


# Search Trigram Similarity
"""
 Postgres SQL query for trigram similarity:
     SELECT title, word_similarity(title, "harry potter") AS word_similarity
     FROM book_book
     WHERE title % "harry potter"
     ORDER BY word_similarity DESC
"""
def trigram_similarity(search_query):
    return Book.objects.annotate(similarity=TrigramSimilarity("title", search_query),).filter(similarity__gte=0.3)\
        .order_by("-similarity")


def trigram_distance(search_query):
    return Book.objects.annotate(distance=TrigramDistance("title", search_query),).filter(ditance__lte=0.5)\
        .order_by("distance")


# Search Headline
def search_headline(search_query):
    vector = SearchVector("authors")
    query = search_query
    return Book.objects.annotate(search=vector, headline=SearchHeadline("authors", query)).filter(search=query)


def post_search(request):
    form = PostSearchForm

    results = []
    if "search" in request.GET:
        form = PostSearchForm(request.GET)
        if form.is_valid():
            search_query = form.cleaned_data["search"]
            results = search_headline(search_query)
    return render(request, "index.html", {"form": form, "results": results, "search_query": search_query})
