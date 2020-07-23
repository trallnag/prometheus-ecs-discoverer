def test_extract_cluster_name():
    cluster_arn = "arn:aws:ecs:eu-central-1:4342432423:cluster/data-cluster"
    cluster_name = cluster_arn.split("/")[-1]
    assert cluster_name == "data-cluster"
