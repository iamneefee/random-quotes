import random

from django.shortcuts import render
from .models import Quote


def get_random_quote():
    quotes = Quote.objects.all()

    if not quotes.exists():
        return None

    weights = [quote.weight for quote in quotes]
    quote = random.choices(quotes, weights=weights, k=1)[0]

    return quote


def random_quote(request):
    quote = get_random_quote()
    quote.add_view()

    return render(request, 'quotes/pages/random_quote.html', {'quote': quote})


def rate_quote(request):
    if request.method == 'POST':
        quote_id = request.POST.get('quote_id')
        action = request.POST.get('action')
        quote = Quote.objects.get(id=quote_id)

        if action == 'like':
            quote.add_like()

        elif action == 'dislike':
            quote.add_dislike()

        return render(request, 'quotes/components/quote_card.html', {'quote': quote})
