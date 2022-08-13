from itertools import combinations
from Hand import Hand, compare

str_to_val = {'2d': 0, '2c': 13, '2h': 26, '2s': 39, '3d': 1, '3c': 14, '3h': 27,
              '3s': 40, '4d': 2,
              '4c': 15, '4h': 28, '4s': 41, '5d': 3, '5c': 16, '5h': 29, '5s': 42,
              '6d': 4, '6c': 17,
              '6h': 30, '6s': 43, '7d': 5, '7c': 18, '7h': 31, '7s': 44, '8d': 6,
              '8c': 19, '8h': 32,
              '8s': 45, '9d': 7, '9c': 20, '9h': 33, '9s': 46, 'td': 8, 'tc': 21,
              'th': 34,
              'ts': 47, 'jd': 9, 'jc': 22, 'jh': 35, 'js': 48, 'qd': 10, 'qc': 23,
              'qh': 36, 'qs': 49,
              'kd': 11, 'kc': 24, 'kh': 37, 'ks': 50, 'ad': 12, 'ac': 25, 'ah': 38,
              'as': 51}

val_to_str = {0: '2d', 13: '2c', 26: '2h', 39: '2s', 1: '3d', 14: '3c', 27: '3h',
              40: '3s', 2: '4d', 15: '4c', 28: '4h', 41: '4s', 3: '5d', 16: '5c',
              29: '5h', 42: '5s', 4: '6d', 17: '6c', 30: '6h', 43: '6s', 5: '7d',
              18: '7c', 31: '7h', 44: '7s', 6: '8d', 19: '8c', 32: '8h', 45: '8s',
              7: '9d', 20: '9c', 33: '9h', 46: '9s', 8: 'td', 21: 'tc', 34: 'th',
              47: 'ts', 9: 'jd', 22: 'jc', 35: 'jh', 48: 'js', 10: 'qd', 23: 'qc',
              36: 'qh', 49: 'qs', 11: 'kd', 24: 'kc', 37: 'kh', 50: 'ks', 12: 'ad',
              25: 'ac', 38: 'ah', 51: 'as'}

p1 = ['ts', 'th']
p2 = ['qs', '6h']


def translate():
    v1 = [str_to_val[p1[0].lower()], str_to_val[p1[1].lower()]]
    v2 = [str_to_val[p2[0].lower()], str_to_val[p2[1].lower()]]
    filtered_cards = list(filter(lambda x: x not in v1 and x not in v2, range(52)))
    return v1, v2, filtered_cards


h1, h2, filtered = translate()


def get_probability():
    hand1_count = 0
    hand2_count = 0
    tie_count = 0
    for community_cards in combinations(filtered, 5):
        hand1 = Hand(list(community_cards) + h1)
        hand2 = Hand(list(community_cards) + h2)
        res = compare(hand1, hand2)
        if res == 1:
            hand1_count += 1
        elif res == -1:
            hand2_count += 1
        else:
            tie_count += 1
        # if hand2_count % 10000 == 0:
        #     print(hand2_count + hand1_count + tie_count)

    total = hand1_count + hand2_count + tie_count
    return {'p1': hand1_count / total, 'p2': hand2_count / total,
            'tie': tie_count / total}


def compare_two_hands(cards1, cards2, community):
    translated_p1 = [str_to_val[card.lower()] for card in cards1]
    translated_p2 = [str_to_val[card.lower()] for card in cards2]
    translated_community = [str_to_val[card.lower()] for card in community]

    hand1 = Hand(list(translated_community) + translated_p1)
    hand2 = Hand(list(translated_community) + translated_p2)
    return compare(hand1, hand2)


print(compare_two_hands(['ks', '7s'], ['ts', '7h'], ['kh', '7d', 'as', 'ad', 'tc']))

# print(f'Probability: {get_probability()}')
