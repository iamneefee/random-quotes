from django import forms
from .models import Source, Quote


class SourceForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = ['name', 'author']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_name(self):
        name = self.cleaned_data['name']

        if Source.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("Источник с таким названием уже существует")

        return name


class QuoteForm(forms.ModelForm):
    weight = forms.IntegerField(
        min_value=Quote.MIN_WEIGHT,
        max_value=Quote.MAX_WEIGHT,
        widget=forms.NumberInput(
            attrs={'class': 'form-control', 'placeholder': f'Выберите вес от {Quote.MIN_WEIGHT} до {Quote.MAX_WEIGHT}'})
    )

    class Meta:
        model = Quote
        fields = ['text', 'source', 'weight']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Введите текст цитаты'
            }),
            'source': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['source'].queryset = Source.objects.all()
        self.fields['source'].empty_label = "Выберите источник"

    def clean(self):
        cleaned_data = super().clean()
        source = cleaned_data.get('source')
        text = cleaned_data.get('text')

        if source and text:
            if Quote.objects.filter(text__iexact=text).exists():
                self.add_error('text', "Такая цитата уже существует")

            if source.quotes.count() >= Quote.MAX_QUOTES_PER_SOURCE:
                self.add_error('source',
                               f"Источник не может содержать более {Quote.MAX_QUOTES_PER_SOURCE} цитат")

        return cleaned_data
