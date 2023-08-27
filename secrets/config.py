import os
import typing as tp
import yaml
import enum


CONFIG_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "config.yaml")


class AppStates(str, enum.Enum):
    main = "main"
    testing = "testing"
    in_container = "in_container"

    ALL = [main, testing, in_container]


def read_all_config() -> dict:
    with open(CONFIG_PATH, "r") as cfg:
        return yaml.safe_load(stream=cfg)


def read_from_config(path: str) -> tp.Optional[str]:
    path = path.split(".")

    result = read_all_config()
    for key in path:
        if result is None:
            return result

        result = result.get(key)

    return result


def set_config(data: dict) -> None:
    with open(CONFIG_PATH, 'w') as cfg:
        yaml.safe_dump(data, cfg)


def update_config(path: str, value) -> None:
    path = path.split(".")
    with open(CONFIG_PATH, "r") as cfg:
        result = yaml.safe_load(stream=cfg)

    cursor = result
    for dir in path[:-1]:
        if dir not in cursor:
            cursor[dir] = dict()
        cursor = cursor[dir]
    cursor[path[-1]] = value

    with open(CONFIG_PATH, 'w') as cfg:
        yaml.safe_dump(result, cfg)


def get_current_env() -> str:
    if os.getenv(AppStates.testing, False):
        return "testing"
    elif os.getenv(AppStates.in_container, False):
        return "in_container"
    else:
        return "main"


def get_database_connection() -> dict:
    prefix = get_current_env() + ".postgres."

    return {
        "url": read_from_config(prefix + "url"),
        "pool_size": read_from_config(prefix + "pool_size"),
        "max_overflow":  read_from_config(prefix + "max_overflow"),
    }
