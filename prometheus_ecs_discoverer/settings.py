BOTO3_DEBUG_LOGGING = False

PROMETHEUS_NAMESPACE = "PrometheusEcsDiscoverer_"
PROMETHEUS_SUBSYSTEM = ""

if BOTO3_DEBUG_LOGGING:
    import boto3

    boto3.set_stream_logger(name="botocore")
