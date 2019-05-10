# code that is meant to place people at a round table
# depends on how much a person wants to sit to another (from 0 to 1)

# the peoples used in this file are hypothetical, and nothing is really real, please don't take seriously
file = open('data.csv','r') # open data file
data = file.read()
file.close()

data = data.split('\n')
data = [i.split(',') for i in data]

names = data[0] # first line is names
data.pop(0)

print(data)
data = [[float(j) for j in i] for i in data] # put values in a table

number = len(names)


# initialize a huge array of relationships (fill it with -1.0)
relationsRaw = []
for i in range(number):
    relationsRaw.append([])
    for j in range(number):
        relationsRaw[i].append(-1.0)


# calculate relations strength
for a in range(number):
    for b in range(a+1, number):
        buffer = [data[a][b], data[b][a]]  # get how much a like b and b like a
        average = (buffer[0] + buffer[1]) / 2 # make the average
        consistencyFactor = min(buffer) / max(buffer) # if difference is high, lower strength
        strength = average
        relationsRaw[a][b] = strength

# calculate how placable a person is
placability = []
for a in range(number):
    value = 0
    # get relation strength
    for b in range(1, number):
        if relationsRaw[a][b] == -1:
            value += relationsRaw[b - 1][a]
            # print('here', names[a], names[b-1], relationsRaw[b-1][a])
        else:
            value += relationsRaw[a][b]
    value = value/(number-1) # make an average
    placability.append([a, value])
placability = sorted(placability, key=lambda x:x[1], reverse=False)


# formatted version of relations
relations = []
for a in range(number):
    for b in range(a+1, number):
        relations.append([[a, b], relationsRaw[a][b]])


def getRelationStrength(x, y):
    couple = [x, y]
    couple = [min(couple), max(couple)]
    try:
        return relations[[i[0] for i in relations].index(couple)][1]
    except ValueError:
        return -1


placabilityBuffer = placability.copy()
person = placabilityBuffer[0][0]
map = [person] # place least placable person first
placabilityBuffer.pop(0)


for i in range(number-1):
    person = placabilityBuffer[0][0]
    satisfaction = []
    satisfaction.append([0, getRelationStrength(person, map[0])])
    for j in range(len(map)-1):
        value = (getRelationStrength(map[j], person) + getRelationStrength(map[j+1], person)) / 2 # average of satisfaction of left and right
        value /= getRelationStrength(map[j], map[j+1]) # divide by satisfaction tat is broken
        satisfaction.append([j + 1, value])

    value = (getRelationStrength(map[len(map)-1], person) + getRelationStrength(map[0], person)) / 2 # circle, do it with first guy
    value /= getRelationStrength(map[len(map)-1], map[0])
    satisfaction.append([len(map)-1, value])

    satisfaction = sorted(satisfaction, key=lambda x:x[1], reverse=True)
    map.insert(satisfaction[0][0], person)
    placabilityBuffer.pop(0)

for i in map:
    print(names[i])
