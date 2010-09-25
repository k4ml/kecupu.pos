from django import template

register = template.Library()

def mult(value, arg):
    "Multiply the value and argument"

    return int(value) * int(arg)

register.filter(mult)
