# todo


## what to do / where to go

* Make DDD service save events along with db changes 
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

* narrow scope, this is becoming too bloated, focus
* make the init sql add 2 random rows to each entity
* then make the front end call the backend 
  * list all entities
  * create new entity
  * update existing entity
  * delete existing entity
* One full flow from UI, to backend, to database and back
* Add caching, e.g. Redis
* Add events queue, e.g. RabbitMQ, using outbox table
* Add consumers for events queue, for async processing



## thoughts on structural reform

* i want to have tests to verify functionality.
  * current approach is too experimental and non deterministic
  * tests should be the definitions of capabilities
  * examples:
    * parser: 
      * block is parsed with type and name
      * assignment is parsed with type, name, value
    * compiler
      * a plugin can register callbacks and will receive calls appropriately
      * the appropriate steps are performed
    * plugins
      * a plugin can run its own tests and validate itself
      * a plugin can register a new object type at root
      * a plugin can register an extension of an existing object
      * a plugin shall verify in its tests
* it seems we need a taxonomy of objects, in order to register new ones:
```
  system
      backend(s)
          microservices
              entities
                  attributes
                  invariants
                  relationships
                  controllers
                  actions
                  events produced
              consumers
              controllers (non-entity ones)
              background tasks
    front-end-apps
        screens
            menu
            entity list/entry
            actions
    environments
    policies
```

* there should be some determinism,
  there seems to be some vagueness in the translations,
  tests should be there to define requirements
  * **soon:** make plugins have test code to verify things
* who defines the struct of things? it seems
  plugins should be able to define new objects (dict) structure,
  and, based on blocks, should be able to (a) validate blocks,
  (b) parse block into the new "objects", 
  and possibly generate output as well
  * **future:** make plugins own definition, structure,
    validation, parsing of arbitrary objects, even as 
    extensions to current objects (e.g. extend entity)
