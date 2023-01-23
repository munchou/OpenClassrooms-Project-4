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
    def __init__(
        self, p_id, player_id, last_name, first_name, birth_date, gender, rank
    ):
        self.p_id = p_id
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
            "p_id": self.p_id,
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

        self.matchlist = []
        self.registered_players_ordered = []

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
        """Load the tournament file."""
        return json.load(open(tournaments_data_file))

    def tournament_update(
        file_name, string_compared, compared_var, string_to_update, added_variable
    ):
        """To update the tournament (using 5 arguments)."""
        obj = json.load(open(file_name))
        for u in obj:
            if u[string_compared] == compared_var:
                u[string_to_update] = added_variable

                with open(file_name, "w") as json_file:
                    json.dump(obj, json_file, indent=4)

    def updated_matchlist(self, newmatchlist):
        """Update the list of the matches."""
        self.matchlist = newmatchlist

    def tournament_players(self):
        """Assign the registered players to the variable 'players'."""
        players = self.registered_players
        return players

    def players_shuffle(self):
        """Shuffle the registered players randomly for the first round."""
        players = self.registered_players
        random.shuffle(players)
        return players

    def roundone_players(self):
        """Make the teams for the first round.
        Generate the match as a tuple of 2 lists of
        the current players and their respective score."""
        playerslist = self.players_shuffle()
        while len(playerslist) >= 2:
            player1 = playerslist[0]
            player2 = playerslist[1]
            self.pair_generator(player1, player2)
            playerslist = playerslist[2:]

    def nextround_players(self):
        """Make the pairs for rounds 2 to 4 depending on the
        score. Two players cannot play against each other twice.
        Safety variable to prevent an infinite loop."""

        playerslist = self.registered_players

        obj = json.load(open(tournaments_data_file))

        different_score = []
        available_ids = []
        teams = []
        infiniteloop = 0

        # print(f"MATCH : {self.matchlist}")
        for tournament in obj:

            if tournament["tournament_id"] == self.tournament_id:
                while len(playerslist) >= 2:
                    infiniteloop += 1
                    # print(f"INFINITE LOOP : {infiniteloop}")

                    if infiniteloop < 20:
                        playerslist = sorted(
                            playerslist, key=lambda score: -score["score"]
                        )

                    if infiniteloop >= 20:
                        playerslist = self.registered_players
                        infiniteloop = 0
                        different_score = []
                        available_ids = []
                        teams = []
                        random.shuffle(playerslist)

                    player1 = playerslist[0]
                    player2 = playerslist[1]
                    player1_saved = player1

                    playerslist.remove(player1)

                    for player in playerslist:
                        if player["player_id"] not in player1_saved["played_against"]:
                            available_ids.append(player)

                    if available_ids:
                        for player in available_ids:
                            if player["score"] != player1_saved["score"]:
                                different_score.append(player)
                                available_ids.remove(player)
                    else:
                        available_ids = []
                        different_score = []
                        teams = []
                        playerslist = self.registered_players
                        continue

                    if different_score:
                        player2 = different_score[0]
                    else:
                        randnum = random.randrange(len(available_ids))
                        player2 = available_ids[randnum]

                    player1 = player1_saved
                    teams.append(player1)
                    teams.append(player2)
                    playerslist.remove(player2)

                    different_score = []
                    available_ids = []

                #     print(f"**** TEAMS : {teams}")
                #     print(f"**** PLAYER 1 : {player1_saved}")
                #     print(f"*********LENGTH TEAMS : {len(teams)} ***********")
                #     print(f"****LENGTH playerslist : {len(playerslist)} ******")

                # print("\n\tFINISHED")

                while teams:
                    player1 = teams[0]
                    # print(f"    PLAYER 1 : {player1}")
                    player2 = teams[1]
                    # print(f"    PLAYER 2 : {player2}")
                    self.pair_generator(player1, player2)
                    teams = teams[2:]

    def pair_generator(self, player1, player2):
        """Make a match as a tuple of 2 lists of the current players and their score.
        Also add the players to another tournament list in order to keep the right
        order of the players and prevent from getting the wrong updated scores."""
        match = (
            f"{player1['last_name']} {player1['first_name']}",
            player1["score"],
            f"{player2['last_name']} {player2['first_name']}",
            player2["score"],
        )
        self.registered_players_ordered.append(player1)
        self.registered_players_ordered.append(player2)
        self.played_against(player1, player2)
        self.matchlist.append(match)

    def played_against(self, p1, p2):
        """Add to each player's [played_against] list the ID of whom
        they have played against."""
        obj = json.load(open(tournaments_data_file))
        for tournament in obj:
            roundplayers = self.registered_players

            if tournament["tournament_id"] == self.tournament_id:
                for player in roundplayers:
                    if self.tournament_id and player["player_id"] == p1["player_id"]:
                        p1list = player["played_against"]
                        p1list.append(p2["player_id"])
                        player["played_against"] = p1list

                    if self.tournament_id and player["player_id"] == p2["player_id"]:
                        p2list = player["played_against"]
                        p2list.append(p1["player_id"])
                        player["played_against"] = p2list

                with open(tournaments_data_file, "w") as json_file:
                    json.dump(
                        obj,
                        json_file,
                        indent=4,
                    )


class Round:
    def __init__(self, round_name, date_start, date_end):
        self.round_name = round_name
        self.date_start = date_start
        self.date_end = date_end
        self.matches = []

    def round(self):
        """Get round's info as a list."""
        return [self.round_name, self.date_start, self.date_end, self.matches]

    def retrieve_matches(self, match):
        """To retrieve the list of match from the tournament and affect them
        to the round's list of matches."""
        self.matches = match
