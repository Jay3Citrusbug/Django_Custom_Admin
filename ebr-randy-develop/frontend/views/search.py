import base64

from core.models import (Review, ReviewCategory)
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from .forums_data_api import forums_data_api


def search_filter(request):
    search = request.GET.get('search_input')
    qry_review_data = Review.objects.filter(status='Published')
    data_model_name = list(qry_review_data.filter(Q(model_name__icontains=search) | Q(
        name__icontains=search)).order_by('-name').values_list('name', 'slug', 'brands__slug').distinct('name'))
    data_brand_name = list(qry_review_data.filter(Q(brands__name__icontains=search)).values_list('brands__name', 'brands__slug').distinct('brands__name'))

    context = {
        'data_model_name': data_model_name,
        'data_brand_name': data_brand_name,
    }

    return JsonResponse({"data": context, 'search': search}, safe=False)


def filter_reviews(min_year, max_year, min_price, max_price, min_weight, max_weight, motor_type, min_battery,
                   max_battery, bike_class,
                   suspension, min_suspension_travel, max_suspension_travel, accessories_fenders, accessories_lights,
                   accessories_racks, keywords, categories, brands, model_name, trim, page_filter_keywords):
    qry_year_review = Review.objects.filter(status='Published').order_by('-id')
    filtered_tags = []
    query = {}
    print(keywords, 'keywords')
    print(page_filter_keywords, 'page_filter_keywords')
    if bike_class != [] and bike_class is not None:
        # qry_year_review = qry_year_review.filter(
        #     review_general_review__demo_bike_class__bike_class__in=bike_class)
        query['review_general_review__demo_bike_class__bike_class__in'] = bike_class
        for class_name in bike_class:
            filtered_tags.append({"bike_class": class_name})

    # Year Filter
    if min_year != "" and min_year is not None or max_year != "" and max_year is not None:
        if min_year is None or min_year == "":
            min_year = min(qry_year_review.values_list('demo_model_year__year', flat=True))
        if max_year is None or max_year == "":
            max_year = max(qry_year_review.values_list('demo_model_year__year', flat=True))
        filtered_tags.append({"min_year-max_year": 'Year:'+str(min_year)+'-'+str(max_year)})

        # qry_year_review = qry_year_review.filter(
        #     demo_model_year__year__range=(min_year, max_year)).distinct('id')
        query['demo_model_year__year__range'] = (min_year, max_year)

    # Price Filter
    if min_price != "" and min_price is not None:
        # qry_year_review = qry_year_review.filter(review_general_review__msrp__gte=min_price)
        filtered_tags.append({"min_price": int(min_price)})
        query['review_general_review__msrp__gte'] = int(min_price)
    if max_price != "" and max_price is not None:
        # qry_year_review = qry_year_review.filter(review_general_review__msrp__lte=max_price)
        filtered_tags.append({"max_price": int(max_price)})
        query['review_general_review__msrp__lte'] = int(max_price)

    # Weight Filter
    if min_weight != "" and min_weight is not None:
        # qry_year_review = qry_year_review.filter(
        #     review_general_review__demo_weight__gte=min_weight)
        # filtered_tags.append({"min_weight": int(min_weight)})
        query['review_general_review__demo_weight__gte'] = int(min_weight)

    if max_weight != "" and max_weight is not None:
        # qry_year_review = qry_year_review.filter(
        #     review_general_review__demo_weight__lte=max_weight)
        # filtered_tags.append({"max_weight": int(max_weight)})
        query['review_general_review__demo_weight__lte'] = int(max_weight)

    if min_weight != "" and min_weight is not None and max_weight != "" and max_weight is not None:
        filtered_tags.append({"min_weight-max_weight": "Weight:"+str(min_weight)+'-'+str(max_weight)})

    # Motor Type Filter
    if motor_type != [] and motor_type is not None:
        # qry_year_review = qry_year_review.filter(
        #     review_general_review__motor_type__in=motor_type)
        for types in motor_type:
            filtered_tags.append({"motor_type": types})
        query['review_general_review__motor_type__in'] = motor_type

    # Battery Capacity Filter
    if min_battery != "" and min_battery is not None:
        # qry_year_review = qry_year_review.filter(
        #     review_general_review__demo_battery_watt_hours__gte=min_battery)
        # filtered_tags.append({"min_battery": int(min_battery)})
        query['review_general_review__demo_battery_watt_hours__gte'] = int(min_battery)

    if max_battery != "" and max_battery is not None:
        # qry_year_review = qry_year_review.filter(
        #     review_general_review__demo_battery_watt_hours__lte=max_battery)
        # filtered_tags.append({"max_battery": int(max_battery)})
        query['review_general_review__demo_battery_watt_hours__lte'] = int(max_battery)

    if min_battery != "" and min_battery is not None and max_battery != "" and max_battery is not None:
        filtered_tags.append({"min_battery-max_battery": 'Battery:'+str(min_battery)+'-'+str(max_battery)})

    # Suspension Filter
    if suspension != [] and suspension is not None:
        # qry_year_review = qry_year_review.filter(
        #     review_general_review__suspension__in=suspension)
        query['review_general_review__suspension__in'] = suspension
        print(suspension, '**********', type(suspension))
        for suspension in suspension:
            filtered_tags.append({"suspension": suspension})

    # Suspension Travel Filter
    if min_suspension_travel != "" and min_suspension_travel is not None:
        # qry_year_review = qry_year_review.filter(
        #     review_frameset_review__demo_suspension_travel__gte=min_suspension_travel)
        # filtered_tags.append({"min_suspension_travel": int(min_suspension_travel)})
        query['review_frameset_review__demo_suspension_travel__gte'] = int(min_suspension_travel)

    if max_suspension_travel != "" and max_suspension_travel is not None:
        # qry_year_review = qry_year_review.filter(
        #     review_frameset_review__demo_suspension_travel__lte=max_suspension_travel)
        # filtered_tags.append({"max_suspension_travel": int(max_suspension_travel)})
        query['review_frameset_review__demo_suspension_travel__lte'] = int(max_suspension_travel)

    if min_suspension_travel != "" and min_suspension_travel is not None and max_suspension_travel != "" and max_suspension_travel is not None:
        filtered_tags.append({"min_suspension_travel-max_suspension_travel": 'Suspension Travel:'+str(min_suspension_travel)+'-'+str(max_suspension_travel)})

    # Accessories Filter
    if accessories_fenders != "" and accessories_fenders is not None:
        # qry_year_review = qry_year_review.filter(
        #     review_accessory_review__fenders=accessories_fenders)
        filtered_tags.append({"accessories_fenders": "Fenders"})
        query['review_accessory_review__fenders'] = accessories_fenders

    if accessories_lights != "" and accessories_lights is not None:
        # qry_year_review = qry_year_review.filter(
        #     review_accessory_review__lights=accessories_lights)
        filtered_tags.append({"accessories_lights": "Lights"})
        query['review_accessory_review__lights'] = accessories_lights
    rack = []
    if accessories_racks != "" and accessories_racks is not None:
        # qry_year_review = qry_year_review.filter(Q(review_accessory_review__front_rack=accessories_racks) | Q(
        #     review_accessory_review__rear_rack=accessories_racks))
        filtered_tags.append({"accessories_racks": "Racks"})
        rack.append(Q(review_accessory_review__front_rack=accessories_racks) | Q(review_accessory_review__rear_rack=accessories_racks))
    # Keyword Filter
    print(page_filter_keywords, "-**/-*/-*/-*/-*/-/-/-*/-*/-*/*/-*/-*/-*/-*/*/*-/*-///*-/")
    if keywords != "" and keywords is not None and "," not in keywords:
        # qry_year_review = qry_year_review.filter(
        #     Q(name__icontains=keywords) | Q(brands__name__icontains=keywords) | Q(model_name__icontains=keywords))
        filtered_tags.append({"keywords": keywords})
        rack.append(Q(name__icontains=keywords) | Q(brands__name__icontains=keywords) | Q(model_name__icontains=keywords))
    if page_filter_keywords != [] and page_filter_keywords is not None:
        # qry_year_review = qry_year_review.filter(
        #     Q(name__in=page_filter_keywords) | Q(brands__name__in=page_filter_keywords) | Q(
        #         model_name__in=page_filter_keywords))
        rack.append(Q(name__icontains=keywords) | Q(brands__name__icontains=keywords) | Q(model_name__icontains=keywords))
        for keyword in page_filter_keywords:
            filtered_tags.append({"keywords": keyword})

    # Categories Filter
    if categories != [] and categories is not None:
        # qry_year_review = qry_year_review.filter(categories__name__in=categories)
        for category in categories:
            filtered_tags.append({"category": category})

    # Brands Filter
    if brands != [] and brands is not None:
        # qry_year_review = qry_year_review.filter(brands__name__in=brands)
        for brand in brands:
            filtered_tags.append({"brands": brand})

    # Model Name Filter
    if model_name != [] and model_name is not None:
        # qry_year_review = qry_year_review.filter(model_name__in=model_name)
        for model_name in model_name:
            filtered_tags.append({"model_name": model_name})

    # Trim Filter
    if trim != [] and trim is not None:
        # qry_year_review = qry_year_review.filter(trim__in=trim)
        for trim in trim:
            filtered_tags.append({"trim": trim})
    print(filtered_tags, '===================')
    qry_year_review = Review.objects.filter(*rack, **query, status='Published').distinct('id').order_by('-id')
    # print(qry_year_review.count())
    data = {
        "filtered_tags": filtered_tags,
        "filtered_reviews": qry_year_review
    }

    return data


