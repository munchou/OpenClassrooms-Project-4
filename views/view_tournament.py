import os
import json

players_data_file = "data/players.json"
tournaments_data_file = "data/tournaments.json"


class TournamentView:
    def __init__(self):
        pass

    def main_menu(self):
        pass

    def input_exit_program(self):
        pass

    @staticmethod
    def tournament_new_header():
        print("\nCREATION D'UN TOURNOI")

    def tournament_new_input(self):
        user_input = ["Nom du tournoi : ", "Lieu : ", "Description : "]
        return user_input

    def players_available(self, index, players):
        return print(f"Joueur {index} : {players}")

    def player_add_choice(self):
        return int(input("\tQuel joueur ajouter ? "))

    @staticmethod
    def input_not_in_list():
        print("\nVeuillez sélectionner le numéro d'un joueur présent dans la liste.")

    def registered_players_number(self, player_final_list):
        return print(
            f"\n\tNombre de joueurs enregistrés : {len(player_final_list)+1} / 8"
        )

    @staticmethod
    def registered_players():
        print("\nJoueurs enregistrés pour le tournois :")

    @staticmethod
    def tournament_saved():
        print("\nLe tournoi a bien été enregistré.")

    def tournament_start_prompt(self):
        choice = input("Voulez-vous commencer ce tournoi ? (O/N) ").casefold()
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
        os.system("cls")
        print("Liste des tournois disponibles :\n")
        tournaments = json.load(open(tournaments_data_file))

        for fields in range(len(tournaments)):
            if tournaments[fields]["status"] == "Ongoing":
                print(f'[{tournaments[fields]["tournament_id"]}]', end=" ")
                print(f'{tournaments[fields]["name"]}', end=" / ")
                print(f'{tournaments[fields]["location"]}', end=" / ")
                print(f'Démarré le : {tournaments[fields]["date_start"]}', end=" / ")
                print(f'Terminé le : {tournaments[fields]["date_end"]}', end=" / ")
                print(
                    f'Round {tournaments[fields]["current_round"]} / {tournaments[fields]["number_of_rounds"]}'
                )
                print(f'Description : {tournaments[fields]["description"]}')
                # print("- " * 50)

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
            print("Wrong input")
            print("Round not started")
            return None
        else:
            return "bye"

    @staticmethod
    def wrong_input():
        print("Erreur de saisie")
