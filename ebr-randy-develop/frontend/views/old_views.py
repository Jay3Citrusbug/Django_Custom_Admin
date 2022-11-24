from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.db.models import Q, Count
import base64
from django.contrib import messages

from django.views.decorators.csrf import csrf_exempt

from frontend.serializers import CommentSerializer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from core.models import (Review, Pages, ReviewCategory, ReviewBrand, ReviewGeneral, ReviewFrameset, ReviewDrivetrain,
                         ReviewComponents, ReviewEbikeSystems, ReviewAccessories, ReviewHighlights, ReviewGalley, UpVote,
                         ModelYear, BikeClass, FrameType, WheelSize, BreakType, Comments, ImageGallery, UpVoteReviewHighlights,
                         User, ContactUs, VisitorHistory
                         )
from django.conf import settings
import requests
import json
import re
from django.shortcuts import redirect
from datetime import datetime

from frontend.utils import review_dict, brand_details_schema, category_details_schema, home_seo, comment_check

from django.template.loader import get_template
from django.core.mail import send_mail


def add_fields(request, pk):
    if pk == 1:
        add_bike_class()
    elif pk == 2:
        add_frame_type()
    elif pk == 3:
        add_break_type()
    elif pk == 4:
        add_wheel_size()
    elif pk == 5:
        add_wieght()
    elif pk == 6:
        add_battery()
    elif pk == 7:
        add_model_year()
    elif pk == 8:
        add_gear()
    elif pk == 9:
        add_motor_nominal()
    elif pk == 10:
        add_load_capacity()
    elif pk == 11:
        add_seatpost_diameter()
    elif pk == 12:
        add_motor_nominal()
    elif pk == 13:
        check_bike_class()
    # print('--------------------')
    return True


def split_str(str):
    if "Class 200" in str:
        new_ = str.replace("Class 200", "")
        new_str = remove_class(new_)
    else:
        new_str = str.split("', '")  # space for class
    return new_str


def split_class(str):
    if "Class 200" in str:
        new_ = str.replace("Class 200", "")
        new_str = remove_class(new_)
    else:
        new_str = str.split("', ' ")  # space for class
    return new_str


def remove_class(str):
    new_str = str.split("', ' ")
    return new_str


def bike_class_split(str):
    new_str = str[2:-2]
    return new_str


def add_bike_class():
    bike_class = BikeClass.objects.all()
    add_bike = ReviewEbikeSystems.objects.all().order_by('id')
    add_general = ReviewGeneral.objects.all().order_by('id')

    for obj, obj_frameset in zip(add_general, add_bike):
        obj_frameset.systems_bike_class = split_class(obj.bike_class[2:-2])
        obj_frameset.save()
        qry_more = bike_class.filter(bike_class__in = split_class(obj.bike_class[2:-2]))
        for i in qry_more:
            obj_frameset.demo_systems_bike_class.add(i)


def add_frame_type():
    add_frame_ = ReviewFrameset.objects.all().order_by('id')
    frame_type = FrameType.objects.all()
    add_general = ReviewGeneral.objects.all().order_by('id')

    for obj, obj_frameset in zip(add_general, add_frame_):
        obj_frameset.frameset_frame_type = obj.frame_type
        obj_frameset.save()
        qry_more = frame_type.filter(frame_type__in = split_str(obj.frame_type[2:-2]))
        for i in qry_more:
            print(obj.frame_type, '============', i, '---------------------------------------', obj.id, obj_frameset.id)
            obj_frameset.demo_frameset_frame_type.add(i)
    return True


def add_break_type():
    break_type = BreakType.objects.all()
    add_general = ReviewGeneral.objects.all().order_by('id')
    add_components = ReviewComponents.objects.all().order_by('id')

    for obj_components, obj_generel in zip(add_components, add_general):
        obj_components.components_brake_type = obj_generel.brake_type
        obj_components.save()
        qry_more = break_type.filter(break_type__in = split_class(obj_generel.brake_type[2:-2]))
        for i in qry_more:
            obj_components.demo_components_brake_type.add(i)
            print(i, '------------------------------------', obj_generel.id)
    return True


def add_wheel_size():
    wheel_size = WheelSize.objects.all()
    add_bike = ReviewGeneral.objects.all().order_by('id')
    add_frame_ = ReviewFrameset.objects.all().order_by('id')

    for obj, obj_frameset in zip(add_bike, add_frame_):
        obj_frameset.frameset_wheel_size = obj.wheel_size
        print(obj.id, '======', obj_frameset.id)
        obj_frameset.save()
        if split_str(obj.wheel_size[2:-2]) != ['']:
            qry_more = wheel_size.filter(wheel_size__in = split_str(obj.wheel_size[2:-2]))
            for i in qry_more:
                obj_frameset.demo_frameset_wheel_size.add(i)
                print(i, '------------', obj_frameset.id, '===', obj.id)
    return True


