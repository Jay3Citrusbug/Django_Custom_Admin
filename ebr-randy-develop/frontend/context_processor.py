from core.models import Menus, ReviewCategory, Review, TrustedAccessories, ModelYear
from django.db.models import Q, Max, Min

from core.models.comment import UpVote
from .views import float_to_value
import requests
import json
from urllib.parse import unquote


def footer_links(request):
    qry_footer_menu = Menus.objects.filter(menu_location='footer_links', parent_menu=None).order_by('order')

    qry_best_electric_bikes = Menus.objects.filter(menu_location='best_electric_bikes', parent_menu=None).order_by(
        'order')

    qry_popular_brands = Menus.objects.filter(menu_location='popular_brands', parent_menu=None).order_by('order')

    qry_popular_categories = Menus.objects.filter(menu_location='popular_categories', parent_menu=None).order_by(
        'order')

    qry_popular_searches = Menus.objects.filter(menu_location='popular_searches', parent_menu=None).order_by('order')

    qry_popular_topics = Menus.objects.filter(menu_location='popular_topics', parent_menu=None).order_by('order')

    qry_main_menu = Menus.objects.filter(menu_location='main_menu', parent_menu=None).order_by('order').values('id',
                                                                                                               'name',
                                                                                                               'link')
    main_menus = qry_main_menu
    for main_menu in main_menus:
        qry_main_menu_child = Menus.objects.filter(menu_location='main_menu', parent_menu=main_menu['id']).order_by(
            'order')
        main_menu['child_menus'] = qry_main_menu_child

    # qry_bike_category = ReviewCategory.objects.filter(parent_category=None, status='Published').order_by('id').values('id', 'name', 'slug', 'short_description', 'icon_image')

    # for bike_category in qry_bike_category:
    # 	qry_parent_review_count = Review.objects.filter(Q(categories=bike_category['id']) | Q(categories__parent_category=bike_category['id'])).count()
    # 	bike_category['total_review'] = float_to_value(qry_parent_review_count)

    qry_review = Review.objects.all().count()

    qry_trusted = TrustedAccessories.objects.filter(status='Published')

    context = {
        'main_menus': main_menus,
        'best_electric_bikes': qry_best_electric_bikes,
        'popular_brands': qry_popular_brands,
        'popular_categories': qry_popular_categories,
        'popular_searches': qry_popular_searches,
        'popular_topics': qry_popular_topics,
        'footer_menus': qry_footer_menu,
        'trusted': qry_trusted,
        # 'categories': qry_bike_category,
        'total_review': qry_review,
    }

    return context


