
class SimilarityCalculator(object):
    def __init__(self, featureCount):
        self.featureCount = featureCount
       
    def similarity_weighted_attributes_friendship(self, persons, friend1ID, friend2ID):
        FRIENDSHIP_WEIGHT = 2.5
        similarity = 0.0
        
        friend1 = persons.getPerson(friend1ID)
        friend2 = persons.getPerson(friend2ID)
        
        for key in friend1.getFeatures():
            friend1Value = friend1.getFeature(key)
            friend2Value = friend2.getFeature(key)
            if friend1Value == friend2Value:
                similarity += 1.0
                
        #normalize
        similarity = (similarity/float(self.featureCount))*10
        
        #consider friendship 
        if friend1.isFriend(friend2ID):
            similarity += FRIENDSHIP_WEIGHT        
        
        return similarity