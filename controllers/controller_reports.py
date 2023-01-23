import json
from os import path

from views.view_reports import ReportsView
from views.view_main import MenuView

players_data_file = "data/players.json"
tournaments_data_file = "data/tournaments.json"


class ReportsController:
    def __init__(self):
        self.menu_view = MenuView()
        self.reports_view = ReportsView()

    def players_alpha(self):
        """Reports - Show all the players in alphabetical order."""
        playerslist = []
        if path.isfile(players_data_file) is True:
            obj = json.load(open(players_data_file))
            for player in obj:
                playerslist.append(player)
            playerslist = sorted(
                playerslist, key=lambda lastname: lastname["last_name"]
            )
            self.reports_view.players_alpha(playerslist)
        else:
            self.menu_view.tournaments_file_error()

    def all_tournaments(self):
        """Reports - Load the tournaments (if the data file exists)"""
        tournamentslist = []
        if path.isfile(tournaments_data_file) is True:
            tournaments = json.load(open(tournaments_data_file))
            for tournament in tournaments:
                tournamentslist.append(tournament)
            self.reports_view.all_tournaments(tournamentslist)
        else:
            self.menu_view.tournaments_file_error()

    def select_tournament(self):
        """Reports - Show all the tournaments to select one."""
        if path.isfile(tournaments_data_file) is True:
            tournaments = json.load(open(tournaments_data_file))

            available_ids = []
            for tournament in tournaments:
                available_ids.append(tournament["tournament_id"])
                print(f'[{tournament["tournament_id"]}]', end=" ")
                print(f'{tournament["name"]}', end=" / ")
                print(f'{tournament["location"]}', end=" / ")
                print(f'Démarré le : {tournament["date_start"]}', end=" / ")
                print(f'Terminé le : {tournament["date_end"]}', end=" / ")
                print(f'Description : {tournament["description"]}')

            while True:
                tourn_choice = self.menu_view.tournament_select()
                if tourn_choice in available_ids:
                    tourn = tourn_choice - 1
                    tournament = tournaments[tourn]
                    break

            return tournament

        else:
            self.menu_view.tournaments_file_error()

    def tournament_players(self):
        """Reports - Show all the players of a selected tournament."""
        if path.isfile(tournaments_data_file) is True:
            tournament = self.select_tournament()
            players = tournament["registered_players"]
            players = sorted(players, key=lambda lastname: lastname["last_name"])

            self.reports_view.tournament_players(tournament, players)

        else:
            self.menu_view.tournaments_file_error()

    def tournament_rounds_matches(self):
        """Reports - Show all the rounds and matches of a selected tournament."""
        if path.isfile(tournaments_data_file) is True:
            tournament = self.select_tournament()
            all_rounds = tournament["rounds_list"]
            tournament_title = (
                f'Tournoi {tournament["tournament_id"]} : {tournament["name"]}'
            )

            print(len(all_rounds))
            if len(all_rounds) == 0 or "Round 1" not in all_rounds[0]:
                self.menu_view.tournament_not_started()
                self.tournament_rounds_matches()
            else:
                self.reports_view.tournament_rounds_matches(
                    tournament_title, all_rounds
                )
        else:
            self.menu_view.tournaments_file_error()
