# Webhooks for external integrations.
from typing import Any, Dict, Iterable

from django.http import HttpRequest, HttpResponse

from zerver.decorator import api_key_only_webhook_view
from zerver.lib.request import REQ, has_request_variables
from zerver.lib.response import json_success
from zerver.lib.webhooks.common import check_send_webhook_message
from zerver.models import UserProfile


@webhook_view('CofAzure')
@has_request_variables
def api_cofazure_webhook(
        request: HttpRequest,
	user_profile: UserProfile,
        payload: Dict[str, Iterable[Dict[str, Any]]]=REQ(argument_type='body'),
) -> HttpResponse:

    # construct the body of the message
    body = ''

    # try to add the Wikipedia article of the day
    body_template = 'Nova mensagem do azure : {detailedMessage}'
    body +=  body_template.format(detailedMessage=payload['detailedMessage']['text'])

    topic = payload['eventType']

    # send the message
    check_send_webhook_message(request, user_profile, topic, body)

    return json_success()
"""

from typing import Any, Callable, Dict, Iterable

from django.http import HttpRequest, HttpResponse
from zerver.decorator import log_exception_to_webhook_logger, webhook_view
from zerver.lib.request import REQ, has_request_variables
from zerver.lib.response import json_success
from zerver.lib.webhooks.common import check_send_webhook_message
from zerver.models import UserProfile
from zerver.lib.webhooks.bodyfunctions import BuildandRelease as br
from zerver.lib.webhooks.bodyfunctions import code as cd
from zerver.lib.webhooks.bodyfunctions import pipelines as pl
from zerver.lib.webhooks.bodyfunctions import workitems as wk

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

"""
"""
Mapeamento do eventtype devolvido pelo GIT
A cada eventtype está a associada uma função que devolve o body e o topic da mensagem a publicar
As funcoes encontram-se num outro ficheiro chamado bodyfunctions
"""
"""
EVENT_FUNCTION_MAPPER:Dict[str, Dict[str, Any]] ={
    "ms.vss-release.deployment-started-event": {"Function":br.release_deployment_started_body,
                                                "Active":True},
    "build.complete": {"Function": br.build_completed_body,
                       "Active": True},
    "ms.vss-release.release-abandoned-event": {"Function": br.release_abandoned_body,
                                               "Active": True},
    "ms.vss-release.release-created-event": {"Function": br.release_created_body,
                                             "Active": True},
    "ms.vss-release.deployment-approval-completed-event": {"Function": br.release_deployment_approval_completed_body,
                                                           "Active": True},
    "ms.vss-release.deployment-approval-pending-event": {"Function": br.release_deployment_approval_pending_body,
                                                         "Active": True},
    "git.pullrequest.merged": {"Function": cd.pull_request_merged_body,
                               "Active": True},
    "git.pullrequest.updated": {"Function": cd.pull_request_updated_body,
                                "Active": True},
    "tfvc.checkin": {"Function": cd.checkin_body,
                     "Active": True},
    "git.push": {"Function": cd.push_body,
                 "Active": True},
    "git.pullrequest.created": {"Function": cd.pull_request_created_body,
                                "Active": True},
    "ms.vss-pipelines.run-state-changed-event": {"Function": pl.run_state_changed_body,
                                                 "Active": True},
    "ms.vss-pipelinechecks-events.approval-completed": {"Function": pl.run_stage_approval_completed_body,
                                                        "Active": True},
    "ms.vss-pipelinechecks-events.approval-pending": {"Function": pl.run_stage_waiting_for_approval_body,
                                                      "Active": True},
    "ms.vss-pipelines.stage-state-changed-event": {"Function": pl.run_stage_state_changed_body,
                                                   "Active": True},
    "workitem.restored": {"Function": wk.work_item_restored_body,
                          "Active": True},
    "workitem.updated": {"Function": wk.work_item_updated_body,
                         "Active": True},
    "workitem.commented": {"Function": wk.work_item_commented_body,
                           "Active": True},
    "workitem.created": {"Function": wk.work_item_created_body,
                         "Active": True},
    "workitem.deleted": {"Function": wk.work_item_deleted_body,
                         "Active": True},
}

@webhook_view('cofazure')
@has_request_variables
def api_cofazure_webhook(
    request: HttpRequest,
    user_profile: UserProfile,
    payload: Dict[str, Iterable[Dict[str, Any]]] = REQ(argument_type='body'),
) -> HttpResponse:
    # Retira o json que vem no body o valor do atributo eventType

    try:
        event = payload["eventType"]

        # Valida se o evento vem preenchido
        if event is None:
            # Helper.log_unsupported(event)
            return json_success()

        # Retira a função a executrar da lista configurada mais acima
        body_function = EVENT_FUNCTION_MAPPER[event]["Functions"]

        # Valida se existe função para o evento pretendido
        if body_function is None:
            # Helper.log_unsupported(event)
            return json_success()

        function_state = EVENT_FUNCTION_MAPPER[event]["Active"]

        if function_state == False:
            return json_success()

        # cria o objecto para passar para a função e atribui á variavel payload o conteudo do json do GIT
        helper = Helper(payload=payload,
                        include_title="",
                            )

        # executa a função para obter o topic e o body
        topic, body = body_function(helper)

        # publica na stream uma mensagem com o topic e o body obtidos
        check_send_webhook_message(request, user_profile, topic, body)
        return json_success()
    except:
        return json_success()
"""