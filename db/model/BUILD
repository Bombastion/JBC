load("@rules_python//python:defs.bzl", "py_library")
load("@py_deps//:requirements.bzl", "requirement")

py_library(
    name = "models",
    srcs = ["__init__.py", "client.py", "item.py", "item_collection.py", "item_type.py", "sqlalchemy_base.py"],
    deps = [
        requirement("psycopg2"),
        requirement("SQLAlchemy"),
    ],
    visibility=["//:__subpackages__"]
)

py_library(
    name = "handler",
    srcs = ["model_handler.py"],
    deps = [
        ":models",
        requirement("psycopg2"),
        requirement("SQLAlchemy"),
    ],
    visibility=["//:__subpackages__"]
)
