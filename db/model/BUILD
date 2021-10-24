load("@rules_python//python:defs.bzl", "py_library")
load("@py_deps//:requirements.bzl", "requirement")

py_library(
    name = "models",
    srcs = ["__init__.py"],
    deps = [
        requirement("psycopg2"),
        requirement("SQLAlchemy"),
    ],
    visibility=["//:__subpackages__"]
)
