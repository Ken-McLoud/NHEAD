from django import template
from urllib.parse import urlencode, quote_plus

register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    """djangos built-in pagination assumes that the page number is the only GET param
    using this tag allows you to add additional get parameters to the "next", "prev", etc... buttons
    """
    query = context["request"].GET.copy()
    try:
        del query["page"]  # prevent url from including the list of previous pages
    except IndexError:
        pass
    query.update(kwargs)
    return query.urlencode()
