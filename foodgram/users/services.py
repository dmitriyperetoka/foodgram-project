from django.db.models import Sum


class PurchaseListFileContentMaker:
    """Make content of purchase list file."""

    def __init__(self):
        self.ingredient = {
            'orm': 'recipe__ingredients__title',
            'verbose': 'Ингредиент',
        }
        self.quantity = {
            'orm': 'recipe__ingredientinrecipe__quantity',
            'verbose': 'Количество',
        }
        self.unit = {
            'orm': 'recipe__ingredients__dimension',
            'verbose': 'Единица',
        }
        self.queryset = None

    def _get_queryset(self, user):
        return user.purchases.select_related('recipe').values(
            self.ingredient['orm'], self.unit['orm']).annotate(
            **{self.quantity['orm']: Sum(self.quantity['orm'])})

    def _get_column_width(self, column):
        return max(
            max(len(str(q[column['orm']])) for q in self.queryset),
            len(column['verbose'])
        )

    def make(self, user):
        self.queryset = self._get_queryset(user)

        if not self.queryset:
            return 'Данный список пуст.'

        ing_width = self._get_column_width(self.ingredient)
        qty_width = self._get_column_width(self.quantity)
        unit_width = self._get_column_width(self.unit)
        total_width = (ing_width + 3) + (qty_width + 3) + (unit_width + 3) + 1

        table_title = 'Список покупок:'
        horiz_div = '-' * total_width
        table_header = (
            f'| {self.ingredient["verbose"]:<{ing_width}} '
            f'| {self.quantity["verbose"]:<{qty_width}} '
            f'| {self.unit["verbose"]:<{unit_width}} |'
        )
        table_footer = 'Сформировано с помощью Foodgram\n'

        lines = [table_title, horiz_div, table_header, horiz_div]
        for q in self.queryset:
            line = (
                f'| {q[self.ingredient["orm"]].capitalize():<{ing_width}} '
                f'| {q[self.quantity["orm"]]:>{qty_width}} '
                f'| {q[self.unit["orm"]]:<{unit_width}} |'
            )
            lines.append(line)
        lines.extend([horiz_div, table_footer])

        return '\n'.join(str(q) for q in lines)
