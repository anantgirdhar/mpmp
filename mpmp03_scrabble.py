import numpy as np
import itertools as it
import pprint

TILES = {
        '': 2,
        'A': 9, 'E': 12, 'I': 9, 'O': 8, 'U': 4, 'L': 4, 'N': 6, 'S': 4, 'T': 6, 'R': 6,
        'D': 4, 'G': 3,
        'B': 2, 'C': 2, 'M': 2, 'P': 2,
        'F': 2, 'H': 2, 'V': 2, 'W': 2, 'Y': 2,
        'K': 1,
        'J': 1, 'X': 1,
        'Q': 1, 'Z': 1,
        }
POINTS = {
        '': 0,
        'A': 1, 'E': 1, 'I': 1, 'O': 1, 'U': 1, 'L': 1, 'N': 1, 'S': 1, 'T': 1, 'R': 1,
        'D': 2, 'G': 2,
        'B': 3, 'C': 3, 'M': 3, 'P': 3,
        'F': 4, 'H': 4, 'V': 4, 'W': 4, 'Y': 4,
        'K': 5,
        'J': 8, 'X': 8,
        'Q': 10, 'Z': 10,
        }
# Create an inverse points map
# Here, each point value corresponds to a list of letters
INV_POINTS = {}
for k, v in POINTS.items():
    if v not in INV_POINTS.keys():
        INV_POINTS[v] = []
    INV_POINTS[v].append(k)

#NUM_TILES_STEP1 = {
#        '': 2,
#        '1': 7,
#        '2': 7,
#        '3': 7,
#        '4': 7,
#        '5': 1,
#        '8': 2,
#        '10': 2,
#        }
#
#POINTS_STEP1 = {
#        '': 0,
#        '1': 1,
#        '2': 2,
#        '3': 3,
#        '4': 4,
#        '5': 5,
#        '8': 8,
#        '10': 10,
#        }

def is_hand_valid(hand, required_total_score, required_num_tiles, POINTS_DICT, NUM_TILES_DICT):
    # Check total number of tiles
    if len(hand) != required_num_tiles:
        return False
    # Check total score
    total_score = sum([POINTS_DICT[tile] for tile in hand])
    if total_score != required_total_score:
        return False
    # Check number of tiles per letter
    for letter in hand:
        if hand.count(letter) > NUM_TILES_DICT[letter]:
            return False
    # If all checks pass
    return True

def brute_force_step_1(total_score, num_tiles):
    # First reduce the problem space by generating new TILES and POINTS dicts
    # that don't have as many tiles. First, create a new tiles dict that has a
    # count of the number of tiles in every point category. This count may be
    # more than num_tiles which is the maximum number of tiles allowed per hand.
    # So we can cap the value of this count to further reduce the search space.
    NUM_TILES_STEP1 = {}
    POINTS_STEP1 = {}
    for letter, count in TILES.items():
        point_value = str(POINTS[letter])
        if point_value not in NUM_TILES_STEP1.keys():
            NUM_TILES_STEP1[point_value] = 0
            POINTS_STEP1[point_value] = int(point_value)
        NUM_TILES_STEP1[point_value] += count
        if NUM_TILES_STEP1[point_value] > num_tiles:
            NUM_TILES_STEP1[point_value] = num_tiles
    # Use these dicts to generate a list of valid hands first
    valid_hands = []
    hands_checked = []
    all_tiles = []
    for k, v in NUM_TILES_STEP1.items():
        for i in range(v):
            all_tiles.append(k)
    print('Total num tiles: ', len(all_tiles))
    possible_hands = it.combinations(all_tiles, num_tiles)
    input('Press enter to continue...')
    for hand in possible_hands:
        if hand in hands_checked:
            continue
        else:
            hands_checked.append(hand)
        print(hand)
        if is_hand_valid(hand, total_score, num_tiles, POINTS_STEP1, NUM_TILES_STEP1):
            print('  VALID')
            valid_hands.append(hand)
    return valid_hands, hands_checked

def brute_force_step_2(prelim_hands):
    overall_combinations = []
    for hand in prelim_hands:
        individual_combinations = []
        # Go through the hand
        # For each point value, generate all possible combinations for that point value
        # Take the cross product of the resulting lists
        #hand.sort()  -> if needed
        for i, point_value in enumerate(hand):
            if point_value == hand[i-1]:
                # This point value has already been considered
                continue
            point_value_count = hand.count(point_value)
            point_value = int(point_value)
            #possible_letters = INV_POINTS[point_value]
            # Create a list of possible letters taking into account their frequency
            possible_letters = []
            for letter in INV_POINTS[point_value]:
                possible_letters.extend([letter, ] * TILES[letter])
            possible_combinations = it.combinations(possible_letters, point_value_count)
            # Get only the unique combinations
            possible_combinations = list(set(possible_combinations))
            # Add this to the list of combinations
            individual_combinations.append(possible_combinations)
        # Take the cross product of the resulting combination lists
        overall_hand_combinations = it.product(*individual_combinations)
        # Get only the unique combinations
        overall_hand_combinations = list(set(overall_hand_combinations))
        #print('For hand ', hand, ' # combinations = ', len(overall_hand_combinations))
        #pprint.pprint(overall_hand_combinations)
        overall_combinations.extend(overall_hand_combinations)
    return overall_combinations


def brute_force_find_hands(total_score, num_tiles):
    # Step 1: Reduce the problem space to find what tile point values are
    # needed to get valid hands.
    valid_hands, checked_hands = brute_force_step_1(total_score, num_tiles)
    # Step 2: Find how many ways these hands can be made using the given the
    # actual tiles, taking into account their frequencies.
    overall_combinations = brute_force_step_2(valid_hands)
    return overall_combinations

