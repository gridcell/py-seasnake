import os
import shutil
from pathlib import Path

import pytest
from pandas import DataFrame

from seasnake.base import MERMAID_API_URL
from seasnake.summaries import BenthicPIT, base


@pytest.fixture
def project_id():
    return "abc"


@pytest.fixture
def api_one_record(project_id):
    return {
        "count": 1,
        "results": [
            {
                "id": "1",
                "name": "John Doe",
                "phone": "555-555-5555",
                "latitude": "34.0522",
                "longitude": "-118.2437",
                "website": "https://example.com",
                "project_id": project_id,
                "created_on": "2023-01-01 00:00:00",
            }
        ],
    }


@pytest.fixture
def api_records(project_id):
    return {
        "count": 2,
        "results": [
            {
                "id": "1",
                "name": "John Doe",
                "phone": "555-555-5555",
                "latitude": "34.0522",
                "longitude": "-118.2437",
                "website": "https://example.com",
                "project_id": project_id,
                "created_on": "2023-01-01 00:00:00",
            },
            {
                "id": "2",
                "name": "Jane Doe",
                "phone": "666-666-6666",
                "latitude": "49.0522",
                "longitude": "-110.3434",
                "project_id": project_id,
                "created_on": "2023-01-01 00:00:00",
            },
        ],
    }


@pytest.fixture
def benthic_pit_obs_url_path(project_id):
    return f"/projects/{project_id}/benthicpits/obstransectbenthicpits/"


@pytest.fixture
def benthic_pit_obs_url(benthic_pit_obs_url_path):
    return f"{MERMAID_API_URL}{benthic_pit_obs_url_path}"


@pytest.fixture
def cache_dir_path():
    original_cache_dir = base.CACHE_DIR
    test_cache_dir = Path(os.getcwd(), ".cache-test")
    base.CACHE_DIR = test_cache_dir
    yield
    base.CACHE_DIR = original_cache_dir
    shutil.rmtree(test_cache_dir, ignore_errors=True)


@pytest.fixture
def benthic_pit_mock_limit_1(
    requests_mock, benthic_pit_obs_url, api_one_record, api_records
):
    requests_mock.get(
        f"{benthic_pit_obs_url}?limit=1", json=api_one_record, status_code=200
    )


@pytest.fixture
def benthic_pit_mock_limit_1000(
    requests_mock, benthic_pit_obs_url, api_one_record, api_records
):
    requests_mock.get(
        f"{benthic_pit_obs_url}?limit=1000", json=api_records, status_code=200
    )


@pytest.fixture()
def bentic_pit_cache(api_records, benthic_pit_obs_url_path, cache_dir_path):
    df = DataFrame(api_records["results"])
    pit = BenthicPIT()
    pit.to_cache(benthic_pit_obs_url_path, df)


def test_write_cache(
    project_id,
    cache_dir_path,
    benthic_pit_obs_url,
    benthic_pit_mock_limit_1,
    benthic_pit_mock_limit_1000,
):
    pit = BenthicPIT()
    cache_file_path, cache_idx_file_path = pit.get_cache_file_paths(
        benthic_pit_obs_url
    )

    assert Path(cache_file_path).exists() is False
    assert Path(cache_idx_file_path).exists() is False

    pit.observations(project_id=project_id)
    assert Path(cache_file_path).exists()
    assert Path(cache_idx_file_path).exists()


def test_empty_data_frame_write_cache(benthic_pit_obs_url_path):
    pit = BenthicPIT()
    df = DataFrame()
    assert pit.to_cache(benthic_pit_obs_url_path, df).empty


def test_missing_created_on_frame_write_cache(
    benthic_pit_obs_url, benthic_pit_obs_url_path, api_one_record, requests_mock
):
    api_one_record["results"][0].pop("created_on")
    requests_mock.get(
        f"{benthic_pit_obs_url}?limit=1", json=api_one_record, status_code=200
    )
    pit = BenthicPIT()
    df = DataFrame()
    assert pit.to_cache(benthic_pit_obs_url_path, df).empty


def test_read_cache(project_id, bentic_pit_cache, benthic_pit_mock_limit_1):
    pit = BenthicPIT()
    df = pit.observations(project_id=project_id)
    assert df is not None
    assert len(df) == 2


def test_read_no_cache(project_id, benthic_pit_mock_limit_1, benthic_pit_obs_url_path):
    pit = BenthicPIT()
    df = pit.read_cache(benthic_pit_obs_url_path)
    assert df is None
