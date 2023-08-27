import os

import pytest
import yaml

import secrets


class TestConfig:
    TEST_CONFIG = {
        "first_d": {
            "second_d": {
                "third": 228,
            },
            "second": "some_str",
        },
        "another_d": {
            "second": 66.6,
        },
        "testing": {
            "postgres": {
                "max_overflow": 1337,
                "pool_size": 666,
                "url": "secret_url"
            },
        },
    }

    ############
    # FIXTURES #
    ############

    @pytest.fixture(scope="function", autouse=True)
    def prepare_config(self):
        with open(secrets.config.CONFIG_PATH, 'r') as cfg:
            old_yaml = yaml.safe_load(stream=cfg)

        with open(secrets.config.CONFIG_PATH, 'w') as cfg:
            yaml.safe_dump(self.TEST_CONFIG, cfg)

        yield

        with open(secrets.config.CONFIG_PATH, 'w') as cfg:
            yaml.safe_dump(old_yaml, cfg)

    @pytest.fixture(scope="function")
    def set_enviroment_varialbe(self, request):
        os.environ.pop(secrets.AppStates.testing)
        os.environ[request.param] = 'True'

        yield

        os.environ.pop(request.param)
        os.environ[secrets.AppStates.testing] = 'True'

    #########
    # TESTS #
    #########

    def test_correctly_reads_all_from_config(self):
        result = secrets.read_all_config()

        assert result == self.TEST_CONFIG

    @pytest.mark.parametrize(
        "path", [
            "",
            "third",
            "first_d.third",
        ],
    )
    def test_returns_none_when_path_is_invalid(self, path):
        result = secrets.read_from_config(path)

        assert result is None

    @pytest.mark.parametrize(
        "path, expected_result", [
            ("first_d", TEST_CONFIG["first_d"]),
            ("first_d.second", "some_str"),
            ("another_d.second", 66.6),
        ],
    )
    def test_returns_correct_result(self, path, expected_result):
        result = secrets.read_from_config(path)

        assert result == expected_result

    def test_correctly_sets_config(self):
        new_config = {
            "new_d": {
                "new_val": 100,
            },
        }

        secrets.set_config(data=new_config)

        assert secrets.read_all_config() == new_config

    @pytest.mark.parametrize(
        "path, value_to_write", [
            ("first_d.second_d.third", 666),
            ("first_d.second_d", "another_str"),
            ("first_d.some_val", 13.37),
            ("new_d", "new_val"),
        ],
    )
    def test_correctly_writes_to_config(self, path, value_to_write):
        secrets.update_config(path, value_to_write)

        assert secrets.read_from_config(path) == value_to_write

    @pytest.mark.parametrize(
        "set_enviroment_varialbe, expected_env_var",
        [
            (secrets.AppStates.main, secrets.AppStates.main),
            (secrets.AppStates.testing, secrets.AppStates.testing),
            (secrets.AppStates.in_container, secrets.AppStates.in_container),
            ("random_var", secrets.AppStates.main),
        ],
        indirect=["set_enviroment_varialbe"],
    )
    def test_correctly_gets_current_env(self, set_enviroment_varialbe, expected_env_var):
        assert secrets.get_current_env() == expected_env_var

    def test_correctly_gets_database_connection(self):
        assert secrets.get_database_connection() == {
            "url": "secret_url",
            "pool_size": 666,
            "max_overflow": 1337,
        }
