from django.db.models import Count, Sum
from django.shortcuts import render

from .utils import get_stats, paginate, get_sort_options
from ..models import Quote


def dashboard_view(request):
    PER_PAGE_OPTIONS = [5, 10, 15]
    DEFAUL_SORT = '-likes'

    active_tab = request.GET.get('tab', 'quotes')
    per_page = int(request.GET.get('per_page', 10))
    page = request.GET.get('page')

    quote_sort = request.GET.get('quote_sort', DEFAUL_SORT)
    source_sort = request.GET.get('source_sort', DEFAUL_SORT)

    stats = get_stats()

    context = {
        'active_tab': active_tab,
        'per_page': per_page,
        'per_page_options': PER_PAGE_OPTIONS,
        'quote_sort': quote_sort,
        'source_sort': source_sort,
        **stats,
    }

    if active_tab == 'quotes':
        quotes = Quote.objects.select_related('source').order_by(quote_sort)
        items = paginate(quotes, per_page, page)
        sort_options = get_sort_options(active_tab)

        context.update({
            'items': items,
            'type': 'quotes',
            'sources': Quote.objects.values_list('source__name', flat=True).distinct(),
            'sort_options': sort_options,
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
        ).order_by(source_sort)
        items = paginate(sources, per_page, page)
        sort_options = get_sort_options(active_tab)

        context.update({
            'items': items,
            'type': 'sources',
            'sort_options': sort_options,
        })

    return render(request, 'quotes/pages/dashboard.html', context)
