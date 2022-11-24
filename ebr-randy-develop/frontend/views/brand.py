from core.models import (Review, Pages, ReviewBrand, UpVote, Comments)
from django.db.models import Q, Count, OuterRef, Subquery
from .forums_data_api import forums_data_api
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from frontend.utils import brand_details_schema
import json


def float_to_value(x):
    if x > 10**6-1:
        return str(x/10**6) + 'M'
    elif x > 10**3-1:
        return str(x/10**3) + 'K'
    else:
        return str(x)


def brand_json(request):
    slug = request.GET.get('slug', None)
    if slug is not None:
        qry_brand = ReviewBrand.objects.filter(slug=slug)
        if qry_brand.exists():
            qry_review_count = Review.objects.filter(
                brands=qry_brand[0].id, status='Published').count()
            # bike_brand['review_count'] = float_to_value(qry_review_count)
            data = {
                "description": qry_brand[0].description,
                "logo": str(qry_brand[0].brand_image_full.url) if qry_brand[0].brand_image_full else '',
                "title": qry_brand[0].name,
                "reviews": qry_review_count
            }
            return JsonResponse(data)
        else:
            return JsonResponse(False, safe=False)
    else:
        return JsonResponse(False, safe=False)


def dashboard_brands(request):
    qry_brand = ReviewBrand.objects.all().order_by('name')
    data = []
    for brand in qry_brand:
        data.append({
            'id': brand.id,
            'slug': brand.slug,
            'name': brand.name,
            'logo_url': brand.brand_image_full.url if brand.brand_image_full else '',
            'description': brand.description
        })
    return JsonResponse({'status': 200, 'brands': data})


def brand(request):
    brand_dict = {}
    for i in range(65, 91):
        qry_bike_brand = ReviewBrand.objects.filter(name__startswith=chr(i), parent_brand=None, status='Published').order_by('name').values(
            'id', 'name', 'slug', 'brand_image_web', 'brand_image_grayscale_web', 'brand_image_darkmode_web'
        )
        brand_dict[chr(i)] = qry_bike_brand
    # print(brand_dict)
    context = {
        'bike_brands': brand_dict,
        'recent_forum_discussion': forums_data_api(),
    }
    return render(request, 'frontend/subpages/brand-list.html', context)


def brand_details(request, brand_slug):
    """
        Get single Brand data with particular brand review.
    """
    num_review = 24
    order = request.GET.get('order', '5')
    request.GET._mutable = True
    request.GET['order'] = order
    request.GET._mutable = False

    if order == '1':
        order_asc = 'review_general_review__msrp'
    elif order == '2':
        order_asc = '-review_general_review__msrp'
    elif order == '3':
        order_asc = '-name'
    elif order == '4':
        order_asc = 'name'
    else:
        order_asc = '-id'

    qry_featured_review = None
    qry_brand = get_object_or_404(ReviewBrand, slug=brand_slug)
    featured_review = qry_brand.featured_review.split(
        ',') if qry_brand.featured_review else None

    qry_review = Review.objects.prefetch_related('categories', 'brands', 'review_general_review', 'review_general_review__demo_bike_class', 'review_galley_review', 'review_galley_review__image', 'review_highlight').filter(
        brands=qry_brand, status='Published').annotate(comment_count=Subquery(Comments.objects.filter(comment_type='Review', comment_type_id=OuterRef('pk'), is_approved=True, parent_id=None).order_by().values('comment_type_id').annotate(cn=Count('*')).values('cn'))).order_by(order_asc)
    total_review = qry_review.count()
    qry_comments_count = Comments.objects.filter(
        comment_type='Brand', parent_id=None, is_approved=True, comment_type_id=qry_brand.id).count()

    if featured_review is not None:
        qry_featured_review = Review.objects.prefetch_related('categories', 'brands', 'review_general_review', 'review_general_review__demo_bike_class', 'review_galley_review', 'review_galley_review__image', 'review_highlight').filter(
            id__in=featured_review, status='Published').annotate(comment_count=Subquery(Comments.objects.filter(comment_type='Review', comment_type_id=OuterRef('pk'), is_approved=True, parent_id=None).order_by().values('comment_type_id').annotate(cn=Count('*')).values('cn')))
        qry_review = qry_review.filter(~Q(id__in=featured_review))
        num_review -= len(featured_review)

    pagination = Paginator(qry_review, num_review)
    page = request.GET.get('page', 1)
    pages = [i for i in range(1, pagination.num_pages + 1)]

    try:
        review_list = pagination.page(page)
    except PageNotAnInteger:
        review_list = pagination.page(1)
    except EmptyPage:
        review_list = pagination.page(pagination.num_pages)
    seo_schema = brand_details_schema(
        qry_brand, qry_featured_review, review_list)
    context = {
        'brand': qry_brand,
        'featured_reviews': qry_featured_review,
        'reviews': review_list,
        'total_reviews': total_review,
        'total_comment': qry_comments_count,
        'recent_forum_discussion': forums_data_api(),
        'pages': pages,
        'seo_schema': json.dumps(seo_schema, indent=4),
    }
    return render(request, 'frontend/subpages/brand-detail.html', context)
