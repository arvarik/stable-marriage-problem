#!/usr/bin/env python3

"""
simulations.py

A script to execute some simulations related to the classic implementation of the stable marriage problem algorithm
"""
import matplotlib.pyplot as plt

from distribution.stable_marriage_problem_distribution import Community
from pandas import DataFrame
from statistics import mean
from time import time


def execute_simulations(starting_num, increment, num_data_points):
    data = {}

    for i in range(starting_num, starting_num*num_data_points, increment):
        start = time()
        stats = {
            'Iterations': [],
            'Male Index': [],
            'Female Index': [],
            'Male Advantage': []
        }
        for j in range(10):
            com = Community(i)
            com.run_stable_marriage_algorithm()

            stats['Iterations'].append(com.iterations)

            average_male_index, average_female_index = com.get_average_index()
            male_advantage = average_female_index - average_male_index
            percentage_advantage = (male_advantage * 100) / float(i - 1)

            # The average rank of every guy's partner from their preferences list
            stats['Male Index'].append(average_male_index)
            # The average rank of every girl's partner from their preference list
            stats['Female Index'].append(average_female_index)

            # Male advantage (may be negative) based on if going from least to most desirable is a 100% gain
            stats['Male Advantage'].append(percentage_advantage)

        final_stats = {}

        for key in stats:
            final_value = round(mean(stats[key]), 2)
            final_stats[key] = final_value

        data[i] = final_stats

        print("Finished 10 Simulations with a Community of {} people in {} seconds".format(i*2, time() - start))

    return DataFrame(data).T


def main():
    start = time()
    data = execute_simulations(starting_num=10, increment=10, num_data_points=101)  # From 10 to 1000 incrementing by 10
    print("Finished simulations in {} seconds".format(time() - start))

    plt.figure(figsize=(6, 6))

    plt.subplot(2, 1, 1)
    plt.plot(data['Iterations'], marker='1')
    plt.xlabel('Number of Pairings')
    plt.ylabel('Number of Algorithm Iterations')
    plt.title('Complexity of SMP Algorithm with Increased Community Size')

    plt.subplot(2, 1, 2)
    plt.plot(data['Male Advantage'], color='r', marker='1')
    plt.xlabel('Number of Pairings')
    plt.ylabel('Percent Male Advantage')
    plt.title('Male Preference Advantage with Increased Community Size')

    plt.tight_layout()
    plt.show()
    plt.clf()


if __name__ == '__main__':
    main()
