from django import template

register = template.Library()

@register.filter
def slice_0_before_program(description):
    program_start = description.find("Программа тура включает:")
    return description[:program_start].strip() if program_start != -1 else description

@register.filter
def program_list(description):
    program_start = description.find("Программа тура включает:")
    if program_start == -1:
        return []

    program_text = description[program_start + len("Программа тура включает:"):].strip()
    items = program_text.split(" - ")
    return [item.strip() for item in items if item]
