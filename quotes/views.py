from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Author, Quote
from .forms import QuoteForm, AuthorForm
from django.core.paginator import Paginator
from django.db.models import Count

def quote_list(request):
    quotes_list = Quote.objects.all()
    paginator = Paginator(quotes_list, 10) 
    page_number = request.GET.get('page')
    quotes = paginator.get_page(page_number)
    top_ten_tags = top_tags()
    return render(request, 'quotes/quote_list.html', {'quotes': quotes, 'top_ten_tags': top_ten_tags})

def top_tags():
    return Quote.objects.values('tags').annotate(tag_count=Count('tags')).order_by('-tag_count')[:10]


# Add Author (only for logged-in users)
@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quotes:quote_list')
    else:
        form = AuthorForm()
    return render(request, 'quotes/add_author.html', {'form': form})

# Add Quote (only for logged-in users)
@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quotes:quote_list')
    else:
        form = QuoteForm()
    return render(request, 'quotes/add_quote.html', {'form': form})

def search_quotes_by_tag(request, tag):
    quotes = Quote.objects.filter(tags__icontains=tag)
    return render(request, 'quotes/search_results.html', {'quotes': quotes, 'tag': tag})

def quotes_by_author(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    quotes_list = Quote.objects.filter(author=author)
    paginator = Paginator(quotes_list, len(quotes_list)) 
    page_number = request.GET.get('page')
    quotes = paginator.get_page(page_number)
    return render(request, 'quotes/quotes_by_author.html', {'author': author, 'quotes': quotes})