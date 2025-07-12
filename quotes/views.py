import random

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count, Sum
from django.shortcuts import render
from .models import Quote, Source


def get_random_quote():
    quotes = Quote.objects.all()

    if not quotes.exists():
        return None

    weights = [quote.weight for quote in quotes]
    quote = random.choices(quotes, weights=weights, k=1)[0]

    return quote


def random_quote(request):
    quote = get_random_quote()

    if quote:
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


def paginate(queryset, per_page, page):
    paginator = Paginator(queryset, per_page)

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    return items


def dashboard(request):
    active_tab = request.GET.get('tab', 'quotes')
    per_page = int(request.GET.get('per_page', 10))
    per_page_options = [1, 10, 15]
    page = request.GET.get('page')

    total_quotes = Quote.objects.count()
    total_sources = Source.objects.count()
    total_likes = Quote.objects.aggregate(total=Sum('likes'))['total'] or 0
    total_dislikes = Quote.objects.aggregate(total=Sum('dislikes'))['total'] or 0
    total_views = Quote.objects.aggregate(total=Sum('views'))['total'] or 0

    context = {
        'active_tab': active_tab,
        'per_page': per_page,
        'per_page_options': per_page_options,
        'total_quotes': total_quotes,
        'total_sources': total_sources,
        'total_likes': total_likes,
        'total_dislikes': total_dislikes,
        'total_views': total_views,
    }

    if active_tab == 'quotes':
        quotes = Quote.objects.select_related('source').order_by('-likes')
        items = paginate(quotes, per_page, page)

        context.update({
            'items': items,
            'type': 'quotes',
            'sources': Quote.objects.values_list('source__name', flat=True).distinct()
        })

    if active_tab == 'sources':
        sources = Quote.objects.values(
            'source__name',
            'source__author'
        ).annotate(
            quote_count=Count('id'),
            likes=Sum('likes'),
            dislikes=Sum('dislikes'),
            views=Sum('views')
        ).order_by('-likes')
        items = paginate(sources, per_page, page)

        context.update({
            'items': items,
            'type': 'sources'
        })

    return render(request, 'quotes/pages/dashboard.html', context)
