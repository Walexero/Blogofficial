from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.utils.text import slugify
from ckeditor.fields import RichTextField
# Create your models here.

class Post(models.Model):
    date_posted = models.DateTimeField(default=datetime.now())
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=550,null=True,blank=True)
    published = models.BooleanField(default=False, null=True, blank=True)
    flag = models.BooleanField(default=False, null=True, blank=True)
    leadimg = models.ImageField(default='myleadimg.jpg', null=True, blank=True)
    leadvid = models.FileField(upload_to='default')

    # body = models.TextField()
    body = RichTextField()

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def save(self,*args,**kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)


    class Meta:
        db_table = 'posts'
        managed = True
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

class Comment(models.Model):
    body = models.TextField()
    commenter = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    reply = models.ForeignKey('Comment', null=True, related_name='replies', on_delete=models.DO_NOTHING)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.body

    class Meta:
        db_table = 'comments'
        managed = True
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

class Shop(models.Model):
    bag_img = models.ImageField(default='shopimg.jpg')
    slug = models.SlugField(max_length=550,null=True,blank=True)
    bag_type = models.CharField(max_length=50)
    bag_descrip = models.CharField(max_length=50, null=True, blank=True)
    full_descrip = models.CharField(max_length=700, null=True, blank=True)
    bag_price = models.CharField(max_length=50)
    bag_maker = models.CharField(max_length=50)
    bag_quantity = models.IntegerField()

    seller = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.bag_type

    def save(self,*args,**kwargs):
        self.slug = slugify(self.bag_type)
        super(Shop, self).save(*args, **kwargs)

    class Meta:
        db_table = 'shops'
        managed = True
        verbose_name = 'Shop'
        verbose_name_plural = 'Shops'


class Cartitem(models.Model):
    product = models.ForeignKey(Shop, on_delete=models.CASCADE)
    is_ordered = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now=True)
    date_ordered = models.DateTimeField(null=True)

    def __str__(self):
        return self.product.bag_type

    class Meta:
        db_table = 'cartitems'
        managed = True
        verbose_name = 'CartItem'
        verbose_name_plural = 'CartItems'

class Cart(models.Model):
    ref_code = models.CharField(max_length=200)
    cart_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_ordered = models.BooleanField(default=False)
    date_ordered = models.DateTimeField(auto_now=True)
    items = models.ManyToManyField(Cartitem)

    def get_cart_item(self):
        return self.items.all()
    
    def get_cart_total(self):
        return sum([item.product.bag_price for item in self.items.all()])

    def __str__(self):
        return str(self.cart_owner)

    class Meta:
        db_table = 'carts'
        managed = True
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'

    




