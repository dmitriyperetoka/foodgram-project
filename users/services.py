from django.db.models import Sum


def make_file_content(user):
    ing = ('recipe__ingredients__title', 'Ингредиент')
    qty = ('recipe__ingredientinrecipe__quantity', 'Количество')
    unit = ('recipe__ingredients__dimension_unit', 'Единица')

    items = user.purchases.select_related(
        'recipe').values(ing[0], unit[0]).annotate(**{qty[0]: Sum(qty[0])})

    if not items:
        return 'Данный список пуст.'

    ing_wid = max(max(len(q[ing[0]]) for q in items), len(ing[1]))
    qty_wid = max(max(len(str(q[qty[0]])) for q in items), len(qty[1]))
    unit_wid = max(max(len(q[unit[0]]) for q in items), len(unit[1]))
    total_wid = (ing_wid + 3) + (qty_wid + 3) + (unit_wid + 3) + 1
    horiz_div = '-' * total_wid

    table_title = 'Список покупок:'
    table_header = (
        f'| {ing[1]:<{ing_wid}} '
        f'| {qty[1]:<{qty_wid}} '
        f'| {unit[1]:<{unit_wid}} |'
    )
    table_footer = 'Сформировано с помощью Foodgram\n'

    lines = [table_title, horiz_div, table_header, horiz_div]
    for q in items:
        line = (
            f'| {q[ing[0]].capitalize():<{ing_wid}} '
            f'| {q[qty[0]]:>{qty_wid}} '
            f'| {q[unit[0]]:<{unit_wid}} |'
        )
        lines.append(line)
    lines.extend([horiz_div, table_footer])

    return '\n'.join(str(q) for q in lines)
