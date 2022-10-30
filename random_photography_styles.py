#!/usr/bin/env python3
import random
from typing import Optional, Union, List

import funcy
from pythonic_toolbox.utils.dict_utils import collect_leaves
from pythonic_toolbox.utils.list_utils import sort_with_custom_orders


class Item:
    def __init__(self, name: str, weight: float = 1, exclusive_items: List[Union[str, 'Item']] = None):
        self.name = name
        self.weight = weight
        if exclusive_items is None:
            exclusive_items = []
        exclusive_items = [Item(item) if isinstance(item, str) else item for item in exclusive_items]
        self.exclusive_items = exclusive_items

    @staticmethod
    def choices(items: List['Item']) -> Optional['Item']:
        return funcy.first(random.choices(items, weights=[_item.weight for _item in items], k=1))

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

    def __bool__(self):
        return bool(self.name)

    def __eq__(self, other):
        if isinstance(other, Item):
            return self.name == other.name
        return False

    def __hash__(self):
        return hash(self.name)

    @staticmethod
    def handle_item_exclusion(items):
        final_items = items[:]
        dislike_pairs = []
        dislike_envolved_items_set = set()
        for _item in items:
            if not _item.exclusive_items:
                continue
            exclusive_items = _item.exclusive_items
            for exclusive_item in exclusive_items:
                try:
                    _exclusive_item = items[items.index(exclusive_item)]
                except ValueError:
                    pass
                else:
                    dislike_envolved_items_set.add(_item)
                    dislike_envolved_items_set.add(_exclusive_item)
                    dislike_pairs.append((_item, _exclusive_item))
        if not dislike_envolved_items_set:
            return final_items

        rest_items_set = set(items).difference(dislike_envolved_items_set)

        dislike_items_split_groups = split_to_groups(dislike_pairs)
        final_items_set = rest_items_set.union(set(random.choice(dislike_items_split_groups)))
        final_items = sort_with_custom_orders(list(final_items_set), items)
        return final_items


day_times = [Item('白天', 8),
             Item('黄昏', 1),
             Item('夜晚', 0.5)]

weathers = [
    Item('晴', 5),
    Item('多云', 1),
    Item('下雨', 0.5),
    Item('下雪', 0.2),
    Item('龙卷风', 0.05),
]

locations = {
    "室内": [
        Item("居家", 0.5),
        Item("展馆", 0.5, exclusive_items=["白天", "黄昏", "夜晚", "晴", "多云", "下雨", "下雪"]),
        Item("影棚", 0.5, exclusive_items=["白天", "黄昏", "夜晚", "晴", "多云", "下雨", "下雪"]),
    ],
    "室外": [
        Item("商业街", 1),
        Item("森林", 1),
        Item("田野", 0.5),
    ],
}
filter_styles = [
    Item("", 5),
    Item("甜美", 4),
    Item("酷", 4),
    Item("复古", 4),
    Item("小清新", 4),
    Item("胶片", 3),
    Item("黑白", 2),
    Item("暗黑", 1),
    Item("纯欲", 1),
    Item("御姐", 1),
    Item("油画", 1),
]

countries = [
    Item(""),
    Item("日系"),
    Item("韩式"),
    Item("法式"),
]

clothes = [
    Item("时尚"),
    Item("学院风"),
    Item("运动服", exclusive_items=["油画", "法式"]),
    Item("婚纱"),
    Item("精灵"),
    Item("女仆"),
    Item("汉服", exclusive_items=["日系", "韩式", "法式", "小清新", "胶片", "商业街"]),
    Item("JK", exclusive_items=["韩式", "法式"]),
    Item("和服", exclusive_items=["韩式", "法式", "胶片"]),
    Item("旗袍", exclusive_items=["日系", "韩式", "法式", "小清新"]),
    Item("西域", exclusive_items=["日系", "韩式", "法式"]),
    Item("圣诞装", exclusive_items=["日系", "韩式", "法式"]),
    Item("新年装", exclusive_items=["日系", "韩式", "法式", "胶片"]),
    Item("Cosplay", exclusive_items=["胶片", "日系", "韩式", "法式", "复古"]),
]

dimensions = [day_times, weathers, locations, countries, filter_styles, clothes]


class Graph:
    def __init__(self, edges, n):
        self.adj_lst = [[] for _ in range(n)]

        for (src, dest) in edges:
            self.adj_lst[src].append(dest)
            self.adj_lst[dest].append(src)


def color_graph(graph, n):
    result = {}

    for u in range(n):
        assigned = set([result.get(i) for i in graph.adj_lst[u] if i in result])
        color = 1
        for c in assigned:
            if color != c:
                break
            color = color + 1
        result[u] = color

    return result


def split_to_groups(dislike_pairs):
    total_set = set()
    for i, j in dislike_pairs:
        total_set.add(i)
        total_set.add(j)

    normalized_idx_map = {}
    for idx, value in enumerate(total_set):
        normalized_idx_map[value] = idx

    lookup_map = {v: k for k, v in normalized_idx_map.items()}

    edges = [(normalized_idx_map[i], normalized_idx_map[j]) for (i, j) in dislike_pairs]
    graph = Graph(edges, len(total_set))
    idx_color_map = color_graph(graph, len(total_set))
    color_nodes_map = {}
    for idx, color in idx_color_map.items():
        color_nodes_map[color] = color_nodes_map.get(color, []) + [idx]

    group_list = sorted(list(color_nodes_map.values()), key=lambda x: len(x), reverse=True)

    # get real groups by lookup_map
    group_list = [[lookup_map[x] for x in group] for group in group_list]
    return group_list


def photography_styles_generator(given_key_words=None, k=10):
    global dimensions
    given_key_words = given_key_words or []

    def _entry():
        items = []
        for dimension in dimensions:
            dimension_items = funcy.lflatten(collect_leaves(dimension))
            for given_key_word_item in [Item(key_word) for key_word in given_key_words]:
                try:
                    item = dimension_items[dimension_items.index(given_key_word_item)]
                    break
                except ValueError:
                    pass
            else:
                item = Item.choices(dimension_items)
            if item:
                items.append(item)

        if any(map(lambda __: __.exclusive_items, items)):
            items = Item.handle_item_exclusion(items)

        items = funcy.lkeep(items)
        result = '-'.join(map(str, items))

        return result

    results = set()
    for i in range(int(k * 1.2)):
        results.add(_entry())

    results = sorted(list(results), key=len, reverse=True)[0: k]

    for res in results:
        yield res


if __name__ == '__main__':
    for res in photography_styles_generator(k=5):
        print(res)

