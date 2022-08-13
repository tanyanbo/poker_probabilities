from itertools import combinations
from Hand import Hand
from translate import str_to_val
from compare import compare

p1 = ['ts', 'th']
p2 = ['qs', '6h']


def translate():
    v1 = [str_to_val[p1[0].lower()], str_to_val[p1[1].lower()]]
    v2 = [str_to_val[p2[0].lower()], str_to_val[p2[1].lower()]]
    filtered_cards = list(filter(lambda x: x not in v1 and x not in v2, range(52)))
    return v1, v2, filtered_cards


def get_probability():
    h1, h2, filtered = translate()
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

    total = hand1_count + hand2_count + tie_count
    return {'p1': hand1_count / total, 'p2': hand2_count / total,
            'tie': tie_count / total}


if __name__ == '__main__':
    res_dict = f'Probability: {get_probability()}'
    print(res_dict)
