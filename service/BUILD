load("@rules_python//python:defs.bzl", "py_binary")
load("@py_deps//:requirements.bzl", "requirement")

filegroup(
    name = "templates",
    srcs = glob(["templates/*"]),
)

py_binary(
    name = "flask_service",
    srcs = ["flask_service.py"],
    data = [
        ":templates",
    ],
    deps = [
        "//db/model:models",
        requirement("Flask"),
    ],
)