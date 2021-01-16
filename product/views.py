from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Sum, Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View, DetailView, ListView
from django.contrib.auth.models import User
from .models import Category, Item, CartItem, Cart, CommentForm, Comment, WishList, WishListItem, Newsletter
import stripe
from django.contrib import messages
from django.db.models import Count, Avg, Sum
from django.views.generic import View
from .forms import AddToCartForm, SearchForm, NewsletterForm
from django.core.paginator import Paginator

stripe.api_key = settings.STRIPE_SECRET_KEY


class HomeView(View):
    def get(self, request):
        all_items = Item.objects.all().select_related('category')
        new_product = all_items.order_by('-pk')[:10]
        top_product = all_items.order_by('-sell_count')[:10]
        context = {
            'category': all_items,
            'new_product': new_product,
            'top_product': top_product,
        }
        return render(request, 'index.html', context)


class ItemDetailView(DetailView):
    model = Item

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object = super().get_object()
        context['form'] = AddToCartForm(instance=object)
        comments = Comment.objects.filter(product_id=object.id)
        com_count = comments.aggregate(Count('product'))  # count customer review
        review_count = comments.aggregate(Avg('rate'))
        paginator = Paginator(comments, 2)
        page_number = self.request.GET.get('page')
        comments = paginator.get_page(page_number)
        context['comments'] = comments
        context['comment_count'] = com_count
        context['review_count'] = review_count
        context['wishlist'] = Item.objects.order_by("id")[:3]
        return context;


class AddToCartView(LoginRequiredMixin, View):
    def get(self, request):
        qty = request.GET.get("qty", 1)
        item_id = request.GET.get("item_id")
        item = Item.objects.get(pk=item_id)

        cart_obj, created = Cart.objects.get_or_create(user=request.user, is_active=True)
        item, created = CartItem.objects.get_or_create(item=item, cart=cart_obj, defaults={'quantity': qty})
        if not created:
            item.quantity = item.quantity + int(qty)
            item.save()
        messages.success(request, 'Item added to your cart')
        return redirect('home')


class AddToWishView(LoginRequiredMixin, View):
    def get(self, request):
        qty = request.GET.get("qty", 1)
        wish_id = request.GET.get("wish_id")
        item = Item.objects.get(pk=wish_id)

        wish_obj, created = WishList.objects.get_or_create(user=request.user, is_active=True)
        item, created = WishListItem.objects.get_or_create(item=item, wishlist=wish_obj, defaults={'quantity': qty})

        messages.success(request, 'Item added to your wish cart')
        return redirect('home')


class Checkout(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart.objects.get(user=request.user, is_active=True)
        items = CartItem.objects.filter(cart=cart)

        context = {
            'cart': cart,
            'items': items,

            'paypal_client_id': settings.PAYPAL_CLIENT_ID,
            'strip_pub_key': settings.STRIPE_PUBLISHABLE_KEY
        }
        return render(request, 'product/checkout.html', context)


# Searching product
def search(request):
    if request.method == 'POST':
        srch = request.POST['srh']
        if srch:
            match = Item.objects.filter(Q(name__icontains=srch) | Q(category__name__icontains=srch))
            if match:
                return render(request, 'product/search_product.html', {'new_product': match})

            else:
                messages.error(request, 'no result found')
        else:
            return HttpResponseRedirect('/search/')

    return render(request, 'product/search_product.html')


# Add customer comments
def addcomment(request, id):
    url = request.META.get('HTTP_REFERER')  # get last url
    if request.method == 'POST':  # check post
        form = CommentForm(request.POST)
        if form.is_valid():
            data = Comment()  # create relation with model
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.comment = form.cleaned_data['comment']
            data.rate = form.cleaned_data['rate']
            data.product_id = id
            current_user = request.user
            data.user_id = current_user.id
            data.save()  # save data to table
            messages.success(request, "Your review has ben sent. Thank you for your interest.")
            return HttpResponseRedirect(url)

    return HttpResponseRedirect(url)


# Find list of category by  category name
def cat_filter(request, cat):
    lists = Item.objects.filter(category__name=cat)
    context = {
        'lists': lists,
    }
    return render(request, 'product/product_list.html', context)


# From all comment and review, find individual comment and review based on product name
def comment_filter(request, cat):
    lists = Comment.objects.filter(product__name=cat)
    comment_count = lists.aggregate(Count('product'))
    review_count = lists.aggregate(Avg('rate'))

    context = {
        'lists': lists,
        'comment_count': comment_count,
        'review_count': review_count,
    }
    return render(request, 'product/test.html', context)


# Give an email address and save it database
def newsletter(request):
    url = request.META.get('HTTP_REFERER')  # get last url
    if request.method == 'POST':  # check post
        form = NewsletterForm(request.POST)
        if form.is_valid():
            data = Newsletter()  # create relation with model
            data.email = form.cleaned_data['email']
            current_user = request.user
            data.user_id = current_user.id
            data.save()  # save data to table
            messages.success(request, "Your email has ben sent. Thank you for your interest.")
            return HttpResponseRedirect(url)

    return HttpResponseRedirect(url)


# Paginator in Command class
def comment_show(request, id):
    all_com = Comment.objects.filter(product_id=id)
    paginator = Paginator(all_com, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'product/item_detail.html', {'page_obj': page_obj})

# class CommentShow(ListView):
#     model=Comment
#     template_name = 'product/item_detail.html'
#     ordering = ['id']
#     paginate_by = 3
