import unittest
import pdb

from app.miner import Miner

class TestMinerClass(unittest.TestCase):
    @classmethod
    def setUpClass(cls): 
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

        cls.miner_fpgrowth = Miner(
            algorithm='fpgrowth',
            data=transactions,
            support_threshold=0.2,
            confidence_threshold=0.8,
        )

        cls.miner_apriori = Miner(
            algorithm='apriori',
            data=transactions,
            support_threshold=0.2,
            confidence_threshold=0.8,
        )
    
    def test_mine_fpgrowth(self):
        result = self.miner_fpgrowth.mine_fpgrowth()
        
        # Testing data types are correct
        self.assertIsInstance(result, dict) # Checking result is a python dict object
        self.assertIn('itemsets', result)
        self.assertIn('rules', result)
        self.assertIsInstance(result['itemsets'], dict)
        self.assertIsInstance(result['rules'], list)

        # Testing values are correct for itemsets
        self.assertEqual(result['itemsets'].get("Diapers,Milk"), 2)
        self.assertEqual(result['itemsets'].get("Milk"), 6)
        self.assertEqual(result['itemsets'].get("Bread,Butter,Milk"), 4)
        self.assertEqual(result['itemsets'].get("Beer,Diapers"), 2)
        self.assertNotEqual(result['itemsets'].get("Beer,Diapers"), 10)

        # Testing rule values are correct for rules
        self.assertEqual(result['rules'][2]['lhs'], ["Butter"])
        self.assertEqual(result['rules'][2]['rhs'], ["Bread", "Milk"])
        self.assertEqual(result['rules'][2]['support'], 0.4)
        self.assertEqual(result['rules'][2]['lift'], 1.6)
        self.assertEqual(result['rules'][2]['conviction'], 2.5000000000000004)
        self.assertEqual(result['rules'][2]['confidence'], 0.8)
        self.assertNotEqual(result['rules'][2]['confidence'], 0.83333)

        # Testing number of rules returned
        self.assertEqual(len(result['rules']), 7)

    def test_mine_apriori(self):
        result = self.miner_apriori.mine_apriori()
        
        # Testing data types are correct
        self.assertIsInstance(result, dict) # Checking result is a python dict object
        self.assertIn('itemsets', result)
        self.assertIn('rules', result)
        self.assertIsInstance(result['itemsets'], dict)
        self.assertIsInstance(result['rules'], list)

        # Testing values are correct for itemsets
        self.assertEqual(result['itemsets'].get("Diapers,Milk"), 2)
        self.assertEqual(result['itemsets'].get("Milk"), 6)
        self.assertEqual(result['itemsets'].get("Bread,Butter,Milk"), 4)
        self.assertEqual(result['itemsets'].get("Beer,Diapers"), 2)
        self.assertNotEqual(result['itemsets'].get("Beer,Diapers"), 10)

        # Testing rule values are correct for rules
        self.assertEqual(result['rules'][9]['lhs'], ["Butter"])
        self.assertEqual(result['rules'][9]['rhs'], ["Bread", "Milk"])
        self.assertEqual(result['rules'][9]['support'], 0.4)
        self.assertEqual(result['rules'][9]['lift'], 1.6)
        self.assertEqual(result['rules'][9]['conviction'], 2.4999999875000007)
        self.assertEqual(result['rules'][9]['confidence'], 0.8)
        self.assertNotEqual(result['rules'][2]['confidence'], 0.83333)

        # Testing number of rules returned
        self.assertEqual(len(result['rules']), 10)

    def test_calculate_support_values(self):
        itemsets = {
            ('Cola',): 2,
            ('Beer', 'Cola'): 2,
            ('Beer',): 4, 
            ('Beer', 'Diapers'): 2,
            ('Diapers', 'Milk'): 2,
            ('Butter',): 5,
            ('Bread', 'Butter'): 5,
            ('Butter', 'Milk'): 4,
            ('Bread', 'Butter', 'Milk'): 4,
            ('Milk',): 6,
            ('Bread', 'Milk'): 5,
            ('Bread',): 6
        }

        lhs = ('Butter',)
        rhs = ('Bread', 'Milk')

        support, lhs_support, rhs_support = self.miner_fpgrowth.calculate_support_values(itemsets, lhs, rhs)

        self.assertEqual(support, 0.4)
        self.assertEqual(lhs_support, 0.5)
        self.assertEqual(rhs_support, 0.5)
        self.assertNotEqual(support, 10)
        self.assertNotEqual(lhs_support, 7)
        self.assertNotEqual(rhs_support, 6)

    def test_calculate_lift(self):
        lift = self.miner_fpgrowth.calculate_lift(0.4, 0.2, 0.6)

        self.assertEqual(lift, 3.3333333333333335)
        self.assertNotEqual(lift, 10)

    def test_calculate_confidence(self):
        conviction = self.miner_fpgrowth.calculate_conviction(0.8, 0.6)

        self.assertEqual(conviction, 2.0000000000000004)
        self.assertNotEqual(conviction, 10)

if __name__ == '__main__':
    unittest.main()



