# prototype a recommender system
# idea is to combine user preference and popularity

def loadCosineMatrix():
    cosine = []
    with open('/jester/cosine.txt', 'r') as f:
        for line in f:
            if line == '':
                continue
            temp = line[:-1].split(',')
            cosine.append([float(a) for a in temp])
    return cosine

def loadAverage():
    average = []
    with open('/jester/average.txt', 'r') as f:
        for line in f:
            if line == '':
                continue
            temp = line.split(',')
            average.append([float(a) for a in temp])
    return average[0]

def normalize(l):
    if not l:
        return []
    mean = float(sum(l))/len(l)
    var = sum([(a - mean)**2 for a in l])/len(l)
    if var < 1e-10:
        return [mean]*len(l)
    else:
        return [(a - mean)*var**-0.5 for a in l]

def recommender(d, num_rec = 5):
    # load cosine
    cosine = loadCosineMatrix()
    average = loadAverage()
    
    distScores = [0]*100
    jokeScores = [0]*100
    
    # rating history
    for joke in d.keys():
        rating = d[joke]
        sign = 1 if rating > 0 else -1
        coeff = sign * (abs(rating)/5.0)**0.5
        for i in range(100):
            distScores[i] += coeff*cosine[joke-1][i]
    
    average = normalize(average)
    distScores = normalize(distScores)
    
    for i in range(len(jokeScores)):
        jokeScores[i] += 0.2*average[i] + 0.8*distScores[i]
    
    jokeScores = sorted([(score, i+1) for i, score in enumerate(jokeScores) if i+1 not in d], reverse = True)
    
    return [t[1] for t in jokeScores[:num_rec]]