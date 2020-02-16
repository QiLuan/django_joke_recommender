path  = 'joke_recommender/Jester/jokes/'
filename = 'init'

def getJokes():
	a = []
	l = len('<!--end of joke -->')
	for i in range(1, 101):
		file = path + 'init' + str(i) + '.html'
		with open(file, 'r') as f:
			s= f.read()
			i, j = s.find('<!--begin of joke -->'), s.find('<!--end of joke -->')
			a.append(s[i:j+l])

	return a