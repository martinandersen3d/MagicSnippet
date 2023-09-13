# This algo will make shure the letters is comming in same order, left to right
def algo_char_in_correct_order(a: str, b: str):
    first_algo_boolean = False
    a_len = len(a)
    
    counter = 0
    # c = character
    for c in a:
        index = b.find(c, counter)
        if index != -1:
            counter = index+1
            first_algo_boolean = True
        else:
            first_algo_boolean = False
            break

    return first_algo_boolean

# Pairwise comparison and counting
# superman
# ['su', 'up', 'pe', 'er', 'rm', 'ma', 'an']

def algo_count_pairwise_letter_match( a: str, b: str):
    score=0
    word = a
    pairs = []
    for i in range(len(word) - 1):
        pair = word[i:i+2]
        pairs.append(pair)
    for w in pairs:
      if w in b:
         score = score + 10
         
    return score

def algo_fullword_match( a: str, b: str):
    score=0
    if a in b:
        score = score +100
         
    return score
    
# Text search algo
def search_algo( a: str, b: str):
    
    total_score = 0
    
    char_in_correct_order = False
    count_pairwise_letter_match = False
    fullword_match = False

    # First algo: Check that the letters is comming in the right order -----------------
    if algo_char_in_correct_order(a,b):
        total_score = total_score + 10
        char_in_correct_order = True
    
    # Second algo: Check that at least two letters is side-by-side in the string -----------------
    pair_wise_score = algo_count_pairwise_letter_match(a, b)
    if pair_wise_score > 0:
        total_score = total_score + pair_wise_score
        count_pairwise_letter_match = True
    
    # Third: FullWord Match ----------------------------
    fullword_score = algo_fullword_match(a, b)
    if fullword_score > 0:
        total_score = total_score + fullword_score
        fullword_match = True
    
    a_length=len(a)
    if a_length > 0 and char_in_correct_order:
        if a_length == 1:
           return total_score
        if a_length == 2  and pair_wise_score == 10:
           return total_score
        if a_length == 3 and pair_wise_score >= 10:
           return total_score
        if a_length == 4 and pair_wise_score >= 20:
           return total_score
        if a_length == 5 and pair_wise_score > 20:
           return total_score
        if a_length == 6 and pair_wise_score >= 30:
           return total_score
        if a_length > 6 and pair_wise_score > 30:
           return total_score
       
    return 0
