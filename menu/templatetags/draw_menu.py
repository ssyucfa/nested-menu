from django import template
from django.db.models import QuerySet, OuterRef, Subquery

from menu.models import Item


register = template.Library()


@register.inclusion_tag("menu/nested_menu.html", takes_context=True)
def draw_menu(context, menu):
    items = Item.objects.filter(menu__title=menu).select_related("parent")

    selected_item_id = context["request"].GET.get(menu)
    if selected_item_id is None:
        return {"items": items.filter(parent=None).values(), "menu": menu}

    return {"items": _get_items_with_children(items, int(selected_item_id)), "menu": menu}


def _get_items_with_children(items: QuerySet[Item], selected_item_id: int) -> list[dict]:
    items_values = items.values()
    selected_items = _get_selected_items(selected_item_id, items_values)

    items_with_children = [item for item in items_values if item["parent_id"] is None]

    for item in items_with_children:
        if item["id"] in selected_items:
            item["children"] = _get_children(items_values, item["id"], selected_items)

    return items_with_children


def _get_children(items_values, parent_id, selected_items):
    children = [item for item in items_values if item["parent_id"] == parent_id]

    for item in children:
        if item["id"] in selected_items:
            item["children"] = _get_children(items_values, item["id"], selected_items)

    return children


def _get_selected_items(parent_id: int, items_values: dict):
    selected_items = []

    while parent_id is not None:
        selected_items.append(parent_id)
        parent_id = [item["parent_id"] for item in items_values if item["id"] == parent_id][0]

    return selected_items
