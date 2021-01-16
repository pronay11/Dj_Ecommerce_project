from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.forms import ModelForm


class Category(models.Model):
    name = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='cat_gallery', default='logo.png')

    def __str__(self):
        return self.name


class ItemManager(models.Manager):
    def new_items(self):
        return self.all().select_related('category').order_by('-pk')[:10]

    def top_items(self):
        return self.all().select_related('category').order_by('-sell_count')[:10]


class Item(models.Model):
    SIZE_CHOICE = (
        ('n', 'No Size'),
        ('s', 'S'),
        ('m', 'M'),
        ('l', 'L'),
    )
    COLOR_CHOICE = (
        ('n', 'No Color'),
        ('red', 'Red'),
        ('white', 'White'),
        ('black', 'Black')
    )
    name = models.CharField(max_length=150)
    brand = models.CharField(max_length=170, default='none')
    new_price = models.DecimalField(max_digits=8, decimal_places=2)
    old_price = models.DecimalField(max_digits=8, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    description = models.TextField()
    size = models.CharField(max_length=5, choices=SIZE_CHOICE)
    color = models.CharField(max_length=5, choices=COLOR_CHOICE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    sell_count = models.IntegerField(default=0)
    featured_image = models.ImageField(upload_to='featured_image', blank=True, null=True)

    objects = ItemManager()

    @property
    def discount(self):
        d = self.old_price - self.new_price
        d_rate = (d * 100) / self.old_price
        return d_rate

    def __str__(self):
        return self.name


class Gallery(models.Model):
    photo = models.ImageField(upload_to='gallery')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='gallery')

    def __str__(self):
        return str(self.pk)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def total_price(self):
        cart_items = self.cart_item.all()
        price = cart_items.aggregate(total=Sum('price'))
        return price["total"]

    def __str__(self):
        return str(self.pk)


class CartItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2,blank = True,null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_item')

    def save(self, *args, **kwargs):
        self.price = self.item.new_price * Decimal(self.quantity)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.item.name


class Comment(models.Model):
    STATUS = (
        ('New', 'New'),
        ('True', 'True'),
        ('False', 'False'),
    )
    product = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=250, blank=True)
    comment = models.CharField(max_length=250, blank=True)
    rate = models.IntegerField(default=1)
    count = models.IntegerField(default=0, blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.user)


class WishListItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    wishlist = models.ForeignKey(WishList, on_delete=models.CASCADE, related_name='wish_item')

    def __str__(self):
        return self.item.name


class Newsletter(models.Model):
    email = models.EmailField(max_length=270, blank=True)

    def __str__(self):
        return self.email


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'comment', 'rate']
