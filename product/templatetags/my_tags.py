from django import template
from django.core.paginator import Paginator
from django.db.models import Count,Avg,Sum
from django.shortcuts import render

from product.models import CartItem, WishListItem,Item,Comment

register = template.Library()


@register.simple_tag
def my_cart_items(username):
    #print("username", username)
    items = CartItem.objects.filter(cart__user__username=username, cart__is_active=True)
    return {'items': items, 'count': items.count()}


@register.simple_tag
def wish_list_items(username):
    #print("username", username)
    items = WishListItem.objects.filter(wishlist__user__username=username, wishlist__is_active=True)
    return {'items': items, 'count': items.count()}


@register.inclusion_tag(filename='product/related_product.html')
def related_items(category, count=4):
    #print("category: ", category)
    items = Item.objects.filter(category=category)[:count]
    return {'item_list': items}


# @register.simple_tag
# def comment_filter(cat):
#     lists = Comment.objects.filter(product__name=cat)
#     comment_count = lists.aggregate(Count('product'))
#     review_count = lists.aggregate(Avg('rate'))
#     return {'list': list, 'comment_count: comment_count, review_count': review_count}


# @register.inclusion_tag(filename='product/item_detail.html')
# def comment_show(request):
#
#     all_com = Comment.objects.all()
#     paginator = Paginator(all_com,3)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return render(request,'product/item_detail.html',{'page_obj':page_obj})