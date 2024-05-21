from game import Bid
import re
import sys


class Config:
  def __init__(self, args):
    self.show_hands_at_settlement = args.show_hands_at_settlement
    self.show_bots_capabilities = args.show_bots_capabilities
    self.wild_mode = args.wild_mode


class Ui:
  def __init__(self, config):
    self.config = config

  def handle_sigint(self):
    print()
    sys.exit(0)

  def announce_game_start(self):
    print(' '.join([
      f"Game start{' in wild mode' if self.config.wild_mode else ''}.",
      'Exit with Ctrl+C.'
    ]), end='\n\n')

  def announce_round_start(self, round, first_player):
    players_names = ', '.join(player.name for player in round.players)
    print(' '.join([
      f'Round {round.num_round} start.',
      f'There are {len(round.players)} players in this round: {players_names}.',
      f'Player {first_player.name} is first.'
    ]))
    if self.config.show_bots_capabilities:
      capabilities = set().union(
        *[capabilities for player in round.players if (capabilities := player.capabilities)]
      )
      labels = list(filter(None, [Ui.capabilities_labels.get(it) for it in capabilities]))
      labels = (
        None if not labels 
        else labels[0] if len(labels) <= 1
        else f'{labels[0]} and {labels[1]}' if len(labels) <= 2
        else ', and '.join([ ', '.join(labels[:-1]), labels[-1]])
      )
      if labels:
        print(f"Beware, bots can {labels}!")

  capabilities_labels = {
    'can_choose_randomly': 'choose randomly',
    'can_bluff': 'bluff'
  }  

  def peek_hand(self, hand):
    print(f"User's hand is {hand}")

  def prompt_user(prompt):
    try: return input(prompt)
    except EOFError: return ''

  def prompt_bid(self, challenge_acceptable):
    parse_number = re.compile(r'\d+').fullmatch

    prompt_count = f"Bid count{' or challenge' if challenge_acceptable else ''}? "
    prompt_count_bid = (lambda: int(match.group(0)) if (match := parse_number(Ui.prompt_user(prompt_count).strip())) else None)
    count = prompt_count_bid()
    while (count is None and not challenge_acceptable) or (count is not None and (count <= 0)):
      print('Invalid count bid. Count must be one or higher. Try again.')
      count = prompt_count_bid()
      
    if count is None:
      return None

    prompt_face = f"Bid face (1-6){' or challenge' if challenge_acceptable else ''}? "
    prompt_face_bid = (lambda: int(match.group(0)) if (match := parse_number(Ui.prompt_user(prompt_face).strip())) else None)
    face = prompt_face_bid()
    while (face is None and not challenge_acceptable) or (face is not None and not (1 <= face <= 6)):
      print('Invalid face bid. Face must be 1 to 6, Try again.')
      face = prompt_face_bid()

    if face is None:
      return None

    return Bid(face, count)

  def announce_invalid_bid(self, bid, current_bid):
    print(f'Bid is unacceptable. Count must be more than {current_bid.count} or else face must be greater than {current_bid.face}. Try again.')

  def announce_turn(self, turn):
    print(f'Player {turn.player.name} bids there are {turn.bid.count} die with face {turn.bid.face} on the whole table.')

  def announce_challenge(self, bidder_player, challenger_player):
    print(f'Player {challenger_player.name} challenges {bidder_player.name}.')

  def announce_challenge_settlement(self, current_bid, players_hands):
    face_count = sum(hand.count(current_bid.face) for hand in players_hands.values())
    print(f'There are {face_count} die with face {current_bid.face} on the whole table.')
    if self.config.wild_mode and current_bid.face != 1:
      ones_count = sum(hand.count(1) for hand in players_hands.values()) 
      print(f'Also, there are {ones_count} die with face 1 on the whole table.')
      print(f'The total bid count id {face_count + ones_count}.')
    if self.config.show_hands_at_settlement:
      print('Players hands:')
      for player, hand in players_hands.items():
        print(f"\t{player.name}'s hand is {hand}.")

  def announce_round_complete(self, looser_player):
    print(f'Player {looser_player.name} lost the round.', end='\n\n')

  def announce_player_dropped(self, looser_player):
    print(f'Player {looser_player.name} dropped from the game.')  

  def announce_game_complete(self, winner_player):
    print(f'Player {winner_player.name} wins the game!', end='\n\n')

  def prompt_continue_play(self):
    continue_play = str(input('Play again (Yes/no)? ')).strip().lower() in ['', 'yes']
    if continue_play: print()
    return continue_play
