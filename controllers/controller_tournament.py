import os
import sys
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

    def clear_screen(self):
        os.system("cls" if sys.platform == "win32" else "clear")

    def tournament_start(self, tourn):
        """Start a new tournament ("tourn") or resume an existing one."""
        self.clear_screen()
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

            # tourn.current_round += 1

            self.tournament.tournament_update(
                tournaments_data_file,
                "tournament_id",
                selected_tournament,
                "current_round",
                tourn.current_round,
            )

        elif tourn.current_round > 1:
            self.round_next(tourn)

            # tourn.current_round += 1

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
                "registered_players",
                tourn.registered_players_ordered,
            )

            self.tournament.tournament_update(
                tournaments_data_file,
                "tournament_id",
                selected_tournament,
                "rounds_list",
                round_one.matches,
            )

        else:
            round_one.matches = tourn.rounds_list

        self.registered_players_update(selected_tournament, tourn.registered_players)

        self.round_view.matches_summary(tourn, round_one, round_one.matches)

        while True:
            choice = self.tournament_view.end_round_prompt()
            if choice == "ok":
                round_one.date_end = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

                self.score_points_input(round_one.matches, tourn)

                round_one.retrieve_matches(tourn.matchlist)

                tourn.rounds_list = []
                tourn.rounds_list.append(round_one.round())
                self.tournament.tournament_update(
                    tournaments_data_file,
                    "tournament_id",
                    selected_tournament,
                    "rounds_list",
                    tourn.rounds_list,
                )
                tourn.current_round += 1

                break
            elif choice == "bye":
                break
            else:
                continue

    def round_next(self, tourn):
        """Rounds 2 to 4, the players are ordered according to their
        score. A player cannot play againsts someone he's already met."""
        selected_tournament = tourn.tournament_id
        round = Round(f"Round {str(tourn.current_round)}", self.timer_fr, " ")

        if f"Round {str(tourn.current_round)}" not in str(tourn.rounds_list):
            players_backup = tourn.registered_players

            tourn.nextround_players()  # Makes the teams for the round

            round.retrieve_matches(tourn.matchlist)

            while len(round.matches) != 4:
                tourn.registered_players = players_backup
                tourn.nextround_players()
                continue

            round.retrieve_matches(tourn.matchlist)

            tourn.registered_players = tourn.registered_players_ordered

            self.tournament.tournament_update(
                tournaments_data_file,
                "tournament_id",
                selected_tournament,
                "registered_players",
                tourn.registered_players,
            )

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

        while True:
            choice = self.tournament_view.end_round_prompt()
            if choice == "ok":
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
                tourn.current_round += 1

                if tourn.current_round == 5:
                    tourn.status = "Finished"
                    self.tournament.tournament_update(
                        tournaments_data_file,
                        "tournament_id",
                        selected_tournament,
                        "status",
                        tourn.status,
                    )

                break
            elif choice == "bye":
                break
            else:
                continue

    def score_points_input(self, matches, tourn):
        selected_tournament = tourn.tournament_id

        players_scores_list = []
        # print(f"ROUNDS (debug - to delete later): {matches}")

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

        # UPDATE the tournament's "rounds_list" as well

        new_matches = []
        new_matchesbis = []
        for match in matches:
            new_match = list(match)
            new_matches.append(new_match)

        players_scores_list_bis = players_scores_list

        for match in new_matches:
            match[1] += players_scores_list_bis[0]
            match[3] += players_scores_list_bis[1]
            players_scores_list_bis = players_scores_list_bis[2:]
            matchtuple = tuple(match)
            new_matchesbis.append(matchtuple)

        tourn.updated_matchlist(new_matchesbis)

        # tourn.matchlist = new_matchesbis

        selected_tournament = tourn.tournament_id

        self.tournament.tournament_update(
            tournaments_data_file,
            "tournament_id",
            selected_tournament,
            "registered_players",
            tourn.registered_players,
        )

    def registered_players_update(self, selected_tournament, players):
        self.tournament.tournament_update(
            tournaments_data_file,
            "tournament_id",
            selected_tournament,
            "registered_players",
            players,
        )

    def tournament_end(self, tourn):
        tourn.date_end = self.timer_fr
