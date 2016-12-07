from kmeans import KMeans
from Evaluation import *
from Network import *
from math import sqrt
import Similarity
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

# def write_file(filename, circle_list, test=False):
#     """
#     function to output the files, not using when testing
#     """
#     f = open(filename, 'w+')
#     f.write('UserId, Predicted\n')
#     # 
#     for person, circles in circle_list.iteritems():
#         line = person + ','
#         if not test:
#             # for circle in circles
#             for i in range(len(circles)):
#                 # for friends in circle
#                 for j in range(len(circles[i])):
#                     line += circles[i][j]
#                     if j != len(circles[i]) - 1:
#                         line += ' '
#                 if i != len(circles) - 1:
#                     line += ';'
#         else:
#             for friend in circles:
#                 line += friend + ' '
#             line += ';'
#         line += '\n'
#         f.write(line)

#     f.close()



if __name__ == '__main__':
    """
    main function for calculating communities
    """
    # construct the network structure 
    print 'Testing data in /{} folder...'.format(TEST)
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
    evaluate({k:training_clusters[k] for k in data.training_data})

    # # function for 
    # testingPeople = [origPerson for origPerson in data.central if origPerson
    #         not in person_training]
    
    # write_file(real_training_data, data.trainingMap)
    #
    #
    # # Validation tests
    # write_file(kmeans_attrs, {k:attribute_clusters[k] for k in data.trainingMap})
    # write_file(kmeans_attrs_friends, {k:attribute_and_friendship_clusters[k] for k in data.trainingMap})
    # write_file(kmeans_weighted_attrs_friends, {k:weighted_attribute_and_friendship_clusters[k] for k in data.trainingMap})
    # # Kaggle submissions
    # write_file(kmeans_kaggle_attrs, {k:attribute_clusters[k] for k in
    #     data.central if k not in data.trainingMap})
    # write_file(kmeans_kaggle_attrs_friends,
    #         {k:attribute_and_friendship_clusters[k] for k in
    #             data.central if k not in data.trainingMap})
    #
    # write_file(kmeans_kaggle_weighted_attrs_friends,
    #         {k:weighted_attribute_and_friendship_clusters[k] for k in
    #             data.central if k not in data.trainingMap})
