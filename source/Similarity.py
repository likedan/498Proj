class Similarity(object):
    """ 
    similarity class that calculating the similarity
    """
    def __init__(self, feature_num):
        """
        initialize the similarity calculator
        """
        self.feature_num = feature_num

    def weighted_network(self, people, person_0, person_1):
        """
        function that calculating the weighted network
        """
        # calculate the weight
        weight = 2.5
        similarity = 0.0
        friend_0 = people.find_person(person_0)
        friend_1 = people.find_person(person_1)
        for key in friend_0.features:
            if friend_0.features.get(key, None) == friend_1.features.get(key, None):
                similarity += 1.0

        # normalize the similarity
        similarity = (similarity/float(self.feature_num))*10
        # assign the weight
        if person_1 in friend_0.friends:
            similarity += weight
        return similarity