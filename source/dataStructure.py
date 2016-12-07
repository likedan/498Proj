import collections
import os

class DataStructure:
    def __init__(self):
        self.friendsDict, self.originalPeople, self.people = self.loadEgoNets('egonets')
        self.featuresDict = self.loadFeatures('features.txt', self.people)
        self.featureList = self.loadFeatureList('featureList.txt')
        self.trainingDict = self.loadTrainingData('training')

    def loadEgoNets(self, directory):
        friendMap = collections.defaultdict(set)
        originalPeople = []
        persons = People()

        for egonetFile in os.listdir(directory):

            currentPerson = egonetFile[:egonetFile.find('.')]
            originalPeople.append(currentPerson)
            persons.originalPeople.append(currentPerson)

            egonetFilePath = os.path.join(directory, egonetFile)

            for line in open(egonetFilePath):
                line = line.strip().split(':')
                currentFriend = line[0]

                friendMap[currentPerson].add(currentFriend)
                friendMap[currentFriend].add(currentPerson)
                persons.getPerson(currentPerson).addFriend(currentFriend)
                persons.getPerson(currentFriend).addFriend(currentPerson)

                friends = line[1].strip().split()

                for friend in friends:
                    friendMap[currentFriend].add(friend)
                    friendMap[friend].add(currentFriend)
                    persons.getPerson(currentFriend).addFriend(friend)
                    persons.getPerson(friend).addFriend(currentFriend)

                    friendMap[currentPerson].add(friend)
                    friendMap[friend].add(currentPerson)
                    persons.getPerson(currentPerson).addFriend(friend)
                    persons.getPerson(friend).addFriend(currentPerson)

        return friendMap, originalPeople, persons

    def loadTrainingData(self, directory):
        trainingMap = collections.defaultdict(list)

        for trainingFile in os.listdir(directory):
            currentPerson = trainingFile[:trainingFile.find('.')]

            trainingFilePath = os.path.join(directory, trainingFile)
            for line in open(trainingFilePath):
                parts = line.strip().split()
                trainingMap[currentPerson].append(parts[1:])

        return trainingMap

    def loadFeatures(self, filename, persons=None):
        featureMap = collections.defaultdict(dict)
        for line in open(filename):
            parts = line.strip().split()
            currentPerson = parts[0]
            for part in parts[1:]:
                key = part[0:part.rfind(';')]
                value = part[part.rfind(';') + 1:]
                featureMap[currentPerson][key] = value
                if persons != None:
                    persons.getPerson(currentPerson).features[key] = value
        return featureMap

    def loadFeatureList(self, filename):
        featureList = []
        for line in open(filename):
            featureList.append(line.strip())
        return featureList


class Person(object):
    def __init__(self, personID):
        self.personID = personID
        self.friends = set()
        self.features = {}

    def addFriend(self, friendID):
        return self.friends.add(friendID)


class People(object):
    def __init__(self):
        self.people = {}
        self.originalPeople = []

    def getPerson(self, person_ID):
        if person_ID not in self.people:
            self.people[person_ID] = Person(person_ID)

        return self.people[person_ID]