# propotypo

This project is an exploration of 
whether business semantics, 
in declarative form,
can allow the creation of a system,
and help bridge the gap between
product and engineering.

Personal notes: 
https://chatgpt.com/c/685b08b2-b914-8008-92eb-bfb2f12e46a5

## roadmap

* parse files
* generate a graph of objects
* discover and load plugins
* do something meaningful

## example

Given the input in the `hello.dsl` file:

```
entity Customer {
  fields {
    Fullname
    Address
  }
}
```

The following SQL was produced:

```sql
CREATE TABLE Customer (
  id INT PRIMARY KEY AUTO_INCREMENT,
  Fullname VARCHAR(255),
  Address VARCHAR(255)
);
```

Also, any file existing in the plugins folder, that contains a `Plugin` class
will be loaded.

## ports in generated system

So far the following ports are defined:

* 8000 - frontend, GET / and go from there
* 8080 - backend, endpoints start with "/api"
* 5432 - database, PostgreSQL
