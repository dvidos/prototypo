# model

* service
  * (database, cache, messaging etc)
* backend app
  * endpoint
  * action
  * messages consumed
  * messages produced
* frontend app
  * menu
  * entity page (list, create, update, delete)


## information flow

* from data files to internal model (context, backend, frontend)
* from model to code and `docker-compose.yaml`
  * simple services like SQL
  * services with code (backend, frontend)
