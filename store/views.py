from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.db.models import Q

from category.models import Category
from store.models import Product
from cart.models import CartItem
from cart.views import _cart_id


def store(request, category_slug=None):
    if category_slug != None:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category, is_available=True)
        products_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products,6)
        page=request.GET.get('page')
        paged_products =paginator.get_page(page)

        products_count = products.count()
    context = {"products": paged_products, "products_count": products_count}
    return render(request, "store/store.html", context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(
            category__slug=category_slug, slug=product_slug
        )
        in_cart = CartItem.objects.filter(
            product=single_product, cart__cart_id=_cart_id(request)
        ).exists()

    except Exception as e:
        raise Exception

    context = {"single_product": single_product, "in_cart": in_cart}
    return render(request, "store/product_detail.html", context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            product=Product.objects.filter(Q(description__icontains=keyword)|Q(product_name__icontains=keyword)).order_by("-created_at")
            products_count = product.count()
    context = {"products": product, "products_count": products_count}
    return render(request, "store/store.html", context)

 
