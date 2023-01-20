import os
import sys
import json

# from models.model_main_menu import MainMenu

players_data_file = "data/players.json"
tournaments_data_file = "data/tournaments.json"


class TournamentView:
    def __init__(self):
        pass

    @staticmethod
    def clear_screen():
        os.system("cls" if sys.platform == "win32" else "clear")

    def main_menu(self):
        pass

    def input_exit_program(self):
        pass

    @staticmethod
    def tournament_new_header():
        print("\no o o | CREATION D'UN TOURNOI | o o o")

    def tournament_new_input(self):
        print("")
        user_input = ["Nom du tournoi : ", "Lieu : ", "Description : "]
        return user_input

    def players_available(self, player):
        return print(
            f'Joueur {player["p_id"]} : {player["player_id"]} | {player["last_name"]} {player["first_name"]} | {player["birth_date"]} | Classement : {player["rank"]}'
        )

    def player_add_choice(self):
        while True:
            choice = input("\tQuel joueur ajouter ? ")
            try:
                choice = int(choice)
                return choice
            except ValueError:
                print("Entrez un nombre uniquement.")

        # return int(input("\tQuel joueur ajouter ? "))

    @staticmethod
    def input_not_in_list():
        print("\nVeuillez sélectionner le numéro d'un joueur présent dans la liste.\n")

    def registered_players_number(self, player_final_list):
        return print(
            f"\n\tNombre de joueurs enregistrés : {len(player_final_list)} / 8"
        )

    @staticmethod
    def players_add_header():
        print("\no o o | Ajout de joueurs pour le nouveau tournoi | o o o\n")

    @staticmethod
    def registered_players_header():
        print("\no o o | Joueurs enregistrés pour le tournois | o o o\n")

    @staticmethod
    def registered_players_titles():
        print("\nNom Prénom | Sexe | Date de naissance | Classement")
        print("--------------------------------------------------")

    @staticmethod
    def tournament_saved():
        print("\nLe tournoi a bien été enregistré.")

    def tournament_start_prompt(self):
        choice = input("\nVoulez-vous commencer ce tournoi ? (O/N) ").casefold()
        if choice == "o":
            return "ok"
        elif choice != "n":
            print("Wrong input")
            self.tournament_start_prompt()
            return None
        else:
            return "bye"

    @staticmethod
    def tournament_resume():
        TournamentView().clear_screen()
        print("o o o | REPRENDRE UN TOURNOI | o o o")
        print("\nListe des tournois disponibles :")
        print("(les tournois terminés ne sont pas affichés)\n")
        tournaments = json.load(open(tournaments_data_file))
        for tournament in tournaments:
            if tournament["status"] == "Ongoing":
                print(f'[{tournament["tournament_id"]}]', end=" ")
                print(f'{tournament["name"]}', end=" / ")
                print(f'{tournament["location"]}', end=" / ")
                print(f'Démarré le : {tournament["date_start"]}', end=" / ")
                print(f'Terminé le : {tournament["date_end"]}', end=" / ")
                print(
                    f'Round {tournament["current_round"]} / {tournament["number_of_rounds"]}'
                )
                print(f'Description : {tournament["description"]}')

    def tournament_resume_input(self):
        return input(
            "\nChoisissez le tournoi que vous souhaitez reprendre : "
        ).casefold()

    def end_round_prompt(self):
        choice = input("Voulez-vous terminer ce round ? (O/N) ").casefold()
        if choice == "o":
            print("\nRound ended.")
            return "ok"
        elif choice != "n":
            self.wrong_input()
            return None
        else:
            return "bye"

    def end_round_scores_input(self):
        print("\tVictoire du joueur 1 : tapez 1")
        print("\tVictoire du joueur 2 : tapez 2")
        print("\tÉgalité : tapez 3")
        choice = input("\tVotre choix : ").casefold()

        if choice == "1":
            return choice
        elif choice == "2":
            return choice
        elif choice == "3":
            return choice

    @staticmethod
    def wrong_input():
        print("Erreur de saisie")
