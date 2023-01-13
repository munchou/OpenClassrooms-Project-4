from os import path
import json
import random
from views.view_main import MenuView
from views.view_tournament import TournamentView


allowed_characters = r"^[a-zA-ZéÉèÈêÊëËâÂàÀîÎïÏçÇôÔûÛüÜ -]*$"
digits_characters = r"^[0-9]*$"
gender_characters = r"^[hHfF]*$"
players_data_file = "data/players.json"
tournaments_data_file = "data/tournaments.json"


class Player:
    def __init__(self, player_id, last_name, first_name, birth_date, gender, rank):
        self.player_id = player_id
        self.last_name = last_name
        self.first_name = first_name
        self.birth_date = birth_date
        self.gender = gender
        self.score = 0.0
        self.rank = rank
        self.played_against = []

        self.menu_view = MenuView()

    def player_serialization(self):
        """Serialize the player."""
        return {
            "player_id": self.player_id,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "birth_date": self.birth_date,
            "gender": self.gender,
            "score": self.score,
            "rank": self.rank,
            "played_against": self.played_against,
        }

    def save_player(self):
        """Save the created player into the corresponding JSON file."""
        main_players_list = []

        if path.isfile(players_data_file) is False:
            with open(players_data_file, "w"):
                self.menu_view.json_file_created()
            with open(players_data_file, "w") as file:
                json.dump(main_players_list, file, indent=4)

        with open(players_data_file) as file:
            try:
                retrieved_dict = json.load(file)

            except json.JSONDecodeError:
                print("In case of irrelevant JSONDecodeError.")

        retrieved_dict.append(self.player_serialization())

        with open(players_data_file, "w") as json_file:
            json.dump(
                retrieved_dict,
                json_file,
                indent=4,
            )

        self.menu_view.player_added()


class Tournament:
    def __init__(
        self,
        tournament_id,
        name,
        location,
        date_start,
        date_end,
        number_of_rounds: int,
        current_round: int,
        status,
        rounds_list,
        registered_players,
        description,
        # number_of_rounds=4,
    ):
        self.tournament_id = tournament_id
        self.name = name
        self.location = location
        self.date_start = date_start
        self.date_end = date_end
        self.number_of_rounds = number_of_rounds
        self.current_round = current_round
        self.status = status
        self.matches = []
        self.rounds_list = rounds_list
        self.registered_players = registered_players
        self.description = description
        # self.number_of_rounds = number_of_rounds

        # self.tour_db = tournaments_data_file

        self.tournament_view = TournamentView()
        self.menu_view = MenuView()

    def tournament_serialization(self):
        """Serialize the tournament."""
        return {
            "tournament_id": self.tournament_id,
            "name": self.name,
            "location": self.location,
            "date_start": self.date_start,
            "date_end": self.date_end,
            "number_of_rounds": self.number_of_rounds,
            "current_round": self.current_round,
            "status": self.status,
            "rounds_list": self.rounds_list,
            "registered_players": self.registered_players,
            "description": self.description,
        }

    def save_tournament(self):
        """Save a new tournament."""
        tournaments_list = []

        if path.isfile(tournaments_data_file) is False:
            with open(tournaments_data_file, "w"):
                self.menu_view.json_file_created()
            with open(tournaments_data_file, "w") as file:
                json.dump(tournaments_list, file, indent=4)

        with open(tournaments_data_file) as file:
            try:
                retrieved_dict = json.load(file)

            except json.JSONDecodeError:
                print("Irrelevant JSONDecodeError.")

        retrieved_dict.append(self.tournament_serialization())

        with open(tournaments_data_file, "w") as json_file:
            json.dump(
                retrieved_dict,
                json_file,
                indent=4,
            )

        self.tournament_view.tournament_saved()

    def load_tournament(self):
        return json.load(open(tournaments_data_file))

    def tournament_update(
        file_name, string_compared, compared_var, string_to_update, added_variable
    ):
        obj = json.load(open(file_name))
        for u in range(len(obj)):
            if obj[u][string_compared] == compared_var:
                obj[u][string_to_update] = added_variable

                with open(file_name, "w") as json_file:
                    json.dump(obj, json_file, indent=4)

    # def players_name_and_score(self):
    #     """Make a new list specifically for matches making,
    #     keeping only the names and score of the each player."""
    #     registered_players = self.registered_players
    #     match_players_list = []
    #     for player in range(len(registered_players)):
    #         player_info = [
    #             f"{registered_players[player]['last_name']} {registered_players[player]['first_name']}, {registered_players[player]['score']}"
    #         ]
    #         match_players_list.append(player_info)
    #     return match_players_list

    def players_shuffle(self):
        """Shuffle the registered players randomly for the first round."""
        players = self.registered_players  # self.players_name_and_score()
        # print(f"Original players list : {players}")
        random.shuffle(players)
        # for players in registered_players:
        # print(f"Shuffled players list : {players}")
        return players

    def roundone_players(self):
        """Make the teams for the first round.
        Generate the match as a tuple of 2 lists of
        the current players and their respective score."""
        playerslist = self.players_shuffle()  # shuffled registered_players
        while len(playerslist) >= 2:
            player1 = playerslist[0]
            player2 = playerslist[1]
            Round.pair_generator(self, player1, player2)
            # del playerslist[:2]
            playerslist = playerslist[2:]
        return playerslist

    def sort_by_score(self):
        """Sort the players according to their score.
        ("score" for ascending sorting, "-score" for descending)"""
        self.registered_players = sorted(
            self.registered_players, key=lambda score: -score["score"]
        )

    def played_against(self, p1, p2):
        obj = json.load(open(tournaments_data_file))

        for fields in range(len(obj)):
            roundplayers = obj[fields]["registered_players"]

            if obj[fields]["tournament_id"] == self.tournament_id:
                for player in range(len(roundplayers)):
                    if (
                        self.tournament_id
                        and roundplayers[player]["player_id"] == p1["player_id"]
                    ):
                        p1list = roundplayers[player]["played_against"]
                        p1list.append(p2["player_id"])
                        roundplayers[player]["played_against"] = p1list

                    if (
                        self.tournament_id
                        and roundplayers[player]["player_id"] == p2["player_id"]
                    ):
                        p2list = roundplayers[player]["played_against"]
                        p2list.append(p2["player_id"])
                        roundplayers[player]["played_against"] = p2list

                with open(tournaments_data_file, "w") as json_file:
                    json.dump(
                        obj,
                        json_file,
                        indent=4,
                    )

        # Optional, to see who played against whom:
        # print(f"{p1['last_name']} played against {p2['last_name']}")


class Round:
    def __init__(self, round_name, date_start, date_end):
        self.round_name = round_name
        self.date_start = date_start
        self.date_end = date_end
        self.matches = []

    def round(self):
        """Get round's info as a list."""
        return [self.round_name, self.date_start, self.date_end, self.matches]

    def pair_generator(self, player1, player2):
        """Match as a tuple of 2 lists of the current players and their score."""
        match = (
            f"{player1['last_name']} {player1['first_name']}",
            player1["score"],
            f"{player2['last_name']} {player2['first_name']}",
            player2["score"],
        )
        self.matches.append(match)
        self.played_against(player1, player2)
