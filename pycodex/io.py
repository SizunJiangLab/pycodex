import os
import re

import pandas as pd

########################################################################################################################
# rename marker
########################################################################################################################


def rename_invalid_marker(marker_name: str) -> str:
    """
    Rename the invalid marker name (containing "/" and ":").

    Args:
        marker (str): Original marker name.

    Returns:
        str: Modified marker name with invalid characters replaced by "_".
    """
    marker_name = re.sub(r"[/:]", "_", marker_name)
    return marker_name


def rename_duplicate_markers(marker_list: list[str]) -> list[str]:
    """
    Renames duplicate markers by appending a numeric suffix to ensure uniqueness.

    Parameters:
    marker_list (list): A list of strings representing marker names.

    Returns:
    list: A list of marker names where duplicates are renamed with a suffix (e.g., '_2', '_3').
    """
    seen = {}
    renamed_list = []

    for marker in marker_list:
        if marker in seen:
            seen[marker] += 1
            renamed_list.append(f"{marker}_{seen[marker]}")
        else:
            seen[marker] = 1
            renamed_list.append(marker)

    return renamed_list


########################################################################################################################
# fusion
########################################################################################################################


def parse_marker_fusion(marker_path: str) -> tuple[str, str, str, str, str]:
    """
    Fusion: Parse marker information from the file name.

    Args:
        marker_path (str): Path to the marker image file (*.tif).

    Returns:
        tuple: Parsed marker information including path, region, cycle, channel, and renamed marker.
    """
    marker_basename = os.path.basename(marker_path)
    marker_dirname = os.path.dirname(marker_path)
    region = os.path.basename(marker_dirname)
    pattern = r"(.+)\.tif"
    match = re.match(pattern, marker_basename)
    (marker,) = match.groups()
    return marker_path, region, rename_invalid_marker(marker)


def get_marker_metadata_fusion(region_dir: str) -> tuple[str, pd.DataFrame]:
    """
    Fusion: Get metadata for all markers in a given region directory.

    Args:
        region_dir (str): Directory containing marker files for a specific region.

    Returns:
        tuple: Region name and metadata DataFrame containing paths, region, cycle, channel, and marker.
    """
    marker_paths = []
    for root, dirs, files in os.walk(region_dir):
        for file in files:
            marker_paths.append(os.path.join(root, file))
    metadata_df = pd.DataFrame(
        [parse_marker_fusion(path) for path in marker_paths],
        columns=["path", "region", "marker"],
    )
    region = metadata_df["region"].unique().item()
    return region, metadata_df


def organize_metadata_fusion(marker_dir: str) -> dict[str, pd.DataFrame]:
    """
    Organize metadata for all regions in the final directory.

    Args:
        marker_dir (str): Directory containing subdirectories which contain marker files for a specific region.

    Returns:
        dict: Dictionary containing region names as keys and metadata DataFrames as values.
    """
    region_dirs = [os.path.join(marker_dir, subdir) for subdir in os.listdir(marker_dir)]
    metadata_dict = {}
    for region_dir in region_dirs:
        region, metadata_df = get_marker_metadata_fusion(region_dir)
        metadata_dict[region] = metadata_df
    return metadata_dict


########################################################################################################################
# keyence
########################################################################################################################


def parse_marker_keyence(marker_path: str) -> tuple[str, str, str, str, str]:
    """
    Keyence: Parse marker information from the file name.

    Args:
        marker_path (str): Path to the marker image file (*.tif).

    Returns:
        tuple: Parsed marker information including path, region, cycle, channel, and renamed marker.
    """
    marker_basename = os.path.basename(marker_path)
    pattern = r"(reg\d+)_(cyc\d+)_(ch\d+)_(.+)\.tif"
    match = re.match(pattern, marker_basename)
    region, cycle, channel, marker = match.groups()
    return marker_path, region, cycle, channel, rename_invalid_marker(marker)


def get_marker_metadata_keyence(region_dir: str) -> tuple[str, pd.DataFrame]:
    """
    Keyence: Get metadata for all markers in a given region directory.

    Args:
        region_dir (str): Directory containing marker files for a specific region.

    Returns:
        tuple: Region name and metadata DataFrame containing paths, region, cycle, channel, and marker.
    """
    marker_paths = []
    for root, dirs, files in os.walk(region_dir):
        for file in files:
            marker_paths.append(os.path.join(root, file))
    metadata_df = pd.DataFrame(
        [parse_marker_keyence(path) for path in marker_paths],
        columns=["path", "region", "cycle", "channel", "marker"],
    )
    region = metadata_df["region"].unique().item()
    return region, metadata_df


def organize_metadata_keyence(marker_dir: str) -> dict[str, pd.DataFrame]:
    """
    Keyence: Organize metadata for all regions in the final directory.

    Args:
        marker_dir (str): Directory containing subdirectories which contain marker files for a specific region.

    Returns:
        dict: Dictionary containing region names as keys and metadata DataFrames as values.
    """
    region_dirs = [os.path.join(marker_dir, subdir) for subdir in os.listdir(marker_dir)]
    metadata_dict = {}
    for region_dir in region_dirs:
        region, metadata_df = get_marker_metadata_keyence(region_dir)
        metadata_dict[region] = metadata_df
    return metadata_dict
