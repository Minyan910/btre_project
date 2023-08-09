from django.shortcuts import get_object_or_404, render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from listings.choices import price_choices, state_choices, bedroom_choices

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

    listing = get_object_or_404(Listing, pk=listing_id)
    # Listing is the model
    # pk is for primary key

    context = {
        'listing': listing
    }

    return render(request, 'listings/listing.html', context)


def search(request):
    queryset_list = Listing.objects.order_by('-list_date').filter(is_published=True)

    # keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        # note it's square brackets instead of parentheses
        if keywords:
            queryset_list = queryset_list.filter(description__icontains=keywords)
            # doesn't have to match exactly
    
    # city
    if 'city' in request.GET:
        city = request.GET['city']
        # note it's square brackets instead of parentheses
        if city:
            queryset_list = queryset_list.filter(city__icontains=city)
    
    # state
    if 'state' in request.GET:
        state = request.GET['state']
        # note it's square brackets instead of parentheses
        if state:
            queryset_list = queryset_list.filter(state__iexact=state)
            # __iexact is case-insentive
            # __exact is case-sensitive

    # bedroom
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        # note it's square brackets instead of parentheses
        if bedrooms:
            queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)
            # __iexact is case-insentive
            # __exact is case-sensitive

    # price
    if 'price' in request.GET:
        price = request.GET['price']
        # note it's square brackets instead of parentheses
        if price:
            queryset_list = queryset_list.filter(price__lte=price)
            # __iexact is case-insentive
            # __exact is case-sensitive

    context = {
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'listings': queryset_list,
        'values': request.GET
    }

    return render(request, 'listings/search.html', context)