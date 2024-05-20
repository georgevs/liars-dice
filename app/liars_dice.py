from game import Game, Config as GameConfig
from players import Players, Bot, User
from strategies import DumbStrategy
from ui import Ui, Config as UiConfig
import random
import signal


def main(config):
  app = App(config)
  app.liars_dice()


class App:
  def __init__(self, config):
    self.config = config
    self.ui = Ui(config.ui)
    self.strategies = [DumbStrategy()]
    def handle_sigint(signum, frame):
      self.ui.handle_sigint()
    signal.signal(signal.SIGINT, handle_sigint)

  def liars_dice(self):
    players = self.establish_players()
    random.shuffle(players)
    
    continue_play = True
    while continue_play:
      game = Game(self.ui, self.config.game)
      game.play(Players(players))
      continue_play = self.ui.prompt_continue_play()

  def establish_players(self):
    bots = [Bot(f'Bot-{i+1}', random.choice(self.strategies)) for i in range(self.config.game.num_bots)]
    user = User(self.ui)
    return bots + [user]


class Config:
  def __init__(self, args):
    self.game = GameConfig(args)
    self.ui = UiConfig(args)


if __name__ == '__main__':
  import argparse
  
  parser = argparse.ArgumentParser()
  parser.add_argument('--num-bots', type=int, default=1)
  parser.add_argument('--show-hands-at-settlement', action='store_true')
  args = parser.parse_args()
  config = Config(args)
  
  main(config)
