import random
from django.shortcuts import render
from .models import Quote


def get_random_quote():
    quotes = Quote.objects.all()

    if not quotes.exists():
        return None

    weights = [quote.weight for quote in quotes]
    quote = random.choices(quotes, weights=weights, k=1)[0]
    quote.add_view()

    return quote


def random_quote(request):
    quote = get_random_quote()

    return render(request, 'quotes/pages/random_quote.html', {'quote': quote})
