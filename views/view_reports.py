import os
import sys
from prettytable import PrettyTable


players_data_file = "data/players.json"


class ReportsView:
    def __init__(self):
        self.table = PrettyTable()

        self.playersheader = [
            "Nom",
            "Prénom",
            "Sexe",
            "Date de naissance",
            "Classement",
        ]

        self.tournamentsheader = [
            "ID",
            "Nom du tournoi",
            "Lieu",
            "Date de début",
            "Date de fin",
            "Status",
            "Description",
        ]

        self.round_players = ["Joueur 1", "Score J1", "Joueur 2", "Score J2"]

    def clear_screen(self):
        """Clear the display."""
        os.system("cls" if sys.platform == "win32" else "clear")

    def players_alpha(self, players):
        """Show the tables of all the players (in the alphabetical order)"""
        self.table.clear()

        self.table.field_names = self.playersheader
        self.table.align["Nom"] = "l"
        self.table.align["Prénom"] = "l"
        self.table.align["Classement"] = "r"

        self.table._min_width = {
            "Nom": 16,
            "Prénom": 16,
            "Sexe": 5,
            "Date de naissance": 10,
            "Classement": 10,
        }
        self.table._max_width = {
            "Nom": 16,
            "Prénom": 16,
            "Sexe": 5,
            "Date de naissance": 10,
            "Classement": 10,
        }

        for i in range(len(players)):
            self.table.add_row(
                [
                    players[i]["last_name"],
                    players[i]["first_name"],
                    players[i]["gender"],
                    players[i]["birth_date"],
                    players[i]["rank"],
                ]
            )

        self.clear_screen()
        print(
            "o o o | JOUEURS PRÉSENTS DANS LA BASE DE DONNÉES (ordre alphabétique) | o o o\n"
        )
        print(self.table)

    def all_tournaments(self, tournaments):
        """Show the tables of all the tournaments (current and over)"""
        self.table.clear()

        self.table.field_names = self.tournamentsheader

        self.table._min_width = {
            "ID": 3,
            "Nom du tournoi": 20,
            "Lieu": 20,
            "Date de début": 10,
            "Date de fin": 10,
            "Status": 8,
            "Description": 50,
        }
        self.table._max_width = {
            "ID": 3,
            "Nom du tournoi": 20,
            "Lieu": 20,
            "Date de début": 10,
            "Date de fin": 10,
            "Status": 8,
            "Description": 50,
        }

        for i in range(len(tournaments)):
            self.table.add_row(
                [
                    tournaments[i]["tournament_id"],
                    tournaments[i]["name"],
                    tournaments[i]["location"],
                    tournaments[i]["date_start"],
                    tournaments[i]["date_end"],
                    tournaments[i]["status"],
                    tournaments[i]["description"],
                ]
            )

        self.clear_screen()
        print("o o o | TOURNOIS PRÉSENTS DANS LA BASE DE DONNÉES | o o o\n")
        print(self.table)

    def tournament_players(self, tournament, players):
        """Show the tables of all the players (in the alphabetical order)
        from a selected tournament"""
        self.table.clear()

        self.table.field_names = self.playersheader
        self.table.align["Nom"] = "l"
        self.table.align["Prénom"] = "l"
        self.table.align["Classement"] = "r"

        self.table._min_width = {
            "Nom": 16,
            "Prénom": 16,
            "Sexe": 5,
            "Date de naissance": 10,
            "Classement": 10,
        }
        self.table._max_width = {
            "Nom": 16,
            "Prénom": 16,
            "Sexe": 5,
            "Date de naissance": 10,
            "Classement": 10,
        }

        for i in range(len(players)):
            self.table.add_row(
                [
                    players[i]["last_name"],
                    players[i]["first_name"],
                    players[i]["gender"],
                    players[i]["birth_date"],
                    players[i]["rank"],
                ]
            )

        self.clear_screen()
        print(
            f'\to o o | JOUEURS DU TOURNOI {tournament["tournament_id"]} (ordre alphabétique) | o o o\n'
        )
        print(self.table)

    def tournament_rounds_matches(self, tournament_title, all_rounds):
        """Show the tables of all the rounds and matches
        from a selected tournament"""
        self.table.clear()

        print(f"\n\to o o | {tournament_title.upper()} | o o o")

        for round in all_rounds:
            matches = round[3]
            self.table.clear()

            tableheader = PrettyTable(
                [f"{round[0]}", f"DÉMARRÉ LE {round[1]}", f"TERMINÉ LE {round[2]}"]
            )

            tableheader.align[round[0]] = "l"

            tableheader.hrules = 1

            print(f"\n{tableheader}")

            for match in matches:

                self.table.field_names = self.round_players
                self.table._min_width = {
                    "Joueur 1": 24,
                    "Score J1": 8,
                    "Joueur 2": 24,
                    "Score J2": 8,
                }
                self.table._max_width = {
                    "Joueur 1": 24,
                    "Score J1": 8,
                    "Joueur 2": 24,
                    "Score J2": 8,
                }

                self.table.add_row([match[0], match[1], match[2], match[3]])

            print(self.table)
