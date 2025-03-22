import pytest


@pytest.fixture
def mock_settings(mocker):
    settings_mock = mocker.patch('worker.consumer.settings')
    settings_mock.kafka_topic = 'test-topic'
    settings_mock.kafka_server = 'localhost:9092'
    settings_mock.kafka_group = 'test-group'
    return settings_mock
