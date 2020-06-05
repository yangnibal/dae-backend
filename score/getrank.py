from scipy.stats import norm

def getPercent(score, average, std_dev):
    percent = 1 - norm.cdf(float(score), loc=float(average), scale=float(std_dev))
    percent = percent * 100
    percent = round(percent, 1)
    return percent

def getRank(percent, cand_num):
    percent = round(percent/100, 2)
    rank = int(cand_num) * percent
    return rank

def getRating(percent):
    if 0 < percent <= 4:
        return 1
    elif 4 < percent <= 11:
        return 2
    elif 11 < percent <= 23:
        return 3
    elif 23 < percent <= 40:
        return 4
    elif 40 < percent <= 60:
        return 5
    elif 60 < percent <= 77:
        return 6
    elif 77 < percent <= 89:
        return 7
    elif 89 < percent <= 96:
        return 8
    elif 96 < percent <= 100:
        return 9

def getZ(score, average, std_dev):
    z = (float(score) - float(average))/float(std_dev)
    z = round(z, 2)
    return z

def getProbDens(z):
    prob_dens = norm.pdf(z)
    prob_dens = round(prob_dens, 3)
    return prob_dens