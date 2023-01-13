import json
import time
from datetime import datetime

from views.view_tournament import TournamentView
from views.view_round import RoundView

from models.models import Tournament
from models.models import Round

timer = datetime.now()

players_data_file = "data/players.json"
tournaments_data_file = "data/tournaments.json"


class TournamentController:
    def __init__(self):
        self.tournament_view = TournamentView()
        self.round_view = RoundView()
        self.tournament = Tournament
        self.round = Round

        self.timer_fr = timer.strftime("%d/%m/%Y %H:%M:%S")

    def tournament_start(self, tourn):
        """Start a new tournament ("tourn") or resume an existing one."""
        # in case of new tournament (from round 1)
        selected_tournament = tourn.tournament_id

        if tourn.current_round == 0:
            tourn.date_start = self.timer_fr
            tourn.current_round += 1

            self.tournament.tournament_update(
                tournaments_data_file,
                "tournament_id",
                selected_tournament,
                "date_start",
                tourn.date_start,
            )

            self.tournament.tournament_update(
                tournaments_data_file,
                "tournament_id",
                selected_tournament,
                "current_round",
                tourn.current_round,
            )

            self.round_one_start(tourn)

    # next rounds until no more
    # save/update tournament in db

    # elif not new tournament (round >1)
    # next rounds until no more
    # save/update tournament in db

    # elif no more rounds left
    # end of tournament

    def round_one_start(self, tourn):
        """First round, the players are shuffled and play against
        each other as their respective score is 0."""
        round_one = Round("Round 1", self.timer_fr, " ")
        tourn.roundone_players()  # Makes the teams for the first round
        round_one.matches = tourn.matches  # Check model to understand why
        # self.tournament_update("rounds_list", round_one.matches)
        self.round_view.matches_summary(tourn, round_one.matches)

        print(f"Matches list: {round_one.matches}")
        # print(tourn.registered_players)  # same order as round_one.matches

    def round_next(self, tourn):
        pass

    def round_end(self, tourn):
        tourn.date_end = self.timer_fr
        # input the score

    def score_points_input(self, tourn):
        players_scores_list = []
        for match in round_one.matches:
            p1 = match[0]
            p1_score = match[1]
            p2 = match[2]
            p2_score = match[3]
            print(
                f"Player 1 : {p1}, score : {p1_score} / Player 2 : {p2}, score : {p2_score}"
            )

            choice = input("Choose the winner (1, 2 or 3)")
            if choice == "1":
                p1_score += 1.0
                players_scores_list.extend([1.0, 0.0])
            if choice == "2":
                p2_score += 1.0
                players_scores_list.extend([0.0, 1.0])
            if choice == "3":
                p1_score += 0.5
                p2_score += 0.5
                players_scores_list.extend([0.5, 0.5])

        for i in range(len(tourn.registered_players)):
            tourn.registered_players[i]["score"] += players_scores_list[i]

        selected_tournament = tourn.tournament_id

        self.tournament.tournament_update(
            tournaments_data_file,
            "tournament_id",
            selected_tournament,
            "registered_players",
            tourn.registered_players,
        )

        pass

    def tournament_resume(self):
        tournaments = self.tournament.load_tournament(self)

        self.tournament_view.tournament_resume()

        while True:
            tourn_choice = self.tournament_view.tournament_resume_input()
            try:
                int(tourn_choice)
                break
            except ValueError:
                self.tournament_view.wrong_input()
                time.sleep(1)
                self.tournament_resume()

        available_ids = []
        for tourn in range(len(tournaments)):
            if tournaments[tourn]["status"] == "Ongoing":
                available_ids.append(tournaments[tourn]["tournament_id"])

        for tourn in range(len(tournaments)):
            if int(tourn_choice) in available_ids:
                tourn = int(tourn_choice) - 1
                tournament = tournaments[tourn]
                tournament = Tournament(**tournament)
                # tournament = Tournament(
                #     tournament["tournament_id"],
                #     tournament["name"],
                #     tournament["location"],
                #     tournament["date_start"],
                #     tournament["date_end"],
                #     tournament["number_of_rounds"],
                #     tournament["current_round"],
                #     tournament["status"],
                #     tournament["rounds_list"],
                #     tournament["registered_players"],
                #     tournament["description"],
                # )
                self.tournament_start(tournament)

            else:
                self.tournament_view.wrong_input()
                time.sleep(1)
                self.tournament_resume()

    def tournament_end(self, tourn):
        pass
