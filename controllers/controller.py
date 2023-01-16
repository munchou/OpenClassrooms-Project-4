from os import path
import json

from models.models import Tournament

from controllers.controller_player_input import PlayerInput
from controllers.controller_tournament import TournamentController

from views.view_main import MenuView
from views.view_tournament import TournamentView

# MAX_PLAYERS = 8

players_data_file = "data/players.json"
tournaments_data_file = "data/tournaments.json"


class MenuController:
    def __init__(self):
        self.menu_view = MenuView()
        self.tournament_view = TournamentView()
        self.player = PlayerInput()
        self.tournamentcontroller = TournamentController()

    def main_menu(self):
        """Main menu with selections."""
        self.menu_view.main_menu()
        self.menu_view.first_prompt()
        user_choice = input()

        if user_choice == "1":
            print("1")
            self.tournament_new()

        elif user_choice == "2":
            self.tournamentcontroller.tournament_resume()

        elif user_choice == "3":
            self.player.players_add()
            # controller appelle model en demandant input, l'input appelle la fonction dans le model

        elif user_choice == "4":
            self.player.player_update()

        elif user_choice == "5":
            self.player.remove_player()

        elif user_choice == "6":
            pass

        elif user_choice == "7":
            # self.players_test()
            pass

        elif user_choice == "8":
            self.menu_view.input_exit_program()

        else:
            self.menu_view.wrong_input()
            self.main_menu()

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
        # self.menu_view.tournament_new()
        tournament_id = 1
        tournament_info = []

        user_input = self.tournament_view.tournament_new_input()
        for entry in user_input:
            tournament_input = input(entry)
            tournament_info.append(tournament_input)

        tournament_players = self.select_players()

        id_list = self.tournament_id_exist()
        print(f"IDs list : {id_list}")
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

    def show_all_players(self):
        """Make a list of ALL the players available in the
        data file with an index in front of each."""
        obj = json.load(open(players_data_file))
        players_list = []
        num_of_players = len(obj)
        self.menu_view.num_of_players(num_of_players)
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
        self.tournament_view.registered_players()
        for players in player_final_list:
            print(players)
        round.test(player_final_list)
        return player_final_list
