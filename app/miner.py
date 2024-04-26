import pyfpgrowth

from efficient_apriori import apriori

from app.apriori_ceri import AprioriCeri

class Miner:
    def __init__(self, algorithm, data, support_threshold, confidence_threshold=0.8):
        """
        Constructor method to initialise a Miner object that can be used for mining association
        rules. sets a default confidence of 0.8 is none is supplied.

        Parameters:
            algorithm (str): algorithm to mine association rules ie. Apriori or FP-Growth. 
            data (2d list): 2 dimensional list containing transactional data. 
            support_threshold (float): support measures how frequently the items in the rule appear together. Set a threshold for this. 
            confidence_threshold (float): confidence measures the reliability of a rule. It is the proportion of transactions containing A that also contains B. Set a threshold for this.

        Example: 
            transactions = [
                ['Milk', 'Bread', 'Butter'],
                ['Beer', 'Diapers'],
                ['Milk', 'Diapers', 'Beer', 'Cola'],
                ['Bread', 'Butter', 'Milk'],
                ['Bread', 'Milk'],
                ['Beer', 'Diapers'],
                ['Milk', 'Diapers', 'Bread', 'Butter'],
                ['Butter', 'Bread', 'Milk'],
                ['Beer', 'Cola'],
                ['Butter', 'Bread']
            ]

            miner = Miner(
                algorithm='fpgrowth',
                data=transactions,
                support_threshold=0.2,
                confidence_threshold=0.8,
            )
            
            result = miner.mine_fpgrowth()

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
            algorithm (class attribute)

        Returns:
            None

        Error handling: 
            Raises a ValueError if algorithm not specified correctly on object creation. 
        """
        if self.algorithm == 'apriori':
            return self.mine_apriori()
        elif self.algorithm == 'fpgrowth': 
            return self.mine_fpgrowth()
        elif self.algorithm == 'apriori-ceri':
            return self.mine_apriori_ceri()
        else:
            raise ValueError("Algorithm not specified correctly.")

    def mine_apriori(self):
        """
        Method to mine association rules using the 'apriori' algorithm. The function utilises 
        the data, support_threshold and confidence threshold class attributes. The method 
        returns a python dictionary containing the itemsets and rule results calculated by 
        the apriori algorithm.

        Parameters:
            data (class attribute)
            support_threshold (class attribute)
            confidence_threshold (class attribute)

        Methods: 
            self.convert_itemsets_to_json_compatible(itemsets)
            self.convert_rules_to_json_format(itemsets, rules)
        
        External class object: 
            apriori() from 'efficient_apriori' library

        Returns:
            results (dict): containing 'itemsets' and 'rules' produced by the apriori mining process.
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
        Method to mine association rules using the 'fpgrowth' algorithm. The function utilises 
        the data, support_threshold and confidence threshold class attributes. The method 
        returns a python dictionary containing the itemsets and rule results calculated by 
        the fpgrowth algorithm.

        Parameters:
            data (class attribute)
            support_threshold (class attribute)
            confidence_threshold (class attribute)

        Methods: 
            self.convert_itemsets_to_json_compatible(itemsets)
            self.convert_rules_to_json_format(itemsets, rules)
        
        External functions: 
            find_frequent_patterns() from 'pyfpgrowth' library
            generate_association_rules() from 'pyfpgrowth' library

        Returns:
            results(dict): containing 'itemsets' and 'rules' produced by the fpgrowth mining process.
        """
        # For the method 'find_frequent_patterns' support parameter is taken in as multiple of 10 (2 instead of 0.2)
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
    
    def mine_apriori_ceri(self):
        """
        Method to mine association rules using the 'apriori-ceri' algorithm which is a custom class. 
        The function utilises the data, support_threshold and confidence threshold class attributes. The method 
        returns a python dictionary containing the itemsets and rule results calculated by 
        the fpgrowth algorithm.

        Parameters:
            data (class attribute)
            support_threshold (class attribute)
            confidence_threshold (class attribute)

        Methods: 
            self.convert_itemsets_to_json_compatible(itemsets)
            self.convert_rules_to_json_format(itemsets, rules)
        
        External functions: 
            generate_association_rules() from 'pyfpgrowth' library. This is used to generate
            rules using the itemsets returned by apriori-ceri.

        Returns:
            results(dict): containing 'itemsets' and 'rules' produced by the apriori-ceri mining process.
        """
        support_threshold_apriori_ceri = self.support_threshold * 10
        apriori_ceri = AprioriCeri(self.data, support_threshold_apriori_ceri, self.confidence_threshold)
        itemsets = apriori_ceri.mine()
        rules = pyfpgrowth.generate_association_rules(itemsets, self.confidence_threshold)

        # Convert rule results to python dict that is JSON compatible by jsonify() function
        rule_results = self.convert_rules_to_json_format(itemsets, rules)

        # Need to ensure 'itemset' python dict returned by mine() function is JSON compatible by jsonify() function
        itemsets_json_compatible = self.convert_itemsets_to_json_compatible(itemsets)

        result = {
            "itemsets": itemsets_json_compatible, 
            "rules": rule_results
        }

        return result
    
    def convert_itemsets_to_json_compatible(self, itemsets): 
        """
        Method to convert a dict of itemsets to a format that is JSON compatible. 
        This means the dict needs to be serialisable by the 'jsonify()' function. 
        The default itemset dicts are returned in different formats for different 
        algorithms. Therefore coinditional statements are utilised to handle
        each algorithm accordingly. 

        Parameters:
            itemsets (dict)
            algorithm (class attribute)

        Returns:
            itemsets_json_compatible(dict): Containing the new itemsets dict that is now json compatible.
        """
        itemsets_json_compatible = {}

        if self.algorithm == 'apriori': 
            new_dict = {}
            for key, value in itemsets.items():
                for itemset, count in value.items():
                    # Join the tuple elements with a comma to create a string key instead of tuple which is returned by default by apriori()
                    itemset_key = ','.join(itemset)
                    new_dict[itemset_key] = count
            itemsets_json_compatible = new_dict
        elif self.algorithm == 'fpgrowth': 
            new_dict = {}
            for key, value in itemsets.items():
                itemset_key = ','.join(key)
                new_dict[itemset_key] = value
            itemsets_json_compatible = new_dict
        elif self.algorithm == 'apriori-ceri':
            new_dict = {}
            for key, value in itemsets.items():
                itemset_key = ', '.join(sorted(key))
                new_dict[itemset_key] = value
            itemsets_json_compatible = new_dict

        return itemsets_json_compatible
    
    def convert_rules_to_json_format(self, itemsets, rules):
        """
        Method to convert a dict of rules to a format that is JSON compatible. 
        This means the dict needs to be serialisable by the 'jsonify()' function. 
        The default rules dicts are returned in different formats for different 
        algorithms. Therefore coinditional statements are utilised to handle
        each algorithm accordingly. This ensures consistency in JSON bodies that are 
        returned for each algorithm meaning the 'client(frontend)' can handle multiple 
        algorithms in the same format.

        Parameters:
            itemsets (dict)
            rules (dict)
            algorithm (class attribute)

        Methods: 
            self.calculate_lift(): external libraries such as pyfpgrowth do not produce this metric. Must be calculated using class method.
            self.calculate_conviction(): external libraries such as pyfpgrowth do not produce this metric. Must be calculated using class method.

        Returns:
            rule_results(dict): Containing the new itemsets dict that is now json compatible.
        """
        rule_results = []

        if self.algorithm == 'apriori': 
            for rule in rules: 
                confidence = rule.confidence
                support = rule.support
                lift = rule.lift
                conviction = 1 if rule.conviction == float('inf') else rule.conviction

                result = {
                    "rule": str(rule), # Rule will be in the format Beer -> Wine. If Beer is bought, then it is likely that Wine is also bought.
                    "lhs": rule.lhs, # Antecedent (IF part of the rule) = Beer in the above case
                    "rhs": rule.rhs, # Consequent (THEN part of the rule) = Wine in the above case
                    "confidence": confidence, # confidence measures the reliability of a rule. It is the proportion of transactions containing A that also contains B. Set a threshold for this.
                    "support": support, # how often the items occur in the rule together in the set of data. Higher support = relevant
                    "lift": lift, # Shows strength of association. Lift < 1 = B is less likely to be bought with A, Lift > 1 = B more likely to be bought with A, Lift of 1 = independent
                    "conviction": conviction # Measure of strength of rule being incorrect. the < conviction = more chance of incorrect. 1 = no association
                }

                rule_results.append(result)
                
        elif self.algorithm == 'fpgrowth' or self.algorithm == 'apriori-ceri':
            for lhs, (rhs, confidence) in rules.items():
                # Calculate support for the rule (you might need to adjust this calculation based on your specific needs)
                support, lhs_support, rhs_support = self.calculate_support_values(itemsets, lhs, rhs)

                # Convert tuple to list for easier formatting of the rule string.
                lhs_list = list(lhs)
                rhs_list = []
                if isinstance(rhs, tuple):
                    rhs_list = list(rhs) 
                else:
                    rhs_list = [rhs]                

                # Calculating conviction and lift metrics using class method
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
        support(A -> B), lhs_support(A) and the rhs_support(B) to perform the calculation. The function
        returns the lift value. Lift shows strength of association. Lift < 1 = B is less 
        likely to be bought with A, Lift > 1 = B more likely to be bought with A, Lift of 1 = independent

        Parameters:
            support (float)
            lhs_support (float)
            rhs_support (float)

        Returns:
            float: The calculated 'lift' value. 

        Formula: 
            lift(A -> B) = support(A -> B) / (support(A) * support(B))

        Example: 
            result = miner.calculate_lift(0.4, 0.2, 0.6)
            print(result) // 3.333333333
        """
        if support == 0 or rhs_support == 0 or lhs_support == 0: 
            return 0
        else: 
            return support / (lhs_support * rhs_support)

    def calculate_conviction(self, confidence, rhs_support): 
        """
        Function to calculate the key metric 'conviction'. The function takes in as parameters:
        confidence(A -> B) and the rhs_support(B) to perform the calculation. The function
        returns the conviction value. Conviction is a measure of strength of the rule being incorrect. 
        the < conviction = more chance of incorrect. 1 = no association. It is important to note
        the method returns a positive infinity value if the confidence is 1. This is because a 
        confidence of 1 implies that the rule has perfect confidence. ie the RHS is always purchased 
        in a transaction when the LHS is purchased.

        Parameters:
            confidence (double)
            rhs_support (double)

        Returns:
            float: The calculated 'conviction' value. 

        Formula: 
            conviction(A -> B) = (1 - rhs_support(B)) / (1 - confidence(A -> B))

        Example: 
            result = miner.calculate_conviction(0.8, 0.6)
            print(result) // 2.00000000
        """
        if 1 - confidence == 0: 
            return 1
        else: 
            return (1 - rhs_support) / (1 - confidence)
    
    def calculate_support_values(self, itemsets, lhs, rhs):
        """
        Function to calculate the key metrics 'support, lhs_support and rhs_support'. 
        The function takes in as parameters: itemsets dict, lhs of (rule) and the rhs of 
        (rule). The support gives an indicator of how frequent an itemset is within all 
        transactions. The Higher the support usually means the itemset is more relevant. 
        It also is a good metric that can be used for further analysis. 

        FYI if an itemset/rule occurs 10 times out of 100 transactions the support would be 0.1

        Parameters:
            itemsets (dict)
            lhs (tuple)
            rhs (tuple)

        Returns:
            support float: The calculated 'support' value for support(A -> B). 
            lhs_support float: The calculated 'lhs_support' value for support(A). 
            rhs_support float: The calculated 'rhs_support' value for support(B). 

        Formula: 
            support(A -> B) = transactions(A -> B) / total number of transactions
            support(A) = transactions(A) / total number of transactions
            support(B) = transactions(B) / total number of transactions
        """     
        # Calculating total number of transactions first
        number_of_transactions = len(self.data)

        # combining lhs and rhs to tuple. This is used for calculating 'support(A -> B)'
        set_union = set(lhs + rhs)

        # Calulating number of times lhs(A), rhs(B) and lhs_rhs(A -> B) occur in itemsets
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
        
        # Perform relevelant calculations to get correct support values
        support = support_count / number_of_transactions
        lhs_support = lhs_count / number_of_transactions
        rhs_support = rhs_count / number_of_transactions

        return support, lhs_support, rhs_support

        
            






