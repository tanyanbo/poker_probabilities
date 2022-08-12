from itertools import combinations
from Hand import Hand, compare

values = {2: [0, 13, 26, 39], 3: [1, 14, 27, 40], 4: [2, 15, 28, 41], 5: [3, 16, 29, 42],
          6: [4, 17, 30, 43], 7: [5, 18, 31, 44], 8: [6, 19, 32, 45], 9: [7, 20, 33, 46],
          10: [8, 21, 34, 47], 11: [9, 22, 35, 48], 12: [10, 23, 36, 49],
          13: [11, 24, 37, 50], 1: [12, 25, 38, 51]}

suit = ['d', 'c', 'h', 's']

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


print(f'Probability: {get_probability()}')
