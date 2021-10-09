load("@com_google_protobuf//:protobuf.bzl", "py_proto_library")

py_proto_library(
    name = "entities",
    srcs = ["entities.proto"],
)

py_proto_library(
    name = "service",
    srcs = ["service.proto"],
    deps = [
        ":entities",
    ],
)