
class AprioriCeri:
    def __init__(self, transactions, support_threshold):
        self.transactions = transactions
        self.support_threshold = support_threshold
    
    def mine(self):
        frontier_itemsets_candidates = self.get_initial_frontier_itemsets_candidates(self.transactions)
        itemsets_large = self.get_itemsets_large(self.transactions, self.support_threshold, frontier_itemsets_candidates)
        return itemsets_large
    
    def count_itemsets(self, itemsets_large):
        """
        method that counts the number of times an itemset occurs in the transaction attribute. 
        The itemset becomes the key in the dictionary and the value becomes the 'count'.

        Parameters:
            transactions (class attribute)
            itemsets_large (list)

        Returns:
            results (dict): containing 'itemset' and 'count' produced by the method.
        """
        # Initialising itemsets with a default count of 0
        itemset_count = {}
        for itemset in itemsets_large:
            itemset_count[itemset] = 0

        # loop through each itemset and count number of times it occurs in transaction
        for transaction in self.transactions:
            for itemset in itemsets_large:
                if itemset.issubset(transaction):
                    itemset_count[itemset] += 1

        return itemset_count      

    """ 
    Function initialises itemset candidates set (frontier set).
    this function will return the unique items withing a list of transactions. 
    """
    def get_initial_frontier_itemsets_candidates(self, transactions):
        itemsets_candidates = set()
        for transaction in transactions:
            for itemset in transaction:
                itemsets_candidates.add(itemset)
        
        # Sets cannot have two items of the same value meaning a unique item is always appended
        new_itemsets_candidates = []
        for item in itemsets_candidates: 
            new_itemsets_candidates.append({item})

        itemsets_candidates = new_itemsets_candidates
        return itemsets_candidates

    """
    Function generates new itemset candidates set (Frontier Set) 
    after each pass on the transactions
    """
    def get_frontier_itemsets_candidates(self, itemsets_large):
        new_itemsets_candidates = []
        
        # If set A ∪ B is equal to the length of item set ‘x+1’ then the union set is appended to the new frontier candidate sets
        for x in range(len(itemsets_large)):
            for y in range(x+1, len(itemsets_large)):
                union_set = itemsets_large[x] | itemsets_large[y] # A ∪ B
                if len(union_set) == len(itemsets_large[x]) + 1: 
                    new_itemsets_candidates.append(union_set)

        # If no itemsets are returned another transaction scan does not occur          
        return new_itemsets_candidates 

    """
    Function generates large itemsets (association rules) based on 
    the support threshold
    """
    def get_itemsets_large(self, transactions, minimum_support, frontier_itemsets_candidates):

        itemsets_large = []
        
        # If the itemsets returned by 'get_frontier_itemsets_candidates' = [] then the transactions are not scanned further
        while frontier_itemsets_candidates:
            
            # itemset_count keeps track of candidates that are subsets in transactions and how frequently they occur
            itemset_count = {}
            for itemset in frontier_itemsets_candidates: 
                itemset_count[frozenset(itemset)] = 0    
            
            # Iterate through and increase itemset_count 'count' by 1 each time a subset occurs
            for transaction in transactions:
                for candidate in frontier_itemsets_candidates:
                    if candidate.issubset(transaction):
                        itemset_count[frozenset(candidate)] += 1

            # Only keep itemsets that meet the minimum support threshold based on comparing against itemset_count 'count'      
            new_frontier_itemsets_candidates = []
            for itemset, count in itemset_count.items():
                if count >= minimum_support:
                    new_frontier_itemsets_candidates.append(itemset)

            frontier_itemsets_candidates = new_frontier_itemsets_candidates

            # Add the found itemsets to the large itemsets
            itemsets_large.extend(frontier_itemsets_candidates)
            
            # Get new frontier set on each scan. When None is returned the loop is ended and algorithm complete. 
            frontier_itemsets_candidates = self.get_frontier_itemsets_candidates(frontier_itemsets_candidates)
        
        itemsets_count = self.count_itemsets(itemsets_large)

        return itemsets_count
