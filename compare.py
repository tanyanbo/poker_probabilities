from Hand import Hand
from Strength import STRENGTH


def _compare_singles(h1: Hand, h2: Hand, number: int, skip_list: list[int]) -> int:
    h1_filtered = list(filter(lambda card: card not in skip_list, h1.sorted_cards))
    h2_filtered = list(filter(lambda card: card not in skip_list, h2.sorted_cards))

    for i in range(number):
        if h1_filtered[i] > h2_filtered[i]:
            return 1
        elif h1_filtered[i] < h2_filtered[i]:
            return -1
    return 0


def _compare_multiples(h1: Hand, h2: Hand, number: int = 0) -> int | list[int]:
    value1 = h1.three_most_common[number][0]
    value2 = h2.three_most_common[number][0]
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
    elif hand_type == STRENGTH.TWO_PAIR:
        t1 = [pair[0] for pair in h1.three_most_common if pair[1] == 2]
        t2 = [pair[0] for pair in h2.three_most_common if pair[1] == 2]
        t1.sort(reverse=True)
        t2.sort(reverse=True)
        for i in range(2):
            if t1[i] > t2[i]:
                return 1
            elif t1[i] < t2[i]:
                return -1
        remaining1 = [card for card in h1.sorted_cards if card not in t1[:2]]
        remaining2 = [card for card in h2.sorted_cards if card not in t2[:2]]
        if remaining1[0] > remaining2[0]:
            return 1
        elif remaining1[0] < remaining2[0]:
            return -1
        else:
            return 0
    elif hand_type == STRENGTH.TRIPS:
        res = _compare_multiples(h1, h2)
        return res if type(res) is int else _compare_singles(h1, h2, 2, [res[1]])
    elif hand_type == STRENGTH.STRAIGHT:
        c1 = h1.straight_highest_card()
        c2 = h2.straight_highest_card()
        return 0 if c1 == c2 else (1 if c1 > c2 else -1)
    elif hand_type == STRENGTH.FLUSH:
        cards1 = h1.get_flush_cards()
        cards2 = h2.get_flush_cards()
        for i in range(5):
            if cards1[i] > cards2[i]:
                return 1
            elif cards1[i] < cards2[i]:
                return -1
        return 0
    elif hand_type == STRENGTH.FULL_HOUSE:
        t1 = [pair[0] for pair in h1.three_most_common if pair[1] == 3]
        t2 = [pair[0] for pair in h2.three_most_common if pair[1] == 3]
        t1.sort(reverse=True)
        t2.sort(reverse=True)
        if t1[0] > t2[0]:
            return 1
        elif t1[0] < t2[0]:
            return -1
        else:
            remaining1 = [pair[0] for pair in h1.three_most_common if
                          pair[1] >= 2 and pair[0] != t1[0]]
            remaining2 = [pair[0] for pair in h2.three_most_common if
                          pair[1] >= 2 and pair[0] != t2[0]]
            remaining1.sort(reverse=True)
            remaining2.sort(reverse=True)
            if remaining1[0] > remaining2[0]:
                return 1
            elif remaining1[0] < remaining2[0]:
                return -1
            else:
                return 0
    elif hand_type == STRENGTH.FOUR_OF_A_KIND:
        res = _compare_multiples(h1, h2)
        return res if type(res) is int else _compare_singles(h1, h2, 1, [res[1]])
    elif hand_type == STRENGTH.STRAIGHT_FLUSH:
        c1 = h1.get_straight_flush_highest_card()
        c2 = h2.get_straight_flush_highest_card()
        return 0 if c1 == c2 else (1 if c1 > c2 else -1)


def compare(h1: Hand, h2: Hand) -> int:
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