def add_wieght():
    qry_review = ReviewGeneral.objects.all().order_by('id')
    qry_frameset = ReviewFrameset.objects.all().order_by('id')
    for obj, obj_frameset in zip(qry_review, qry_frameset):
        if obj.weight:
            obj.demo_weight = obj.weight
        else:
            obj.demo_weight = None
        obj.save()
        if obj_frameset.frameset_weight != 'None':
            obj_frameset.demo_frameset_weight = obj_frameset.frameset_weight
        else:
            obj_frameset.demo_frameset_weight = None
        obj_frameset.save()
        pass
    return True


def add_battery():
    qry_review = ReviewGeneral.objects.all().order_by('id')
    qry_ebike = ReviewEbikeSystems.objects.all().order_by('id')
    for obj, obj_ebike in zip(qry_review, qry_ebike):
        if obj.battery_watt_hours:
            obj.demo_battery_watt_hours = obj.battery_watt_hours
        else:
            obj.battery_watt_hours = None
        obj.save()
        if obj_ebike.systems_battery_watt_hours:
            obj_ebike.demo_systems_battery_watt_hours = obj_ebike.systems_battery_watt_hours
        else:
            obj_ebike.demo_systems_battery_watt_hours = None
        obj_ebike.save()
    return True


def add_model_year():
    qry_frame_type = list(
        Review.objects.all().values_list('model_year', flat=True))
    model_year = ModelYear.objects.all()
    add_bike = Review.objects.all()
    for i, val in zip(qry_frame_type, add_bike):
        if ',' in i:
            print("entered in ifff")
            qry_more = model_year.filter(year__in=i.split(', '))
            for j in qry_more:
                val.demo_model_year.add(j)
        else:
            if i != '':
                val.demo_model_year.add(model_year.get(year=int(i)))
                print("else save done ---------")
    return True


def add_gear():
    qry_review = ReviewGeneral.objects.all().order_by('id')
    qry_drivetrain = ReviewDrivetrain.objects.all().order_by('id')
    for general, drevetrain in zip(qry_review, qry_drivetrain):
        if general.gears != '':
            general.demo_gear = general.gears
        else:
            general.demo_gear = None
        general.save()
        if drevetrain.drivetrain_gears != '':
            drevetrain.demo_drivetrain_gears = drevetrain.drivetrain_gears
        else:
            drevetrain.demo_drivetrain_gears = None
        drevetrain.save()
    return True


def add_motor_nominal():
    qry_review = ReviewGeneral.objects.all().order_by('id')
    qry_drivetrain = ReviewEbikeSystems.objects.all().order_by('id')
    for general, drevetrain in zip(qry_review, qry_drivetrain):
        if general.motor_nominal_output != '':
            general.demo_motor_nominal_output = general.motor_nominal_output
        else:
            general.demo_motor_nominal_output = None
        general.save()
        if drevetrain.systems_motor_nominal_output != '':
            drevetrain.demo_systems_motor_nominal_output = drevetrain.systems_motor_nominal_output
        else:
            drevetrain.demo_systems_motor_nominal_output = None
        drevetrain.save()
    return True


def add_load_capacity():
    qry_review = ReviewFrameset.objects.all().order_by('id')
    for general in qry_review:
        if general.load_capacity != '':
            general.demo_load_capacity = general.load_capacity
        else:
            general.demo_load_capacity = None
        general.save()
    return True


def add_seatpost_diameter():
    qry_review = ReviewComponents.objects.all().order_by('id')
    for general in qry_review:
        if general.seatpost_diameter != '':
            general.demo_seatpost_diameter = general.seatpost_diameter
        else:
            general.demo_seatpost_diameter = None
        general.save()
    return True


def add_suspension_travel():
    qry_review = ReviewFrameset.objects.all().order_by('id')
    for general in qry_review:
        if general.suspension_travel != '':
            general.demo_suspension_travel = general.suspension_travel
        else:
            general.demo_suspension_travel = None
        general.save()
    return True


def check_bike_class():
    add_bike = ReviewEbikeSystems.objects.all().order_by('id')
    add_general = ReviewGeneral.objects.all().order_by('id')
    for obj_generel, obj_ebike in zip(add_general, add_bike):
        print(obj_generel.id, '----', obj_ebike.id)
        for generel_bike_class, ebike_bike_class in zip(obj_generel.demo_bike_class.all(), obj_ebike.demo_systems_bike_class.all()):
            if generel_bike_class != ebike_bike_class:
                print(obj_generel.id, '====', obj_ebike.id)
    return True


def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)


def float_to_value(x):
    if x > 10**6-1:
        return str(x/10**6) + 'M'
    elif x > 10**3-1:
        return str(x/10**3) + 'K'
    else:
        return str(x)


def handler404(request, *args, **kwargs):
    return render(request, '404.html')



def price_range_filter(request):
    start_price = request.GET.get('min_price')
    end_price = request.GET.get('max_price')
    if not start_price:
        start_price = 0
    if not end_price:
        end_price = max(ReviewGeneral.objects.all().values_list('msrp'))[0]
    qry_raview = Review.objects.filter(review_general_review__msrp__range=(
        int(start_price), int(end_price)), status='Published')
    data_dict = {
        'total_review': list(qry_raview.values_list(flat=True)),
        'max_price': end_price,
    }
    return JsonResponse(data_dict, safe=False)


