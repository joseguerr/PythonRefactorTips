"""Process car part orders and output results."""

from decouple import config
import pandas as pd
from utils import (
    assign_factory,
    calculate_order_volume,
    calculate_volume,
    create_individual_parts_file,
    get_car_part_count,
    sort_orders,
    yaml_to_dict,
)

live_run = config("live_run", cast=bool)
settings_dict = yaml_to_dict("settings.yaml")


if live_run:
    orders = pd.read_csv(f"{settings_dict['live_input']}orders.csv")
    car_parts = pd.read_csv(f"{settings_dict['live_input']}car_parts.csv")
else:
    orders = pd.read_csv(f"{settings_dict['staging_input']}orders.csv")
    car_parts = pd.read_csv(f"{settings_dict['staging_input']}car_parts.csv")

orders = assign_factory(orders.copy(), settings_dict)

car_parts = calculate_volume(car_parts.copy())
orders = calculate_order_volume(orders.copy(), car_parts.copy())

orders = sort_orders(orders.copy(), settings_dict)

rank_list = create_individual_parts_file(orders.copy())

car_parts_count_d = get_car_part_count(orders)
car_parts_count = pd.DataFrame(
    car_parts_count_d.items(), columns=["car_parts", "total_quantity"]
)

if live_run:
    orders.to_csv(f"{settings_dict['live_output']}orders.csv", index=False)
    rank_list.to_csv(f"{settings_dict['live_output']}rank_list.csv", index=False)
    car_parts_count.to_csv(f"{settings_dict['live_output']}car_parts_count.csv", index=False)
else:
    orders.to_csv(f"{settings_dict['staging_output']}orders.csv", index=False)
    rank_list.to_csv(f"{settings_dict['staging_output']}rank_list.csv", index=False)
    car_parts_count.to_csv(f"{settings_dict['staging_output']}car_parts_count.csv", index=False)
