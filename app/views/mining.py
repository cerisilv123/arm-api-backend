from flask import Blueprint, request
from app import db
from app.response import Response
from app.miner import Miner
from app.models.db_daos import Result, Itemset, Rule, LHS, RHS

mining = Blueprint('mining', __name__)

@mining.route('/mine', methods=["POST"])
def mine():
    """
    Returns association rule mining results for a transactional data set and saves data set to
    database.

    Request:
    - HttpRequest (JSON): JSON object containing details such as list of transactions, algorithm specified, 
      support_threshold and confidence_threshold. See API documentation and report for more on this.  
      
    Returns:
    - HttpResponse: JSON object containing user details (name, email) if found, otherwise
      returns an error message with appropriate HTTP status code.

    Raises:
    - Error: If all required data has not been sent in request body.
    - Error: If all required data is not present in request.
    - Error: If required data in request is not of the correct type and format.
    - Error: If data types in transactions list are not of same type (should all be str).

    Note:
    - More information on this API endpoint can be found in the API documentation and report
      that accompanies this code.
    """

    # Get JSON data from request
    data = request.get_json()

    # Checking all required data has been sent
    required_keys = ["algorithm", "transactions", "support_threshold", "confidence_threshold"]
    
    # Validating all required data is present in request
    if not all(key in data for key in required_keys):
        response_obj_err = Response("You are missing data in the request body. Please ensure all keys are present.")
        return response_obj_err.return_error_response()
    
    # Validating all required data in request is of the correct type and format
    if not isinstance(data["algorithm"], str) or not isinstance(data["transactions"], list) or not isinstance(data["support_threshold"], float) or not isinstance(data["confidence_threshold"], float):
        response_obj_err = Response("Data sent in the request is not of the corrrect format.")
        return response_obj_err.return_error_response()
    
    # Validating data types in transactions list are of same type (should all be str).
    for transaction in data["transactions"]: 
        if not all(isinstance(item, str) for item in transaction):
            response_obj_err = Response("All transactions in the list should be of data type string.")
            return response_obj_err.return_error_response()
    
    # Creating miner object to handle association rule mining
    miner = Miner(
        algorithm=data["algorithm"], 
        data=data["transactions"], 
        support_threshold=data["support_threshold"],
        confidence_threshold=data["confidence_threshold"],
    )

    mine_results = miner.mine_association_rules()

    data = mine_results
    itemsets = data["itemsets"]
    rules = data["rules"]

    result_obj = ''

    # Begin a new SQLAlchemy transaction and adding result to DB
    with db.session.begin():

        result = Result(
            count = 10,
        )
        db.session.add(result)
        
        # Itemsets
        for key, value in itemsets.items():
            itemset = Itemset(
              items = key, 
              count = value, 
              result = result, # Setting foreign key 
            )
            db.session.add(itemset)

        # Rules
        for r in rules:               
            rule = Rule(
                confidence = r["confidence"], 
                conviction = r["conviction"], 
                lift = r["lift"], 
                support = r["support"],
                rule = r["rule"],
                result = result,
            )
            db.session.add(rule)

            for x in r["rhs"]:
                rhs = RHS(
                    item = x,
                    rule = rule,
                )
                db.session.add(rhs)


            for x in r["lhs"]:
                lhs = LHS(
                    item = x,
                    rule = rule,
                )
                db.session.add(lhs)

        result_obj = result
    
    # Returning JSON body with results from request
    response_obj = Response("Data mined successfully!", data=result_obj.to_dict())
    return response_obj.return_success_response()

@mining.route('/result/<string:id>', methods=["GET"])
def read_result(id):

    # Check if result exists in DB based on id
    result = Result.query.filter_by(id=id).first()
    if not result: 
        response_obj_err = Response("Could not find result based on that id.")
        return response_obj_err.return_error_response()
    
    response_obj = Response("Result retrieved successfully!", data=result.to_dict())
    return response_obj.return_success_response()
