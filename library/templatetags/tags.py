from django import template
register = template.Library()

@register.filter
def keyvalue(Dict, i):
    try:
        Dict[str(i)]
    except Exception as e:
        try:
            Dict.update({str(i): ''})
        except Exception as e:
            Dict = {str(i): ''}
    return Dict[str(i)]

@register.filter
def notstars(stars):
    res = []
    for i in range(0, 5 - len(stars)):
        res.append(i)
    return res