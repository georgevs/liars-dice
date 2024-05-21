from game import Bid
import random

class Config:
  def __init__(self, args):
    self.wild_mode = args.wild_mode
    self.can_choose_randomly = 1 <= args.bot_level
    self.can_bluff = 2 <= args.bot_level


class DumbStrategy:
  def __init__(self, config):
    self.config = config

  @property
  def capabilities(self):
    return set(filter(None, [
       self.config.can_choose_randomly and 'can_choose_randomly',
       self.config.can_bluff and 'can_bluff'
    ]))

  def peek_hand(self, hand):
    self.hand = hand

  def bid(self, round, challenge_acceptable):
    if not challenge_acceptable:
      bid_face = self.hand[random.randint(0, len(self.hand)-1)]
      hand_face_count = self.hand.count(bid_face)
      hand_ones_count = self.hand.count(1)
      hand_bid_count = hand_face_count + (hand_ones_count if self.config.wild_mode and bid_face != 1 else 0)
      if self.config.can_choose_randomly:
        hand_bid_count = random.randint(1, hand_bid_count)
      if self.config.can_bluff:
        bid_face = random.randint(1, 6)
      return Bid(bid_face, random.randint(1, hand_bid_count))

    else:
      current_bid = round.current_bid()
      hand_bid_face_count = self.hand.count(current_bid.face)
      hand_ones_count = self.hand.count(1)
      hand_bid_count = hand_bid_face_count + (hand_ones_count if self.config.wild_mode and current_bid.face != 1 else 0)
      max_possible_bid_face_count = (
        sum(player.dice_count for player in round.players) +
        (hand_bid_count - len(self.hand))
      )
      should_challenge = max_possible_bid_face_count < current_bid.count
      if should_challenge:
        return None

      bid_count = current_bid.count + 1
      if self.config.can_choose_randomly and bid_count < max_possible_bid_face_count:
        bid_count = random.randint(bid_count, max_possible_bid_face_count)

      return (
        None if should_challenge 
        else Bid(current_bid.face, bid_count)
      )
