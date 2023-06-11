"""Perform orders data transformation for car parts."""

from math import pi

import pandas as pd
import yaml


def assign_factory(orders, settings):
    """Assign factory based on car type."""
    orders["factory"] = orders["car_type"].map(settings["car_type_settings"])
    return orders


def calculate_volume(car_parts):
    """Calculate total volume in each of the orders."""
    # Create volume column
    car_parts["volume"] = 0

    # Assign the correct volume function based on shape field
    car_parts["volume"] = car_parts.apply(
        lambda row: _shape_to_volume(row), axis=1
    )
    return car_parts


def _shape_to_volume(row):
    """Return volume based on dimensions and shape."""
    if row["shape"] == "cuboid":
        return row["length"] * row["width"] * row["depth"]

    if row["shape"] == "sphere":
        return (4 / 3) * pi * ((row["width"] / 2) ** 3)

    if row["shape"] == "cylinder":
        return (
            pi
            * row["length"]
            * ((row["width"] / 2) ** 2)  # width is the diameter
        )

    raise ValueError(f"Shape {row.shape} not recognised. Please use a valid shape.")


def calculate_order_volume(orders, car_parts):
    """Calculate total car parts volume present in an order."""
    # Create the mapping with car part code and volume
    car_parts["code"] = (
        car_parts["category"].str[:2] + "-" + car_parts["car_part_id"].astype("string")
    )
    code_volume_mapping = dict(zip(car_parts["code"], car_parts["volume"]))

    # apply function to column and create new column with sums
    orders["orders_volume"] = orders.apply(
        _sum_list_values,
        axis=1,
        code_to_vol=code_volume_mapping,
    )
    return orders


def _sum_list_values(row, code_to_vol):
    codes = row["car_parts"].split()
    return sum(code_to_vol.get(code, 0) for code in codes)


def sort_orders(orders, settings):
    """Sort orders based on priority settings and delivery date."""

    # Sort rows by factory priority (via dict lookup) and delivery date
    return (
        orders.sort_values(by="factory", key=lambda x: x.map(settings["factory_settings"]))
              .sort_values(by="delivery_date", ascending=True)
    )


def create_individual_parts_file(orders):
    """Split items in an order into separate rows and assign a rank to them."""

    # Initial solution using indexing
    df_list = []
    for row in orders.itertuples(index=False):
        order = row.order_id
        values = row.car_parts.split()
        for rank, value in enumerate(values, 1):
            split_parts = value.split("-")
            df_list.append([order, rank, split_parts[1]])

    return pd.DataFrame(
        df_list, columns=["order_id", "rank", "car_part_id"]
    )


def get_car_part_count(orders):
    """Count the number of time each car part is present in the orders."""

    orders = orders.assign(split_car_parts=orders["car_parts"].str.split())
    orders = orders.explode("split_car_parts")

    car_part_list = orders["split_car_parts"].to_list()
    # Iterate through the list and increment the count for each item
    car_part_count = {}
    for car_part in car_part_list:
        if car_part in car_part_count:
            # Add +1 to counter
            car_part_count[car_part] += 1
        else:
            # Initialise key
            car_part_count[car_part] = 1
    return car_part_count


def yaml_to_dict(filename):
    """Read Yaml file into dictionary."""
    with open(filename) as file:
        return yaml.load(file, Loader=yaml.FullLoader)
