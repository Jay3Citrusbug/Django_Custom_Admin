from frontend.shortcodes import parser
from django import template
from math import floor, ceil
import pandas as pd

register = template.Library()


def shortcodes_replace(value, request=None):
    """
    A filter for parsing a string on the format ``[shortcode keyword=value]``
    using the shortcodes parser method.
    """
    return parser.parse(value, request)


@register.simple_tag
def url_replace(request, field, value):

    dict_ = request.GET.copy()
    if 'page' in dict_:
        del dict_['page']

    dict_[field] = value

    return dict_.urlencode()


def float_to_value(x):
    if x > 10**6-1:
        return str(x/10**6) + 'M'
    elif x > 10**3-1:
        return str(x/10**3) + 'K'
    else:
        return str(x)


def category_name_clean(name):
    name = name.replace('-', ' ')
    return name.upper()


def search_tags_name(name):
    name = name.replace('_', ' ')
    return name.title()


def pound_to_kg(weight):
    weight_float = float(weight)
    return "{:.2f}".format(weight_float * .454)


def table_to_list(html_table):
    dfs = pd.read_html(html_table)
    df = dfs[0]
    final_list = {}
    for key, value in zip(df[0], df[1]):
        final_list[key] = value
    return final_list


def more_details_for_compare(reviews):
    data_list = {}
    if reviews:
        for review in reviews:
            table = table_to_list(review.more_details)
            for key, value in table.items():
                if key in data_list:
                    data = data_list[key]
                    data.append(value)
                    data_list[key] = data
                else:
                    data_list[key] = [value]
        return data_list
    return ''


def more_details_dict(dict_list):
    return dict_list.items()


def key_from_more_details_dict(dict, key):
    return dict[key]


register.filter('shortcodes', shortcodes_replace)
register.filter('float_to_value', float_to_value)
register.filter('category_name_clean', category_name_clean)
register.filter('search_tags_name', search_tags_name)
register.filter('pound_to_kg', pound_to_kg)

register.filter('table_to_list', table_to_list)
register.filter('more_details_for_compare', more_details_for_compare)
register.filter('more_details_dict', more_details_dict)
register.filter('key_from_more_details_dict', key_from_more_details_dict)
