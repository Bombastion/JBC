load("@rules_python//python:defs.bzl", "py_binary")
load("@py_deps//:requirements.bzl", "requirement")

py_binary(
    name = "grpc_service",
    srcs = ["grpc_service.py"],
    deps = [
        "//api:service_py_proto",
        requirement("grpcio"),
        requirement("py"),
    ],
)