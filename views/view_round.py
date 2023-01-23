from prettytable import PrettyTable


players_data_file = "data/players.json"


class RoundView:
    def __init__(self):
        self.table = PrettyTable()

        self.round_players = [
            "Match",
            "Player 1 - NAME",
            "P1 - SCORE",
            "",
            "Player 2 - NAME",
            "P2 - SCORE",
        ]

    def matches_summary(self, tourn, round, matches):
        """Show the tables of the tournament and the current round."""

        tableheader = PrettyTable(["NOM DU TOURNOI", tourn.name])

        tableheader._min_width = {"NOM DU TOURNOI": 16, tourn.name: 80}
        tableheader._max_width = {"NOM DU TOURNOI": 16, tourn.name: 80}

        tableheader.align["NOM DU TOURNOI"] = "l"
        tableheader.align[tourn.name] = "l"

        tableheader.add_row(["LIEU", tourn.location])
        tableheader.add_row(["DÉMARRÉ LE", round.date_start])
        tableheader.add_row(["TERMINÉ LE", round.date_end])
        tableheader.add_row(["DESCRIPTION", tourn.description])

        tableheader.add_row(
            ["ROUND", f"Round {tourn.current_round} sur {tourn.number_of_rounds}"]
        )
        tableheader.hrules = 1

        print(tableheader)

        self.table.clear()
        self.table.field_names = self.round_players
        self.table._min_width = {
            "Match": 8,
            "Player 1 - NAME": 25,
            "P1 - SCORE": 12,
            "": 2,
            "Player 2 - NAME": 25,
            "P2 - SCORE": 12,
        }
        self.table._max_width = {
            "Match": 8,
            "Player 1 - NAME": 25,
            "P1 - SCORE": 12,
            "": 2,
            "Player 2 - NAME": 25,
            "P2 - SCORE": 12,
        }

        for i in range(len(matches)):
            row = list(matches[i])
            row.insert(0, str(i + 1))
            row.insert(3, "VS")

            self.table.add_row(row)

        print(self.table)
