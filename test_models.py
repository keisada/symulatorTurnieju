import unittest
from models import Tournament, Team, Player


class TestTournamentModels(unittest.TestCase):

    def setUp(self):
        """Metoda uruchamiana przed każdym testem. Tworzy pusty turniej."""
        self.tournament = Tournament()

    def test_initial_state(self):
        """Testuje, czy turniej startuje w poprawnym, pustym stanie."""
        self.assertEqual(self.tournament.phase, "SETUP")
        self.assertEqual(len(self.tournament.teams), 0)

    def test_add_team(self):
        """Testuje dodawanie drużyny."""
        self.tournament.add_team("Testowa Drużyna")
        self.assertEqual(len(self.tournament.teams), 1)
        self.assertEqual(self.tournament.teams[0].name, "Testowa Drużyna")
        with self.assertRaises(ValueError):
            self.tournament.add_team("Testowa Drużyna")

    def test_add_player_with_stats(self):
        """Testuje dodawanie zawodnika z ręcznie podanymi statystykami."""
        self.tournament.add_team("FC Test")
        team = self.tournament.teams[0]
        team.add_player("Jan", "Kowalski", attack=10, defense=5, aggression=2)

        self.assertEqual(len(team.players), 1)
        player = team.players[0]
        self.assertEqual(player.name, "Jan Kowalski")
        self.assertEqual(player.attack, 10)
        self.assertEqual(player.defense, 5)
        self.assertEqual(player.aggression, 2)

    def test_add_player_random_stats(self):
        """Testuje dodawanie zawodnika, gdzie statystyki powinny być losowe."""
        self.tournament.add_team("FC Random")
        team = self.tournament.teams[0]
        team.add_player("Losowy", "Gracz")  # Nie podajemy statystyk

        player = team.players[0]
        self.assertIn(player.attack, range(1, 11))
        self.assertIn(player.defense, range(1, 11))
        self.assertIn(player.aggression, range(1, 11))

    def test_player_limit(self):
        """Testuje limit 11 zawodników w drużynie."""
        self.tournament.add_team("Pełny Skład")
        team = self.tournament.teams[0]
        for i in range(11):
            team.add_player(f"Gracz{i}", "Testowy")
        self.assertEqual(len(team.players), 11)
        with self.assertRaises(ValueError):
            team.add_player("Dwunasty", "Gracz")

    def test_generate_random_tournament(self):
        """Testuje, czy losowy turniej jest generowany i rozpoczynany poprawnie."""
        self.tournament.generate_random_tournament()
        self.assertEqual(self.tournament.phase, "GROUP_STAGE")
        self.assertEqual(len(self.tournament.teams), 16)
        self.assertTrue(all(len(t.players) == 11 for t in self.tournament.teams))
        self.assertGreater(len(self.tournament.matches), 0)


if __name__ == '__main__':
    unittest.main()