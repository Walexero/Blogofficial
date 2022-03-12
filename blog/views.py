from django.shortcuts import render,redirect
from .models import Post,Shop,Comment,Cartitem, Cart
from django.contrib.auth.models import User
from django.contrib import messages,auth
from django.db.models import Count
from .forms import PostForm, RegisterForm, CommentForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    return render(request, 'blog/home.html')

@login_required
def blog(request):
    pubpost = Post.objects.order_by('-date_posted').filter(published=True).filter(flag=False)
    context = {
        'posts':pubpost
    }
    return render(request, 'blog/blog.html',context)

# For the Search Function
def search(request):
    wordsearch = request.GET['mysearch']
    getter = Post.objects.filter(title__icontains=wordsearch)
    context = {
        'getter':getter
    }
    return render(request, 'blog/searchresult.html',context)

# For the Shop Section
@login_required
def shop(request):
    goods = Shop.objects.order_by('-bag_price')
    goodscarted = Cartitem.objects.count()
    context = {
        'good':goods,
        'counter':goodscarted
    }
    return render(request, 'blog/shop.html',context)

def addtocart(request,id):
    goods = Shop.objects.filter(id=id).first()
    buygoods = Cartitem.objects.get_or_create(product_id = goods.id)
    orders = Cart.objects.all()
    for things in orders:
        things.items.set(buygoods)
        things.cart_owner = request.user
    else:
        messages.error(request, 'Dang! Cannot add to cart')

        
    context = {
        'goods':goods,
        'buygoods':buygoods,
        'orders':orders,
        'things':things
    }
    return render(request, 'blog/cart.html',context)

def buy(request,slug_id):
    goodbuy = Shop.objects.filter(slug=slug_id)
    context = {
        'goodbuy':goodbuy
    }
    return render(request, 'blog/buy.html', context)


@login_required
def postdetails(request,slug_id):
    thepost = Post.objects.filter(slug=slug_id).first()
    allcomments = Comment.objects.order_by('-bag_quantity').filter(post_id = thepost.id, reply=None)
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        comment_qs = None
        if form.is_valid():
            thecomment = form.save(commit=False)
            thecomment.commenter = request.user
            thecomment.post = thepost
            thecomment.reply_id = request.POST.get('item_id')  
            if thecomment.reply_id:
                comment_qs = Comment.objects.get(id=thecomment.reply_id)
            thecomment.save()

            return redirect('post',thepost.slug)

    context= {
        'posts':thepost,
        'form':form,
        'comments':allcomments,
    }
    return render(request, 'blog/post.html', context)

@login_required
def createpost(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            thepost = form.save(commit=False)
            thepost.author = request.user
            thepost.save()
            return redirect('blog')
    context = {
        'form': form
    }
    return render(request, 'blog/createpost.html', context)

# Security bits go here
def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username,password=password)
            login(request,user)
            return redirect('login')

    context = {
        'form':form
    }
    return render(request, 'blog/register.html',context)


#Admin bits go here
def myadmin(request):
    return render(request, 'adminuser/admin.html')

def userprofile(request):
    data = Post.objects.filter(author=request.user)
    context = {
        'data':data
    }
    return render(request, 'adminuser/userprofile.html',context)

def userpostview(request,slug_id):
    post = Post.objects.filter(slug=slug_id)
    context= {
        'post':post,
    }
    return render(request, 'adminuser/userpostview.html',context)

def userpostedit(request,postid):
    info = Post.objects.filter(author=request.user).filter(id=postid).first()
    form = PostForm(instance=info)
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES,instance=info)
        if form.is_valid():
            info = form.save(commit=False)
            info.author = request.user
            info.save()
            return redirect('userprofile')

    context = {
        'info':info,
        'form':form
    }
    return render(request, 'adminuser/userpostedit.html',context)

def userpostdelete(request,title):
    info = Post.objects.filter(title=title)
    context = {
        'info':info
    }
    return render(request, 'adminuser/userpostdelete.html', context)

def delpost(request,title):
    info =Post.objects.filter(title=title)
    info.delete()
    return render(request, 'adminuser/userprofile.html')

