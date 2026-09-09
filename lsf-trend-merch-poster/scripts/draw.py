"""Draw independent uniform choices; preserve explicitly selected values."""
import argparse
import json
import secrets


def draw(mode="random", background="random"):
    modes = tuple("ABCDEFG")
    backgrounds = tuple("ABC")
    if mode not in (*modes, "random"):
        raise ValueError("mode must be A-G or random")
    if background not in (*backgrounds, "random"):
        raise ValueError("background must be A-C or random")
    return {
        "mode": secrets.choice(modes) if mode == "random" else mode,
        "background": secrets.choice(backgrounds) if background == "random" else background,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=[*"ABCDEFG", "random"], default="random")
    parser.add_argument("--background", choices=[*"ABC", "random"], default="random")
    args = parser.parse_args()
    print(json.dumps(draw(args.mode, args.background)))