def forums_data_api():
    days = 180
    url = settings.IFRAME_URL + \
        '/forums/api/threads?direction=desc&order=last_post_date&last_days={}'
    headers = {'XF-Api-Key': settings.IFRAME_API_KEY}
    response = requests.get(url.format(days), headers=headers)
    data_list = []
    if response.status_code == 200:
        forums_list = json.loads(response.text)
        for i in forums_list['threads'][:11]:
            data_dict = {}
            data_dict['title'] = i['title']
            data_dict['forum'] = i['Forum']['title']
            data_dict['forum_link'] = i['Forum']['view_url']
            data_dict['link'] = i['view_url']
            data_dict['post_date'] = datetime.fromtimestamp(i['post_date'])
            data_list.append(data_dict)
    return data_list


def index(request):
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
    qry_review_bike = Review.objects.prefetch_related('categories', 'brands', 'review_general_review', 'review_general_review__demo_bike_class', 'review_galley_review', 'review_galley_review__image').filter(status='Published').order_by(order_asc)
    pagination = Paginator(qry_review_bike, 24)
    page = request.GET.get('page', 1)
    pages = [i for i in range(1, pagination.num_pages+1)]
    try:
        bike_reviews = pagination.page(page)
    except PageNotAnInteger:
        bike_reviews = pagination.page(1)
    except EmptyPage:
        bike_reviews = pagination.page(pagination.num_pages)

    context = {
        'bike_review': bike_reviews,
        'recent_forum_discussion': forums_data_api(),
        'pages': pages,
        'seo_schema': json.dumps(home_seo(), indent=4),
    }
    return render(request, 'frontend/subpages/index.html', context)



def get_category(request, cat_slug):
    qry_category = ReviewCategory.objects.filter(slug=cat_slug)
    if qry_category.exists():
        qry_review = Review.objects.filter(categories=qry_category[0])
        category_schema = {
            "@context": "http://schema.org",
            "@type": "CollectionPage",
            "@id": "https://electricbikereview.com/"+qry_category[0].slug+"/#WebPage",
            "mainEntity": {
                "@type": "ItemList",
                        "itemListElement": [
                        ]
            },
            "isPartOf": {
                "@type": "WebSite",
                "@id": "https://electricbikereview.com/#WebSite",
                "name": "ElectricBikeReview.com",
                "url": "https://electricbikereview.com/"
            },
            "name": qry_category[0].name,
            "about": qry_category[0].name+" Electric Bike Reviews",
            "description": qry_category[0].name+" Electric Bike Reviews",
            "publisher": {
                "@type": "Organization",
                "@id": "https://electricbikereview.com/#Organization",
                "name": "Electric Bike Review",
                "url": "https://electricbikereview.com/"
            },
            "breadcrumb": {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": 1,
                        "item": {
                            "@id": "https://electricbikereview.com",
                            "name": "Home",
                            "url": "https://electricbikereview.com"
                        }
                    },
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "item": {
                            "@id": "https://electricbikereview.com/category/bikes/",
                            "name": "Reviews",
                            "url": "https://electricbikereview.com/category/bikes/"
                        }
                    },
                    {
                        "@type": "ListItem",
                        "position": 3,
                        "item": {
                            "@id": "https://electricbikereview.com/category/"+qry_category[0].slug+"/",
                            "name":"Kids Electric Bike Reviews",
                            "url":"https://electricbikereview.com/category/"+qry_category[0].slug+"/"
                        }
                    }
                ]
            }
        }
        for review in qry_review:
            qry_review_highlight = ReviewHighlights.objects.filter(
                review=review)
            category_schema['mainEntity']['itemListElement'].append(
                {
                    "@context": "https://schema.org/",
                    "@type": "Product",
                    "name": review.name,
                    "image": str(review.featured_image),
                    "description": "The "+review.model_name+" is an electric bike manufactured by "+review.brands.all()[0].name,
                    "brand": {
                                "@type": "Brand",
                                "@id": "https://electricbikereview.com/brand/"+review.brands.all()[0].slug+"/#Brand",
                                "name": review.brands.all()[0].name,
                        "url": "https://electricbikereview.com/brand/"+review.brands.all()[0].slug+"/",
                        "logo": str(review.brands.all()[0].brand_image_full),
                        "description": review.brands.all()[0].description
                    },
                    "model": review.model_name,
                    "review": {
                        "@type": "Review",
                        "@id": "https://electricbikereview.com/"+review.brands.all()[0].slug+"/"+review.slug+"/#Review",
                        "name": review.name,
                        "url": "https://electricbikereview.com/"+review.brands.all()[0].slug+"/"+review.slug+"/",
                        "headline": review.name,
                        "reviewBody": ".".join([rh.highlight for rh in qry_review_highlight]),
                        "video": "https://youtube.com/watch?v="+review.youtube_video,
                        "commentCount": "",
                        "author": {
                                        "@type": "Person",
                                        "@id": "https://electricbikereview.com/#Court",
                                               "name": "Court Rye",
                                               "url": "https://electricbikereview.com/",
                                        "affiliation": {
                                            "@type": "Organization",
                                            "@id": "https://electricbikereview.com/#Organization",
                                            "name": "Electric Bike Review",
                                                    "url": "https://electricbikereview.com/"
                                        }
                        },
                        "contributor": {
                            "@type": "Person",
                            "@id": "https://electricbikereview.com/#Tyson",
                            "name": "Tyson Roehrkasse",
                            "url": "https://twirltech.solutions/",
                            "affiliation": {
                                "@type": "Organization",
                                "@id": "https://electricbikereview.com/#Organization",
                                "name": "Electric Bike Review",
                                "url": "https://electricbikereview.com/"
                            }
                        },
                        "publisher": {
                            "@type": "Organization",
                            "@id": "https://electricbikereview.com/#Organization",
                            "name": "Electric Bike Review",
                            "url": "https://electricbikereview.com/"
                        },
                        "datePublished": review.publish_date.strftime("%b %d, %Y"),
                        "sameAs": "https://electricbikereview.com/"+review.brands.all()[0].slug+"/"+review.slug+"/"
                    }
                }
            )
    context = {
        'category_details': qry_category,
        'category_schemas': json.dumps(category_schema, indent=4)
    }
    return render(request, 'frontend/review_seo.html', context)
    # return HttpResponse("<h4>This "+str(cat_slug)+" category list page.</h4>")


