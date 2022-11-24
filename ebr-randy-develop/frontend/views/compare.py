from urllib.parse import unquote
from django.shortcuts import render
from core.models import ReviewCategory, ReviewBrand, Review
from django.db.models import Q


def only_featured_review():
    qry_category_featured_review_list = ReviewCategory.objects.filter(~Q(featured_review=None)).values_list('featured_review', flat=True)
    qry_brand_featured_review_list = ReviewBrand.objects.filter(~Q(featured_review=None)).values_list('featured_review', flat=True)
    featured_review_list = []
    for featured_review in qry_category_featured_review_list:
        featured_review_list.extend(featured_review.split(','))
    for featured_review in qry_brand_featured_review_list:
        featured_review_list.extend(featured_review.split(','))
    qry_featured_review = Review.objects.prefetch_related('categories', 'brands', 'review_general_review', 'review_galley_review', 'review_galley_review__image').filter(id__in=set(featured_review_list))
    return qry_featured_review


def compare(request):
    compare_review_ids = unquote(request.COOKIES.get('id', ''))
    if compare_review_ids:
        compare_review_ids = eval(compare_review_ids)

    if len(compare_review_ids) > 0:
        qry_review = Review.objects.prefetch_related(
            'categories', 'brands', 'review_general_review', 'review_frameset_review', 'review_drivetrain_review',
            'review_components_review', 'review_ebike_systems_review', 'review_accessory_review'
        ).filter(id__in=compare_review_ids)  # .values('id', 'name', 'slug', 'brands__name', 'review_general_review__msrp', 'review_general_review__bike_class', 'review_general_review__demo_bike_class__all', 'review_general_review__frame_type', 'review_general_review__demo_frame_type', 'review_general_review__suspension', 'review_general_review__wheel_size', 'review_general_review__demo_wheel_size', 'review_general_review__gears', 'review_general_review__demo_gear', 'review_general_review__brake_type', 'review_general_review__demo_brake_type', 'review_general_review__motor_type', 'review_general_review__motor_nominal_output', 'review_general_review__demo_motor_nominal_output', 'review_general_review__battery_watt_hours', 'review_general_review__demo_battery_watt_hours', 'review_general_review__demo_weight', 'review_general_review__weight', )
        context = {
            'review_list': list(qry_review),
            'featured_reviews': only_featured_review(),
        }
        return render(request, 'frontend/subpages/compare.html', context)
    else:
        context = {
            'featured_reviews': only_featured_review(),
        }
        return render(request, 'frontend/subpages/compare.html', context)