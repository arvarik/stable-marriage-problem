#!/usr/bin/env python3

"""
Stable Marriage Problem
https://en.wikipedia.org/wiki/Stable_marriage_problem

This is the classic implementation of the Stable Marriage Problem
"""

import random
import names

from statistics import mean


class Person:
    """
    Representation of a person, including data about their gender, name, availability and whom they prefer of the
    opposite gender.

    A group of Persons will be represented as a community
    """
    def __init__(self, gender, name, is_available, preference_list):
        self.gender = gender
        self.name = name
        self.is_available = is_available
        self.preference_list = preference_list
        self.proposed_by = []  # This field will only be relevant to the gender getting proposed

    def __repr__(self):
        return self.name

    def print_person(self):
        available = "is available" if self.is_available else "is not available"
        print("{}: {} {} => {}".format(self.gender, self.name, available, self.preference_list))


class Pairing:
    """
    Representation of two Person objects that have been matched, either temporary or permanent
    """
    def __init__(self, guy, girl):
        self.guy = guy
        self.girl = girl

    def __repr__(self):
        return "({}, {})".format(self.guy.name, self.girl.name)


class Community:
    """
    A Community is a grouping of Person objects with additional functionality to help ship them according to their
    preference lists and the rules of the stable marriage problem algorithm
    """
    def __init__(self, num_gender):
        self.num_gender = num_gender
        self.guys = {}
        self.girls = {}

        guy_names = set()
        girl_names = set()

        # Set the people's names - the while loops are necessary in order to get unique names
        while len(guy_names) < num_gender:
            guy_names.add(names.get_first_name(gender='male'))
        while len(girl_names) < num_gender:
            girl_names.add(names.get_first_name(gender='female'))

        # Converting to lists to be able to shuffle them
        guy_names = list(guy_names)
        girl_names = list(girl_names)

        # Set the people in the community
        for guy_name in guy_names:
            sc_girls = girl_names[:]  # Need to make a shallow copy here to avoid side effects with Random module
            random.shuffle(sc_girls)
            self.guys[guy_name] = Person('M', guy_name, True, sc_girls)
        for girl_name in girl_names:
            sc_guys = guy_names[:]
            random.shuffle(sc_guys)
            self.girls[girl_name] = Person('F', girl_name, True, sc_guys)

        # Initially no one is matched up yet
        self.pairs = {}
        self.is_everyone_paired = False
        self.iterations = 0

    def print_community(self):
        for guy in self.guys:
            self.guys[guy].print_person()

        for girl in self.girls:
            self.girls[girl].print_person()

    def print_pairs(self):
        print(self.pairs.values())

    def get_first_available_guy(self):
        for guy_name in self.guys.keys():
            if self.guys[guy_name].is_available:
                return guy_name
        return None

    def run_stable_marriage_algorithm(self):
        available_guy_name = self.get_first_available_guy()
        iterations = 0
        while available_guy_name is not None:
            available_guy = self.guys[available_guy_name]
            proposed_girl = None  # Setting a dummy initialization, it must get reassigned in the following loop

            for preference in available_guy.preference_list:  # Going in order from highest preference to lowest
                if available_guy_name not in self.girls[preference].proposed_by:
                    # Found highest preference girl that hasn't been proposed to
                    proposed_girl = self.girls[preference]
                    proposed_girl.proposed_by.append(available_guy_name)
                    break

            if proposed_girl.is_available:
                proposed_girl.is_available = False
                available_guy.is_available = False
                # The key here is the girl's name in order to find other matches easier
                self.pairs[proposed_girl.name] = Pairing(available_guy, proposed_girl)
            else:
                # This means another guy is matched to the first preference girl
                other_guy = self.pairs[proposed_girl.name].guy
                proposed_girl_preference = proposed_girl.preference_list
                if proposed_girl_preference.index(available_guy_name) < proposed_girl_preference.index(other_guy.name):
                    other_guy.is_available = True
                    available_guy.is_available = False
                    self.pairs[proposed_girl.name] = Pairing(available_guy, proposed_girl)

            available_guy_name = self.get_first_available_guy()
            iterations += 1

        self.is_everyone_paired = True
        self.iterations = iterations

    def get_average_index(self):
        preference_indices_male = []
        preference_indices_female = []
        for pair in self.pairs:
            guy = self.pairs[pair].guy
            girl = self.pairs[pair].girl
            preference_indices_male.append(guy.preference_list.index(girl.name) + 1)  # Adding one for true ranking
            preference_indices_female.append(girl.preference_list.index(guy.name) + 1)

        average_male_index = mean(preference_indices_male)
        average_female_index = mean(preference_indices_female)\

        return average_male_index, average_female_index

    def stats(self):
        if not self.is_everyone_paired:
            print("Run the run_stable_marriage_algorithm first!")
        else:
            print("This stable marriage solution took {} iterations to complete.".format(self.iterations))
            male_index, female_index = self.get_average_index()
            print("In each pairing, the average girl ranking for a guy was {}.".format(male_index))
            print("In each pairing, the average guy ranking for a girl was {}.".format(female_index))

            if female_index > male_index:
                index_difference = female_index - male_index
                print("Therefore on average, guys got {} preference ranks higher than the girls."
                      .format(index_difference))
            else:
                index_difference = male_index - female_index
                print("Therefore on average, girls got {} preference ranks higher than the guys."
                      .format(index_difference))

            print("Based on the population of the community, this is {}% better"
                  .format(index_difference * 100 / float(self.num_gender - 1)))


def main():
    # Initialize the community with 10 people of either gender
    com = Community(10)

    # Show all the people in the community and their preferences
    com.print_community()

    # Run the stable marriage algorithm
    com.run_stable_marriage_algorithm()

    # Print out all the matching pairs from the algorithm result
    com.print_pairs()

    # Run the stats method to print out some accumulated stats from the stable marriage algorithm
    com.stats()


if __name__ == '__main__':
    main()
