from game import Bid
import random


class DumbStrategy:
  def peek_hand(self, hand):
    self.hand = hand

  def bid(self, round, challenge_acceptable):
    if not challenge_acceptable:
      face = self.hand[random.randint(0, len(self.hand)-1)]
      count = self.hand.count(face)
      return Bid(face, count)

    else:
      current_bid = round.current_bid()
      max_possible_bid_face_count = (
        sum(player.dice_count for player in round.players) +
        (self.hand.count(current_bid.face) - len(self.hand))
      )
      should_challenge = max_possible_bid_face_count < current_bid.count
      return None if should_challenge else Bid(current_bid.face, current_bid.count + 1)
