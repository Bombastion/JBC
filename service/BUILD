load("@rules_python//python:defs.bzl", "py_binary")
load("@py_deps//:requirements.bzl", "requirement")

filegroup(
    name = "templates",
    srcs = glob(["templates/*"]),
)

filegroup(
    name = "javascript",
    srcs = glob(["static/scripts/*"]),
)

filegroup(
    name = "styles",
    srcs = glob(["static/styles/*"]),
)

py_library(
    name = "server_exceptions",
    srcs = ["exception.py"],
    deps = [
        requirement("Flask"),
    ]
)

py_binary(
    name = "flask_service",
    srcs = ["flask_service.py"],
    data = [
        ":javascript",
        ":styles",
        ":templates",
    ],
    deps = [
        ":server_exceptions",
        "//db/model:models",
        "//db/model:handler",
        requirement("Flask"),
    ],
)
