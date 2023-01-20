import os
from os import path
import sys
import json
import re

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
        os.system("cls" if sys.platform == "win32" else "clear")

    def main_header(self):
        self.clear_screen()
        print("\t**********************")
        print("\t*   CENTRE ÉCHECS    *")
        print("\t*  Là où on réussit  *")
        print("\t**********************\n")

    def menu(self):
        """Shows the main menu with some data info."""
        num_of_players = self.number_of_player()
        print("\nMENU PRINCIPAL")
        print("1. Créer un nouveau tournoi")
        print("2. Reprendre un tournoi")
        print(f"3. Ajouter un nouveau joueur ({num_of_players} joueurs disponibles)")
        print("4. Mettre à jour les informations d'un joueur")
        print("5. Supprimer un joueur")
        print("6. Voir les rapports")
        print("7. Voir la liste de tous les joueurs de la base de données")
        print("\n10. Quitter le programme")

    def back_to_menu(self):
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
        choice = input("Quitter le programme ? (O/N) ").casefold()
        if choice == "o":
            return "ok"
        elif choice != "n":
            print("O ou N")
            return None
        else:
            return "bye"

    def num_of_players(self, num_of_players):
        print(f"Il y a {num_of_players} joueurs dans la base de données.")

    def number_of_player(self):
        if path.isfile(players_data_file) is False:
            return 0
        else:
            obj = json.load(open(players_data_file))
            num_of_players = len(obj)
            return num_of_players

    def number_of_tournaments(self):
        if path.isfile(tournaments_data_file) is False:
            return 0
        else:
            tournaments = json.load(open(tournaments_data_file))
            num_of_tournaments = len(tournaments)
            return num_of_tournaments

    def not_enough_players(self):
        self.clear_screen()
        num_of_players = self.number_of_player()
        if num_of_players < MAX_PLAYERS:
            print(
                f"\nIl y a {num_of_players} joueurs disponibles. Veuillez en ajouter de nouveaux.\n"
            )
            checker = True
            return checker
        checker = False
        # self.main_menu()

    @staticmethod
    def first_prompt():
        """Tell the user to choice an option and confirm it"""
        print("\nFaites votre choix et pressez la touche [ENTREE] : ")

    @staticmethod
    def new_player_header():
        print("\no o o | AJOUT D'UN NOUVEAU JOUEUR | o o o")

    def input_playerid(self):
        return input("\nIdentifiant du joueur (AB12345): ").upper()

    @staticmethod
    def input_playerid_lengtherror():
        print("\nIl semble y avoir une erreur dans la saisie de l'identifiant.")

    @staticmethod
    def input_playerid_exist():
        print("\nL'identifiant saisi existe déjà dans la base de données.")

    @staticmethod
    def input_playerid_charaerror():
        print("\nIl faut 2 lettres puis 5 chiffres. Réessayez.\n")

    def input_player_last_name(self):
        return input("Nom du joueur : ").capitalize()

    def input_player_lastname(self, last_name):
        while True:
            last_name = input("Nom du joueur : ").capitalize()
            if re.match(allowed_characters, last_name) and len(last_name) > 1:
                return last_name
            if re.match(allowed_characters, last_name) and len(last_name) <= 1:
                self.input_player_name_lengtherror()
            if not re.match(allowed_characters, last_name):
                self.input_player_invalidchara()

    def input_player_firstname(self):
        return input("Prénom du joueur : ").capitalize()

    @staticmethod
    def input_player_name_lengtherror():
        print("\nVeuillez entrer au moins 2 caractères.\n")

    @staticmethod
    def input_player_invalidchara():
        print("\nVous avez entré des caractères non valides.\n")

    @staticmethod
    def wrong_input():
        print("\nVeuillez saisir des informations correctes.")

    def input_player_birth_date(self):
        return input("Date de naissance (jjmmaaaa) : ")

    @staticmethod
    def input_player_birth_date_invalid():
        print("\nLa date est invalide, veuillez réessayer.\n")

    def input_player_gender(self):
        return input("Sexe (H/F) : ").capitalize()

    def input_player_rank(self):
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
        print("\nFichier de données créé.\n")

    @staticmethod
    def player_added():
        print("\nLe joueur a bien été enregistré.\n")

    def input_player_remove(self):
        return input("\nEntrez l'ID du joueur à supprimer : ").upper()

    def input_player_update(self):
        return input("\nEntrez l'ID du joueur à mettre à jour : ").upper()

    @staticmethod
    def player_updated():
        print("\nLe joueur a bien été mis à jour")

    def input_player_updateanother(self):
        return input("\nSouhaitez-vous mettre à jour un autre joueur ? (O/N) ")

    @staticmethod
    def input_player_wrongid():
        print("\nErreur de saisie ou ID inexistant.")

    @staticmethod
    def player_removed():
        print("\nLe joueur a bien été supprimé.")

    def input_player_removeanother(self):
        return input("\nSouhaitez-vous supprimer un autre joueur ? (O/N) ")

    @staticmethod
    def cancelled():
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
        choice = input("\n\tVoulez-vous afficher un autre rapport ? (O/N) ").casefold()
        if choice == "o":
            return "ok"
        elif choice != "n":
            self.wrong_input()
            return None
        else:
            return "bye"

    def tournament_select(self):
        return input("Choisissez un tournoi : ").casefold()

    @staticmethod
    def tournaments_file_error():
        print("ERREUR : Le fichier des tournois n'existe pas.")

    @staticmethod
    def tournament_not_started():
        print("\nRien à afficher, le premier round n'a pas été terminé.\n")
