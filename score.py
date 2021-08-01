
import os

HIGHSCORE_FILE = './data/data/HIGHSCORE.SCORE'
def make_file(file, data = ''):
	with open(file, 'w') as f:
		f.write(data)
	return True


def check_file(file, data_if_none = 0):
	if os.path.isfile(file):
		return True
	else:
		try:
			make_file(file, data_if_none)
			return True
		except  :
			return False
def read_file(file):
	with open(file, 'r') as f:
		return f.read()

class ScoreManager :
    @staticmethod
    def  is_highscore(score):
        previous = read_file(HIGHSCORE_FILE)
        try:
        	previous = int(previous)
        except :
        	make_file(HIGHSCORE_FILE,'0')
        	previous = 0
        if previous < score:
        	print(f'validating score : {score}   highscore : {previous}')
        	make_file(HIGHSCORE_FILE, str(score))
        	print('highscore !!\n')
        	return True
        else:
        	return False
    @staticmethod
    def get_highscore():
    	score = read_file(HIGHSCORE_FILE)
    	try:
    		score = int(score)
    	except:
    		make_file(HIGHSCORE_FILE, 0)
    		score = 0
    	return score
#print(PointManager.is_highscore(220))