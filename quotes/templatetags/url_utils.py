from django import template

register = template.Library()

@register.simple_tag
def sort_url(active_tab, per_page, value):
    base = f"?tab={active_tab}&per_page={per_page}"

    if active_tab == 'quotes':
        return f"{base}&quote_sort={value}"

    if active_tab == 'sources':
        return f"{base}&source_sort={value}"