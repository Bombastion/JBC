load("@rules_python//python:defs.bzl", "py_binary")
load("@py_deps//:requirements.bzl", "requirement")

py_binary(
    name = "flask_service",
    srcs = ["flask_service.py"],
    deps = [
        "//db/model:models",
        requirement("Flask"),
    ],
)