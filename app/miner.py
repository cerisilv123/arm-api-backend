import pyfpgrowth

from efficient_apriori import apriori

class Miner:
    def __init__(self, algorithm, data, support_threshold, confidence_threshold):
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

    def mine_association_rules(self):
        """
        Method that checks the algorithm attribute and calls the correct method to mine
        association rules. 

        Parameters:
            None

        Returns:
            None

        Error handling: 
            Raises a ValueError if algorithm not specified correctly on object creation. 
        """
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

        Returns:
            tuple: A tuple containing the JSON success response and the HTTP status code 200.
        """
        itemsets, rules = apriori(self.data, min_support=self.support_threshold,  min_confidence=self.confidence_threshold)

        # Need to ensure 'itemset' python dict returned by apriori()function is JSON conpatible by jsonify() function
        itemsets_json_compatible = self.convert_itemsets_to_json_compatible(itemsets)
        
        # Convert rule results to python dict that is JSON compatible by jsonify() function
        rule_results = self.convert_rules_to_json_format(itemsets, rules)
        
        result = {
            "itemsets": itemsets_json_compatible, 
            "rules": rule_results
        }

        return result
    
    def mine_fpgrowth(self):
        """
        Method to mine association rules using the 'fpgrowth' algorithm. The method uses the data attribute
        along with metrics and returns a python dictionary containing the itemsets and rule results.

        Parameters:
            data (class attribute)

        Returns:
            tuple: A tuple containing the JSON success response and the HTTP status code 200.
        """
        support_threshold_fpgrowth = self.support_threshold * 10
        itemsets = pyfpgrowth.find_frequent_patterns(self.data, support_threshold_fpgrowth)
        rules = pyfpgrowth.generate_association_rules(itemsets, self.confidence_threshold)

        # Convert rule results to python dict that is JSON compatible by jsonify() function
        rule_results = self.convert_rules_to_json_format(itemsets, rules)

        # Need to ensure 'itemset' python dict returned by frpgrowth()function is JSON conpatible by jsonify() function
        itemsets_json_compatible = self.convert_itemsets_to_json_compatible(itemsets)


        result = {
            "itemsets": itemsets_json_compatible, 
            "rules": rule_results
        }

        return result
    
    def convert_itemsets_to_json_compatible(self, itemsets): 
        itemsets_json_compatible = {}

        if self.algorithm == 'apriori': 
            for key, value in itemsets.items():
                new_dict = {}
                for itemset, count in value.items():
                    # Join the tuple elements with a comma to create a string key instead of tuple which is returned by default by apriori()
                    itemset_key = ','.join(itemset)
                    new_dict[itemset_key] = count
                itemsets_json_compatible[key] = new_dict
        elif self.algorithm == 'fpgrowth': 
            new_dict = {}
            for key, value in itemsets.items():
                # Join the tuple elements with a comma to create a string key instead of tuple which is returned by default by apriori()
                itemset_key = ','.join(key)
                new_dict[itemset_key] = value
            itemsets_json_compatible = new_dict

        return itemsets_json_compatible
    
    def convert_rules_to_json_format(self, itemsets, rules):
        rule_results = []

        if self.algorithm == 'apriori': 
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
                
        elif self.algorithm == 'fpgrowth':
            for lhs, (rhs, confidence) in rules.items():
                # Calculate support for the rule (you might need to adjust this calculation based on your specific needs)
                support, lhs_support, rhs_support = self.calculate_support_values(itemsets, lhs, rhs)

                # Convert tuple to list 
                lhs_list = list(lhs)
                rhs_list = []
                if isinstance(rhs, tuple):
                    rhs_list = list(rhs) 
                else:
                    rhs_list = [rhs]                

                # Calculating conviction and lift metrics
                lift = self.calculate_lift(support, lhs_support, rhs_support)
                conviction = self.calculate_conviction(confidence, rhs_support)

                # Creating the rule string so it follows the same format as other algorithms
                rule_str = f"{{{', '.join(lhs_list)}}} -> {{{', '.join(rhs_list)}}} (conf: {confidence:.3f}, supp: {support:.3f}, lift: {lift:.3f}, conv: {conviction:.3f})"

                rule_dict = {
                    "confidence": confidence,
                    "lhs": lhs_list,
                    "rhs": rhs_list,
                    "rule": rule_str,
                    "support": support,
                    "lift": lift,
                    "conviction": conviction
                }

                rule_results.append(rule_dict)

        return rule_results

    def calculate_lift(self, support, lhs_support, rhs_support):
        """
        Function to calculate the key metric 'lift'. The function takes in as parameters:
        confidence (A -> B) and the rhs_support (B) to perform the calculation. The function
        returns the lift value. Lift shows strength of association. Lift < 1 = B is less 
        likely to be bought with A, Lift > 1 = B more likely to be bought with A, Lift of 1 = independent

        Parameters:
            confidence (double)
            rhs_support (double)

        Returns:
            double: The calculated 'lift' value. 

        Formula: 
            lift(A -> B) = support(A -> B) / (support(A) * support(B))
        """
        if support == 0 or rhs_support == 0 or lhs_support == 0: 
            return 0
        else: 
            return support / (lhs_support * rhs_support)

    def calculate_conviction(self, confidence, rhs_support): 
        """
        Function to calculate the key metric 'conviction'. The function takes in as parameters:
        confidence(A -> B) and the rhs_support(B) to perform the calculation. The function
        returns the conviction value. Conviction # Measure of strength of rule being incorrect. 
        the < conviction = more chance of incorrect. 1 = no association. It is important to note
        the method returns a positive infinity value if the confidence is 1. This is because a 
        confidence of 1 implies that the rule has perfect confidence. ie the RHS is always purchased 
        in a transaction when the LHS is purchased.

        Parameters:
            confidence (double)
            rhs_support (double)

        Returns:
            double: The calculated 'conviction' value. 

        Formula: 
            conviction(A -> B) = (1 - rhs_support(B)) / (1 - confidence(A -> B))
        """
        if 1 - confidence == 0: 
            return float('inf') 
        else: 
            return (1 - rhs_support) / (1 - confidence)
    
    def calculate_support_values(self, itemsets, lhs, rhs):     
        # Calculating total number of transactions first
        number_of_transactions = len(self.data)

        # combining lhs and rhs to tuple. This is used for calculating 'support'
        set_union = set(lhs + rhs)

        # Calculating item support metric for lhs & rhs combined, lhs and rhs
        support_count = 0
        lhs_count = 0
        rhs_count = 0
        for itemset in itemsets: 
            set_itemset = set(itemset)
            if set_union == set_itemset: 
                support_count += itemsets[itemset]
            if lhs == itemset: 
                lhs_count += itemsets[itemset]
            if rhs == itemset: 
                rhs_count += itemsets[itemset]

        support = support_count / number_of_transactions
        lhs_support = lhs_count / number_of_transactions
        rhs_support = rhs_count / number_of_transactions

        return support, lhs_support, rhs_support

        
            






