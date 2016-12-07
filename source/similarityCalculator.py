
class SimilarityCalculator(object):
    def __init__(self, featureCount):
        self.featureCount = featureCount

    def similarity_weighted_attributes_friendship(self, people, friend1ID, friend2ID):
        FRIENDSHIP_WEIGHT = 2.5
        similarity = 0.0
        friend1 = people.getPerson(friend1ID)
        friend2 = people.getPerson(friend2ID)
        for key in friend1.features:
            if friend1.features.get(key, None) == friend2.features.get(key, None):
                similarity += 1.0

        #normalize
        similarity = (similarity/float(self.featureCount))*10

        if friend2ID in friend1.friends:
            similarity += FRIENDSHIP_WEIGHT

        return similarity