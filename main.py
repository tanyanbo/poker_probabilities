from itertools import combinations
from Hand import Hand, compare

str_to_val = {'2d': 0, '2c': 13, '2h': 26, '2s': 39, '3d': 1, '3c': 14, '3h': 27,
              '3s': 40, '4d': 2,
              '4c': 15, '4h': 28, '4s': 41, '5d': 3, '5c': 16, '5h': 29, '5s': 42,
              '6d': 4, '6c': 17,
              '6h': 30, '6s': 43, '7d': 5, '7c': 18, '7h': 31, '7s': 44, '8d': 6,
              '8c': 19, '8h': 32,
              '8s': 45, '9d': 7, '9c': 20, '9h': 33, '9s': 46, '10d': 8, '10c': 21,
              '10h': 34,
              '10s': 47, 'Jd': 9, 'Jc': 22, 'Jh': 35, 'Js': 48, 'Qd': 10, 'Qc': 23,
              'Qh': 36, 'Qs': 49,
              'Kd': 11, 'Kc': 24, 'Kh': 37, 'Ks': 50, 'Ad': 12, 'Ac': 25, 'Ah': 38,
              'As': 51}

val_to_str = {0: '2d', 13: '2c', 26: '2h', 39: '2s', 1: '3d', 14: '3c', 27: '3h',
              40: '3s', 2: '4d', 15: '4c', 28: '4h', 41: '4s', 3: '5d', 16: '5c',
              29: '5h', 42: '5s', 4: '6d', 17: '6c', 30: '6h', 43: '6s', 5: '7d',
              18: '7c', 31: '7h', 44: '7s', 6: '8d', 19: '8c', 32: '8h', 45: '8s',
              7: '9d', 20: '9c', 33: '9h', 46: '9s', 8: '10d', 21: '10c', 34: '10h',
              47: '10s', 9: 'Jd', 22: 'Jc', 35: 'Jh', 48: 'Js', 10: 'Qd', 23: 'Qc',
              36: 'Qh', 49: 'Qs', 11: 'Kd', 24: 'Kc', 37: 'Kh', 50: 'Ks', 12: 'Ad',
              25: 'Ac', 38: 'Ah', 51: 'As'}

h1 = [6, 35]
h2 = [38, 51]
filtered = list(filter(lambda x: x not in h1 and x not in h2, range(52)))


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

# print(f'Probability: {get_probability()}')
