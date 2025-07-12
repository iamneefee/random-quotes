from django.shortcuts import render

from .utils import get_random_quote
from ..models import Quote


def random_quote_view(request):
    quote = get_random_quote()

    if quote:
        quote.add_view()

    return render(request, 'quotes/pages/random_quote.html', {'quote': quote})


def rate_quote_view(request):
    if request.method == 'POST':
        quote_id = request.POST.get('quote_id')
        action = request.POST.get('action')
        quote = Quote.objects.get(id=quote_id)

        if action == 'like':
            quote.add_like()

        elif action == 'dislike':
            quote.add_dislike()

        return render(request, 'quotes/components/quote_card.html', {'quote': quote})
