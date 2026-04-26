import unittest

from guard_game import Entrant, Game


class GuardGameTests(unittest.TestCase):
    def test_should_allow_only_when_clean(self):
        self.assertTrue(Entrant("A", "shelter", False, False, 30, "Medic", "🧑").should_allow)
        self.assertFalse(Entrant("A", "shelter", True, False, 30, "Medic", "🧑").should_allow)
        self.assertFalse(Entrant("A", "shelter", False, True, 30, "Medic", "🧑").should_allow)

    def test_judge_increments_score_on_correct_decision(self):
        game = Game(days=1, entrants_per_day=1, seed=1)
        entrant = Entrant("A", "shelter", False, False, 30, "Medic", "🧑")
        ok, _ = game.judge(entrant, "allow")
        self.assertTrue(ok)
        self.assertEqual(game.score, 1)
        self.assertEqual(game.strikes, 0)

    def test_judge_increments_strike_on_wrong_decision(self):
        game = Game(days=1, entrants_per_day=1, seed=1)
        entrant = Entrant("A", "shelter", True, False, 30, "Medic", "🧑")
        ok, _ = game.judge(entrant, "allow")
        self.assertFalse(ok)
        self.assertEqual(game.score, 0)
        self.assertEqual(game.strikes, 1)

    def test_outcome_suspended_on_five_strikes(self):
        game = Game(days=1, entrants_per_day=5)
        game.strikes = 5
        self.assertEqual(game.outcome_text(), "Suspended. The base needs steadier hands.")


if __name__ == "__main__":
    unittest.main()
