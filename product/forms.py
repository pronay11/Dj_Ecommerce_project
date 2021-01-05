from django import forms
from .models import Category, Item, Comment, CartItem,Newsletter


#
# class WriterForm(forms.ModelForm):
#     class Meta:
#         model = Writer
#         fields = '__all__'


class AddToCartForm(forms.ModelForm):
    qty = forms.IntegerField(initial=1)

    class Meta:
        model = Item
        fields = ('size', 'color', 'qty')

        widgets = {
            'size': forms.Select(attrs={'class': 'input-select', 'disabled': True}),
            'color': forms.Select(attrs={'class': 'input-select', 'disabled': True}),
        }


class SearchForm(forms.Form):
    query = forms.CharField(max_length = 200)
    cat_id = forms.IntegerField()


class NewsletterForm(forms.Form):
    email = forms.EmailField()



