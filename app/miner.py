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
        itemsets = pyfpgrowth.find_frequent_patterns(self.data, self.support_threshold)
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
        print(rules.items())

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
                support, lhs_support, rhs_support = self.calculate_lhs_and_rhs_support(itemsets, lhs, rhs)
                lhs_support = itemsets.get(lhs, 0)
                rhs_support = itemsets.get(rhs, 0)
                rule_support = min(lhs_support, rhs_support) # This is a simplification, adjust as needed

                # Convert tuple to list 
                lhs_list = list(lhs)
                rhs_list = []
                if isinstance(rhs, tuple):
                    rhs_list = list(rhs) 
                else:
                    rhs_list = [rhs]

                # Creating the rule string so it follows the same format as other algorithms
                rule_str = f"{{{', '.join(lhs_list)}}} -> {{{', '.join(rhs_list)}}} (conf: {confidence:.3f}, supp: {rule_support:.3f})"
                
                print(confidence)
                print(rhs_support)

                # Calculating conviction and lift metrics
                #lift = self.calculate_lift(confidence, rhs_support)
                #conviction = self.calculate_conviction(confidence, rhs_support)

                rule_dict = {
                    "confidence": confidence,
                    "lhs": lhs_list,
                    "rhs": rhs_list,
                    "rule": rule_str,
                    "support": rule_support,
                    #"lift": lift,
                    #"conviction": conviction
                }

                rule_results.append(rule_dict)

        return rule_results

    def calculate_lift(self, confidence, rhs_support):
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
            lift(A -> B) = confidence(A -> B) / rhs_support(B)
        """
        return confidence/rhs_support

    def calculate_conviction(self, confidence, rhs_support): 
        """
        Function to calculate the key metric 'conviction'. The function takes in as parameters:
        confidence (A -> B) and the rhs_support (B) to perform the calculation. The function
        returns the conviction value. Conviction # Measure of strength of rule being incorrect. 
        the < conviction = more chance of incorrect. 1 = no association

        Parameters:
            confidence (double)
            rhs_support (double)

        Returns:
            double: The calculated 'conviction' value. 

        Formula: 
            conviction(A -> B) = (1 - rhs_support(B)) / (1 - confidence(A -> B))
        """
        return (1 - rhs_support) / (1 - confidence)
    
    def calculate_lhs_and_rhs_support(self, itemsets, lhs, rhs): 
        support = 0
        lhs_support = 0
        rhs_support = 0
    
        # Calculating total number of transactions first
        number_of_transactions = 0

        for itemset in itemsets: 
            number_of_transactions += itemsets[itemset]

        # combining lhs and rhs to unique set. This is used for calculating 'support'
        lhs_set = set(lhs.split(","))
        rhs_set = set(rhs.split(","))
        set_combined = lhs_set.union(rhs_set)
        itemset_combined = ",".join(set_combined)

        # Calculating item support metric for lhs & rhs combined, lhs and rhs
        for itemset in itemsets: 
            if set_combined == itemset: 
                support = itemsets[itemset] / number_of_transactions
            if lhs == itemset: 
                lhs_support = itemsets[itemset] / number_of_transactions
            if rhs == itemset: 
                rhs_support = itemsets[itemset] / number_of_transactions
            if lhs_support != 0 and rhs_support != 0: 
                break

        return support, lhs_support, rhs_support

        
            






