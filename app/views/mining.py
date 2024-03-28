from flask import Blueprint
from app.response import Response
from app.miner import Miner

mining = Blueprint('mining', __name__)

@mining.route('/mine', methods=["GET"])
def mine():
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

    '''miner = Miner(
        algorithm='fpgrowth',
        data=transactions,
        support_threshold=0.2,
        confidence_threshold=0.8,
    )

    result = miner.mine_fpgrowth()'''

    miner = Miner(
        algorithm='apriori',
        data=transactions,
        support_threshold=0.2,
        confidence_threshold=0.8,
    )

    result = miner.mine_apriori()

    '''miner = Miner(
        algorithm='apriori-ceri', 
        data=transactions, 
        support_threshold=0.2, 
        confidence_threshold=0.8
    )

    result = miner.mine_apriori_ceri()'''

    response_obj = Response("Test message response", data=result)
    return response_obj.return_success_response()