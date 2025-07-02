# todo


## what to do / where to go

* One full flow from UI, to backend, to database and back
* Add caching, e.g. Redis
* Add events queue, e.g. RabbitMQ
* Add consumers for events queue, for async processing
* Add actions per entity
* Add plugin to create Java Spring Boot app (instead of Python FastAPI)
* Add other infra (vault, monitoring, logging, feature toggling)

## what has been done

* Reading TF-like syntax, into tree of blocks and assignments
* Plugin architecture, discovers plugins in the `plugins` directory
* Plugins can utilize templates to generate configuration / code
* Internal core (mental) model of:
  * Services (e.g. redis or application server)
  * Entities (e.g. user, product, order)
  * Value Types (e.g. Email, ISBN, UPC)
  * Domain Actions (e.g. subscribe, purchase, promote)
  * Controllers, Endpoints, DataModels
* Internal model populated from DSL via plugins
* Given the core model, plugins generate code for apps, configuration for docker, k8s etc.
