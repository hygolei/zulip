from zerver.lib.test_classes import WebhookTestCase


class cofazureTests(WebhookTestCase):
    STREAM_NAME = "cofazure"
    URL_TEMPLATE = "/api/v1/external/cofazure?stream={stream}"
    FIXTURE_DIR_NAME = "cofazure"

    def test_cofazure(self) -> None:
        expected_topic = "teste"
        expected_message = "teste"

        self.check_webhook(
            "hello",
            expected_topic,
            expected_message,
            content_type="application/x-www-form-urlencoded",
        )

        expected_message = "[Build](https://www.codeship.com/projects/10213/builds/973711) triggered by beanieboi on master branch started."
        self.check_webhook("cofazure", self.TOPIC, expected_message)

