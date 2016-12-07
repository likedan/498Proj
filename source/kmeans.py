from collections import defaultdict
import random
import sys

class KMeans(object):
    def __init__(self, people=None, similarity_calculator=None):
        self.similarity_calculator = similarity_calculator
        self.people = people

    #compute the kmeans
    def fit(self, data_points, k, similarity_diff_threshold):
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

    #assign each data point to the most similiar centroid
    def _assignToClusters(self, data_points, centroids):
        clusters = defaultdict(list)
        
        for point in data_points:
            maximum_similarity = 0
            maximum_similarity_centroid = None
            for centroid in centroids:
                similarity = self.similarity_calculator(self.people, point, centroid)
                if similarity > maximum_similarity:
                    maximum_similarity = similarity
                    maximum_similarity_centroid = centroid
            if maximum_similarity_centroid:
                clusters[maximum_similarity_centroid].append(point)
        
        #return the computed clusters
        return clusters

    # compute maximum and minimum similarity from centroid for each ccluster
    def _trim_clusters(self, clusters, similarity_diff_threshold):
        for centroid in clusters:
            min_sim = sys.maxint
            max_sim = -sys.maxint

            for friend in clusters[centroid]:
                similarity = self.similarity_calculator(self.people, centroid, friend)
                if similarity < min_sim:
                    min_sim = similarity
                if similarity > max_sim:
                    max_sim = similarity
            similarity_difference_in_cluster = max_sim - min_sim

            if similarity_difference_in_cluster > similarity_diff_threshold:
                friends_to_remove = []
                for friend in clusters[centroid]:
                    similarity = self.similarity_calculator(self.people, centroid, friend)
                    if similarity < max_sim - similarity_diff_threshold:
                        friends_to_remove.append(friend)
                for friend_to_remove in friends_to_remove:
                    clusters[centroid].remove(friend_to_remove)
     
        return clusters
        
    
    