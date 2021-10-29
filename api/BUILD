load("@com_google_protobuf//:protobuf.bzl", "py_proto_library")

py_proto_library(
    name = "entities_py_proto",
    srcs = ["entities.proto"],
    visibility = ["//visibility:public"],
)

py_proto_library(
    name = "service_py_proto",
    srcs = ["service.proto"],
    deps = [
        ":entities_py_proto",
    ],
    visibility = ["//visibility:public"],
)