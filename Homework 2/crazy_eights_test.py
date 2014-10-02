__author__ = 'Christopher Raleigh'

import unittest

import crazy_eights


class MyTestCase(unittest.TestCase):
    def test_something(self):
        state = crazy_eights.State()
        print('Face-up card:')
        print(crazy_eights.CardNames.full_name(state.partial_state.face_up_card))
        print('')
        print('Cards in hand:')
        for card in state.partial_state.hand.cards:
            print(crazy_eights.CardNames.full_name(card))
        print('')
        print('Opponent in hand:')
        for card in state.hand.cards:
            print(crazy_eights.CardNames.full_name(card))


if __name__ == '__main__':
    unittest.main()
