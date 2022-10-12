import argparse
import os
from pathlib import Path
from typing import Dict

import numpy as np


def read_folder(path_to_folder: str) -> Dict[float, str]:
    """
    Reads all images' paths and timestamps from folder
    :param path_to_folder: path to folder to read
    :return: dictionary where keys are timestamps and values are path to image
    """
    files = os.listdir(path_to_folder)
    timestamps = [float(Path(file).stem) for file in files]
    files = [os.path.join(path_to_folder, x) for x in files]
    timestamp_image_kvp = dict(zip(timestamps, files))
    return timestamp_image_kvp


def associate(
    color_images: Dict, depth_images: Dict, offset: float, max_difference: float
) -> list:
    """
    Associates color and depth images
    :param color_images: (timestamp, path) KVP for color images
    :param depth_images: (timestamp, path) KVP for depth images
    :param offset: time offset added to the timestamps of the depth images
    :param max_difference: maximally allowed time difference for matching entries
    :return: best matches for color and depth images
    """
    first_keys = np.asarray(list(color_images.keys()))
    second_keys = np.asarray(list(depth_images.keys()))
    best_matches = list()
    for timestamp in first_keys:
        best_match = second_keys[np.argmin(np.abs(second_keys + offset - timestamp))]
        if abs(best_match + offset - timestamp) < max_difference:
            best_matches.append((timestamp, best_match))
    return sorted(best_matches)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""
    This script takes two data files with timestamps and associates them   
    """
    )
    parser.add_argument("color_folder", help="path to folder with color images")
    parser.add_argument("depth_folder", help="path to folder with depth images")
    parser.add_argument(
        "--offset",
        type=float,
        help="time offset added to the timestamps of the depth images (default: 0.0)",
        default=0.0,
    )
    parser.add_argument(
        "--max_difference",
        type=float,
        help="maximally allowed time difference for matching entries (default: 1000)",
        default=1000,
    )
    parser.add_argument(
        "--timestamp2sec",
        type=float,
        help="constant for performing the conversion to sec (default: 1e6)",
        default=1e6,
    )
    args = parser.parse_args()

    first_list = read_folder(args.color_folder)
    second_list = read_folder(args.depth_folder)

    matches = associate(first_list, second_list, args.offset, args.max_difference)

    for a, b in matches:
        print(
            a / args.timestamp2sec,
            first_list[a],
            b / args.timestamp2sec,
            second_list[b],
        )
