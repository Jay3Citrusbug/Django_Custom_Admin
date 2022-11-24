from core.models import (Review, Pages, ReviewCategory, UpVote, Comments)
from django.db.models import Q, Count, Subquery, OuterRef
from .forums_data_api import forums_data_api
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from frontend.utils import category_details_schema
import json


def category_count_ajax(request):
    category_id = request.GET.get('category_id')
    if category_id is None or category_id == '':
        qry_category_reviews = Review.objects.all().count()
    else:
        category_id = category_id.split(',')
        qry_category_reviews = Review.objects.filter(Q(categories__id__in=category_id) & Q(
            categories__parent_category=None), status='Published').distinct('id').count()
        if qry_category_reviews == 0:
            qry_category_reviews = Review.objects.all().count()
    return JsonResponse({'data': qry_category_reviews}, safe=False)


def category(request):
    qry_bike_category = ReviewCategory.objects.filter(parent_category=None, status='Published').annotate(total_review=Count(
        'review_category')).order_by('order').values('id', 'name', 'slug', 'short_description', 'icon_image', 'total_review')
    for bike_category in qry_bike_category:
        qry_child_bike_category = ReviewCategory.objects.filter(parent_category=bike_category['id'], status='Published').annotate(
            total_review=Count('review_category')).order_by('order').values('id', 'name', 'slug', 'short_description', 'icon_image', 'total_review')
        bike_category['child_bike_category'] = qry_child_bike_category

    context = {
        'bike_category': qry_bike_category,
        'recent_forum_discussion': forums_data_api()
    }
    return render(request, 'frontend/subpages/category-list.html', context)


def category_detail(request, cat_slug):
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

    num_review = 24
    qry_featured_review = None
    featured_review_ids = []
    category_id = [int(i) for i in request.COOKIES.get('remove_category_id', '').split('%2C') if i != '']
    get_prent_category = ReviewCategory.objects.filter(slug=cat_slug)

    if get_prent_category.first().parent_category is None:
        get_prent_category = ReviewCategory.objects.exclude(Q(id__in=category_id)).filter(
            Q(slug=cat_slug) | Q(parent_category__slug=cat_slug)).order_by('-parent_category', 'order')
    else:
        get_prent_category = ReviewCategory.objects.exclude(
            Q(id__in=category_id)).filter(Q(slug=cat_slug)).order_by('-parent_category', 'order')
    if get_prent_category.count() == 0:
        return redirect('/')

    qry_comments_count = Comments.objects.filter(
        comment_type='Category', parent_id=None, is_approved=True, comment_type_id=get_prent_category[0].id).count()

    for featured_review_category in get_prent_category:
        if featured_review_category.featured_review:
            featured_review = featured_review_category.featured_review.split(
                ',')
            featured_review_ids = featured_review_ids + featured_review
    if order in ['1', '2', '3', '4']:
        qry_category_reviews = Review.objects.prefetch_related('categories', 'brands', 'review_general_review', 'review_general_review__demo_bike_class', 'review_galley_review', 'review_galley_review__image', 'review_highlight').filter(Q(categories__in=get_prent_category) | Q(
            categories__parent_category__in=get_prent_category), status='Published').annotate(comment_count=Subquery(Comments.objects.filter(comment_type='Review', comment_type_id=OuterRef('pk'), is_approved=True, parent_id=None).order_by().values('comment_type_id').annotate(cn=Count('*')).values('cn'))).distinct('id').order_by('-id')
        qry_category_reviews = Review.objects.filter(id__in=qry_category_reviews).order_by(order_asc)
    else:
        qry_category_reviews = Review.objects.prefetch_related('categories', 'brands', 'review_general_review', 'review_general_review__demo_bike_class', 'review_galley_review', 'review_galley_review__image', 'review_highlight').filter(Q(categories__in=get_prent_category) | Q(
            categories__parent_category__in=get_prent_category), status='Published').annotate(comment_count=Subquery(Comments.objects.filter(comment_type='Review', comment_type_id=OuterRef('pk'), is_approved=True, parent_id=None).order_by().values('comment_type_id').annotate(cn=Count('*')).values('cn'))).distinct('id').order_by(order_asc)
    if featured_review_ids is not None:
        qry_featured_review = Review.objects.filter(
            id__in=featured_review_ids, status='Published')
        qry_category_reviews = qry_category_reviews.filter(
            ~Q(id__in=featured_review_ids))
        num_review -= len(featured_review_ids)

    pagination = Paginator(qry_category_reviews, num_review)
    page = request.GET.get('page', 1)
    pages = [i for i in range(1, pagination.num_pages+1)]
    try:
        bike_category = pagination.page(page)
    except PageNotAnInteger:
        bike_category = pagination.page(1)
    except EmptyPage:
        bike_category = pagination.page(pagination.num_pages)

    seo_schema = category_details_schema(
        get_prent_category[0], qry_featured_review, bike_category)
    context = {
        'selected_categories': [get_prent_category[0].id],
        'category': get_prent_category,
        'featured_reviews': qry_featured_review,
        'reviews': bike_category,
        'total_reviews': qry_category_reviews.count(),
        'total_comment': qry_comments_count,
        'recent_forum_discussion': forums_data_api(),
        'pages': pages,
        'seo_schema': json.dumps(seo_schema, indent=4),
    }
    return render(request, 'frontend/subpages/category-detail.html', context)
