# myapp/templatetags/league_filters.py
from django import template

register = template.Library()

@register.filter(name='format_league')
def format_league(value):
    """
    Tire ile ayrılmış bir lig adını, her kelimenin ilk harfini büyük yaparak
    aralarına boşluk koyarak biçimlendirir.
    Örnek: "england-premier-league" => "England Premier League"
    """
    if not isinstance(value, str):
        return value
    words = value.split('-')
    return " ".join(word.capitalize() for word in words)



