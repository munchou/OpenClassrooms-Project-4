import os
from os import path
import sys
import json
import re
from datetime import datetime

allowed_characters = r"^[a-zA-ZéÉèÈêÊëËâÂàÀîÎïÏçÇôÔûÛüÜ -]*$"
digits_characters = r"^[0-9]*$"
gender_characters = r"^[hHfF]*$"
players_data_file = "data/players.json"
tournaments_data_file = "data/tournaments.json"
MAX_PLAYERS = 8


class MenuView:
    def __init__(self):
        pass

    @staticmethod
    def clear_screen():
        """Clear the display."""
        os.system("cls" if sys.platform == "win32" else "clear")

    def main_header(self):
        """Header before the main menu."""
        self.clear_screen()
        print("\t**********************")
        print("\t*   CENTRE ÉCHECS    *")
        print("\t*  Là où on réussit  *")
        print("\t**********************\n")

    def menu(self):
        """Display the main menu with some data info."""
        num_of_players = self.number_of_player()
        print("\nMENU PRINCIPAL")
        print("1. Créer un nouveau tournoi")
        print("2. Reprendre un tournoi")
        print(f"3. Ajouter un nouveau joueur ({num_of_players} joueurs disponibles)")
        print("4. Mettre à jour les informations d'un joueur")
        print("5. Supprimer un joueur")
        print("6. Voir les rapports")
        print("\n10. Quitter le programme")

    def back_to_menu(self):
        """Input to go back to the main menu."""
        choice = input(
            "\n\tVoulez-vous retourner au menu principal ? (O/N = quitter) "
        ).casefold()
        if choice == "o":
            return "ok"
        elif choice != "n":
            self.wrong_input()
            return None
        else:
            return "bye"

    def input_exit_program(self):
        """Input to exit the program."""
        choice = input("Quitter le programme ? (O/N) ").casefold()
        if choice == "o":
            return "ok"
        elif choice != "n":
            print("O ou N")
            return None
        else:
            return "bye"

    def num_of_players(self, num_of_players):
        """Display the number of players in the database."""
        print(f"Il y a {num_of_players} joueurs dans la base de données.")

    def number_of_player(self):
        """Retrieve the number of players in the database."""
        if path.isfile(players_data_file) is False:
            return 0
        else:
            obj = json.load(open(players_data_file))
            num_of_players = len(obj)
            return num_of_players

    def number_of_tournaments(self):
        """Retrieve the number of tournaments in the database."""
        if path.isfile(tournaments_data_file) is False:
            return 0
        else:
            tournaments = json.load(open(tournaments_data_file))
            num_of_tournaments = len(tournaments)
            return num_of_tournaments

    def not_enough_players(self):
        """Check the number of players."""
        self.clear_screen()
        num_of_players = self.number_of_player()
        if num_of_players < MAX_PLAYERS:
            print(
                f"\nIl y a {num_of_players} joueurs disponibles. Veuillez en ajouter de nouveaux.\n"
            )
            checker = True
            return checker
        checker = False

    @staticmethod
    def first_prompt():
        """Tell the user to choice an option and confirm it."""
        print("\nFaites votre choix et pressez la touche [ENTREE] : ")

    @staticmethod
    def new_player_header():
        """Header for 'add player'."""
        MenuView().clear_screen()
        print("o o o | AJOUT D'UN NOUVEAU JOUEUR | o o o")

    def input_playerid(self):
        """Input for player's ID"""
        return input("\nIdentifiant du joueur (AB12345): ").upper()

    @staticmethod
    def input_playerid_lengtherror():
        """Input error for player's ID."""
        print("\nIl semble y avoir une erreur dans la saisie de l'identifiant.")

    @staticmethod
    def input_playerid_exist():
        """Error if the player's ID already exists."""
        print("\nL'identifiant saisi existe déjà dans la base de données.")

    @staticmethod
    def input_playerid_charaerror():
        """Input error for player's ID that doesn't match 2 letters and 5 digits."""
        print("\nIl faut 2 lettres puis 5 chiffres. Réessayez.\n")

    def input_player_last_name(self):
        """Input for new player's last name."""
        return input("Nom du joueur : ").capitalize()

    def player_last_name_update(self, last_name):
        """Update player's last name."""
        while True:
            last_name = self.input_player_last_name()
            if re.match(allowed_characters, last_name) and len(last_name) > 1:
                return last_name
            if re.match(allowed_characters, last_name) and len(last_name) <= 1:
                self.input_player_name_lengtherror()
            if not re.match(allowed_characters, last_name):
                self.input_player_invalidchara()

    def player_first_name_update(self, first_name):
        """Update player's first name."""
        while True:
            first_name = self.input_player_firstname()
            if re.match(allowed_characters, first_name) and len(first_name) > 1:
                return first_name
            if re.match(allowed_characters, first_name) and len(first_name) <= 1:
                self.input_player_name_lengtherror()
            if not re.match(allowed_characters, first_name):
                self.input_player_invalidchara()

    def player_birth_date_update(self, birth_date):
        """Update player's birth date."""
        while True:
            date = self.input_player_birth_date()
            try:
                birth_date = datetime.strptime(date, "%d%m%Y").strftime("%d/%m/%Y")
                return birth_date
            except ValueError:
                self.input_player_birth_date_invalid()

    def player_gender_update(self, gender):
        """Update player's gender."""
        while True:
            gender = self.input_player_gender()
            if re.match(gender_characters, gender):
                if gender == "h" or gender == "H":
                    gender = "Homme"
                    return gender
                else:
                    gender = "Femme"
                    return gender
            else:
                self.input_player_invalidchara()

    def player_rank_update(self, rank):
        """Update player's rank."""
        while True:
            rank = self.input_player_rank()
            if re.match(digits_characters, rank):
                return rank
            else:
                self.input_player_invalidchara()

    def input_player_firstname(self):
        """Input for new player's first name."""
        return input("Prénom du joueur : ").capitalize()

    @staticmethod
    def input_player_name_lengtherror():
        """Input length error."""
        print("\nVeuillez entrer au moins 2 caractères.\n")

    @staticmethod
    def input_player_invalidchara():
        """Input invalid characters error."""
        print("\nVous avez entré des caractères non valides.\n")

    @staticmethod
    def wrong_input():
        """Wrong input."""
        print("\nVeuillez saisir des informations correctes.")

    def input_player_birth_date(self):
        """Input for new player's birth date."""
        return input("Date de naissance (jjmmaaaa) : ")

    @staticmethod
    def input_player_birth_date_invalid():
        """Invalid birth date error message."""
        print("\nLa date est invalide, veuillez réessayer.\n")

    def input_player_gender(self):
        """Input for new player's gender."""
        return input("Sexe (H/F) : ").capitalize()

    def input_player_rank(self):
        """Input for new player's rank."""
        return input("Classement : ")

    def player_summary(
        self, player_id, last_name, first_name, birth_date, gender, rank
    ):
        """Show the summary of the new player's info
        before confirming or cancelling it."""
        print(
            "\nRécapitulatif :\n"
            f"Identifiant : {player_id}, "
            f"Nom : {last_name}, "
            f"Prénom : {first_name}, "
            f"Date de naissance : {birth_date}, "
            f"Sexe : {gender}, "
            f"Classement : {rank}"
        )

    @staticmethod
    def json_file_created():
        """Confirm the json file was created."""
        print("\nFichier de données créé.\n")

    @staticmethod
    def player_added():
        """Confirm the new player was saved."""
        print("\nLe joueur a bien été enregistré.\n")

    def input_player_remove(self):
        """Input the ID of the player to delete."""
        return input("\nEntrez l'ID du joueur à supprimer : ").upper()

    @staticmethod
    def player_remove_header():
        MenuView().clear_screen()
        print("o o o | SUPPRIMER UN JOUEUR | o o o\n")
        print("ID disponibles (par ordre alphabétique) : ")

    @staticmethod
    def player_update_header():
        MenuView().clear_screen()
        print("o o o | MODIFIER UN JOUEUR | o o o\n")
        print("ID disponibles (par ordre alphabétique) : ")

    def input_player_update(self):
        """Input the ID of the player to update."""
        return input("\nEntrez l'ID du joueur à mettre à jour : ").upper()

    @staticmethod
    def player_updated():
        """Confirm the player was updated.."""
        print("\nLe joueur a bien été mis à jour")

    def input_player_updateanother(self):
        """Input to update another player."""
        return input("\nSouhaitez-vous mettre à jour un autre joueur ? (O/N) ")

    @staticmethod
    def input_player_wrongid():
        """Wrong or unknown ID."""
        print("\nErreur de saisie ou ID inexistant.")

    @staticmethod
    def player_removed():
        """Confirm the player was deleted."""
        print("\nLe joueur a bien été supprimé.")

    def input_player_removeanother(self):
        """Input to remove another player."""
        return input("\nSouhaitez-vous supprimer un autre joueur ? (O/N) ")

    @staticmethod
    def cancelled():
        """Confirm the operation was cancelled."""
        print("\nOpération annulée.\n")

    def reports_menu(self):
        """Shows the reports menu with some data info."""
        num_of_players = self.number_of_player()
        num_of_tournaments = self.number_of_tournaments()
        self.clear_screen()
        print("o o o | AFFICHER DES RAPPORTS | o o o\n")
        print(f"1. Afficher les {num_of_players} joueurs enregistrés")
        print(f"2. Afficher les {num_of_tournaments} tournois")
        print("3. Afficher les joueurs d'un tournoi")
        print("4. Afficher les rounds et matchs d'un tournoi")
        print("\n0. Retourner au menu principal")
        print("\n10. Quitter le programme")

    def reports_showmore(self):
        """Input to display another report."""
        choice = input("\n\tVoulez-vous afficher un autre rapport ? (O/N) ").casefold()
        if choice == "o":
            return "ok"
        elif choice != "n":
            self.wrong_input()
            return None
        else:
            return "bye"

    def tournament_select(self):
        """Input to select a tournament."""

        while True:
            tourn_choice = input("\nChoisissez un tournoi : ").casefold()
            try:
                tourn_choice = int(tourn_choice)
                return tourn_choice
            except ValueError:
                self.wrong_input()

    @staticmethod
    def tournaments_file_error():
        """Error message about non-existing tournament file."""
        print("ERREUR : Le fichier des tournois n'existe pas.")

    @staticmethod
    def tournament_not_started():
        """Error message informing the first round has not been finished yet."""
        print("\nRien à afficher, le premier round n'a pas été terminé.\n")
