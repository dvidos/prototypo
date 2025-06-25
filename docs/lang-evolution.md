## Objective

It all boils down to adding up the layers:

* Assembly, one level above the CPU
* C, one level above assembly (give up on specific memory and instruction control, but simpler coding)
* Java / Python, one level above C (give up manial memory control, but simpler coding)
* What could come next?
  * Something generic enough
  * Giving up something (implementation) to gain simpler, higher level coding
  * Maybe it could be functional, express what is happening, not how. Don't code implementation.
  * Give up details in coding
    * e.g. [try / code / catch / code] for a failable block of code.
    * e.g. [load / validate / update / persist] for a update-type block.
  * It should automatically apply all the things we may forget as coders, e.g. events, follow-ups etc.
  * It could automatically handle cross-versions concerns (migrations etc)
  * It must definitely be some form of script / language / declaration style, to be compiled and run.
  * It may execute, or it may produce code.
  * Instead of variables (int, pointers) it could have higher level constructs:
    * A list of values, a specific business value (e.g. an ISBN)
    * A list of entities, an entity, an attribute
    * Predicates or Conditions, named, to combine and build logic on top
    * Policy or Rule, based on conditions, when failing means exception
    * Action, something fired or recurrent, having a load-update-persist cycle, producing side effects
    * Notification or Message, something with a recipient, waiting to be acted upon
    * Let's call the above a "Business Taxonomy"
  * Maybe plugins could bridge the gap between this abstract/business world and tech stack.
    * Databases (SQL + NoSQL) for persistence
    * TypeScript for UIs
    * API for communications, actions etc. Idempotency, authorization etc
    * Queues for messages
    * Let's have configured behaviors & code for each business taxonomy entry.
      * A set of behaviors can do something (e.g. produce a python app, or a Spring Boot app)
  * What do we give up?
    * Fine control of what happens when an API call is received
    * What index is used to load the entities
    * Names of tables or queues (do we really care?)
    * Names of variables, methods of iteration, etc
    * Implementation of Hashtables and other things in memory
    * Hand-crafted docker files creation
    * Implementation of Dead Letter Queues
    * Implementation of exponential back-off retry policy
    * Implementation of idempotency details
    * Having to write unit tests for business rules...
  * Examples of apps / systems:
    * Warehouse Management
    * Pet Clinic Calendar

  * Counter examples:
    * How would this system integrate with existing systems?
      (how can one describe detailed integration points to this system?)
    * How would this system aid with legacy systems?
      (how can one describe the legacy situation to this system?)
    * How would this system evolve versions that are in production?
      (how can one describe the production situation to this system?)
    * How can this system produce very performant systems?
      (e.g. can it generate Go/C++ code?)

### overall

* This is a tool that takes lots of files and produces code / changes.
* Business types are pre-defined and extendable
  * e.g. ValueType, Entity, Attribute, Condition, Policy, Action, Notification, etc
* Behavior and capabilities of the various business types are pre-defined and extendable
  * e.g. code generation, SQL table create / update, message queues creation etc
  * code could run in predefined runtimes as well (e.g. a FastAPI app, or SpringBoot app)
* Business instances are described (Customer, Invoice)
  * Description defines structure, behavior, policies, side effects etc.
  * They bridge the business description and system modification.
* The most simplest thing should be supported, by using useful defaults:


```
Aggregate Customer {
    Attributes {
        Name,
        Address
    }
}
FrontEnd MainUiApp {
    Tabs {
        Customer
    }
}
Environments {
    Dev {
        SqlServer { ... }
        Kubernetes { ... }
        Docker { ... }
    }
} 
```

The above should be enough to produce a usable minimal UI (React or TypeScript), 
with a back end, powered by some database, using some service.

Essentially, such system could be the bridge between Business Language
and application infrastructure, exactly the gap that a senior/staff engineer
would fill, by talking both the business language and the computer language.