def navbar_data(request):
    qry_bike_category = ReviewCategory.objects.filter(parent_category=None, status='Published').order_by('id').values(
        'id', 'name', 'slug', 'short_description', 'icon_image')

    for bike_category in qry_bike_category:
        qry_parent_review_count = Review.objects.filter(
            Q(categories=bike_category['id']) & Q(categories__parent_category=None)).distinct('id').count()
        bike_category['total_review'] = float_to_value(qry_parent_review_count)
        qry_category_list = ReviewCategory.objects.filter(
            Q(id=bike_category['id']) | Q(parent_category=bike_category['id'])).order_by('-parent_category')
        category_list = ','.join([str(i.id) for i in qry_category_list])
        bike_category['category_list'] = category_list

    # compare_review_ids = [int(i) for i in request.COOKIES.get('id', '').split('%2C') if i != '']
    compare_review_ids = unquote(request.COOKIES.get('id', ''))
    if compare_review_ids:
        compare_review_ids = eval(compare_review_ids)

    qry_bike_review = Review.objects.all().order_by('-id')
    qry_hub_motors = qry_bike_review.filter(review_general_review__motor_type='Hub')
    qry_mid_drive_motors = qry_bike_review.filter(review_general_review__motor_type='Mid-Drive')
    qry_class_1 = qry_bike_review.filter(review_general_review__bike_class__contains='Class 1')
    qry_class_2 = qry_bike_review.filter(review_general_review__bike_class__contains='Class 2')
    qry_class_3 = qry_bike_review.filter(review_general_review__bike_class__contains='Class 3')
    qry_class_other = qry_bike_review.filter(review_general_review__bike_class__contains='Other')
    qry_suspension_rigid = qry_bike_review.filter(review_general_review__suspension='None')
    qry_suspension_hardtail = qry_bike_review.filter(review_general_review__suspension='Front Suspension')
    qry_suspension_softail = qry_bike_review.filter(review_general_review__suspension='Rear Suspension')
    qry_suspension_full_suspension = qry_bike_review.filter(review_general_review__suspension='Full Suspension')
    qry_accessories_lights = qry_bike_review.filter(review_accessory_review__lights='Yes')
    qry_accessories_fenders = qry_bike_review.filter(review_accessory_review__fenders='Yes')
    qry_accessories_rack = qry_bike_review.filter(
        Q(review_accessory_review__front_rack='Yes') | Q(review_accessory_review__rear_rack='Yes'))

    model_year = ModelYear.objects.aggregate(Min('year'), Max('year'))

    min_year = request.GET.get('min_year', None)
    max_year = request.GET.get('max_year', None)
    min_weight = request.GET.get('min_weight', None)
    max_weight = request.GET.get('max_weight', None)
    motor_type = request.GET.getlist('motor_type[]', None)
    min_battery = request.GET.get('min_battery', None)
    max_battery = request.GET.get('max_battery', None)
    bike_class = request.GET.getlist('bike_class', None)
    suspension = request.GET.getlist('suspension', None)
    min_suspension_travel = request.GET.get('min_suspension_travel', None)
    max_suspension_travel = request.GET.get('max_suspension_travel', None)
    accessories_fenders = request.GET.get('accessories_fenders', None)
    accessories_lights = request.GET.get('accessories_lights', None)
    accessories_racks = request.GET.get('accessories_racks', None)
    keywords = request.GET.get('keywords', None)
    categories = request.GET.getlist('category[]', None)
    brands = request.GET.getlist('brands[]', None)
    model_name = request.GET.getlist('model_name[]', None)
    trim = request.GET.getlist('trim[]', None)
    min_price = request.GET.get("min_price", None)
    max_price = request.GET.get("max_price", None)
    page_filter_keywords = request.GET.getlist("keywords", None)
    category_ids = request.GET.get('categories', None)

    # print(min_year, "min_year")
    # print(max_year, "max_year")
    # print(min_weight, "min_weight")
    # print(max_weight, "max_weight")
    # print(motor_type, "motor_type")
    # print(min_battery, "min_battery")
    # print(max_battery, "max_battery")
    # print(bike_class, "bike_class")
    # print(suspension, "suspension")
    # print(min_suspension_travel, "min_suspension_travel")
    # print(max_suspension_travel, "max_suspension_travel")
    # print(accessories_fenders, "accessories_fenders")
    # print(accessories_lights, "accessories_lights")
    # print(accessories_racks, "accessories_racks")
    # print(keywords, "keywords")
    # print(min_price, "min_price")
    # print(max_price, "max_price")
    # print(category_ids, "category_ids")

    qry_review_model_year = []
    for year in range(model_year['year__max'], model_year['year__min'] - 1, -1):
        qry_review_model_year.append(year)
    context = {
        'bike_categories': qry_bike_category,
        'bike_reviews': qry_bike_review.count(),
        'hub_motors': qry_hub_motors,
        'mid_drive_motors': qry_mid_drive_motors,
        'review_class_1': qry_class_1,
        'review_class_2': qry_class_2,
        'review_class_3': qry_class_3,
        'review_class_other': qry_class_other,
        'suspension_rigid': qry_suspension_rigid,
        'suspension_hardtail': qry_suspension_hardtail,
        'suspension_softail': qry_suspension_softail,
        'suspension_full_suspension': qry_suspension_full_suspension,
        'accessories_lights': qry_accessories_lights,
        'accessories_fenders': qry_accessories_fenders,
        'accessories_rack': qry_accessories_rack,
        'review_year_range': qry_review_model_year,
        'compare_review': compare_review_ids,
        'pre_selected_min_year': int(min_year) if min_year else '',
        'pre_selected_max_year': int(max_year) if min_year else '',
        'pre_selected_min_weight': min_weight,
        'pre_selected_max_weight': max_weight,
        'pre_selected_motor_type': motor_type,
        'pre_selected_min_battery': min_battery,
        'pre_selected_max_battery': max_battery,
        'pre_selected_bike_class': bike_class,
        'pre_selected_suspension': suspension,
        'pre_selected_min_suspension_travel': min_suspension_travel,
        'pre_selected_max_suspension_travel': max_suspension_travel,
        'pre_selected_accessories_fenders': accessories_fenders,
        'pre_selected_accessories_lights': accessories_lights,
        'pre_selected_accessories_racks': accessories_racks,
        'pre_selected_keywords': keywords,
        'pre_selected_categories': categories,
        'pre_selected_brands': brands,
        'pre_selected_model_name': model_name,
        'pre_selected_trim': trim,
        'pre_selected_min_price': min_price,
        'pre_selected_max_price': max_price,
        'pre_selected_page_filter_keywords': page_filter_keywords,
        # 'pre_selected_category_ids': category_ids,
    }

    return context
