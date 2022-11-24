from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Count
from youtubesearchpython import VideosSearch
from frontend.utils import review_dict
from core.models import (Review, ReviewCategory, ReviewBrand, ReviewGeneral, ReviewFrameset, ReviewDrivetrain,
                         ReviewComponents, ReviewEbikeSystems, ReviewAccessories, ReviewHighlights, ReviewGalley,
                         Comments, ImageGallery, UpVoteReviewHighlights)
from .forums_data_api import forums_data_api
from django.template.loader import get_template


def review_detail(request, brand_slug, slug):
    # qry_reviews = Review.objects.all().order_by("-id")
    # qry_review = qry_reviews.get(brands__slug=brand_slug, slug=slug)
    qry_review = get_object_or_404(Review.objects.prefetch_related('categories', 'brands'), slug=slug, status='Published')
    obj_review_general = ReviewGeneral.objects.prefetch_related('demo_frame_type', 'demo_bike_class', 'demo_wheel_size', 'demo_brake_type').get(review=qry_review)
    obj_review_frameset = ReviewFrameset.objects.prefetch_related('demo_frameset_wheel_size', 'demo_frameset_wheel_size').get(review=qry_review)
    obj_review_drivetrain = ReviewDrivetrain.objects.get(review=qry_review)
    obj_review_components = ReviewComponents.objects.prefetch_related('demo_components_brake_type').get(review=qry_review)
    obj_review_ebikeSystems = ReviewEbikeSystems.objects.prefetch_related('demo_systems_bike_class').get(review=qry_review)
    obj_review_accessories = ReviewAccessories.objects.get(review=qry_review)
    qry_review_gallery = ReviewGalley.objects.prefetch_related('image').filter(review=qry_review.id).order_by('order')
    qry_review_highlights = ReviewHighlights.objects.filter(review=qry_review.id).order_by('id')
    qry_main_review_comments = Comments.objects.filter(
        comment_type='Review', parent_id=None, is_approved=True, comment_type_id=qry_review.id).count()
    featured_review_ids = []

    featured_review_category = list(filter(lambda ele: ele is not None, set(list(qry_review.categories.all().values_list('featured_review', flat=True)))))
    related_review = Review.objects.exclude(id__in=featured_review_category).\
        exclude(id=qry_review.id).filter(
        categories__in=qry_review.categories.all(), status='Published'
    ).prefetch_related('categories', 'brands', 'review_general_review', 'review_general_review__demo_bike_class', 'review_galley_review', 'review_galley_review__image').order_by('-id').distinct('id')

    for category_review in featured_review_category:
        featured_review_ids = list(set(featured_review_ids + category_review.split(",")))

    qry_featured_review = None
    if featured_review_ids is not None:
        qry_featured_review = Review.objects.prefetch_related('categories', 'brands', 'review_general_review', 'review_general_review__demo_bike_class', 'review_galley_review', 'review_galley_review__image').exclude(id=qry_review.id).filter(id__in=featured_review_ids, status='Published')
        # qry_reviews = qry_reviews.filter(~Q(id__in=featured_review_ids)).distinct('id').order_by('-id')

    videosSearch = VideosSearch(qry_review.name, limit=5)

    if qry_review.youtube_video:
        video_ids = [qry_review.youtube_video]
    else:
        video_ids = []

    for video in videosSearch.result()['result']:
        if video['id'] not in video_ids:
            video_ids.append(video['id'])

    # Make review footer from brand and category.
    brand_category_list = []
    for brand in qry_review.brands.all():
        for category in qry_review.categories.all():
            brand_category_list.append((brand, category))
    brand_category_footer = []
    for brand, category in brand_category_list:
        # qry_brand = ReviewBrand.objects.get(id=brand)
        # qry_category = ReviewCategory.objects.get(id=category)
        footer_name = brand.name + " " + category.name
        footer_review = Review.objects.prefetch_related('brands').filter(brands=brand, categories=category).exclude(id=qry_review.id).order_by('-id')[:5]
        if footer_review:
            brand_category_footer.append({
                'footer_name': footer_name,
                'reviews': footer_review
            })

    context = {
        'featured_reviews': qry_featured_review,
        'related_review': related_review[:10-len(featured_review_ids)],
        'review': qry_review,
        'review_general': obj_review_general,
        'review_frameset': obj_review_frameset,
        'review_drivetrain': obj_review_drivetrain,
        'review_components': obj_review_components,
        'review_ebikeSystems': obj_review_ebikeSystems,
        'review_accessories': obj_review_accessories,
        'total_comment': qry_main_review_comments,
        'review_gallery': qry_review_gallery,
        'recent_forum_discussion': forums_data_api(),
        'videos': video_ids[0:5],
        'is_first': 'True',
        'review_highlights': qry_review_highlights[0] if qry_review_highlights else '',
        'footer_reviews': brand_category_footer,
    }
    return render(request, 'frontend/subpages/review_detail.html', context)


@csrf_exempt
def get_review_highlights(request):
    if request.method == 'POST':
        review_id = request.POST['review_id']
        show_all = request.POST['show_all']
        user_ip = request.POST['ip']
        qry_review = Review.objects.get(id=review_id)
        print(request.POST['show_all'])
        qry_review_highlights = ReviewHighlights.objects.filter(review=qry_review).annotate(
            upvote_count=Count('upvotereviewhighlights__review_highlight_id')
        ).order_by('-upvote_count')

        total_highlights = qry_review_highlights.count()

        qry_upvote_list = UpVoteReviewHighlights.objects.filter(ip=user_ip).values_list('review_highlight_id', flat=True)

        if show_all == 'false':
            review_highlights = qry_review_highlights[:3]
        else:
            review_highlights = qry_review_highlights
        t = get_template("frontend/include/highlights.html")
        response = t.render({
            'review_highlights': review_highlights,
            'upvote_list': qry_upvote_list,
            'review': qry_review,
            'show_all': show_all,
            'total_highlights': total_highlights
        })
        context = {
            'status': True,
            'message': "Upvote added in highlights.",
            'data': response
        }
    else:
        context = {
            'status': False,
            'message': "Get method not allowed."
        }
    return JsonResponse(context)


@csrf_exempt
def highlights_update_vote(request):
    if request.method == 'POST':
        highlights_id = request.POST['highlights_id']
        ip = request.POST['ip']
        qry_highlights = ReviewHighlights.objects.filter(id=highlights_id)
        if qry_highlights.exists():
            qry_upvote = UpVoteReviewHighlights.objects.filter(ip=ip, review_highlight_id=qry_highlights[0])
            if not qry_upvote.exists():
                qry_highlights_upvote = UpVoteReviewHighlights(ip=ip, review_highlight_id=qry_highlights[0])
                qry_highlights_upvote.save()
                change = True
            else:
                qry_upvote.delete()
                change = False
            context = {
                'status': True,
                'message': "Upvote added in highlights.",
                'change': change
            }
        else:
            context = {
                'status': False,
                'message': "Highlights not found."
            }
    else:
        context = {
            'status': False,
            'message': "Get method not allowed."
        }
    return JsonResponse(context)
