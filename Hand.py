import math
from collections import Counter

from Strength import STRENGTH


class Hand:
    def __init__(self, cards: list[int]):
        self.cards = cards
        self.sorted_cards = [card % 13 for card in self.cards]
        self.sorted_cards.sort(reverse=True)
        self.count = Counter(self.sorted_cards)
        self.three_most_common = self.count.most_common(3)
        self.suit_count = Counter([math.floor(card / 13) for card in self.cards])

    def _is_four_of_a_kind(self):
        return self.three_most_common[0][1] == 4

    def _is_full_house(self):
        return self.three_most_common[0][1] == 3 and self.three_most_common[1][1] >= 2

    def _is_flush(self) -> bool:
        return self.suit_count.most_common(1)[0][1] >= 5

    def _is_straight(self) -> bool:
        count = 1
        for i in range(1, 7):
            if self.sorted_cards[i - 1] - self.sorted_cards[i] > 1:
                count = 1
                if i >= 3:
                    return 12 in self.sorted_cards and self._contains_range(0, 3)
            elif self.sorted_cards[i - 1] - self.sorted_cards[i] == 1:
                count += 1
            if count == 5:
                return True
        return 12 in self.sorted_cards and self._contains_range(0, 3)

    def _is_trips(self):
        return self.three_most_common[0][1] == 3

    def _is_two_pair(self):
        return self.three_most_common[0][1] == 2 and self.three_most_common[1][1] == 2

    def _is_pair(self):
        return self.three_most_common[0][1] == 2

    def _is_straight_flush(self):
        flush_cards = [card % 13 for card in self.get_flush_cards()]
        flush_cards.sort()
        count = 1
        for i in range(1, len(flush_cards)):
            if flush_cards[i] - flush_cards[i - 1] > 1:
                count = 1
                if i >= 3:
                    return 12 in flush_cards and self._contains_range(0, 3, flush_cards)
            elif flush_cards[i] - flush_cards[i - 1] == 1:
                count += 1
            if count == 5:
                return True
        return 12 in flush_cards and self._contains_range(0, 3, flush_cards)

    def _contains_range(self, start: int, end: int, cards=None) -> bool:
        for i in range(start, end + 1):
            if i not in self.sorted_cards if not cards else cards:
                return False
        return True

    def straight_highest_card(self) -> int:
        cards = self.sorted_cards[::-1]
        for i in range(1, 7):
            if cards[i] - cards[i - 1] > 1 and i >= 3:
                return cards[i - 1]
        return cards[-1]

    def get_flush_cards(self):
        count = Counter([math.floor(card / 13) for card in self.cards])
        suit = count.most_common(1)[0][0]
        filtered_cards = list(filter(lambda card: math.floor(card / 13) == suit,
                                     self.cards))
        filtered_cards.sort(reverse=True)
        return filtered_cards[:5]

    def get_straight_flush_highest_card(self):
        suit = self.suit_count.most_common(1)[0][0]
        filtered_cards = list(filter(lambda card: math.floor(card / 13) == suit,
                                     self.cards))
        for i in range(len(filtered_cards)):
            filtered_cards[i] %= 13
        filtered_cards.sort()
        for i in range(1, len(filtered_cards)):
            if filtered_cards[i] - filtered_cards[i - 1] > 1 and i >= 3:
                return filtered_cards[i - 1]
        return filtered_cards[-1]

    def get_type(self):
        is_straight = self._is_straight()
        is_flush = self._is_flush()
        if is_straight and is_flush and self._is_straight_flush():
            if self.get_straight_flush_highest_card() == 12:
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
        elif self._is_two_pair():
            return STRENGTH.TWO_PAIR
        elif self._is_pair():
            return STRENGTH.PAIR
        else:
            return STRENGTH.HIGH_CARD
