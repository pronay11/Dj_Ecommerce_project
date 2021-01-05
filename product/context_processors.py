from product.models import Category, CartItem


def menus(request):
    categories = Category.objects.all()
    # items = CartItem.objects.filter(user=request.user,  is_active=True)
    data = {
        'menus': categories,
        # 'items': items,
    }
    return data