from django.shortcuts import render
from book.forms import PostSearchForm
from book.models import Book

def post_search(request):
    form = PostSearchForm

    results = []
    if "search" in request.GET:
        form = PostSearchForm(request.GET)
        if form.is_valid():
            search_query = form.cleaned_data["search"]
            results = Book.objects.filter(title__contains=search_query)
    return render(request, "index.html", {"form": form, "results": results})