def review_page(request, brand, slug):
    qry_review = Review.objects.filter(slug=slug)
    if qry_review.exists():
        category = qry_review[0].categories.all().values()
        brand = qry_review[0].brands.all().values()
        qry_review_highlight = ReviewHighlights.objects.filter(
            review=qry_review[0])
        review_data = {
            'id': qry_review[0].id,
            'review_name': qry_review[0].name,
            'review_slug': qry_review[0].slug,
            'meta_title': qry_review[0].meta_title,
            'category': category,
            'brand': brand,
            'review_featured_image': 'https://ebr-dev-bucket.s3.amazonaws.com/'+str(qry_review[0].featured_image),
            'review_featured_image_thumbnail': 'https://ebr-dev-bucket.s3.amazonaws.com/'+str(qry_review[0].featured_image_thumbnail),
            'description': qry_review[0].description,
            'model_name': qry_review[0].model_name,
            'model_year': qry_review[0].model_year,
            'trim': qry_review[0].trim,
            'review_general': ReviewGeneral.objects.get(review=qry_review[0].id),
            'review_frameset': ReviewFrameset.objects.get(review=qry_review[0].id),
            'review_drivetrain': ReviewDrivetrain.objects.get(review=qry_review[0].id),
            'review_components': ReviewComponents.objects.get(review=qry_review[0].id),
            'review_ebike_systems': ReviewEbikeSystems.objects.get(review=qry_review[0].id),
            'review_accessory': ReviewAccessories.objects.get(review=qry_review[0].id),
            'review_highlights': ReviewHighlights.objects.filter(review=qry_review[0].id),
            'review_gallery': ReviewGalley.objects.filter(review=qry_review[0].id).order_by('order'),
            'schema': json.dumps({
                "@context": "http://schema.org",
                "@type": "WebPage",
                "@id": "https://electricbikereview.website/"+brand[0]['slug']+"/"+qry_review[0].slug+"/#WebPage",
                "url": "https://electricbikereview.website/"+brand[0]['slug']+"/"+qry_review[0].slug+"/",
                "name": qry_review[0].name,
                "mainEntity": {
                    "@type": "Review",
                    "@id": "https://electricbikereview.website/"+brand[0]['slug']+"/"+qry_review[0].slug+"//#Review",
                    "name": qry_review[0].name,
                    "url": "https://electricbikereview.website/"+brand[0]['slug']+"/"+qry_review[0].slug+"/",
                    "itemReviewed":
                            {
                                "@type": "Product",
                                "name": qry_review[0].name,
                                "image": "https://ebr-dev-bucket.s3.amazonaws.com/"+str(qry_review[0].featured_image),
                                "description": striphtml(qry_review[0].description)[:100],
                                "brand":
                                {
                                    "@type": "Brand",
                                    "@id": "https://electricbikereview.com/brand/"+brand[0]['slug']+"/#Brand",
                                    "name": brand[0]['name'],
                                    "url": "https://electricbikereview.com/brand/"+brand[0]['slug']+"/",
                                    "logo": "https://ebr-dev-bucket.s3.amazonaws.com/"+brand[0]['brand_image_full'],
                                    "description": brand[0]['description']
                                },
                                "model": qry_review[0].model_name,
                                "review":
                                {
                                    "@type": "Review",
                                    "@id": "https://electricbikereview.website/"+brand[0]['slug']+"/"+qry_review[0].slug+"//#Review",
                                    "name": qry_review[0].name,
                                    "url": "https://electricbikereview.website/"+brand[0]['slug']+"/"+qry_review[0].slug+"/"
                                }
                    },
                    "headline": qry_review[0].name,
                    "reviewBody": ".".join([rh.highlight for rh in qry_review_highlight]),
                    "commentCount": "0",
                    "author":
                    {
                                "@type": "Person",
                                "@id": "https://electricbikereview.com/#Court",
                                "name": "Court Rye",
                                "url": "https://electricbikereview.com/",
                                "affiliation":
                                {
                                    "@type": "Organization",
                                    "@id": "https://electricbikereview.com/#Organization",
                                    "name": "Electric Bike Review",
                                    "url": "https://electricbikereview.com/"
                                }

                    },
                    "contributor":
                    {
                                "@type": "Person",
                                "@id": "https://electricbikereview.com/#Tyson",
                                "name": "Tyson Roehrkasse",
                                "url": "https://twirltech.solutions/",
                                "affiliation":
                                {
                                    "@type": "Organization",
                                    "@id": "https://electricbikereview.com/#Organization",
                                    "name": "Electric Bike Review",
                                    "url": "https://electricbikereview.com/"
                                }
                    },
                    "publisher":
                    {
                                "@type": "Organization",
                                "@id": "https://electricbikereview.com/#Organization",
                                "name": "Electric Bike Review",
                                "url": "https://electricbikereview.com/"
                    },
                    "datePublished": qry_review[0].publish_date.strftime("%b %d, %Y"),
                    "dateModified": qry_review[0].update_at.strftime("%b %d, %Y"),
                    "sameAs": "https://electricbikereview.website/"+brand[0]['slug']+"/"+qry_review[0].slug+"/"
                },
                "isPartOf":
                {
                    "@type": "WebSite",
                    "@id": "https://electricbikereview.com/#WebSite",
                    "name": "ElectricBikeReview.com",
                            "url": "https://electricbikereview.com/"
                },
                "description": qry_review[0].name,
                "about": qry_review[0].name,
                "publisher": {
                    "@type": "Organization",
                    "@id": "https://electricbikereview.com/#Organization",
                    "name": "Electric Bike Review",
                            "url": "https://electricbikereview.com/"
                },
                "breadcrumb":
                {
                    "@type": "BreadcrumbList",
                    "itemListElement":
                    [
                        {
                            "@type": "ListItem",
                            "position": 1,
                            "item": {
                                "@id": "https://electricbikereview.website",
                                "name": "Home",
                                "url": "https://electricbikereview.website"
                            }
                        },
                        {
                            "@type": "ListItem",
                            "position": 2,
                            "item": {
                                "@id": "https://electricbikereview.website/category/bikes/",
                                "name": "Reviews",
                                "url": "https://electricbikereview.website/category/bikes/"
                            }
                        },
                        {
                            "@type": "ListItem",
                            "position": 3,
                            "item": {
                                "@id": "https://electricbikereview.website/brand/",
                                "name": "Brands",
                                "url": "https://electricbikereview.website/brand/"
                            }
                        },
                        {
                            "@type": "ListItem",
                            "position": 4,
                            "item": {
                                "@id": "https://electricbikereview.website/brand/"+brand[0]['slug']+"/",
                                "name": brand[0]['name'],
                                "url": "https://electricbikereview.website/brand/"+brand[0]['slug']+"/"
                            }
                        },
                        {
                            "@type": "ListItem",
                            "position": 5,
                            "item": {
                                "@id": "https://electricbikereview.website/"+brand[0]['slug']+"/"+qry_review[0].slug+"/",
                                "name": qry_review[0].name,
                                "url": "https://electricbikereview.website/"+brand[0]['slug']+"/"+qry_review[0].slug+"/"
                            }
                        }
                    ]
                }
            }, indent=4)
        }
        context = {
            'review_details': review_data
        }
        return render(request, 'frontend/review_seo.html', context)
    else:
        return HttpResponse("done...")

