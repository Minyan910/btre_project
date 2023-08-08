from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from .models import Listing


def index(request):
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)
    # the above is fetching listings by inverse order (the dash) of list_date
    # newest to oldest 

    paginator = Paginator(listings, 6) # want 6 listings per page
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    context = {
        'listings': paged_listings
    }
    return render(request, 'listings/listings.html', context)

def listing(request, listing_id):
    # listing_id is also part of the input
    # b/c in /listings/urls.py you pass in the id
    return render(request, 'listings/listing.html')

def search(request):
    return render(request, 'listings/search.html')