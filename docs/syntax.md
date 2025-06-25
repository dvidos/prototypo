# syntax

In a file we define blocks in curly braces

```
{
    # this is a comment
}
```

Each block can have a name and a type. If only one is given, it's considered a name.

```
entity Customer {
    # ...
}

notes {
    # ...
}
```

Inside a block there can be none to many subblocks, but also assignments.
These are in the following format:

```
{
    type name
    type name = value
    name = value
    name = "value in quotes"
    name
}
```

All the above should be enough for most of our declarations.