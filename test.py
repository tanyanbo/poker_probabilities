from translate import str_to_val
from Hand import Hand
from compare import compare


def compare_two_hands(cards1, cards2, community):
    translated_p1 = [str_to_val[card.lower()] for card in cards1]
    translated_p2 = [str_to_val[card.lower()] for card in cards2]
    translated_community = [str_to_val[card.lower()] for card in community]

    hand1 = Hand(list(translated_community) + translated_p1)
    hand2 = Hand(list(translated_community) + translated_p2)
    return compare(hand1, hand2)


res = compare_two_hands(['ks', '7s'], ['ts', '7h'], ['kh', '7d', 'as', 'ad', 'tc'])
print(res)
