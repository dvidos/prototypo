# todo


## what to do / where to go

(to get to next point)

* each entity, create a "module" folder in backend, with:
  * controller
  * service
  * repository
  * entity
* make the init sql add 2 random rows to each entity
* then make the front end call the backend 
  * list all entities
  * create new entity
  * update existing entity
  * delete existing entity


(overall)

* One full flow from UI, to backend, to database and back
* Add caching, e.g. Redis
* Add events queue, e.g. RabbitMQ, using outbox table
* Add consumers for events queue, for async processing
* Add actions per entity
* Ability to distribute entities to one or many microservices
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
