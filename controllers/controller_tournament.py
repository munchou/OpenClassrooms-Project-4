import json
import time
from datetime import datetime

from views.view_tournament import TournamentView
from views.view_round import RoundView

from models.models import Tournament
from models.models import Round


players_data_file = "data/players.json"
tournaments_data_file = "data/tournaments.json"


class TournamentController:
    def __init__(self):
        self.tournament_view = TournamentView()
        self.round_view = RoundView()
        self.tournament = Tournament
        self.round = Round

        self.timer_fr = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def tournament_start(self, tourn):
        """Start a new tournament ("tourn") or resume an existing one."""
        selected_tournament = tourn.tournament_id

        # in case of new tournament (from round 1):

        if tourn.current_round == 1:
            tourn.date_start = self.timer_fr

            self.tournament.tournament_update(
                tournaments_data_file,
                "tournament_id",
                selected_tournament,
                "date_start",
                tourn.date_start,
            )

            self.round_one_start(tourn)

            tourn.current_round += 1

            self.tournament.tournament_update(
                tournaments_data_file,
                "tournament_id",
                selected_tournament,
                "current_round",
                tourn.current_round,
            )

        elif tourn.current_round > 1:
            self.round_next(tourn)

            tourn.current_round += 1

            self.tournament.tournament_update(
                tournaments_data_file,
                "tournament_id",
                selected_tournament,
                "current_round",
                tourn.current_round,
            )

        elif tourn.status == "Finished":
            self.tournament_end(tourn)

    def round_one_start(self, tourn):
        """First round, the players are shuffled and play against
        each other as their respective score is 0."""
        selected_tournament = tourn.tournament_id

        round_one = Round("Round 1", self.timer_fr, "Pending")

        if not tourn.rounds_list:
            tourn.roundone_players()  # Makes the teams for the first round

            round_one.retrieve_matches(tourn.matchlist)

            self.tournament.tournament_update(
                tournaments_data_file,
                "tournament_id",
                selected_tournament,
                "rounds_list",
                round_one.matches,
            )

            # round_one.matches = tourn.rounds_list  # Check model to understand why

        else:
            round_one.matches = tourn.rounds_list

        self.registered_players_update(selected_tournament, tourn.registered_players)

        self.round_view.matches_summary(tourn, round_one, round_one.matches)

        choice = self.tournament_view.end_round_prompt()

        while choice:
            if choice == "ok":
                break
            elif choice == "bye":
                quit()

        round_one.date_end = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        self.score_points_input(round_one.matches, tourn)

        tourn.rounds_list = []
        tourn.rounds_list.append(round_one.round())
        self.tournament.tournament_update(
            tournaments_data_file,
            "tournament_id",
            selected_tournament,
            "rounds_list",
            tourn.rounds_list,
        )

    def round_next(self, tourn):
        """Rounds 2 to 4, the players are ordered according to their
        score. A player cannot play againsts someone he's already met."""
        selected_tournament = tourn.tournament_id
        round = Round(f"Round {str(tourn.current_round)}", self.timer_fr, " ")

        if f"Round {str(tourn.current_round)}" not in str(tourn.rounds_list):
            tourn.nextround_players()  # Makes the teams for the round
            round.retrieve_matches(tourn.matchlist)

            self.tournament.tournament_update(
                tournaments_data_file,
                "tournament_id",
                selected_tournament,
                "rounds_list",
                round.matches,
            )

            tourn.rounds_list.append(round.round())

        round.matches = tourn.rounds_list[tourn.current_round - 1][3]

        self.tournament.tournament_update(
            tournaments_data_file,
            "tournament_id",
            selected_tournament,
            "rounds_list",
            tourn.rounds_list,
        )

        self.registered_players_update(selected_tournament, tourn.registered_players)

        self.round_view.matches_summary(tourn, round, round.matches)

        choice = self.tournament_view.end_round_prompt()

        while choice:
            if choice == "ok":
                break
            elif choice == "bye":
                quit()

        round.date_end = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        self.score_points_input(round.matches, tourn)

        del tourn.rounds_list[-1]
        tourn.rounds_list.append(round.round())
        self.tournament.tournament_update(
            tournaments_data_file,
            "tournament_id",
            selected_tournament,
            "rounds_list",
            tourn.rounds_list,
        )

        if tourn.current_round == 4:
            tourn.status = "Finished"
            self.tournament.tournament_update(
                tournaments_data_file,
                "tournament_id",
                selected_tournament,
                "status",
                tourn.status,
            )

    def round_end(self, tourn):
        pass
        # input the score

    def score_points_input(self, matches, tourn):
        print(f"TOURN MATCHES : {tourn.matches}")
        players_scores_list = []
        print(f"ROUNDS : {matches}")
        i = 0
        for match in matches:
            p1 = match[0]
            p1_score = match[1]
            p2 = match[2]
            p2_score = match[3]
            i += 1

            while True:
                print("")
                print(f"[MATCH {i}]")
                print(f"[{p1}, score : {p1_score} [VS] {p2}, score : {p2_score}]")
                choice = self.tournament_view.end_round_scores_input()
                if choice in ["1", "2", "3"]:
                    if choice == "1":
                        p1_score += 1.0
                        players_scores_list.extend([1.0, 0.0])
                        break
                    if choice == "2":
                        p2_score += 1.0
                        players_scores_list.extend([0.0, 1.0])
                        break
                    if choice == "3":
                        p1_score += 0.5
                        p2_score += 0.5
                        players_scores_list.extend([0.5, 0.5])
                        break
                else:
                    self.tournament_view.wrong_input()
                    continue

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

        # tourn.current_round += 1

        # self.tournament.tournament_update(
        #     tournaments_data_file,
        #     "tournament_id",
        #     selected_tournament,
        #     "current_round",
        #     tourn.current_round,
        # )

    def registered_players_update(self, selected_tournament, players):
        self.tournament.tournament_update(
            tournaments_data_file,
            "tournament_id",
            selected_tournament,
            "registered_players",
            players,
        )

    def tournament_resume(self):
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
                break

            else:
                self.tournament_view.wrong_input()
                time.sleep(1)
                self.tournament_resume()

    def tournament_end(self, tourn):
        tourn.date_end = self.timer_fr
        print("Sorry, the Princess is in another castle...")
        print("GAME OVER")
