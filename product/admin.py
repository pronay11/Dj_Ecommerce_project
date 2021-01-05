from django.contrib import admin
from .models import Category, Item, Gallery, Cart, CartItem, Comment,WishListItem,Newsletter


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name']


class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['id','email']


class GalleryInline(admin.StackedInline):
    model = Gallery


class ItemAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'featured_image']
    inlines = [GalleryInline]


class CartInline(admin.StackedInline):
    model = CartItem


class CartAdmin(admin.ModelAdmin):
    inlines = [CartInline]


class CartItemAdmin(admin.ModelAdmin):
    list_display = ['pk', 'item', 'quantity', 'price']


class CommentAdmin(admin.ModelAdmin):
    list_display = [ 'id','user', 'product','name', 'comment', 'status', 'email', 'rate', 'create_at']


class WishListAdmin(admin.ModelAdmin):
    list_display = ['user','is_active']


class WishListItemAdmin(admin.ModelAdmin):
    list_display = ['pk','id', 'item', 'quantity']


admin.site.register(Category,CategoryAdmin)
admin.site.register(Newsletter,NewsletterAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Gallery)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(WishListItem, WishListItemAdmin)