def search(request):
    num_review = 24

    category_ids = request.GET.get('categories', None)
    page = request.GET.get('page', 1)

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

    if category_ids != None:
        qry_featured_review = None
        featured_review_ids = []
        print("heloooo", category_ids)
        if category_ids == '':
            return redirect('/')
        category_id_list = category_ids.split(',')
        print(category_id_list)
        # try:
        #     encoded_categroy_ids = base64.b64decode(
        #         category_ids).decode('ascii')
        #     category_id_list = list(map(int, encoded_categroy_ids.split(',')))
        #     print(category_id_list)
        # except:
        #     return HttpResponse('<h1>404 Error</h1>')

        removed_category = [int(i) for i in request.COOKIES.get(
            'remove_category_id', '').split('%2C') if i != '']
        qry_category = ReviewCategory.objects.exclude(
            Q(id__in=removed_category)).filter(
            Q(id__in=category_id_list)).order_by('-parent_category')
        parent_categories = qry_category.filter(id__in=category_id_list)

        if qry_category.count() == 0:
            return redirect('/')
        elif qry_category.count() == 1:
            return redirect(f'/category/{qry_category.first().slug}')

        for featured_review_category in qry_category:
            if featured_review_category.featured_review:
                featured_review = featured_review_category.featured_review.split(
                    ',')
                featured_review_ids = list(set(featured_review_ids + featured_review))

        # qry_category_reviews = Review.objects.exclude(categories__in=removed_category).filter(
        #     Q(categories__in=qry_category)).distinct('id').order_by('-id')
        if order in ['1', '2', '3', '4']:
            qry_category_reviews = Review.objects.filter(Q(categories__in=qry_category)).distinct('id').order_by('-id')
            qry_category_reviews = Review.objects.filter(id__in=qry_category_reviews).order_by(order_asc).prefetch_related('categories', 'brands', 'review_general_review', 'review_general_review__demo_bike_class', 'review_galley_review', 'review_galley_review__image')
        else:
            qry_category_reviews = Review.objects.filter(Q(categories__in=qry_category)).distinct('id').order_by(order_asc).prefetch_related('categories', 'brands', 'review_general_review', 'review_general_review__demo_bike_class', 'review_galley_review', 'review_galley_review__image')

        if len(featured_review_ids) > 0:
            qry_featured_review = Review.objects.filter(
                id__in=featured_review_ids)
            qry_category_reviews = qry_category_reviews.filter(
                ~Q(id__in=featured_review_ids))
            num_review -= len(featured_review_ids)

        pagination = Paginator(qry_category_reviews, num_review)
        pages = [i for i in range(1, pagination.num_pages + 1)]

        try:
            bike_category = pagination.page(page)
        except PageNotAnInteger:
            bike_category = pagination.page(1)
        except EmptyPage:
            bike_category = pagination.page(pagination.num_pages)
        category_id_list = list(set(category_id_list) ^ set(removed_category))

        context = {
            'selected_categories': category_id_list,
            'category': qry_category,
            'featured_reviews': qry_featured_review,
            'reviews': bike_category,
            'total_reviews': qry_category_reviews.count(),
            'recent_forum_discussion': forums_data_api(),
            'pages': pages,
            'category_reviews': True,
        }

        return render(request, 'frontend/subpages/search_result.html', context)
    else:
        min_year = request.GET.get('min_year')
        max_year = request.GET.get('max_year')
        min_weight = request.GET.get('min_weight')
        max_weight = request.GET.get('max_weight')
        motor_type = request.GET.getlist('motor_type')
        min_battery = request.GET.get('min_battery')
        max_battery = request.GET.get('max_battery')
        bike_class = request.GET.getlist('bike_class')
        suspension = request.GET.getlist('suspension')
        min_suspension_travel = request.GET.get('min_suspension_travel')
        max_suspension_travel = request.GET.get('max_suspension_travel')
        accessories_fenders = request.GET.get('accessories_fenders')
        accessories_lights = request.GET.get('accessories_lights')
        accessories_racks = request.GET.get('accessories_racks')
        keywords = request.GET.get('keywords')
        categories = request.GET.getlist('category[]')
        brands = request.GET.getlist('brands[]')
        model_name = request.GET.getlist('model_name[]')
        trim = request.GET.getlist('trim[]')
        min_price = request.GET.get("min_price")
        max_price = request.GET.get("max_price")
        page_filter_keywords = request.GET.getlist("keywords[]")
        featured_review_ids = []

        print("motor_type ##################", motor_type)
        qry_review = filter_reviews(min_year, max_year, min_price, max_price, min_weight, max_weight, motor_type,
                                    min_battery, max_battery, bike_class,
                                    suspension, min_suspension_travel, max_suspension_travel, accessories_fenders,
                                    accessories_lights,
                                    accessories_racks, keywords, categories, brands, model_name, trim,
                                    page_filter_keywords)

        featured_review_category = list(filter(lambda ele: ele is not None, set(list(
            qry_review['filtered_reviews'].values_list('categories__featured_review', flat=True)))))
        for category_review in featured_review_category:
            featured_review_ids = list(set(featured_review_ids + category_review.split(",")))

        featured_review_brand = list(filter(lambda ele: ele is not None, set(list(
            qry_review['filtered_reviews'].values_list('brands__featured_review', flat=True)))))
        for brand_reaview in featured_review_brand:
            featured_review_ids = list(set(featured_review_ids + brand_reaview.split(",")))

        if featured_review_ids is not None:
            qry_featured_review = Review.objects.filter(id__in=featured_review_ids, status='Published')
            qry_review['filtered_reviews'] = qry_review['filtered_reviews'].filter(
                ~Q(id__in=featured_review_ids)).distinct('id').order_by('-id')
            num_review -= len(featured_review_ids)

        filtered_tags = qry_review['filtered_tags']

        if order in ['1', '2', '3', '4']:
            qry_review = qry_review['filtered_reviews'].distinct('id').order_by('-id')
            qry_review = Review.objects.filter(id__in=qry_review).order_by(order_asc).prefetch_related('categories', 'brands', 'review_general_review', 'review_general_review__demo_bike_class', 'review_galley_review', 'review_galley_review__image')
        else:
            qry_review = qry_review['filtered_reviews'].distinct('id').order_by(order_asc).prefetch_related('categories', 'brands', 'review_general_review', 'review_general_review__demo_bike_class', 'review_galley_review', 'review_galley_review__image')
        pagination = Paginator(qry_review, num_review)
        pages = [i for i in range(1, pagination.num_pages + 1)]

        try:
            bike_reviews = pagination.page(page)
        except PageNotAnInteger:
            bike_reviews = pagination.page(1)
        except EmptyPage:
            bike_reviews = pagination.page(pagination.num_pages)

        context = {
            'filtered_tags': filtered_tags,
            'featured_reviews': qry_featured_review,
            'reviews': bike_reviews,
            'total_reviews': qry_review.count(),
            'recent_forum_discussion': forums_data_api(),
            'pages': pages,
            'search_reviews': True,
        }
        return render(request, 'frontend/subpages/search_result.html', context)


