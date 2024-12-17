from distutils.log import INFO
import json
from faker import Faker
from datetime import timedelta
import random
import requests
import logging

logger = logging.getLogger(__name__)
def generate_row(future=False, invalid=False):
    datagen = Faker()
    record = {}
    record['firstname'] = datagen.first_name()
    record['lastname'] = datagen.last_name()
    record['totalprice'] = datagen.pyint()
    record['depositpaid'] = datagen.pybool()
    checkin = datagen.future_date() if future else datagen.past_date()
    record['bookingdates'] = {}
    record['bookingdates']['checkin'] = checkin.isoformat()
    delta = random.randint(1, 10) if not invalid else -10
    checkout = checkin + timedelta(delta)
    record['bookingdates']['checkout'] = checkout.isoformat()
    record['additionalneeds'] = datagen.text(15)

    return record


def create_scenarios():
    records = {}

    # create scenario
    records["createbooking1"] = generate_row(future=False)
    records["createbooking2"] = generate_row(future=True)
    records["invalidbooking1"] = generate_row(future=False, invalid=True)

    #missing data
    missingdata = generate_row()
    missingdata2 = missingdata.copy()
    missingdata.pop("bookingdates")
    missingdata2.pop("totalprice")
    records["missingfields1"] = missingdata
    records["missingfields2"] = missingdata2

    #update records
    records["updatebooking1"] = generate_row()
    records["updatebooking2"] = generate_row()
    records["expiredbooking1"] = generate_row(future=False)

    partialdata1 = generate_row()
    partialdata2 = generate_row()

    records["partialUpdatebooking1"] = {"firstname":partialdata1["firstname"], "additionalneeds":partialdata1["additionalneeds"] }
    records["partialUpdatebooking2"] = {"lastname":partialdata2["lastname"], "additionalneeds":partialdata2["additionalneeds"] }

    return records

def load_test_data():
    bookingids = []
    records = []
    for i in range(10):
        future = random.randint(0,1)
        if i == 5:
            future = False
        record = generate_row(future=future)
        headers = {'Content-type': 'application/json'}
        response = requests.post('https://restful-booker.herokuapp.com/booking',headers=headers, data=json.dumps(record))
        response.raise_for_status()
        resp = response.json()
        if i<=5:
            bookingids.append(resp)
        else:
            records.append(resp["booking"])
        
    
    return bookingids, records

def write_data(filename:str):
    records = create_scenarios()
    bookingids, filter = load_test_data()
    records["invalidbookingid"] = 999999999
    records["updatebookingid"] = bookingids[0]["bookingid"]
    records["expiredbookingid"] = bookingids[-1]["bookingid"]
    records["readbookingid"] = bookingids[2]["bookingid"]
    records["deletebookingid1"] = bookingids[1]["bookingid"]
    records["deletebookingid2"] = bookingids[3]["bookingid"]
    records["readbookingresponse"] = bookingids[2]["booking"]

    records["filters"] = []
    records["filters"].append({"firstname":filter[0]["firstname"]})
    records["filters"].append({"lastname":filter[1]["lastname"]})
    records["filters"].append({"checkin":filter[2]["bookingdates"]["checkin"]})
    records["filters"].append({"checkout":filter[3]["bookingdates"]["checkout"]})
    records["filters"].append({"firstname":filter[1]["firstname"], "lastname":filter[1]["lastname"]})
    records["filters"].append({"checkin":filter[3]["bookingdates"]["checkin"], "checkout":filter[3]["bookingdates"]["checkout"]})

    with open(filename, "w") as f:
        json.dump(records, f, indent=4)
    

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("Generating test data...")
    write_data("tests/resources/testdata.json")
    logging.info("test data complete")




