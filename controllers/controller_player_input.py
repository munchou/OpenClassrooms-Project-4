from os import path
import os
import re
import json
from datetime import datetime

from models.models import Player
from views.view_main import MenuView


allowed_characters = r"^[a-zA-ZéÉèÈêÊëËâÂàÀîÎïÏçÇôÔûÛüÜ -]*$"
digits_characters = r"^[0-9]*$"
gender_characters = r"^[hHfF]*$"
players_data_file = "data/players.json"


class PlayerInput:
    def __init__(self):
        self.menu_view = MenuView()

    def id_exist(self):
        """Check if a player ID exists."""
        obj = json.load(open(players_data_file))
        id_list = []
        for u in range(len(obj)):
            existing_id = obj[u]["player_id"]
            id_list.append(existing_id)
        return id_list

    def players_id(self):
        """Input for new player's ID."""
        id_list = self.id_exist()
        while True:
            self.player_id = self.menu_view.input_playerid()
            if len(self.player_id) != 7:
                self.menu_view.input_playerid_lengtherror()
                continue
            if self.player_id in id_list:
                self.menu_view.input_playerid_exist()
                continue
            if self.player_id[:2].isalpha() and self.player_id[2:7].isdigit():
                return self.player_id
            self.menu_view.input_playerid_charaerror()

    def player_last_name(self):
        """Input for new player's last name."""
        while True:
            self.last_name = self.menu_view.input_player_last_name()
            if re.match(allowed_characters, self.last_name) and len(self.last_name) > 1:
                return self.last_name
            if (
                re.match(allowed_characters, self.last_name)
                and len(self.last_name) <= 1
            ):
                self.menu_view.input_player_name_lengtherror()
            if not re.match(allowed_characters, self.last_name):
                self.menu_view.input_player_invalidchara()

    def player_first_name(self):
        """Input for new player's first name."""
        while True:
            self.first_name = self.menu_view.input_player_firstname()
            if (
                re.match(allowed_characters, self.first_name)
                and len(self.first_name) > 1
            ):
                return self.first_name
            if (
                re.match(allowed_characters, self.first_name)
                and len(self.first_name) <= 1
            ):
                self.menu_view.input_player_name_lengtherror()
            if not re.match(allowed_characters, self.first_name):
                self.menu_view.input_player_invalidchara()

    def player_birth_date(self):
        """Input for new player's birth date."""
        while True:
            date = self.menu_view.input_player_birth_date()
            try:
                self.birth_date = datetime.strptime(date, "%d%m%Y").strftime("%d/%m/%Y")
                return self.birth_date
            except ValueError:
                self.menu_view.input_player_birth_date_invalid()

    def player_gender(self):
        """Input for new player's gender."""
        while True:
            gender = self.menu_view.input_player_gender()
            if re.match(gender_characters, gender):
                if gender == "h" or gender == "H":
                    self.gender = "Homme"
                    return self.gender
                else:
                    self.gender = "Femme"
                    return self.gender
            else:
                self.menu_view.input_player_invalidchara()

    def player_score(self):
        """Default created player's score."""
        self.score = 0.0

    def player_rank(self):
        """Input for new player's rank."""
        while True:
            self.rank = self.menu_view.input_player_rank()
            if re.match(digits_characters, self.rank):
                return self.rank
            else:
                self.menu_view.input_player_invalidchara()

    # def player_summary(self):
    #     """Show the summary of the new player's info
    #     before confirming or cancelling it."""
    #     print(
    #         "\nRécapitulatif :\n"
    #         f"Identifiant : {self.player_id}, "
    #         f"Nom : {self.last_name}, "
    #         f"Prénom : {self.first_name}, "
    #         f"Date de naissance : {self.birth_date}, "
    #         f"Sexe : {self.gender}, "
    #         f"Classement (?) : {self.rank}"
    #     )

    def players_add(self):
        """Create a player, serialize it, add it to the json file."""
        running = True
        while running:
            id_input = self.players_id()
            lastname_input = self.player_last_name()
            firstname_input = self.player_first_name()
            birthdate_input = self.player_birth_date()
            gender_input = self.player_gender()
            self.player_score()
            rank_input = self.player_rank()

            self.menu_view.player_summary(
                id_input,
                lastname_input,
                firstname_input,
                birthdate_input,
                gender_input,
                rank_input,
            )

            while True:
                check_info = input("\nCes informations sont-elles correctes ? (O/N) ")
                if (check_info == "o") or (check_info == "n"):
                    break
                else:
                    self.menu_view.wrong_input()
                    continue

            if check_info == "n":
                os.system("cls")
                self.menu_view.cancelled()
                continue

            else:
                player = Player(
                    id_input,
                    lastname_input,
                    firstname_input,
                    birthdate_input,
                    gender_input,
                    rank_input,
                )
                # Player.player_serialization(self)

                player.save_player()

                while True:
                    add_more_player = input("Ajouter un autre joueur ? O/N\n")
                    if add_more_player == "o":
                        running = True
                        break
                    elif add_more_player == "n":
                        running = False
                        os.system("cls")
                        from controllers.controller import MenuController

                        MenuController().main_menu()
                    else:
                        print("Choisissez O ou N.")
                        continue

    def remove_player(self):
        """Show the list of IDs in the alphabetical order.
        Remove a player by typing their ID."""
        while True:
            os.system("cls")
            obj = json.load(open(players_data_file))

            # Show the available IDs that can be removed - To remove later
            print("ID disponibles (par ordre alphabétique) : ")
            id_list = []
            for u in range(len(obj)):
                a = f"{obj[u]['player_id']} - {obj[u]['first_name']} {obj[u]['last_name']}"
                id_list.append(a)
            for ordered_ids in sorted(id_list):
                print(ordered_ids)

            id_to_pop = self.menu_view.input_player_remove()

            for u in range(len(obj)):
                wrong_id = False
                if obj[u]["player_id"] == id_to_pop:
                    obj.pop(u)
                    # print(obj)
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

    def player_update(self):
        """Show the list of IDs in the alphabetical order.
        Choose the ID of the player to be changed"""
        while True:
            os.system("cls")
            obj = json.load(open(players_data_file))

            # Show the available IDs that can be updated - To remove later

            print("ID disponibles (par ordre alphabétique) : ")
            id_list = []
            for u in range(len(obj)):
                a = f"{obj[u]['player_id']} - {obj[u]['first_name']} {obj[u]['last_name']}"
                id_list.append(a)
            for ordered_ids in sorted(id_list):
                print(ordered_ids)

            id_to_update = self.menu_view.input_player_update()

            for u in range(len(obj)):
                wrong_id = False
                if obj[u]["player_id"] == id_to_update:
                    last_name = None
                    # first_name = None
                    # birth_date = None
                    # gender = None
                    # rank = None
                    obj[u]["last_name"] = self.menu_view.input_player_lastname(
                        last_name
                    )
                    obj[u]["first_name"] = PlayerInput.player_first_name(self)
                    obj[u]["birth_date"] = PlayerInput.player_birth_date(self)
                    obj[u]["gender"] = PlayerInput.player_gender(self)
                    obj[u]["rank"] = PlayerInput.player_rank(self)

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
                remove_more = self.menu_view.input_player_updateanother()
                if (remove_more == "o") or (remove_more == "n"):
                    break
                else:
                    self.menu_view.wrong_input()
                    continue

            if remove_more == "n":
                self.main_menu()
