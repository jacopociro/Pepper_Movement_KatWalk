import argparse
import math

parser = argparse.ArgumentParser()

parser.add_argument(
    "--ip",
    type=str,
    default="130.251.13.138",
    help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'."
)

parser.add_argument(
    "--port",
    type=int,
    default=9559,
    help="Naoqi port number"
)

parser.add_argument(
    '-p',
    '--precise',
    help='Enable precise movement',
    action='store_true',
)

parser.add_argument(
    '-b',
    '--bool',
    help='Enable precise movement',
    action='store_false',
)

parser.add_argument(
    '-ip',
    '--socketip',
    help='socket ip',
    type=str,
    default="127.0.0.1",
)

parser.add_argument(
    '-pt',
    '--socketport',
    help='Socket Port',
    type=float,
    default=3001,
    )

parser.add_argument(
    '-bs',
    '--buffersize',
    help='socket buffer size ',
    type=float,
    default=86,
    )

parser.add_argument(
    '-c',
    '--calibration',
    help='head calibration',
    type=float,
    default=0,
)

parser.add_argument(
    '-s',
    '--speed',
    help='walking speed',
    type=float,
    default=0.6
)

parser.add_argument(
    '-r',
    '--range',
    help='precision of movement',
    type=int,
    default=5
)

parser.add_argument(
    '-k',
    '--k',
    help='proportional value of control',
    type=float,
    default=0.3
)