from .compare import only_featured_review
def page_view(request, page_slug):
    filtered_min_price = request.GET.get('page_filter_min_price')
    filtered_max_price = request.GET.get('page_filter_max_price')
    filtered_min_year = request.GET.get('page_filter_min_year')
    filtered_max_year = request.GET.get('page_filter_max_year')
    filtered_brands = request.GET.getlist('page_filter_brands')

    num_review = 12
    qry_page = get_object_or_404(Pages, slug=page_slug, status='Published')
    qry_reviews = Review.objects.filter(status='Published').order_by('-id')
    qry_categories = ReviewCategory.objects.filter(status='Published').order_by('id')
    qry_brand = ReviewBrand.objects.filter(status='Published').order_by('id')
    featured_review_ids = []
    if qry_page:
        if qry_page.is_filter == True:
            if qry_page.filter_type == True:
                qry_reviews = qry_reviews.filter(name__icontains = qry_page.search_text)

                featured_review_category = list(filter(lambda ele:ele is not None, set(list(qry_categories.values_list('featured_review', flat=True)))))
                for category_review in featured_review_category:
                    featured_review_ids = list(set(featured_review_ids + category_review.split(",")))
                    # featured_review_category = list(set(featured_review_category + category_review.split(",")))

                featured_review_brand = list(filter(lambda ele:ele is not None, set(list(qry_brand.values_list('featured_review', flat=True)))))
                for brand_reaview in featured_review_brand:
                    featured_review_ids = list(set(featured_review_ids + brand_reaview.split(",")))
                    # featured_review_brand = list(set(brand_reaview.split(",")))

                # featured_review_ids =  featured_review_category + featured_review_brand
                # featured_review_ids = [eval(i) for i in featured_review_ids]

                if featured_review_ids is not None:
                    qry_featured_review = Review.objects.filter(id__in=featured_review_ids, status='Published')
                    qry_reviews = qry_reviews.filter(~Q(id__in=featured_review_ids)).distinct('id').order_by('-id')
                    num_review -= len(featured_review_ids)

            else:
                print(type(qry_page.model_name) , 'model_name', qry_page.trim, 'trim', qry_page.accessories, 'accessories')
                if qry_page.min_year or qry_page.max_year:
                    qry_reviews = qry_reviews.filter(demo_model_year__year__range=(int(qry_page.min_year), int(qry_page.max_year))).distinct('id')
                    print('year', len(qry_reviews))

                if qry_page.brands.all().count() > 0:
                    qry_reviews = qry_reviews.filter(brands__in=qry_page.brands.all())
                    qry_brand = qry_brand.filter(id__in=qry_page.brands.all())
                    print('brand', len(qry_reviews))

                if qry_page.categories.all().count() > 0:
                    qry_reviews = qry_reviews.filter(categories__in=qry_page.categories.all())
                    qry_categories = qry_categories.filter(id__in=qry_page.categories.all())
                    print('category', len(qry_reviews))

                if qry_page.model_name != '[]':
                    qry_page.model_name = qry_page.model_name[2:-2].split("', '")
                    qry_reviews = qry_reviews.filter(model_name__in = qry_page.model_name)
                    print('model-name', len(qry_reviews))

                if qry_page.trim != '[]':
                    qry_page.trim = qry_page.trim[2:-2].split("', '")
                    qry_reviews = qry_reviews.filter(trim__in = qry_page.trim)
                    print('trim', len(qry_reviews))

                if qry_page.min_price or qry_page.max_price:
                    min_price = qry_page.min_price
                    max_price = qry_page.max_price
                    if qry_page.min_price == None:
                        min_price = min(list(qry_reviews.values_list('review_general_review__msrp', flat=True)))
                    if qry_page.max_price == None:
                        max_price = max(list(qry_reviews.values_list('review_general_review__msrp', flat=True)))
                    qry_reviews = qry_reviews.filter(review_general_review__msrp__range=(min_price, max_price)).distinct('id')
                    print('price', len(qry_reviews))

                if qry_page.suspension != "":
                    qry_reviews = qry_reviews.filter(review_general_review__suspension=qry_page.suspension)
                    print('suspension', len(qry_reviews))

                if qry_page.accessories != '[]':
                    qry_page.accessories = qry_page.accessories[2:-2].split("', '")
                    light_accessories = "None"
                    fenders_accessories = "None"
                    front_rack_accessories = "None"
                    rear_rack_accessories = "None"
                    if 'Lights' in qry_page.accessories:
                        light_accessories = 'Yes'
                        print('Lights')
                        qry_reviews = qry_reviews.filter(review_accessory_review__lights=light_accessories)
                    if 'Fenders' in qry_page.accessories:
                        fenders_accessories = 'Yes'
                        print('Fenders')
                        qry_reviews = qry_reviews.filter(review_accessory_review__fenders=fenders_accessories)
                    if 'Front Rack' in qry_page.accessories or 'Rear Rack' in qry_page.accessories:
                        front_rack_accessories = 'Yes'
                        rear_rack_accessories = 'Yes'
                        print('Rack')
                        qry_reviews = qry_reviews.filter(Q(review_accessory_review__front_rack=front_rack_accessories) | Q(review_accessory_review__rear_rack=rear_rack_accessories))
                    print('accessories', len(qry_reviews))

                if qry_page.motor_type:
                    qry_reviews = qry_reviews.filter(review_general_review__motor_type=qry_page.motor_type)
                    print('Motor Type', len(qry_reviews))

                if qry_page.min_battery_capacity:
                    qry_reviews = qry_reviews.filter(review_general_review__demo_battery_watt_hours__gte=qry_page.min_battery_capacity)
                    print('Min Battery Capacity', len(qry_reviews))
                if qry_page.max_battery_capacity:
                    qry_reviews = qry_reviews.filter(review_general_review__demo_battery_watt_hours__lte=qry_page.max_battery_capacity)
                    print('Max Battery Capacity', len(qry_reviews))

                if qry_page.min_weight:
                    qry_reviews = qry_reviews.filter(review_general_review__demo_weight__gte=qry_page.min_weight)
                    print('Min Weight', len(qry_reviews))
                if qry_page.max_weight:
                    qry_reviews = qry_reviews.filter(review_general_review__demo_weight__lte=qry_page.max_weight)
                    print('Max Weight', len(qry_reviews))

                if qry_page.bike_class:
                    qry_reviews = qry_reviews.filter(review_general_review__demo_bike_class__bike_class__icontains=qry_page.bike_class)
                    print('Bike Class', len(qry_reviews))

                if qry_page.keyword:
                    qry_page.keyword = qry_page.keyword.split(",")
                    qry_reviews = qry_reviews.filter(Q(name__in=qry_page.keyword) | Q(brands__name__in=qry_page.keyword) | Q(model_name__in=qry_page.keyword))
                    # qry_reviews = qry_reviews.filter(Q(name__icontains=qry_page.keyword) | Q(brands__name__icontains=qry_page.keyword) | Q(model_name__icontains=qry_page.keyword))
                    print('Keyword', len(qry_reviews))

                print(qry_reviews.count(), '====')

                featured_review_category = list(filter(lambda ele:ele is not None, set(list(qry_categories.values_list('featured_review', flat=True)))))
                for category_review in featured_review_category:
                    featured_review_ids = list(set(featured_review_ids + category_review.split(",")))
                    # featured_review_category = list(set(featured_review_category + category_review.split(",")))

                featured_review_brand = list(filter(lambda ele:ele is not None, set(list(qry_brand.values_list('featured_review', flat=True)))))
                for brand_reaview in featured_review_brand:
                    featured_review_ids = list(set(featured_review_ids + brand_reaview.split(",")))
                    # featured_review_brand = list(set(brand_reaview.split(",")))

                if featured_review_ids is not None:
                    qry_featured_review = Review.objects.filter(id__in=featured_review_ids, status='Published')
                    qry_reviews = qry_reviews.filter(~Q(id__in=featured_review_ids)).distinct('id').order_by('-id')
                    num_review -= len(featured_review_ids)

            if filtered_min_price or filtered_max_price:
                if not filtered_min_price:
                    filtered_min_price = min(list(qry_reviews.values_list('review_general_review__msrp', flat=True)))
                if not filtered_max_price:
                    filtered_max_price = max(list(qry_reviews.values_list('review_general_review__msrp', flat=True)))
                qry_reviews = qry_reviews.filter(review_general_review__msrp__range=(int(filtered_min_price), int(filtered_max_price)))
            print('max prive', qry_reviews.count())
            if filtered_min_year or filtered_max_year:
                if not filtered_min_year:
                    filtered_min_year = min(list(qry_reviews.values_list('demo_model_year__year', flat=True)))
                if not filtered_max_year:
                    filtered_max_year = max(list(qry_reviews.values_list('demo_model_year__year', flat=True)))
                qry_reviews = qry_reviews.filter(demo_model_year__year__range=(int(filtered_min_year), int(filtered_max_year)))
            print('max year', qry_reviews.count())
            if filtered_brands:
                qry_reviews = qry_reviews.filter(brands__name__in=filtered_brands)
            print('brands....', qry_reviews.count())
            pagination = Paginator(qry_reviews, num_review)
            page = request.GET.get('page', 1)
            pages = [i for i in range(1, pagination.num_pages+1)]
            try:
                bike_reviews = pagination.page(page)
            except PageNotAnInteger:
                bike_reviews = pagination.page(1)
            except EmptyPage:
                bike_reviews = pagination.page(pagination.num_pages)

            context = {
                'featured_reviews': qry_featured_review,
                'page_details': qry_page,
                'bike_review': bike_reviews,
                'brands':qry_brand,
                'total_reviews': qry_reviews.count()+qry_featured_review.count(),
                'pages': pages,
                'recent_forum_discussion': forums_data_api(),
            }

        else:
            if page_slug == 'terms':
                context = {
                    'recent_forum_discussion': forums_data_api(),
                }
                return render(request, 'frontend/subpages/terms.html', context)
            elif page_slug == 'about-us':
                context = {
                    'recent_forum_discussion': forums_data_api(),
                }
                return render(request, 'frontend/subpages/aboutus.html', context)
            elif page_slug == 'contact':
                context = {
                    'recent_forum_discussion': forums_data_api(),
                }
                return render(request, 'frontend/subpages/contact.html', context)
            elif page_slug == 'advertise':
                context = {
                    'recent_forum_discussion': forums_data_api(),
                }
                return render(request, 'frontend/subpages/advertise.html', context)
            elif page_slug == 'shop-directory':
                context = {
                    'featured_reviews': only_featured_review(),
                }
                return render(request, 'frontend/subpages/directory.html', context)
            else:
                context = {
                    'page_details': qry_page,
                    'recent_forum_discussion': forums_data_api(),
                }

        return render(request, 'frontend/subpages/common_page.html', context)
    else:
        return HttpResponse("<h1>Page not found.</h1>")


