from game import Game, Config as GameConfig
from players import Players, Bot, User
from strategies import DumbStrategy, Config as StrategyConfig
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
    self.strategies = [DumbStrategy(config.strategy)]
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
      continue_play = not self.config.game.no_user and self.ui.prompt_continue_play()

  def establish_players(self):
    bots_count = (
      max(2, self.config.game.bots_count) if self.config.game.no_user
      else max(1, self.config.game.bots_count)
    )
    bots = [Bot(f'Bot-{i+1}', random.choice(self.strategies)) for i in range(bots_count)]
    return bots if self.config.game.no_user else (bots + [User(self.ui)])


class Config:
  def __init__(self, args):
    self.strategy = StrategyConfig(args)
    self.game = GameConfig(args)
    self.ui = UiConfig(args)


if __name__ == '__main__':
  import argparse
  
  parser = argparse.ArgumentParser()
  parser.add_argument('--bot-level', type=int, default=0)
  parser.add_argument('--bots-count', type=int, default=1)
  parser.add_argument('--no-user', action='store_true')
  parser.add_argument('--show-hands-at-settlement', action='store_true')
  parser.add_argument('--show-bots-capabilities', action='store_true')
  parser.add_argument('--wild-mode', action='store_true')
  args = parser.parse_args()
  config = Config(args)
  
  main(config)
