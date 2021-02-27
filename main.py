from utils import HubData
import argparse


def get_args():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--period", choices=["day", "week", "month", "year"], default="day"
    )
    parser.add_argument("--filename", default=None)
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    period = args.period
    hub_data = HubData(period)

    hub_data.save_to_csv(args.filename)
