__author__ = 'Christopher Raleigh'

import unittest

import crazy_eights


class MyTestCase(unittest.TestCase):
    def test_something(self):
        pass


class StateTest(unittest.TestCase):
    def test_best_move(self):
        ai_hand = crazy_eights.Hand([crazy_eights.Card(x) for x in [0, 1, 2, 3, 4, 5, 6, 7]])
        human_hand = crazy_eights.Hand([crazy_eights.Card(x) for x in [8, 9, 10, 11, 12, 13, 14]])
        face_up_card = crazy_eights.Card(16)
        deck_card_indices = [x for x in xrange(face_up_card.rank + 1, crazy_eights.Deck.max_deck_size())]
        deck_cards = [crazy_eights.Card(x) for x in deck_card_indices]
        partial_state = crazy_eights.PartialState(
            face_up_card=face_up_card.rank,
            suit=face_up_card.suit,
            hand=human_hand,
            history=[crazy_eights.Move.play(0, 2, 1)]
        )
        state = crazy_eights.State(
            hand=ai_hand,
            deck=crazy_eights.Deck(deck_cards),
            partial_state=partial_state
        )
        depth_limit = 4
        expected = (1, 3, 0, 0)
        self.assertEqual(expected, state.best_move(depth_limit).to_tuple())

    def test_random_state(self):
        state = crazy_eights.State()
        print('Face-up card:')
        print(crazy_eights.CardNames.full_name(state.partial_state.face_up_card))
        print('')
        print('Cards in hand:')
        for card in state.partial_state.hand.cards:
            print(crazy_eights.CardNames.full_name(card))
        print('')
        print('Opponent\'s hand:')
        for card in state.hand.cards:
            print(crazy_eights.CardNames.full_name(card))
        print('')
        print('Cards in Deck:')
        for card in state.deck.cards:
            print(crazy_eights.CardNames.full_name(card))


if __name__ == '__main__':
    unittest.main()
