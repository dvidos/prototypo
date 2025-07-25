# nursery

This is a prototype, proof-of-concept web application, 
aimed at verifying a design that features:

* A **backend** that offers an HTTP API
* A **frontend** that allows user interaction
* A **database** (SQL and/or NoSQL) to store data
* A **messaging** solution (e.g. Kafka & Debezium) for event propagation
* Asynchronous, reactive, event **consumers** for async processing
* **Caching** layer for performance.

Additionally, supporting services are to be demonstrated:

* Logs concentraction & querying
* Metrics concentration, dashboards, alerting
* Secrets management

The above ecosystem is to run in a containerized 
environment, which allows execution in local docker,
in kubernetes, or even as images in VMs.

## this to do

* backend, make OrderStatus a value type, return the options in some controller
* front end, make filters a shared component, create ability to filter orders by status
* front end, sort by clicking on columns headers
* backend, integrate OpenAPI, page with endpoints documentation 

## 1000 miles view

* Frontend allows users or AI to perform API calls
* API is exposed that allows actions to be triggered
* Actions will result in state changes and triggered events
* Events will result in async processing, further state changes and triggered events
* Finally, all data flow into lake, for analytics purposes

Concerns:

* API validations act as quality guard
* API should be idempotent, i.e. allow for retries over network failures
* Consumers should be idempotent, i.e. allow for republishing of events without ill effects
* Dual writes should follow at-least-once delivery principle, paired with idempotency leads to once processing
* Multiple deploys of same code must lock resources to avoid corruption and lost updates
* SQL changes become atomic with event publication via the outbox pattern
* To avoid spread of downtime in sync calls, the circuit breaker pattern can enable degraded more of operation
* Async processing can update a performant RO view (CQRS)
* An API gateway sits in front of all backend, to empower platform-like entry.
* If updates are required in distributed services, the Saga pattern is used.
