from typing import List
import random 


class Players(List):
  def __init__(self, *args):
    super().__init__(*args)
    if len(self) < 2:
      raise ValueError('Must start with at least 2 players')

  def first_player(self):
    return self[0]

  def next_player(self, player):
    pos = self.index(player)
    return self[(pos + 1) % len(self)]

  def drop_player(self, player):
    self.remove(player)

  def players_count(self):
    return len(self)


class Player:
  def __init__(self, name):
    self.name = name
    self._dice_count = None
    self.hand = None

  @property
  def capabilities(self):
    return None

  def deal_dice(self, dice_count):
    self._dice_count = dice_count  

  def roll_dice(self):
    self.hand = [random.randint(1, 6) for _ in range(self._dice_count)]
    self.hand.sort()

  def drop_hand(self):
    hand, self.hand = self.hand, None
    return hand 

  def decrease_dice(self):
    self._dice_count = max(0, self._dice_count - 1)

  @property
  def dice_count(self):
    return self._dice_count

  def bid(self, round, challenge_acceptable):
    raise NotImplementedError()


class User(Player):
  def __init__(self, ui):
    super().__init__('User')
    self.ui = ui

  def roll_dice(self):
    super().roll_dice()
    self.ui.peek_hand(self.hand)

  def bid(self, round, challenge_acceptable=False):
    return self.ui.prompt_bid(challenge_acceptable)


class Bot(Player):
  def __init__(self, name, strategy):
    super().__init__(name)
    self.strategy = strategy

  @property
  def capabilities(self):
    return self.strategy.capabilities

  def roll_dice(self):
    super().roll_dice()
    self.strategy.peek_hand(self.hand)

  def bid(self, round, challenge_acceptable=False):
    return self.strategy.bid(round, challenge_acceptable)
