from itertools import combinations
from Hand import Hand
from translate import str_to_val
from compare import compare
from random import sample

p1 = ['7d', 'jc']
p2 = ['9s', '8d']


def translate():
    v1 = [str_to_val[p1[0].lower()], str_to_val[p1[1].lower()]]
    v2 = [str_to_val[p2[0].lower()], str_to_val[p2[1].lower()]]
    filtered_cards = list(filter(lambda x: x not in v1 and x not in v2, range(52)))
    return v1, v2, filtered_cards


def get_probability(should_sample: bool = True, sample_size: int = 10000):
    h1, h2, filtered = translate()
    hand1_count = 0
    hand2_count = 0
    tie_count = 0
    all_combinations = list(combinations(filtered, 5))

    if should_sample:
        all_combinations = sample(all_combinations, sample_size)

    for community_cards in all_combinations:
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
    return {'p1': f'{round(100 * hand1_count / total, 2)}%',
            'p2': f'{round(100 * hand2_count / total, 2)}%',
            'tie': f'{round(100 * tie_count / total, 2)}%'}


if __name__ == '__main__':
    res_dict = f'Probability: {get_probability()}'
    print(res_dict)
