import math
from collections import Counter

from Strength import STRENGTH


class Hand:
    def __init__(self, cards: list[int]):
        self.cards = cards
        self.sorted_cards = [card % 13 for card in self.cards]
        self.sorted_cards.sort(reverse=True)
        self.count = Counter([card % 13 for card in self.cards])

    def _is_four_of_a_kind(self):
        return self.count.most_common(1)[0][1] == 4

    def _is_full_house(self):
        two_most_common = self.count.most_common(2)
        return two_most_common[0][1] == 3 and two_most_common[1][1] == 2

    def _is_flush(self) -> bool:
        count = Counter([math.floor(card / 13) for card in self.cards])
        for _, value in count.items():
            if value >= 5:
                return True
        return False

    def _is_straight(self) -> bool:
        count = 1
        for i in range(1, 7):
            if self.sorted_cards[i - 1] - self.sorted_cards[i] > 1:
                count = 1
            elif self.sorted_cards[i - 1] - self.sorted_cards[i] == 1:
                count += 1
            if count == 5:
                return True
        return 12 in self.sorted_cards and self._contains_range(0, 3)

    def _is_trips(self):
        return self.count.most_common(1)[0][1] == 3

    def _is_pair(self):
        return self.count.most_common(1)[0][1] == 2

    def _contains_range(self, start: int, end: int) -> bool:
        for i in range(start, end + 1):
            if i not in self.sorted_cards:
                return False
        return True

    def straight_highest_card(self) -> int:
        cards = self.sorted_cards[::-1]
        for i in range(1, 7):
            if cards[i] - cards[i - 1] > 1 and i >= 3:
                return cards[i]
        return cards[-1]

    def get_flush_cards(self):
        count = Counter([math.floor(card / 13) for card in self.cards])

    def get_type(self):
        is_straight = self._is_straight()
        is_flush = self._is_flush()
        if is_straight and is_flush:
            if self._contains_range(8, 12):
                return STRENGTH.ROYAL_FLUSH
            else:
                return STRENGTH.STRAIGHT_FLUSH
        if self._is_four_of_a_kind():
            return STRENGTH.FOUR_OF_A_KIND
        elif self._is_full_house():
            return STRENGTH.FULL_HOUSE
        elif is_flush:
            return STRENGTH.FLUSH
        elif is_straight:
            return STRENGTH.STRAIGHT
        elif self._is_trips():
            return STRENGTH.TRIPS
        elif self._is_pair():
            return STRENGTH.PAIR
        else:
            return STRENGTH.HIGH_CARD


def _compare_singles(h1: Hand, h2: Hand, number: int, skip_list: list[int]) -> int:
    h1_filtered = list(filter(lambda card: card not in skip_list, h1.sorted_cards))
    h2_filtered = list(filter(lambda card: card not in skip_list, h2.sorted_cards))

    for i in range(number):
        if h1_filtered[i] > h2_filtered[i]:
            return 1
        elif h1.sorted_cards[i] < h2.sorted_cards[i]:
            return -1
    return 0


def _compare_multiples(h1: Hand, h2: Hand, number: int = 0) -> int | list[int]:
    value1 = h1.count.most_common(1)[number][0]
    value2 = h2.count.most_common(1)[number][0]
    if value1 > value2:
        return 1
    elif value1 < value2:
        return -1
    return [0, value1]


def _compare_kicker(h1: Hand, h2: Hand, hand_type: int) -> int:
    if hand_type == STRENGTH.HIGH_CARD:
        for i in range(5):
            if h1.sorted_cards[i] > h2.sorted_cards[i]:
                return 1
            elif h1.sorted_cards[i] < h2.sorted_cards[i]:
                return -1
        return 0
    elif hand_type == STRENGTH.PAIR:
        res = _compare_multiples(h1, h2)
        return res if type(res) is int else _compare_singles(h1, h2, 3, [res[1]])
    elif hand_type == STRENGTH.TRIPS:
        res = _compare_multiples(h1, h2)
        return res if type(res) is int else _compare_singles(h1, h2, 2, [res[1]])
    elif hand_type == STRENGTH.STRAIGHT:
        c1 = h1.straight_highest_card()
        c2 = h2.straight_highest_card()
        if c1 > c2:
            return 1
        elif c1 < c2:
            return -1
        else:
            return 0
    elif hand_type == STRENGTH.FLUSH:
        pass
    elif hand_type == STRENGTH.FOUR_OF_A_KIND:
        res = _compare_multiples(h1, h2)
        return res if type(res) is int else _compare_singles(h1, h2, 1, [res[1]])


def compare(c1: list[int], c2: list[int]) -> int:
    h1 = Hand(c1)
    h2 = Hand(c2)
    h1_type = h1.get_type()
    h2_type = h2.get_type()
    if h1_type > h2_type:
        return 1
    elif h2_type > h1_type:
        return -1
    elif h1_type == STRENGTH.ROYAL_FLUSH:
        return 0
    else:
        return _compare_kicker(h1, h2, h1_type)
