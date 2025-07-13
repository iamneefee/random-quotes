import random

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Sum

from ..models import Quote, Source


def get_random_quote():
    quotes = Quote.objects.all()

    if not quotes.exists():
        return None

    weights = [quote.weight for quote in quotes]
    quote = random.choices(quotes, weights=weights, k=1)[0]

    return quote


def paginate(queryset, per_page, page):
    paginator = Paginator(queryset, per_page)

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    return items


def get_sort_options(active_tab):
    if active_tab == 'quotes':
        return {
            '-likes': 'Лайки (по убыванию)',
            'likes': 'Лайки (по возрастанию)',
            '-dislikes': 'Дизлайки (по убыванию)',
            'dislikes': 'Дизлайки (по возрастанию)',
            '-views': 'Просмотры (по убыванию)',
            'views': 'Просмотры (по возрастанию)',
        }

    if active_tab == 'sources':
        return {
            '-likes': 'Лайки (по убыванию)',
            'likes': 'Лайки (по возрастанию)',
            '-dislikes': 'Дизлайки (по убыванию)',
            'dislikes': 'Дизлайки (по возрастанию)',
            '-views': 'Просмотры (по убыванию)',
            'views': 'Просмотры (по возрастанию)',
            '-quote_count': 'Количество цитат (по убыванию)',
            'quote_count': 'Количество цитат (по возрастанию)',
        }


def get_stats():
    stats = {
        'total_quotes': Quote.objects.count(),
        'total_sources': Source.objects.count(),
        'total_likes': Quote.objects.aggregate(total=Sum('likes'))['total'] or 0,
        'total_dislikes': Quote.objects.aggregate(total=Sum('dislikes'))['total'] or 0,
        'total_views': Quote.objects.aggregate(total=Sum('views'))['total'] or 0,
    }

    return stats
