import os
import time
import logging as log

from database import Database
from game import Game
import models

class Main:
	"""
	Entry point of the simulation
	"""

	def __init__(self):
		self._init_logger()
		
		self.db = Database('localhost', 'root', 'root', 'iSpy_features')
		self.cursor = self.db.cursor

		self.setup()

		start = time.time()

		self.simulate()

		end = time.time()

		log.info("Simulation complete! (Took %ds)", int(end - start))


	def simulate(self):
		"""
		Run the simulation
		"""

		log.info('Starting simulation')

		games_folder = os.getcwd() + '/Human_Games'

		wins = 0
		losses = 0
		num_questions = 0
		avg_win = 0
		avg_lose = 0
		questions_asked = {}
		question_answers = {}

		for number in range(16, 31):
			game = Game(self.db, number)
			#models.info(self.cursor, game)
			game_wins, game_losses, game_num_questions, game_win_avg, game_lose_avg, game_answers, game_questions = game.play()

			questions_asked[game.id] = game_questions
			question_answers = game_answers

			wins += game_wins
			losses += game_losses
			num_questions += game_num_questions
			# TODO: Are these averages correct?
			avg_win += game_win_avg
			avg_lose += game_lose_avg

			models.build(game, 3, questions_asked, question_answers)


	def setup(self):
		"""
		Perform optional pre-simulation tasks
		"""

		log.info('Performing setup')


	def _init_logger(self):
		log.basicConfig(level='DEBUG', format='[ %(levelname)-5.5s]  %(message)s')
		rootLogger = log.getLogger()

		fileFormatter = log.Formatter('%(asctime)s [ %(levelname)-5.5s]  %(message)s')
		fileHandler = log.FileHandler('log.txt')
		fileHandler.setFormatter(fileFormatter)
		rootLogger.addHandler(fileHandler)

		log.info('\n'*8 + '='*31 + '| NEW SIMULATION |' + '='*31 + '\n')


if __name__ == '__main__':
	Main()