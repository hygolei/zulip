from typing import Any, Dict, Iterable
from zerver.decorator import log_exception_to_webhook_logger

COFAZURE_TOPIC_TEMPLATE = "{title}"
COFAZURE_MESSAGE_TEMPLATE = "{message}"

class Helper:
    def __init__(
        self,
        payload: Dict[str, Iterable[Dict[str, Any]]],
        include_title: bool,
    ) -> None:
        self.payload = payload
        self.include_title = include_title

    def log_unsupported(self, event: str) -> None:
        summary = f"The '{event}' event isn't currently supported by the cofazure webhook"
        log_exception_to_webhook_logger(
            summary=summary,
            unsupported_event=True,
        )

class BuildandRelease:
    def build_completed_body(helper: Helper):
        return COFAZURE_TOPIC_TEMPLATE.format(title="Build completed"), \
               COFAZURE_MESSAGE_TEMPLATE.format(message=helper.payload["detailedMessage"]["text"])

    def release_deployment_started_body(helper: Helper):
        return COFAZURE_TOPIC_TEMPLATE.format(title="Release Deployment Started"), \
               COFAZURE_MESSAGE_TEMPLATE.format(message=helper.payload["detailedMessage"]["text"])

    def release_abandoned_body(helper: Helper):
        return COFAZURE_TOPIC_TEMPLATE.format(title="Release Abandoned"), \
               COFAZURE_MESSAGE_TEMPLATE.format(message=helper.payload["detailedMessage"]["text"])

    def release_created_body(helper: Helper):
        return COFAZURE_TOPIC_TEMPLATE.format(title="Release Created"), \
               COFAZURE_MESSAGE_TEMPLATE.format(message=helper.payload["detailedMessage"]["text"])

    def release_deployment_approval_completed_body(helper: Helper):
        return COFAZURE_TOPIC_TEMPLATE.format(title="Release Deployment Approval Completed"), \
               COFAZURE_MESSAGE_TEMPLATE.format(message=helper.payload["detailedMessage"]["text"])

    def release_deployment_approval_pending_body(helper: Helper):
        return COFAZURE_TOPIC_TEMPLATE.format(title="Release Deployment Approval Pending"), \
               COFAZURE_MESSAGE_TEMPLATE.format(message=helper.payload["detailedMessage"]["text"])

    def release_deployment_completed_body(helper: Helper):
        return COFAZURE_TOPIC_TEMPLATE.format(title="Release Deployment Completed"), \
               COFAZURE_MESSAGE_TEMPLATE.format(message=helper.payload["status"])

class code:
    def pull_request_updated_body(helper: Helper):
        return COFAZURE_TOPIC_TEMPLATE.format(title="Pull Request Updated"), \
               COFAZURE_MESSAGE_TEMPLATE.format(message=helper.payload["detailedMessage"]["text"])

    def checkin_body(helper: Helper):
        return COFAZURE_TOPIC_TEMPLATE.format(title="Check In"), \
               COFAZURE_MESSAGE_TEMPLATE.format(message=helper.payload["detailedMessage"]["text"])

    def push_body(helper: Helper):
        return COFAZURE_TOPIC_TEMPLATE.format(title="Push"), \
               COFAZURE_MESSAGE_TEMPLATE.format(message=helper.payload["detailedMessage"]["text"])

    def pull_request_created_body(helper: Helper):
        return COFAZURE_TOPIC_TEMPLATE.format(title="Pull Request Created"), \
               COFAZURE_MESSAGE_TEMPLATE.format(message=helper.payload["detailedMessage"]["text"])

    def pull_request_merged_body(helper: Helper):
        return COFAZURE_TOPIC_TEMPLATE.format(title="Pull Request Merged"), \
               COFAZURE_MESSAGE_TEMPLATE.format(message=helper.payload["detailedMessage"]["text"])

class pipelines:
    def run_state_changed_body(helper: Helper):
        return COFAZURE_TOPIC_TEMPLATE.format(title="Pipeline Run State Changed"), \
               COFAZURE_MESSAGE_TEMPLATE.format(message=helper.payload["detailedMessage"]["text"])

    def run_stage_approval_completed_body(helper: Helper):
        return COFAZURE_TOPIC_TEMPLATE.format(title="Pipeline Run Stage Approval Completed"), \
               COFAZURE_MESSAGE_TEMPLATE.format(message=helper.payload["detailedMessage"]["text"])

    def run_stage_state_changed_body(helper: Helper):
        return COFAZURE_TOPIC_TEMPLATE.format(title="Pipeline Run Stage State Changed"), \
               COFAZURE_MESSAGE_TEMPLATE.format(message=helper.payload["detailedMessage"]["text"])

    def run_stage_waiting_for_approval_body(helper: Helper):
        return COFAZURE_TOPIC_TEMPLATE.format(title="Pipeline Run Stage Waiting For Approval"), \
               COFAZURE_MESSAGE_TEMPLATE.format(message=helper.payload["detailedMessage"]["text"])

class workitems:
    def work_item_restored_body(helper: Helper):
        return COFAZURE_TOPIC_TEMPLATE.format(title="Work Item Restored"), \
               COFAZURE_MESSAGE_TEMPLATE.format(message=helper.payload["detailedMessage"]["text"])

    def work_item_updated_body(helper: Helper):
        return COFAZURE_TOPIC_TEMPLATE.format(title="Work Item Updated"), \
               COFAZURE_MESSAGE_TEMPLATE.format(message=helper.payload["detailedMessage"]["text"])

    def work_item_commented_body(helper: Helper):
        return COFAZURE_TOPIC_TEMPLATE.format(title="Work Item Commented"), \
               COFAZURE_MESSAGE_TEMPLATE.format(message=helper.payload["detailedMessage"]["text"])

    def work_item_created_body(helper: Helper):
        return COFAZURE_TOPIC_TEMPLATE.format(title="Work Item Created"), \
               COFAZURE_MESSAGE_TEMPLATE.format(message=helper.payload["detailedMessage"]["text"])

    def work_item_deleted_body(helper: Helper):
        return COFAZURE_TOPIC_TEMPLATE.format(title="Work Item Deleted"), \
               COFAZURE_MESSAGE_TEMPLATE.format(message=helper.payload["detailedMessage"]["text"])
