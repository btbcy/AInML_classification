# perceptron.py
# -------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# Perceptron implementation
import util
PRINT = True

class PerceptronClassifier:
    """
    Perceptron classifier.

    Note that the variable 'datum' in this code refers to a counter of features
    (not to a raw samples.Datum).
    """
    def __init__( self, legalLabels, max_iterations):
        self.legalLabels = legalLabels
        self.type = "perceptron"
        self.max_iterations = max_iterations
        self.weights = {}
        for label in legalLabels:
            self.weights[label] = util.Counter() # this is the data-structure you should use

    def setWeights(self, weights):
        assert len(weights) == len(self.legalLabels)
        self.weights = weights

    def train( self, trainingData, trainingLabels, validationData, validationLabels ):
        """
        The training loop for the perceptron passes through the training data several
        times and updates the weight vector for each label based on classification errors.
        See the project description for details.

        Use the provided self.weights[label] data structure so that
        the classify method works correctly. Also, recall that a
        datum is a counter from features to values for those features
        (and thus represents a vector a values).

        ## Something you might need to use:
        ## trainingData[i]: a feature vector, an util.Counter()
        ## trainingLabels[i]: label for each trainingData[i]
        ## self.weights[label]: weight vector for a label (class), an util.Counter()
        """

        self.features = trainingData[0].keys() # could be useful later
        # DO NOT ZERO OUT YOUR WEIGHTS BEFORE STARTING TRAINING, OR
        # THE AUTOGRADER WILL LIKELY DEDUCT POINTS.

        # from random import shuffle
        # training = {trainingLabels[i]:trainingData[i] for i in range(len(trainingData))}
        # shuffle(trainingLabels, lambda: 0)
        # trainingData = [training[trainingLabels[i]] for i in range(len(trainingLabels))]
        newWeights = util.Counter()
        correctNum = util.Counter()
        for iteration in range(self.max_iterations):
            print "Starting iteration ", iteration, "..."
            for i in range(len(trainingData)):
                "*** YOUR CODE HERE ***"
                # scores = util.Counter()
                # for label in self.legalLabels:
                #     scores[label] = self.weights[label] * trainingData[label]
                # guess = scores.argMax()
                feat = trainingData[i]
                guess = self.classify([feat])[0]
                if guess != trainingLabels[i]:
                    self.weights[trainingLabels[i]] += feat
                    self.weights[guess] -= feat

            correctNum[iteration] = 0
            guesses = self.classify(validationData)
            for y, y_Pr in zip(validationLabels, guesses):
                if y == y_Pr:
                    correctNum[iteration] += 1
            newWeights[iteration] = self.weights.copy()
        bestIteration = correctNum.argMax()
        self.weights = newWeights[bestIteration]


    def classify(self, data ):
        """
        Classifies each datum as the label that most closely matches the prototype vector
        for that label.  See the project description for details.

        Recall that a datum is a util.counter...
        """
        guesses = []
        for datum in data:
            vectors = util.Counter()
            for l in self.legalLabels:
                vectors[l] = self.weights[l] * datum
            guesses.append(vectors.argMax())
        return guesses


    def findHighWeightFeatures(self, label):
        """
        Returns a list of the 100 features with the greatest weight for some label

        ## Something you might need to use:
        ## self.weights[label]: weight vector for a label (class), an util.Counter()
        """
        featuresWeights = []

        "*** YOUR CODE HERE ***"
        featuresWeights = self.weights[label].sortedKeys()[:100]
        return featuresWeights
