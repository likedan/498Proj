from collections import defaultdict
import random
import sys

class KMeans(object):
    def __init__(self, persons=None, similarity_calculator=None):
        self._similarity_calculator = similarity_calculator
        self._persons = persons
    
    def _assignToClusters(self, data_points, centroids):
        clusters = defaultdict(list)
        
        #for all data points(friends in our case), findout which centroid they are most similar to
        #assign them to most similiar centroid
        for data_point in data_points:
            maximum_similarity = 0
            maximum_similarity_centroid = None
            for centroid in centroids:
                similarity = self._similarity_calculator(self._persons, data_point, centroid)
                if similarity > maximum_similarity:
                    maximum_similarity = similarity
                    maximum_similarity_centroid = centroid
            if maximum_similarity_centroid:
                clusters[maximum_similarity_centroid].append(data_point)
        
        #return the computed clusters
        return clusters
                
    def _trim_clusters(self, clusters, similarity_diff_threshold):
        for centroid in clusters:
            #compute maximum and minimum similarity from centroid for each circle/cluster
            minimum_similarity = sys.maxint
            maximum_similarity = -sys.maxint

            for friend in clusters[centroid]:
                similarity = self._similarity_calculator(self._persons, centroid, friend)
                if similarity < minimum_similarity:
                    minimum_similarity = similarity
                if similarity > maximum_similarity:
                    maximum_similarity = similarity
            similarity_difference_in_cluster = maximum_similarity - minimum_similarity

            if similarity_difference_in_cluster > similarity_diff_threshold:
                friends_to_remove = []
                for friend in clusters[centroid]:
                    similarity = self._similarity_calculator(self._persons, centroid, friend)
                    if similarity < maximum_similarity - similarity_diff_threshold:
                        friends_to_remove.append(friend)
                for friend_to_remove in friends_to_remove:
                    clusters[centroid].remove(friend_to_remove)
     
        return clusters
        
    def computeClusters(self, data_points, k, similarity_diff_threshold):
        data_points = list(data_points)
        centroids = []
        # choose random k points as seed
        if k > len(data_points):
            k = len(data_points)
        random.shuffle(data_points)
        for i in range(k):
            centroids.append(data_points[i])

        clusters = self._assignToClusters(data_points, centroids)
        
        return self._trim_clusters(clusters, similarity_diff_threshold)
        
    
    