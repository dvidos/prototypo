# output

The output of the application is 
code, documents, updates to infra, etc.

We identified that the best unit of output
will be _services_, examples can be:

* Database service (e.g. postgres)
* Backend service (e.g. a FastApi app)
* Frontend service (e.g. a React app)
* Caching service
* Messaging service
* A documentation service (e.g. Swagger)
* Other services (metrics, logs, etc)

## environments

The idea was that each service would have
support for various environments.
Each environment might be described in a 
`environment` block.

Given the output of the tool, it felt 
productive to make all the outputs 
containerized, and allow them to run
either on local docker, on local
kubernetes, or even on Cloud k8s clusters.

## plugins

The idea is that plugins register callbacks
on hooks. When these callbacks are called,
a `RunContext` is passed to them.

The plugins can then call methods on the 
context for adding and modifying services,
creating logs, errors etc.

So, entity plugins may contribute to 
backend services 
(for ORM models and CRUD controllers),
but also to database services
(for DDL scripts).

And finally, other plugins may use that information
to generate applications in various languages,
e.g. Python, Java etc.

