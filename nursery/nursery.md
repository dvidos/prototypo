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