from collections import defaultdict
from math import inf, sqrt
import random
import csv


def point_avg(points):
    """
    Accepts a list of points, each with the same number of dimensions.
    (points can have more dimensions than 2)
    
    Returns a new point which is the center of all the points.
    """
    
    sum_of_points = [sum(x) for x in zip(*points)]
    num = len(points)
    if(num <= 0):
        raise ValueError("Number of points should be greater than 0.")
    return  [x / num for x in sum_of_points] 

def update_centers(data_set, assignments):
    """
    Accepts a dataset and a list of assignments; the indexes 
    of both lists correspond to each other.
    Compute the center for each of the assigned groups.
    Return `k` centers in a list
    """
    
    #Finding value of k
    unique_assignments_list = list(set(assignments))
    k = len(unique_assignments_list)

    if(k <= 0):
        raise ValueError("k should be greater than 0.")

    list_of_clusters = {}
    cluster_sizes = [0]*k

    for data, assignment in zip(data_set, assignments):
        if assignment not in list_of_clusters:
            list_of_clusters[assignment] = []
        list_of_clusters[assignment].append(data)

    centers = []
    for key, values in list_of_clusters.items():
        centers.append(point_avg(values))
    
    return centers
    

def assign_points(data_points, centers):
    """
    Finds the center with the shortest distance to each point
    """
    assignments = []
    for point in data_points:
        shortest = inf  # positive infinity
        shortest_index = 0
        for i in range(len(centers)):
            val = distance(point, centers[i])
            if val < shortest:
                shortest = val
                shortest_index = i
        assignments.append(shortest_index)
    return assignments


def distance(a, b):
    """
    Returns the Euclidean distance between a and b
    """

    sum_of_squares = 0

    for i,j in zip(a,b):
        sum_of_squares = sum_of_squares + pow(i-j, 2)
    distance = sqrt(sum_of_squares/len(a))

    return distance


def generate_k(data_set, k):
    """
    Given `data_set`, which is an array of arrays,
    return a random set of k points from the data_set
    """
    return random.sample(data_set, k)


def get_list_from_dataset_file(dataset_file):
    """
    Converting the data from file into list of points
    """
    data = []
    with open(dataset_file) as csvfile:
        reader = csv.reader(csvfile)
        data = list(list(point) for point in csv.reader(csvfile, delimiter=','))

    #Converting to float values
    data  = [[float(y) for y in x] for x in data]
    return data
        



def cost_function(clustering):
    """
    Calculating the total cost (sum of Euclidean distances from centroid) for each cluster
    """
    total_cost = 0
    for cluster, points in clustering.items():
        centroid = point_avg(points)
        for point in points:
            total_cost = total_cost + distance(centroid, point)
    return total_cost


def k_means(dataset_file, k):
    """
    Running K-means
    """
    dataset = get_list_from_dataset_file(dataset_file)
    k_points = generate_k(dataset, k)
    assignments = assign_points(dataset, k_points)
    old_assignments = None
    while assignments != old_assignments:
        new_centers = update_centers(dataset, assignments)
        old_assignments = assignments
        assignments = assign_points(dataset, new_centers)
    clustering = defaultdict(list)
    for assignment, point in zip(assignments, dataset):
        clustering[assignment].append(point)
    return clustering
