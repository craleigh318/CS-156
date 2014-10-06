__author__ = 'Christopher Raleigh'

import unittest

import crazy_eights


class MyTestCase(unittest.TestCase):
    def test_something(self):
        pass


class StateTest(unittest.TestCase):
    @staticmethod
    def make_test_state():
        ai_hand = crazy_eights.Hand([crazy_eights.Card(x) for x in [0, 1, 2, 3, 4, 5, 6, 7]])
        human_hand = crazy_eights.Hand([crazy_eights.Card(x) for x in [8, 9, 10, 11, 12, 13, 14]])
        face_up_card = crazy_eights.Card(16)
        deck_card_indices = [x for x in xrange(face_up_card.rank + 1, crazy_eights.Deck.max_deck_size())]
        deck_cards = [crazy_eights.Card(x) for x in deck_card_indices]
        partial_state = crazy_eights.PartialState(
            face_up_card=face_up_card,
            hand=human_hand,
            history=[crazy_eights.Move.play(0, face_up_card.rank, face_up_card.suit)]
        )
        state = crazy_eights.State(
            hand=ai_hand,
            deck=crazy_eights.Deck(deck_cards),
            partial_state=partial_state
        )
        return state

    def test_legal_moves(self):
        state = StateTest.make_test_state()
        expected = [crazy_eights.Move.play(1, 3, 0),
                    crazy_eights.Move.play(1, 7, 0),
                    crazy_eights.Move.play(1, 7, 1),
                    crazy_eights.Move.play(1, 7, 2),
                    crazy_eights.Move.play(1, 7, 3),
                    crazy_eights.Move.draw(1, 1)]
        actual = state._State__legal_moves(state.hand)
        expected = sorted([m.to_tuple() for m in expected])
        actual = sorted([m.to_tuple() for m in actual])
        self.assertEqual(expected, actual)

    def test_best_move(self):
        state = StateTest.make_test_state()
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

    def test_move_from_partial_state(self):
        partial_state = crazy_eights.PartialState.from_tuple((0, 0, [1, 2, 3, 4, 5, 6, 7, 8], []))
        state = partial_state.random_state()
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
