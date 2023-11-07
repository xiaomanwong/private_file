# xxx

@startwbs
* Business Process Modelling WBS
** Launch the project
*** Complete Stakeholder Research
*** Initial Implementation Plan
** Design phase
*** Model of AsIs Processes Completed
****< Model of AsIs Processes Completed1
****> Model of AsIs Processes Completed2
***< Measure AsIs performance metrics
***< Identify Quick Wins
@endwbs



@startyaml
ZapManager:
    - init(context, XRouterApp.() - Unit)
    - of(nameOrPath) -> ZapService
    - addService(nameOrPath, ZapService) -> ZapManager
    - alisa(path, name)
    - ticket(path) -> ZapTicket

ZapService:
    - onRoute(path, RouteRequest, ResultResolver)
    - onAction(path, action, param, options, ResultResolver)
    - onInit()
    - onExit()
ZapTicket:RouteTicket
    - withAction(action) -> ZapTicket
    - withServiceParams(JSONObject) -> ZapTicket
    - ship()
@endyaml


@startyaml
Ticket:RouteTicket


@endyaml