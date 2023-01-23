from os import path
import time
import json

from models.models import Tournament

from controllers.controller_player_input import PlayerInput
from controllers.controller_tournament import TournamentController
from controllers.controller_reports import ReportsController

from views.view_main import MenuView
from views.view_tournament import TournamentView


players_data_file = "data/players.json"
tournaments_data_file = "data/tournaments.json"


class MenuController:
    def __init__(self):
        self.menu_view = MenuView()
        self.tournament_view = TournamentView()
        self.tournamentcontroller = TournamentController()
        self.reports = ReportsController()
        self.player = PlayerInput()

        self.tournament = Tournament

    def main_menu(self):
        """Main menu with selections."""
        self.menu_view.main_header()

        self.menu_view.menu()

        self.menu_view.first_prompt()
        user_choice = input()

        if user_choice == "1":
            self.tournament_new()

        elif user_choice == "2":
            self.tournament_resume()

        elif user_choice == "3":
            self.player_add()

        elif user_choice == "4":
            self.player_update()

        elif user_choice == "5":
            self.player_remove()

        elif user_choice == "6":
            self.reports_menu()

        elif user_choice == "10":
            self.exit_program()

        else:
            self.menu_view.wrong_input()
            self.main_menu()

        while True:
            choice = self.menu_view.back_to_menu()
            if choice == "ok":
                self.main_menu()
            elif choice == "bye":
                exit()
            else:
                continue

    def tournament_id_exist(self):
        """Check if a tournament ID exists."""
        id_list = []
        if path.isfile(tournaments_data_file) is False:
            with open(tournaments_data_file, "w") as json_file:
                json.dump(
                    id_list,
                    json_file,
                    indent=4,
                )
                self.menu_view.json_file_created()

        with open(tournaments_data_file) as file:
            try:
                obj = json.load(file)
                for tournament in obj:
                    existing_id = tournament["tournament_id"]
                    id_list.append(existing_id)
                    if not id_list:
                        id_list = [0]
                return id_list
            except Exception:
                pass

    def tournament_new(self):
        """Create a new tournament."""
        tournament_id = 1
        tournament_info = []

        self.tournament_view.tournament_new_header()
        user_input = self.tournament_view.tournament_new_input()
        for entry in user_input:
            tournament_input = input(entry)
            tournament_info.append(tournament_input)

        tournament_players = self.select_players()

        id_list = self.tournament_id_exist()
        for tournament_id in id_list:
            if tournament_id in id_list:
                tournament_id += 1

        tournament = Tournament(
            tournament_id=tournament_id,
            name=tournament_info[0],
            location=tournament_info[1],
            date_start="Pending",
            date_end="Pending",
            number_of_rounds=4,
            current_round=1,
            status="Ongoing",
            rounds_list=[],
            registered_players=tournament_players,
            description=tournament_info[2],
        )

        tournament.save_tournament()

        choice = self.tournament_view.tournament_start_prompt()

        while choice:
            if choice == "ok":
                break
            elif choice == "bye":
                self.main_menu()

        self.tournamentcontroller.tournament_start(tournament)

    def tournament_resume(self):
        """Resume a tournament."""
        tournaments = self.tournament.load_tournament(self)

        self.tournament_view.tournament_resume()

        while True:
            tourn_choice = self.tournament_view.tournament_resume_input()
            try:
                tourn_choice = int(tourn_choice)
                break
            except ValueError:
                self.tournament_view.wrong_input()
                time.sleep(1)
                self.tournament_resume()

        available_ids = []
        for tournament in tournaments:
            if tournament["status"] == "Ongoing":
                available_ids.append(tournament["tournament_id"])

        for tourn in tournaments:
            if tourn_choice in available_ids:
                tourn = tourn_choice - 1
                tournament = tournaments[tourn]
                tournament = Tournament(**tournament)
                self.tournamentcontroller.tournament_start(tournament)
                break

            else:
                self.tournament_view.wrong_input()
                time.sleep(1)
                self.tournament_resume()

    def player_add(self):
        """Calls the function to create a new player."""
        self.menu_view.new_player_header()
        self.player.players_add()

    def player_update(self):
        """Show the list of IDs in the alphabetical order.
        Choose the ID of the player to be changed"""
        while True:
            self.menu_view.clear_screen()
            obj = json.load(open(players_data_file))

            self.menu_view.player_update_header()
            id_list = []
            for player in obj:
                a = f"\t{player['player_id']} - {player['first_name']} {player['last_name']}"
                id_list.append(a)
            for ordered_ids in sorted(id_list):
                print(ordered_ids)

            id_to_update = self.menu_view.input_player_update()

            for player in obj:
                wrong_id = False
                if player["player_id"] == id_to_update:
                    last_name = None
                    first_name = None
                    birth_date = None
                    gender = None
                    rank = None
                    player["last_name"] = self.menu_view.player_last_name_update(
                        last_name
                    )
                    player["first_name"] = self.menu_view.player_first_name_update(
                        first_name
                    )
                    player["birth_date"] = self.menu_view.player_birth_date_update(
                        birth_date
                    )
                    player["gender"] = self.menu_view.player_gender_update(gender)
                    player["rank"] = self.menu_view.player_rank_update(rank)

                    with open(players_data_file, "w") as json_file:
                        json.dump(
                            obj,
                            json_file,
                            indent=4,
                        )
                    self.menu_view.player_updated()
                    break
                else:
                    wrong_id = True

            if wrong_id:
                self.menu_view.input_player_wrongid()
                wrong_id = False

            while True:
                update_more = self.menu_view.input_player_updateanother()
                if (update_more == "o") or (update_more == "n"):
                    break
                else:
                    self.menu_view.wrong_input()
                    continue

            if update_more == "n":
                self.main_menu()

    def player_remove(self):
        """Show the list of IDs in the alphabetical order.
        Remove a player by typing their ID."""
        while True:
            self.menu_view.clear_screen()
            obj = json.load(open(players_data_file))

            self.menu_view.player_remove_header()
            id_list = []
            for player in obj:
                a = f"\t{player['player_id']} - {player['first_name']} {player['last_name']}"
                id_list.append(a)
            for ordered_ids in sorted(id_list):
                print(ordered_ids)

            id_to_pop = self.menu_view.input_player_remove()

            for u in range(len(obj)):
                wrong_id = False
                if obj[u]["player_id"] == id_to_pop:
                    obj.pop(u)
                    with open(players_data_file, "w") as json_file:
                        json.dump(
                            obj,
                            json_file,
                            indent=4,
                        )
                    self.menu_view.player_removed()
                    break
                else:
                    wrong_id = True

            if wrong_id:
                self.menu_view.input_player_wrongid()
                wrong_id = False

            while True:
                remove_more = self.menu_view.input_player_removeanother()
                if (remove_more == "o") or (remove_more == "n"):
                    break
                else:
                    self.menu_view.wrong_input()
                    continue

            if remove_more == "n":
                break

    def reports_menu(self):
        """Menu to show reports."""
        self.menu_view.reports_menu()

        self.menu_view.first_prompt()
        user_choice = input()

        if user_choice == "1":
            self.reports.players_alpha()

        elif user_choice == "2":
            self.reports.all_tournaments()

        elif user_choice == "3":
            self.reports.tournament_players()

        elif user_choice == "4":
            self.reports.tournament_rounds_matches()

        elif user_choice == "0":
            self.main_menu()

        elif user_choice == "10":
            self.exit_program()

        else:
            self.menu_view.wrong_input()
            self.reports_menu()

        while True:
            morereports = self.menu_view.reports_showmore()
            if morereports == "ok":
                self.reports_menu()
            elif morereports == "bye":
                self.main_menu()
            else:
                continue

    def show_all_players(self):
        """Make a list of ALL the players available in the
        data file with an index in front of each."""
        obj = json.load(open(players_data_file))
        players_list = []
        for players in obj:
            players_list.append(players)
        return players_list

    def select_players(self):
        """Select and save players available in the data file for the new tournament."""
        player_final_list = []
        players_available_choices = self.show_all_players()

        check_players_avail = self.menu_view.not_enough_players()
        while check_players_avail:
            self.player.players_add()
            continue

        while True:
            ids_list = []
            self.tournament_view.players_add_header()
            for player in players_available_choices:
                ids_list.append(player["p_id"])
                self.tournament_view.players_available(player)

            choice = self.tournament_view.player_add_choice()

            if choice not in ids_list:
                self.tournament_view.input_not_in_list()
                continue

            for player in players_available_choices:
                if choice == player["p_id"]:
                    selected_player = player
                    player_final_list.append(selected_player)
                    players_available_choices.remove(selected_player)

            self.tournament_view.registered_players_number(player_final_list)

            if len(player_final_list) < 8:
                continue
            break

        self.menu_view.clear_screen()
        self.tournament_view.registered_players_header()
        self.tournament_view.registered_players_titles()

        for players in player_final_list:
            print(
                f'{players["last_name"]} {players["first_name"]} | {players["gender"]} | \
{players["birth_date"]} | {players["rank"]}'
            )
        return player_final_list

    def exit_program(self):
        """Exit the program."""
        while True:
            choice = self.menu_view.input_exit_program()
            if choice == "ok":
                exit()
            elif choice == "bye":
                self.main_menu()
            else:
                continue
