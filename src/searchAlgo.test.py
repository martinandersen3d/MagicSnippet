import unittest

# This algorithm will compare two sentences.
# It will check that:
# 1. the individual letters is in the same order
# 2. But the letters do not have to be sequental order

# Example of a match:
# we will match the string "HelloDay" with:
# "/HelloWorld/ItAGoodDay"
# Here we have a match, since all letters is in the same order, but not in the same sequential order, or not at the same index.


# a is the word we want to check for
# b is the complete line
# Note this algo is case-sensitive, so convert to lower case before use
def search_algo(a: str, b: str):
    a_len = len(a)
    allow_spellmistake = False
    
    if a_len >= 3:
        allow_spellmistake = True
    
    counter = 0
    spellmistakes = 0
    # c = character
    for c in a:
        index = b.find(c, counter)
        if index != -1:
            counter = index+1
        elif allow_spellmistake and spellmistakes == 0:
            spellmistakes = 1    
        else:
            return False
    return True
        
class TestAddFunction(unittest.TestCase):
    
    def test_is_match(self):
        result = search_algo("HelloDay", "/HelloWorld/ItAGoodDay")
        self.assertEqual(result, True)
    
    def test_wrong_order(self):
        result = search_algo("DayHello", "/HelloWorld/ItAGoodDay")
        self.assertEqual(result, False)
    
    def test_match_with_one_spell_mistake(self):
        result = search_algo("HellxDay", "/HelloWorld/ItAGoodDay")
        self.assertEqual(result, True)
    
    def test_match_with_one_spell_mistake2(self):
        result = search_algo("Hex", "/HelloWorld/ItAGoodDay")
        self.assertEqual(result, True)
    
    def test_match_with_one_spell_mistake3(self):
        result = search_algo("Hrl", "/HelloWorld/ItAGoodDay")
        self.assertEqual(result, True)
    
    def test_fail_with_two_spell_mistake(self):
        result = search_algo("HelloQu", "/HelloWorld/ItAGoodDay")
        self.assertEqual(result, False)
    
    def test_with_one_spell_mistake4(self):
        result = search_algo("Dax", "/HelloWorld/ItAGoodDay")
        self.assertEqual(result, True)
    
    def test_with_one_letter(self):
        result = search_algo("D", "/HelloWorld/ItAGoodDay")
        self.assertEqual(result, True)
    
    def test_with_one_and_one_mistake_letter(self):
        result = search_algo("Dx", "/HelloWorld/ItAGoodDay")
        self.assertEqual(result, False)
    
    def test_empty_string(self):
        result = search_algo("", "/HelloWorld/ItAGoodDay")
        self.assertEqual(result, True)
    

if __name__ == '__main__':
    unittest.main()