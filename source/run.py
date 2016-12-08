from kmeans import KMeans
from Evaluation import *
from Network import *
from Weight import *
from math import sqrt
import Similarity
import shutil
import os
import sys


TEST = sys.argv[1]

def output(clusters):
    """
    the function to convert the format of clusters
    """
    clusters_output = {}
    for central in clusters:
        circles = []
        for centroid in clusters[central]:
            circles.append( clusters[central][centroid] )
        clusters_output[central] = circles
    return clusters_output

def evaluate(result):
    """
    the function to evaluate the communities with equation in CESNA
    """
    result = dict(result)
    total = 0.0
    for (person, data) in result.iteritems():
        person_network = []
        file_name = TEST+ "/" + person + ".circles"
        # reading the data
        with open(file_name) as f:
            for line in f:
                result = line.replace("\n", "")
                result_arr = result.split(" ")
                person_network.append(result_arr[1:])
        evaluate_obj = Evaluation(person_network, data)
        total += evaluate_obj.get_score()
    print 'Accuracy: {}'.format(total / float(len(result)))

def write_output(data):
    print 'Outputs in source/results/...'
    output_result = data
    if os.path.exists("results"):
        shutil.rmtree("results")
    os.mkdir("results")

    for key, values in dict(output_result).iteritems():
        file_name = "results/" + key + ".circles"
        f = open(file_name, 'w+')
        for value in values:
            line = "circle" + value[0] + ":"
            for id in value:
                line += " "
                line += id
            line += "\n"
            f.write(line)
        f.close()


if __name__ == '__main__':
    """
    main function for calculating communities
    """
    # construct the network structure 
    print 'Testing...'.format(TEST)
    data = Network(TEST)

    # parse all persons in training network
    person_training = []
    for central_person in data.training_data:
        person_training.append(central_person)
    
    # calculate similarity for communities
    similarity = Similarity.Similarity(len(data.feature_list))
    training_clusters = {}

    # implement k mean from scrath to calculate communities
    k_means = KMeans(data.people, similarity.weighted_network)
    for person in data.central:
        friends = data.people.find_person(person).friends
        #approximate number of centers
        k = int(sqrt(len(friends))) + 1
        clusters = k_means.computeClusters(friends, k, 3.5)
        training_clusters[person] = clusters
    training_clusters = output(training_clusters)

    # evaluate the communities with CESNA equation 8
    # evaluate({k:training_clusters[k] for k in data.training_data})
    write_output({k:training_clusters[k] for k in data.central})
