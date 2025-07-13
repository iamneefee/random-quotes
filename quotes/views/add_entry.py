from django.shortcuts import render, redirect
from django.contrib import messages
from ..forms import SourceForm, QuoteForm


def add_source_view(request):
    if request.method == 'POST':
        form = SourceForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Источник успешно добавлена!')
            return redirect('quotes:add-source')
    else:
        form = SourceForm()

    return render(request, 'quotes/pages/add_source.html', {'form': form})


def add_quote_view(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Цитата успешно добавлена!')
            return redirect('quotes:add-quote')
    else:
        form = QuoteForm()

    return render(request, 'quotes/pages/add_quote.html', {'form': form})
