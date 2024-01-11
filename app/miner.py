from efficient_apriori import apriori

class Miner:
    def __init__(self, algorithm, data, support_threshold, confidence_threshold, min_length=1, max_length=8):
        """
        Constructor method to initialise a Miner object that can be used for mining association
        rules. 

        Parameters:
            algorithm (str): algorithm to mine association rules ie. Apriori or FP-Growth. 
            data (2d list): 2 dimensional list containing transactional data. 
            support_threshold (int): support measures how frequently the items in the rule appear together. Set a threshold for this. 
            confidence_threshold (int): 
            
        Returns:
            tuple: A tuple containing the JSON success response and the HTTP status code 200.
        """
        self.algorithm=algorithm 
        self.data=data #2d list containing transactional data
        self.support_threshold=support_threshold
        self.confidence_threshold=confidence_threshold
        self.min_length=min_length
        self.max_length=max_length

    def mine_association_rules(self):
        if self.algorithm == 'apriori':
            self.mine_apriori()
        elif self.algorithm == 'fpgrowth': 
            self.mine_fpgrowth()
        else:
            raise ValueError("Algorithm not specified correctly.")

    def mine_apriori(self):
        """
        Method to mine association rules using the 'apriori' algorithm. The function takes in a dataset
        as argument along with metrics and returns a python dictionary containing the itemsets and rule
        results.

        Parameters:
            data (class attribute)
            data (list, optional): Additional data to be included in the response (default is an empty list).

        Returns:
            tuple: A tuple containing the JSON success response and the HTTP status code 200.
        """
        itemsets, rules = apriori(self.data, min_support=self.support_threshold,  min_confidence=self.confidence_threshold)
        
        # Need to ensure 'itemset' python dict returned by apriori()function is JSON conpatible by jsonify() function
        itemsets_json_compatible = {}
        for key, value in itemsets.items():
            new_dict = {}
            for itemset, count in value.items():
                # Join the tuple elements with a comma to create a string key instead of tuple which is returned by default by apriori()
                itemset_key = ','.join(itemset)
                new_dict[itemset_key] = count
            itemsets_json_compatible[key] = new_dict
        
        # Convert rule results to python dict that is JSON compatible by jsonify() function
        rule_results = []
        for rule in rules: 
            confidence = rule.confidence
            support = rule.support
            lift = rule.lift
            conviction = rule.conviction

            result = {
                "rule": str(rule), # Rule will be in the format Beer -> Wine. If Beer is bought, then it is likely that Wine is also bought.
                "lhs": rule.lhs, # Antecedent (IF part of the rule) = Beer in the above case
                "rhs": rule.rhs, # Consequent (THEN part of the rule) = Wine in the above case
                "confidence": confidence, 
                "support": support, # how often the items occur in the rule together in the set of data. Higher support = relevant
                "lift": lift, # Shows strength of association. Lift < 1 = B is less likely to be bought with A, Lift > 1 = B more likely to be bought with A, Lift of 1 = independent
                "conviction": conviction # Measure of strength of rule being incorrect. the < conviction = more chance of incorrect. 1 = no association
            }

            rule_results.append(result)
        
        result = {
            "itemsets": itemsets_json_compatible, 
            "rules": rule_results
        }

        return result
    
    def mine_fpgrowth(self):
        pass

    def calculate_lift(rule):
        lift = rule.support / (rule.lhs_support * rule.rhs_support)
        return lift

    def calculate_conviction(self, rule): 
        if rule.confidence == 1: 
            return -1
        else: 
            conviction = (1 - rule.rhs_support) / (1 - rule.confidence)
            return conviction






