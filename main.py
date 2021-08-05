import pytest
import json
import requests
from datetime import datetime


def get_deliveries_for_planning():
    with open("deliveries_for_planning.json") as f:
        data = json.load(f)
        return data


def get_deliveries_for_planning_weights_sum():
    deliveries_for_planning = get_deliveries_for_planning()
    weights_sum = sum(
        [d["algorithm_fields"]["weight"] for d in deliveries_for_planning]
    )
    return weights_sum


def get_planned_deliveries():
    response = requests.get(
        "https://my-json-server.typicode.com/haithambb/Plotwise/planned_route"
    )
    return response.json()


def get_planned_route_time_range():
    planned_deliveries = get_planned_deliveries()
    route_min_time = datetime.strptime(
        planned_deliveries["route_min_time"], "%Y-%m-%dT%H:%M:%S.%fZ"
    )
    route_max_time = datetime.strptime(
        planned_deliveries["route_max_time"], "%Y-%m-%dT%H:%M:%S.%fZ"
    )
    return [route_min_time, route_max_time]


def get_time_diff_between_2_consecutive_deliveries_list():
    planned_deliveries = get_planned_deliveries()["deliveries"]
    etas_list = [
        datetime.strptime(d["algorithm_fields"]["eta"], "%Y-%m-%dT%H:%M:%S.%fZ")
        for d in planned_deliveries
    ]
    etas_diff_list = [
        int((eta2 - eta1).total_seconds())
        for eta1, eta2 in zip(etas_list[:-1], etas_list[1:])
    ]
    return etas_diff_list


# All deliveries from "deliveries_for_planning.json" that are in current_state "planned" are present in
# "planned_route.json"
@pytest.mark.parametrize("delivery_for_planning", get_deliveries_for_planning())
def test_all_planned_deliveries_present(delivery_for_planning):
    if delivery_for_planning["current_state"] == "planned":
        id = delivery_for_planning["id"]
        planned_deliveries = get_planned_deliveries()
        planned_delivery_ids = [d["id"] for d in planned_deliveries["deliveries"]]
        assert id in planned_delivery_ids


# The sum of weights of the deliveries is less than the carrying_capacity of the vehicle
def test_weights_sum_lt_vehicle_carrying_capacity():
    weights_sum = get_deliveries_for_planning_weights_sum()
    planned_deliveries = get_planned_deliveries()
    carrying_capacity = planned_deliveries["resource"]["carrying_capacity"]
    assert weights_sum < carrying_capacity


# All eta-s of deliveries in planning (estimated time of arrivals) with type "delivery" are within the route_min_time
# and route_max_time
@pytest.mark.parametrize("planned_delivery", get_planned_deliveries()["deliveries"])
def test_all_deliveries_in_planning_etas_within_route_time_range(planned_delivery):
    if planned_delivery["algorithm_fields"]["type"] == "delivery":
        id = planned_delivery["id"]
        eta = datetime.strptime(
            planned_delivery["algorithm_fields"]["eta"], "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        route_min_time = get_planned_route_time_range()[0]
        route_max_time = get_planned_route_time_range()[1]
        assert (
                route_min_time <= eta <= route_max_time
        ), "ETA for delivery {0} is not within route time range!".format(id)


# All eta-s of deliveries in planning are within their delivery_min_time and delivery_max_time
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
        assert (
                delivery_min_time <= eta <= delivery_max_time
        ), "ETA for delivery {0} is not within delivery time range!".format(id)


# The travel time_to_next (in seconds) is less than or equal to the time difference between any 2 consecutive deliveries
# in "planned_route.json"
@pytest.mark.parametrize(
    "planned_delivery", get_planned_deliveries()["deliveries"][:-1]
)
def test_travel_time_to_next_lte_time_diff_between_any_2_consecutive_deliveries(
        planned_delivery,
):
    id = planned_delivery["id"]
    time_to_next = planned_delivery["algorithm_fields"]["time_to_next"]
    etas_diff_list = get_time_diff_between_2_consecutive_deliveries_list()
    assertion_error = "Travel time to next of delivery {0} is not less than or equal to \
    any time diff between any two consecutive deliveries found in {1}!".format(
        id, etas_diff_list
    )
    assert any(time_to_next <= diff for diff in etas_diff_list), assertion_error


if __name__ == "__main__":
    pytest.main(["-sv", "main.py"])
