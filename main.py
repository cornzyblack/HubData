from utils import HubData
import argparse

def get_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('--period',
                        choices=['day', 'week', 'month'],
                        default='day'
                       )

    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()
    period = args.get("period")
    print(period)
    # HubData(period)