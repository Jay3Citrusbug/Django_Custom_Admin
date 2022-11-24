import re
from django.conf import settings
from core.models import ReviewHighlights, Comments
from django.db.models import Count, OuterRef


def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)


def review_highlight(highlights):
    highlight = ''
    for rh in highlights:
        highlight += rh.highlight+'.'
    return highlight


def review_schema(brand, review):
    host_url = settings.SCHEMA_URL
    dict = {
            "@context": "https://schema.org/",
            "@type": "Product",
            "name": review.name,
            "image": settings.AWS_IMAGE_URL + str(review.featured_image) if review.featured_image else '',
            "description": "The "+review.model_name+" is an electric bike manufactured by "+brand.name,
            "brand": {
               "@type": "Brand",
               "@id": "{}/brand/{}/#Brand".format(host_url, brand.slug),
               "name": brand.name,
               "url": "{}/brand/{}/".format(host_url, brand.slug),
               "logo": settings.AWS_IMAGE_URL+str(brand.brand_image_full) if brand.brand_image_full else '',
               "description": brand.description
            },
            "model": review.name,
            "review": {
               "@type": "Review",
               "@id": "{}/{}/{}/#Review".format(host_url, brand.slug, review.slug),
               "name": review.name,
               "url": "{}/{}/{}/".format(host_url, brand.slug, review.slug),
               "headline": review.name,
               "reviewBody": review_highlight(review.review_highlight.all()),
               "video": "https://youtube.com/watch?v={}".format(review.youtube_video),
               "commentCount": str(review.comment_count) if review.comment_count is not None else '0',
               "author":{
                  "@type": "Person",
                  "@id": "https://electricbikereview.com/#Court",
                  "name": "Court Rye",
                  "url": "https://electricbikereview.com/",
                  "affiliation":{
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
               "sameAs": "{}/{}/{}/".format(host_url, brand.slug, review.slug),
            }
         }
    return dict


def brand_details_schema(brand, featured_reviews, reviews):
    host_url = settings.SCHEMA_URL

    brand_details_dict = {
        "@context": "http://schema.org",
        "@type": "CollectionPage",
        "@id": "{}/{}/#WebPage".format(host_url, brand.slug),
        "mainEntity": {
          "@type": "ItemList",
          "itemListElement": []
        },
        "isPartOf":{
          "@type": "WebSite",
          "@id": "{}/#WebSite".format(host_url),
          "name": "ElectricBikeReview.com",
          "url": host_url
        },
        "name": brand.name,
        "about": brand.name,
        "description": brand.name,
        "publisher": {
          "@type": "Organization",
          "@id": "{}/#Organization".format(host_url),
          "name": "Electric Bike Review",
          "url": host_url
        },
        "breadcrumb": {
          "@type": "BreadcrumbList",
          "itemListElement": [
             {
                "@type": "ListItem",
                "position": 1,
                "item": {
                   "@id": host_url,
                   "name": "Home",
                   "url": host_url
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
                   "@id": "{}/brand/".format(host_url),
                   "name": "Brands",
                   "url": "{}/brand/".format(host_url)
                }
             },
             {
                "@type": "ListItem",
                "position": 4,
                "item": {
                   "@id": "{}/brand/{}/".format(host_url, brand.slug),
                   "name": brand.name,
                   "url": "{}/brand/{}/".format(host_url, brand.slug)
                }
             }
          ]
        }
    }
    itemListElement = []
    if featured_reviews is not None:
        for review in featured_reviews:
            itemListElement.append(review_schema(brand, review))
    for review in reviews:
        itemListElement.append(review_schema(brand, review))

    brand_details_dict['mainEntity']['itemListElement'] = itemListElement
    return brand_details_dict