@csrf_exempt
def send_message(request):
# def send_message(request, page_slug):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        description = request.POST.get('description')
        new_description = re.sub("[^A-Za-z0-9]", "", description)
        is_spam = comment_check('', request.META['HTTP_USER_AGENT'], name, email, new_description)
        qry_contactus = ContactUs(name=name, email=email, message=description, is_spam=is_spam)
        qry_contactus.save()
        send_mail('Automated Response - Contact Form Submission Received', 'Greetings! \n This is an auto-generated response to let you know that we received your Contact Us form submission on ElectricBikeReview.com. A member of our support team will be in contact with you soon!', 'info@electricbikereview.com', [email])
        if not is_spam:
            t = get_template("frontend/include/contact_us_email.html")
            html_message = t.render({
                'name': name,
                'email': email,
                'description': description,
            })
            # print(html_message)
            send_mail('Fwd: EBR Contact Form Submission from {}'.format(name), '', 'info@electricbikereview.com', ['vicky@mailinator.com'], html_message=html_message)

    return JsonResponse({"data":"Done"}, safe=False)
    # return redirect('/'+page_slug+'/')


def visitor_history(request):
    ip = request.GET['ip']
    type = request.GET['type']
    type_name = request.GET['type_name']
    type_id = request.GET['type_name_id']
    type_url = request.GET['type_url']

    qry_visitor_history = VisitorHistory(ip=ip, type=type, type_name=type_name, type_id=type_id, type_url=type_url)
    qry_visitor_history.save()
    return JsonResponse(True, safe=False)


