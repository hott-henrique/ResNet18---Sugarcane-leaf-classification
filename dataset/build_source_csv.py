import argparse, json, os, re


def main(base_path: str, metadata_path: str, include_extra_columns: bool):
    diseases_dir = os.path.join(base_path, "Diseases")
    dried_leaves_dir = os.path.join(base_path, "Dried Leaves")
    healthy_leaves_dir = os.path.join(base_path, "Healthy Leaves")

    columns = [ "image_path", "image_class" ]

    if include_extra_columns:
        with open(metadata_path, mode="r") as f:
            MAP_VIDEOS_ID = json.load(f)

        columns = [ "context", "video_id", "out_of_distribution", "zoom", "from_internet" ] + columns

    print(*columns, sep=',')

    for file in os.listdir(dried_leaves_dir):
        if not file.endswith(".jpg"):
            continue

        columns = [ os.path.join("Dried Leaves", file), "Dried Leaves" ]

        if include_extra_columns:
            m = re.search(r".*?(\d+)\.jpg$", file)

            if m is None:
                raise ValueError()

            x = int(m.group(1))

            d: dict = next(filter(lambda d: x >= d["image_suffix_start"] and x <= d["image_suffix_end"], MAP_VIDEOS_ID["Dried Leaves"]))

            columns = [
                d["context"],
                d["video_id"],
                d.get("out_of_distribution", 0), d.get("zoom", 0), d.get("from_internet", 0)
            ] + columns

        print(*columns, sep=',')

    for file in os.listdir(healthy_leaves_dir):
        if not file.endswith(".jpg"):
            continue

        columns = [ os.path.join("Healthy Leaves", file), "Healthy Leaves" ]

        if include_extra_columns:
            m = re.search(r".*?(\d+)\.jpg$", file)

            if m is None:
                raise ValueError()

            x = int(m.group(1))

            d: dict = next(filter(lambda d: x >= d["image_suffix_start"] and x <= d["image_suffix_end"], MAP_VIDEOS_ID["Healthy Leaves"]))

            columns = [
                d["context"],
                d["video_id"],
                d.get("out_of_distribution", 0), d.get("zoom", 0), d.get("from_internet", 0)
            ] + columns

        print(*columns, sep=',')

    diseases_classes = [
        file
        for file in os.listdir(diseases_dir)
        if os.path.isdir(os.path.join(diseases_dir, file))
    ]

    diseases_classes = [
        "Banded Chlorosis",
        "BrownRust",
        "Brown Spot",
        "Grassy shoot",
        "Pokkah Boeng",
        "Sett Rot",
        "smut",
        "Viral Disease",
        "Yellow Leaf"
    ]

    for disease_class in diseases_classes:
        disease_dir = os.path.join(diseases_dir, disease_class)

        for file in os.listdir(disease_dir):
            if not file.endswith(".jpg"):
                continue

            columns = [ os.path.join("Diseases", disease_class, file), disease_class ]

            if include_extra_columns:
                m = re.search(r".*?(\d+)\.jpg$", file)

                if m is None:
                    raise ValueError()

                x = int(m.group(1))

                d: dict = next(filter(lambda d: x >= d["image_suffix_start"] and x <= d["image_suffix_end"], MAP_VIDEOS_ID[disease_class]))

                columns = [
                    d["context"],
                    d["video_id"],
                    d.get("out_of_distribution", 0), d.get("zoom", 0), d.get("from_internet", 0)
                ] + columns

            print(*columns, sep=',')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--base-path",
        type=str,
        required=True,
        help='The base path with the following folders: "Diseases", "Dried Leaves" and "Healthy Leaves".'
    )

    parser.add_argument(
        "--metadata-path",
        type=str,
        required=True,
        help='The path for the metadata json.'
    )

    parser.add_argument(
        "--include-extra-columns",
        action="store_true",
        default=False,
        required=False,
        help='Flag to inclue the extra columns: "video_id", "context", "out_of_distribution"'
    )

    args = parser.parse_args()

    main(
        base_path=args.base_path,
        metadata_path=args.metadata_path,
        include_extra_columns=args.include_extra_columns
    )
