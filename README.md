# Assignment for QA Test Engineer role

## Task no. 1
Find the 2 attached JSON files. The file named "deliveries_for_planning.json" has a list of deliveries. The file named "planned_route.json" has a planned route for the deliveries. Mock the API (using http://jsonplaceholder.typicode.com/ for example) and write Python (requests + pytest) tests to evaluate the following conditions:
1. All deliveries from "deliveries_for_planning.json" that are in `current_state` "planned" are present in "planned_route.json"
1. The sum of weights of the deliveries is less than the `carrying_capacity` of the vehicle
1. All eta-s of deliveries in planning (estimated time of arrivals) with `type` "delivery" are within the `route_min_time` and `route_max_time`
1. All eta-s of deliveries in planning are within their `delivery_min_time` and `delivery_max_time`
1. The `travel_time_to` next (in seconds) is less than or equal to the time difference between any 2 consecutive deliveries in "planned_route.json"

### Solution
- The contents of "planned_route.json" were copied to "db.json" to mock the API using http://jsonplaceholder.typicode.com/
- "planned_route.json" is accessible using https://my-json-server.typicode.com/haithambb/Plotwise/planned_route 
- "deliveries_for_planning.json" has been added to the repo as input to the tests

#### How to run the solution
Clone the repository and cd to it
```
git clone https://github.com/haithambb/Plotwise.git
cd Plotwise
```
Install `pytest` and `requests`
```
pip install pytest
pip install requests
```
Run test with the following command
Note: main.py contains 
```
python main.py
```
The output of the test run should look something like this
```
hbayoumi@JPN Plotwise % python main.py
================================================================================================= test session starts ==================================================================================================
platform darwin -- Python 2.7.17, pytest-4.6.11, py-1.10.0, pluggy-0.13.1 -- /usr/local/opt/python@2/bin/python2.7
cachedir: .pytest_cache
rootdir: /Users/hbayoumi/indeed/Plotwise
collected 19 items                                                                                                                                                                                                     

main.py::test_all_planned_deliveries_present[delivery_for_planning0] PASSED
main.py::test_all_planned_deliveries_present[delivery_for_planning1] PASSED
main.py::test_all_planned_deliveries_present[delivery_for_planning2] PASSED
main.py::test_all_planned_deliveries_present[delivery_for_planning3] PASSED
main.py::test_weights_sum_lt_vehicle_carrying_capacity FAILED
main.py::test_all_deliveries_in_planning_etas_within_route_time_range[planned_delivery0] PASSED
main.py::test_all_deliveries_in_planning_etas_within_route_time_range[planned_delivery1] PASSED
main.py::test_all_deliveries_in_planning_etas_within_route_time_range[planned_delivery2] PASSED
main.py::test_all_deliveries_in_planning_etas_within_route_time_range[planned_delivery3] PASSED
main.py::test_all_deliveries_in_planning_etas_within_route_time_range[planned_delivery4] PASSED
main.py::test_all_deliveries_in_planning_etas_within_delivery_time_range[planned_delivery0] PASSED
main.py::test_all_deliveries_in_planning_etas_within_delivery_time_range[planned_delivery1] PASSED
main.py::test_all_deliveries_in_planning_etas_within_delivery_time_range[planned_delivery2] FAILED
main.py::test_all_deliveries_in_planning_etas_within_delivery_time_range[planned_delivery3] PASSED
main.py::test_all_deliveries_in_planning_etas_within_delivery_time_range[planned_delivery4] PASSED
main.py::test_travel_time_to_next_lte_time_diff_between_any_2_consecutive_deliveries[planned_delivery0] PASSED
main.py::test_travel_time_to_next_lte_time_diff_between_any_2_consecutive_deliveries[planned_delivery1] PASSED
main.py::test_travel_time_to_next_lte_time_diff_between_any_2_consecutive_deliveries[planned_delivery2] PASSED
main.py::test_travel_time_to_next_lte_time_diff_between_any_2_consecutive_deliveries[planned_delivery3] PASSED

======================================================================================================= FAILURES =======================================================================================================
____________________________________________________________________________________ test_weights_sum_lt_vehicle_carrying_capacity _____________________________________________________________________________________

    def test_weights_sum_lt_vehicle_carrying_capacity():
        weights_sum = get_deliveries_for_planning_weights_sum()
        planned_deliveries = get_planned_deliveries()
        carrying_capacity = planned_deliveries["resource"]["carrying_capacity"]
>       assert weights_sum < carrying_capacity
E       assert 183 < 180

main.py:68: AssertionError
__________________________________________________________________ test_all_deliveries_in_planning_etas_within_delivery_time_range[planned_delivery2] __________________________________________________________________

planned_delivery = {'algorithm_fields': {'eta': '2017-11-13T08:53:08.000000Z', 'stop_time': 720, 'time_to_next': 0, 'type': 'delivery', ...}, 'bucket': '85812fcb-e272-476f-aa43-17b8c773ff10', 'current_state': 'planned', 'delivery_order_index': 2, ...}

    @pytest.mark.parametrize("planned_delivery", get_planned_deliveries()["deliveries"])
    def test_all_deliveries_in_planning_etas_within_delivery_time_range(planned_delivery):
        if planned_delivery["algorithm_fields"]["type"] == "delivery":
            id = planned_delivery["id"]
            eta = datetime.strptime(
                planned_delivery["algorithm_fields"]["eta"], "%Y-%m-%dT%H:%M:%S.%fZ"
            )
            delivery_min_time = datetime.strptime(
                planned_delivery["min_time"], "%Y-%m-%dT%H:%M:%S.%fZ"
            )
            delivery_max_time = datetime.strptime(
                planned_delivery["max_time"], "%Y-%m-%dT%H:%M:%S.%fZ"
            )
>           assert (
                    delivery_min_time <= eta <= delivery_max_time
            ), "ETA for delivery {0} is not within delivery time range!".format(id)
E           AssertionError: ETA for delivery 60adbe31-d693-4dd7-8368-94545be514de is not within delivery time range!
E           assert datetime.datetime(2017, 11, 13, 8, 53, 8) <= datetime.datetime(2017, 11, 13, 8, 30)

main.py:101: AssertionError
========================================================================================= 2 failed, 17 passed in 8.16 seconds ==========================================================================================
```

## Task no. 2
There is a planning REST API service that accomplishes the following task given the appropriate input. 
The REST_API service can take in a list of places to visit and calculates the best route possible for a day. 
It can optimize routes for the fastest travel and for shortest travel. 
A taco food truck can take in orders online. 
All incoming orders are for delivering as soon as possible. 
In the city where the delivery truck operates, it is allowed to cook inside vehicles ONLY when stationary. 
The owner of the truck who uses the planning REST_API service waits for at most 20 orders before starting deliveries. 
Being a tech-savvy taco truck owner, he hires a developer to automate the feed of incoming orders and how it interacts with the planning REST_API. 
He has to keep in mind that there are runs needed for
- Refueling
- Buying groceries when supplies run low
- Depositing money at the local bank since it is not safe to carry loose cash
  
You are a tester who has contracts to test both the planning REST_API and the work of the developer hired by the food truck owner. Think of various scenarios that need testing. Create a test plan with the following in mind:
1. 10 functional/feature tests
1. 5 performance test points

Choose the format of the test plan that you think is the most suitable, but it shall not be limited to test cases only. Please provide a plan in separate well-structured rich text or pdf document format.

### Solution
The proposed solution is not comprehensive in any way. 

It is merely an exercise in imagining the architecture of such a solution and its components based on a few assumptions and an interpretation of the requirements to facilitate testing considerations.

Here you will find a separate document for the test plan <br>
https://docs.google.com/document/d/1TH4fnsLsi7bHxA9VmfSrNeMqq-Mki5TJtsLXgY51rqI/edit#heading=h.7oyre2n7je0g <br>
Note: The test plan is usually the product of several contributors, so __*please feel free to add comments or questions*__.

#### Assumptions
- Orders are dealt with on a first come, first served basis.
- A predetermined list of locations where the delivery truck can remain stationary for the duration of cooking is available. The reasoning behind this assumption are
  - “In the city where the delivery truck operates, it is allowed to cook inside vehicles ONLY when stationary”
  - City parking regulations may apply
- Customers will come pick up their orders from a predetermined delivery spot.
- A predetermined list of banks where the delivery truck can make deposits is available. Once the cash register hits a certain threshold of cash, a deposit is scheduled, “since it is not safe to carry loose cash”.
- The Planning REST API Service (PRAS) has a very low latency and can provide optimized routes on the fly.
- Fuel tracking is an automated process that can be estimated provided with initial input of truck fuel gauge reading at the start of a workday.
- Supplies tracking is an automated process (same as fuel).

#### Additional Requirements
The tech-savvy taco truck owner has set a service level objective (SLO) to deliver fresh tacos to all city dwellers within a reasonable amount of time after order placement, therefore “all incoming orders are for delivering as soon as possible”.

#### Inputs
The Automated Order Feed System (AOFS) will have to take in the following inputs

- Initialization (start of the workday)
  - Truck fuel gauge reading
  - Taco supplies

- Order
  - Dish details (additional fields may apply)
    - Type
    - Special instructions (optional field)
    - Quantity
  - Cost (Computed)
  - Delivery location

#### Constrains
The AOFS has to take into account the following constraints
- No more than 20 orders can be placed at any given time, since “The owner of the truck ... waits for at most 20 orders before starting deliveries”.
- The total amount in the cash in the register cannot exceed a certain threshold without making a drop off at the nearest bank to make a deposit.

#### System Components
The AOFS has several components that intake orders, evaluate constraints and generate optimized routes based on its interaction with the PRAS.

The AOFS will refrain from placing an order if the truck is operating at full capacity, or it cannot deliver the order in a timely manner from its current location.

1. Order location will be normalized to the nearest delivery drop off location
1. Evaluation of constraints
   1. Check of total number of placed orders
   1. Estimated fuel consumption
   1. Estimated supplies usage
   1. Current total in cash register
1. The delivery drop off location and any other on-the-way stops, i.e. gas stations, grocery stores or banks, are fed to the PRAS.
1. PRAS generates an optimized route that is evaluated in terms of order delivery times (orders can be made in a timely manner)

#### Functional Tests
Based on the above, here are examples of 10 functional tests that could be covered through unit and integration tests.
1. Order intake is contains all required fields i.e. order details mainly dish details and delivery location
1. Delivery location is being normalized to the nearest delivery drop off location
1. No further orders are accepted when order capacity (20 orders) has been reached
1. Order is not accepted when delivery cannot be made in a reasonable amount of time
1. An order is accepted as soon as vacancy is available and constraints are met (i.e. order capacity = 19 and delivery can be made in a timely manner)
1. Gas station is added to route if the truck is running low on fuel
1. Grocery shop is added to route if the truck is running low on supplies
1. Bank is added to route if cash register content exceeded a certain amount
1. Order delivery ETA is within range of time of placing an order to the customer receiving it
1. All accepted orders and on-the-way stops are present in the optimized routes

#### Performance Tests
Here are examples of 4 performance tests
1. A number of simultaneous orders within maximum order capacity are made from varying locations throughout the city
1. A number of orders exceeding the maximum order capacity (orders’ magnitudes can be increased throughout the test) are made from the same normalized location
1. A number of orders exceeding the maximum order capacity are made from randomized location that are normalized to different delivery spots
1. System response time is within predefined response metrics upon order placement when under load

## Task no. 3
After using the planning REST API for a while, truck owner (from task 2) has decided that he wants to make some adjustments to the process, therefore the API needs to automatically plan the restock relying on the following:
- He will be storing enough supplies to make 100 tacos and will plan a stop for groceries shopping after at least 80 tacos are ordered
- He won’t buy fresh groceries near the end of the working day (starting 3 hours before the end of the shift)
- Any products that are left at the end of the day he will take home, therefore each working day he will start with buying fresh supplies for 100 tacos

Developer has started to implement the required functionality. In the meanwhile, as a tester, you need to design behaviour-driven tests using Gherkin language. Please, create at least 5 tests for the described new functionality based on the truck owner’s requirements. Allowed syntax includes: `Given`, `When`, `Then`, `And`. Submit the results in .feature file or in the text document.

### Solution
I quickly familiarised myself with Gherkin ([Gherkin Reference](https://cucumber.io/docs/gherkin/reference/)) and came up with the following 5 tests (I disregarded prior assumptions I made in the previous task).

```
Given Taco food truck stars a day
And time is start of day
Then plan a stop for groceries to buy enough supplies to make 100 tacos
```

```
Given Taco food truck stars a day
And Taco food truck is stoked on supplies
And at least 80 tacos are ordered
When deadline to buy fresh groceries has NOT been reached
Then plan a stop for groceries
```

```
Given Taco food truck stars a day
And at least 80 tacos are ordered
When deadline to buy fresh groceries has been reached
Then do NOT plan a stop for groceries
```

```
Given Taco food truck stars a day
And Taco food truck is stoked on supplies
And at most 79 tacos are ordered
When deadline to buy fresh groceries has NOT been reached
Then do NOT plan a stop for groceries
```

```
Given Taco food truck stars a day
And Taco food truck is stoked on supplies
And at most 79 tacos are ordered
When deadline to buy fresh groceries has been reached
Then do NOT plan a stop for groceries
```
