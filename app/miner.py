from efficient_apriori import apriori

class Miner:
    def __init__(self, algorithm, data, support_threshold, confidence_threshold, min_length=1, max_length=8):
        self.algorithm=algorithm
        self.data=data
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
        itemsets, rules = apriori(self.data, min_support=self.support_threshold,  min_confidence=self.confidence_threshold)

        rule_results = []
        for rule in rules: 
            confidence = rule.confidence
            support = rule.support
            lift = rule.lift
            conviction = rule.conviction

            result = {
                "rule": str(rule), 
                "lhs": rule.lhs, 
                "rhs": rule.rhs,
                "confidence": confidence, 
                "support": support, 
                "lift": lift, 
                "conviction": conviction
            }

            rule_results.append(result)

        result = {
            "itemsets": itemsets, 
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






