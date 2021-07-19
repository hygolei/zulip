#cofazure

cofazure é um webhook que permite a integração com os eventos do Azure

##Estrutura
Este webhook é constituido por três ficheiros essenciais:
1) view.py -  Ficheiro onde se encontra o código do webhook.
2) bodyfunctions.py - Ficheiro onde se encontram as funçoes que controem os textos a publicar na Stream
3) teste.py - Ficheiro com os casos de testes.

Existe ainda uma subpasta (Fixtures) onde se encontram ficheiros de JSon onde se encontram os exemplos de retornos do Azure
Dentro dessa pasta existem subpastas divididas por grupos de eventos do Azure:
1) Build and Release
2) Code
3) Pipelines
4) Work Items

##Codigo

###bodyfunctions.py
Dentro deste ficheiro as funçoes para obter o texto estão divididas em classes consoante a divisão feita na pasta (fixtures), e segue esta estrutura:

```class code:
    def pull_request_updated_body(helper: Helper):
        return COFAZURE_TOPIC_TEMPLATE.format(title="Pull Request Updated"), \
               COFAZURE_MESSAGE_TEMPLATE.format(message=helper.payload["detailedMessage"]["text"])

    def checkin_body(helper: Helper):
        return COFAZURE_TOPIC_TEMPLATE.format(title="Check In"), \
               COFAZURE_MESSAGE_TEMPLATE.format(message=helper.payload["detailedMessage"]["text"])
```

###view.py
Dentro deste ficheiro está o codigo do webhook e o essencial é

- Importação do ficheiro das funçoes
```
    import bodyfunctions as bf
```
- Mapeamento de eventos com funções
```
EVENT_FUNCTION_MAPPER:Dict[str, Dict[str, Any]] ={
    "ms.vss-release.deployment-started-event": {"Function":bf.BuildandRelease.release_deployment_started_body,
                                                "Active":True},
    "build.complete": {"Function": bf.BuildandRelease.build_completed_body,
                       "Active": True},
    "ms.vss-release.release-abandoned-event": {"Function": bf.BuildandRelease.release_abandoned_body,
                                               "Active": True},
    "ms.vss-release.release-created-event": {"Function": bf.BuildandRelease.release_created_body,
                                             "Active": True},
    "ms.vss-release.deployment-approval-completed-event": {"Function": bf.BuildandRelease.release_deployment_approval_completed_body,
                                                           "Active": True},
    "ms.vss-release.deployment-approval-pending-event": {"Function": bf.BuildandRelease.release_deployment_approval_pending_body,
                                                         "Active": True},
    "git.pullrequest.merged": {"Function": bf.code.pull_request_merged_body,
                               "Active": True},
    "git.pullrequest.updated": {"Function": bf.code.pull_request_updated_body,
                                "Active": True},
    "tfvc.checkin": {"Function": bf.code.checkin_body,
                     "Active": True},
    "git.push": {"Function": bf.code.push_body(),
                 "Active": True},
    "git.pullrequest.created": {"Function": bf.code.pull_request_created_body(),
                                "Active": True},
    "ms.vss-pipelines.run-state-changed-event": {"Function": bf.pipelines.run_state_changed_body,
                                                 "Active": True},
    "ms.vss-pipelinechecks-events.approval-completed": {"Function": bf.pipelines.run_stage_approval_completed_body,
                                                        "Active": True},
    "ms.vss-pipelinechecks-events.approval-pending": {"Function": bf.pipelines.run_stage_waiting_for_approval_body,
                                                      "Active": True},
    "ms.vss-pipelines.stage-state-changed-event": {"Function": bf.pipelines.run_stage_state_changed_body,
                                                   "Active": True},
    "workitem.restored": {"Function": bf.workitems.work_item_restored_body,
                          "Active": True},
    "workitem.updated": {"Function": bf.workitems.work_item_updated_body,
                         "Active": True},
    "workitem.commented": {"Function": bf.workitems.work_item_commented_body,
                           "Active": True},
    "workitem.created": {"Function": bf.workitems.work_item_created_body,
                         "Active": True},
    "workitem.deleted": {"Function": bf.workitems.work_item_deleted_body,
                         "Active": True},
}
```
- Dentro da função do webhook
    - existe uma variável chamada payload que tem o conteúdo do json enviado pelo Azure em formato dicionário
        Para aceder a um dicionário em Python faz-se da seguinte maneira:

            payload["Nome atributo"]
            ou
            payload["Nome atributo"]["Nome sub-atributo"]

    - Com a variavel payload retira-se o tipo de evento:
        ```
        payload["eventType]
        ```
    - Com o evento obtem-se a função a executar:
        ```
        EVENT_FUNCTION_MAPPER[event]["Function"]
        ```
    - Com o evento obtem-se o estado da função a executar:
        ```
        EVENT_FUNCTION_MAPPER[event]["Active"]
        ```
    - Executa-se a função para obter a mensagem e o topico
        ```
        topic, body = body_function(helper)
        ```
    - Envia-se a mensagem para a stream
        ```
        check_send_webhook_message(request, user_profile, topic, body)
        ```

