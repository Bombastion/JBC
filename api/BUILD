load("@rules_proto//proto:defs.bzl", "proto_library")

proto_library(
    name = "entities",
    srcs = ["entities.proto"],
)

proto_library(
    name = "service",
    srcs = ["service.proto"],
    deps = [
        ":entities",
    ],
)