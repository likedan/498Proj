class Evaluation:
    """
    evaluation function
    """
    def __init__(self, network_prejaccard_dicttion, network):
        """
        initialize the variables
        """
        self.network_prejaccard_dicttion = network_prejaccard_dicttion
        self.network = network
        self.jaccard_dict = {}

    def calculate_jaccard(self, a, b):
        """
        calculate the jaccard similarity for input a and b
        """
        if a in self.jaccard_dict:
            if b in self.jaccard_dict[a]:
                return self.jaccard_dict[a][b]
        anb = a.intersection(b)
        result = float(len(anb)) / float(len(a) + len(b) - len(anb))
        if a not in self.jaccard_dict:
            self.jaccard_dict[a] = {}
        if b not in self.jaccard_dict:
            self.jaccard_dict[b] = {}
        self.jaccard_dict[a][b] = result
        self.jaccard_dict[b][a] = result
        return result

    def get_score(self):
        """
        calculate the overall accuracy
        """
        detected = [frozenset([j for j in x]) for x in self.network_prejaccard_dicttion]
        truth = [frozenset([j for j in x]) for x in self.network]

        # calculate prediction
        first = 0
        for d in detected:
            cur = -1
            for t in truth:
                cur = max(cur, self.calculate_jaccard(d, t))
            first += cur
        first = 1.0 / float(2.0 * len(detected)) * first

        # calculate ground truth
        second = 0
        for t in truth:
            cur = -1
            for d in detected:
                cur = max(cur, self.calculate_jaccard(t, d))
            second += cur
        second = 1.0 / float(2.0 * len(truth)) * second

        result = first + second
        return result