def review_seo(request):
    qry_review = Review.objects.all().order_by('id').values('id', 'name', 'slug', 'meta_title', 'publish_date', 'description', 'featured_image', 'featured_image_web',
                                                            'model_name', 'model_year', 'trim', 'categories__name', 'brands__name', 'brands__slug', 'more_details', 'review_general_review__msrp').distinct('id')
    data = []
    for review in qry_review:
        review["schema"] = json.dumps({
            "@context": "http://schema.org/",
            "@type": "Review",
            "@id": "https://electricbikereview.com/"+review['brands__name']+"/"+review['slug']+"/#Review",
            "url": "https://electricbikereview.com/"+review['brands__name']+"/"+review['slug']+"/",
            "itemReviewed":
            {
                "@type": "Product",
                "name": review['name'],
                "image": ''+review['featured_image'],
                "description": striphtml(review['description'])[:150],
                "model": review['model_name'],
                "review":
                {
                    "@type": "Review",
                        "@id": "https://electricbikereview.com/"+review['brands__name']+"/"+review['slug']+"/#Review",
                        "name": review['name'],
                        "url": "https://electricbikereview.com/"+review['brands__name']+"/"+review['slug']+"/"
                }
            },
            "headline": review['name'],
            "author":
            {
                "@type": "Person",
                    "@id": "https://electricbikereview.com/#Court",
                    "name": "Court Rye",
                    "url": "https://electricbikereview.com/",
                    "affiliation":
                        {
                            "@type": "Organization",
                            "@id": "https://electricbikereview.com/#Organization",
                            "name": "Electric Bike Review",
                            "url": "https://electricbikereview.com/"
                        }

            },
            "contributor":
            {
                "@type": "Person",
                    "@id": "https://electricbikereview.com/#Tyson",
                    "name": "Tyson Roehrkasse",
                    "url": "https://twirltech.solutions/",
                    "affiliation":
                        {
                            "@type": "Organization",
                            "@id": "https://electricbikereview.com/#Organization",
                            "name": "Electric Bike Review",
                            "url": "https://electricbikereview.com/"
                        }
            },
            "publisher":
            {
                "@type": "Organization",
                    "@id": "https://electricbikereview.com/#Organization",
                    "name": "Electric Bike Review",
                    "url": "https://electricbikereview.com/"
            },
            "datePublished": review['publish_date'].strftime("%b %d, %Y"),
            "sameAs": "https://electricbikereview.com/"+review['brands__name']+"/"+review['slug']+"/"
        }, indent=4)
        data.append(review)
    context = {
        'reviews': data
    }
    return render(request, 'frontend/home_seo.html', context)


def comment_upvote(request):
    ip = request.GET['ip']
    comment_type = request.GET['comment_type']
    comment_id = request.GET['comment_id']
    qry_comment = Comments.objects.filter(id=comment_id)
    if qry_comment.exists():
        qry_upvote = UpVote.objects.filter(ip=ip, comment_id=qry_comment[0])
        if not qry_upvote.exists():
            qry_comment_upvote = UpVote(ip=ip, comment_id=qry_comment[0])
            qry_comment_upvote.save()
            change = True
        else:
            qry_upvote.delete()
            change = False
        context = {
            'status': True,
            'message': "Upvote added in comment.",
            'change': change
        }
    else:
        context = {
            'status': False,
            'message': "Comment not found."
        }
    return JsonResponse(context)