def more_filter(request):
    qry_year_review = Review.objects.filter(status='Published').order_by('-id')
    min_year = request.GET.get('min_year')
    max_year = request.GET.get('max_year')
    min_weight = request.GET.get('min_weight')
    max_weight = request.GET.get('max_weight')
    motor_type = request.GET.getlist('motor_type')
    min_battery = request.GET.get('min_battery')
    max_battery = request.GET.get('max_battery')
    bike_class = request.GET.getlist('bike_class')
    suspension = request.GET.getlist('suspension')
    min_suspension_travel = request.GET.get('min_suspension_travel')
    max_suspension_travel = request.GET.get('max_suspension_travel')
    accessories_fenders = request.GET.get('accessories_fenders')
    accessories_lights = request.GET.get('accessories_lights')
    accessories_racks = request.GET.get('accessories_racks')
    keywords = request.GET.get('keywords')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('min_price')
    categories = request.GET.getlist('category[]')
    brands = request.GET.getlist('brands[]')
    model_name = request.GET.getlist('model_name[]  ')
    trim = request.GET.getlist('trim[]')
    page_filter_keywords = request.GET.getlist("keywords[]")
    # qry_year_review = review_qry
    print("motor_type ##################", motor_type)
    qry_year_review = filter_reviews(min_year, max_year, min_price, max_price, min_weight, max_weight, motor_type,
                                     min_battery, max_battery, bike_class,
                                     suspension, min_suspension_travel, max_suspension_travel, accessories_fenders,
                                     accessories_lights,
                                     accessories_racks, keywords, categories, brands, model_name, trim,
                                     page_filter_keywords)

    data_dict = {
        "total_reviews": list(qry_year_review['filtered_reviews'].distinct('id').values_list(flat=True)),
    }
    return JsonResponse(data_dict, safe=False)
