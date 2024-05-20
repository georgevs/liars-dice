from dataclasses import dataclass


class Config:
  def __init__(self, args):
    self.num_bots = args.num_bots


class Game:
  def __init__(self, ui, config):
    self.ui = ui
    self.config = config

  def play(self, players):
    self.ui.announce_game_start()
    for player in players:
      player.deal_dice(Game.starting_dice_count)

    first_player = players.first_player()
    num_round = 0

    while players.players_count() > 1:
      num_round += 1
      round = Round(num_round, players)
      looser_player = self.play_round(round, first_player)
      looser_player.decrease_dice()
      if looser_player.dice_count > 0:
        first_player = looser_player
      else:
        first_player = players.next_player(looser_player)
        players.drop_player(looser_player)
        self.ui.announce_player_dropped(looser_player)

    winner_player = first_player
    self.ui.announce_game_complete(winner_player)

    return winner_player

  def play_round(self, round, first_player):
    self.ui.announce_round_start(round, first_player)

    for player in round.players:
      player.roll_dice()
    
    player = first_player
    bid = player.bid(round)
    while bid:
      turn = Turn(bid, player)
      self.ui.announce_turn(turn)
      round.record_turn(turn)
      player = round.players.next_player(player)
      bid = player.bid(round, challenge_acceptable=True)
      while bid and bid <= round.current_bid():
        self.ui.announce_invalid_bid(bid, round.current_bid())
        bid = player.bid(round, challenge_acceptable=True)

    bidder_player, challenger_player = round.current_bidder(), player
    self.ui.announce_challenge(bidder_player, challenger_player)

    players_hands = self.reveal_hands(round.players)
    current_bid = round.current_bid()
    self.ui.announce_challenge_settlement(current_bid, players_hands)

    looser_player = (
      challenger_player if self.is_valid_bid(current_bid, list(players_hands.values()))
      else bidder_player
    )
    self.ui.announce_round_complete(looser_player)
    
    return looser_player

  def reveal_hands(self, players):
    players_hands = { player: player.drop_hand() for player in players }
    return players_hands

  def is_valid_bid(self, bid, hands):
    face_count_in_hands = sum(hand.count(bid.face) for hand in hands)
    return bid.count <= face_count_in_hands

  starting_dice_count = 5

class Round:
  def __init__(self, num_round, players):
    self.num_round = num_round
    self.players = players
    self.turns = []

  def record_turn(self, turn):
    self.turns.append(turn)

  def current_bid(self):
    return self.turns[-1].bid
  
  def current_bidder(self):
    return self.turns[-1].player


@dataclass(repr=True, order=True, frozen=True)
class Bid:
  face: int
  count: int

@dataclass(repr=True, frozen=True)
class Turn:
  bid: Bid
  player: 'Player'
