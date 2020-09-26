# noqa

import datetime

from dateutil.tz import tzlocal, tzutc

list_clusters_response = {
    "clusterArns": ["arn:aws:ecs:eu-central-1:123456789123:cluster/cluster-name"],
    "ResponseMetadata": {
        "RequestId": "01234567-8901-2345-6789-012345678901",
        "HTTPStatusCode": 200,
        "HTTPHeaders": {
            "x-amzn-requestid": "01234567-8901-2345-6789-012345678901",
            "content-type": "application/x-amz-json-1.1",
            "content-length": "74",
            "date": "Tue, 20 Jul 2020 20:00:00 GMT",
        },
        "RetryAttempts": 0,
    },
}

list_container_instances_parameters = {
    "cluster": list_clusters_response["clusterArns"][0]
}
list_container_instances_response = {
    "containerInstanceArns": [
        "arn:aws:ecs:eu-central-1:123456789123:container-instance/01234567-8901-8325-6789-012345678901",
        "arn:aws:ecs:eu-central-1:123456789123:container-instance/e0e32bca-2890-4988-9c04-ebdef8085892",
    ],
    "ResponseMetadata": {
        "RequestId": "01234567-8901-2345-6789-012345678901",
        "HTTPStatusCode": 200,
        "HTTPHeaders": {
            "x-amzn-requestid": "01234567-8901-2345-6789-012345678901",
            "content-type": "application/x-amz-json-1.1",
            "content-length": "219",
            "date": "Tue, 20 Jul 2020 20:00:00 GMT",
        },
        "RetryAttempts": 0,
    },
}

list_task_definitions_response = {
    "taskDefinitionArns": [
        "arn:aws:ecs:eu-central-1:123456789123:task-definition/hello-world:1",
        "arn:aws:ecs:eu-central-1:123456789123:task-definition/cloudwatch-superman:2",
        "arn:aws:ecs:eu-central-1:123456789123:task-definition/webapp-template:4",
        "arn:aws:ecs:eu-central-1:123456789123:task-definition/webapp-test-1:2",
        "arn:aws:ecs:eu-central-1:123456789123:task-definition/webapp-test-2:2",
        "arn:aws:ecs:eu-central-1:123456789123:task-definition/webapp-test-3:2",
        "arn:aws:ecs:eu-central-1:123456789123:task-definition/webapp-test-4:1",
        "arn:aws:ecs:eu-central-1:123456789123:task-definition/daemon-service:1",
        "arn:aws:ecs:eu-central-1:123456789123:task-definition/hello:9",
        "arn:aws:ecs:eu-central-1:123456789123:task-definition/dockertest:25",
        "arn:aws:ecs:eu-central-1:123456789123:task-definition/what:13",
        "arn:aws:ecs:eu-central-1:123456789123:task-definition/eoifjioejffew:41",
    ],
    "ResponseMetadata": {
        "RequestId": "01234567-8901-2345-6789-012345678901",
        "HTTPStatusCode": 200,
        "HTTPHeaders": {
            "x-amzn-requestid": "01234567-8901-2345-6789-012345678901",
            "content-type": "application/x-amz-json-1.1",
            "content-length": "912",
            "date": "Tue, 20 Jul 2020 20:00:00 GMT",
        },
        "RetryAttempts": 0,
    },
}

list_tasks_parameters = {"cluster": list_clusters_response["clusterArns"][0]}
list_tasks_response = {
    "taskArns": [
        "arn:aws:ecs:eu-central-1:123456789123:task/36f40835-a5d5-4750-95d1-6c9aa56fd3d9",
        "arn:aws:ecs:eu-central-1:123456789123:task/39d7befd-fe02-43dc-bc2a-6ae5b254fa38",
        "arn:aws:ecs:eu-central-1:123456789123:task/550b823c-288a-4f31-b3e1-69f9ea15060d",
        "arn:aws:ecs:eu-central-1:123456789123:task/5b8a1891-52ea-4357-8fd9-838478fd98f5",
        "arn:aws:ecs:eu-central-1:123456789123:task/867a60d8-895d-44de-930f-da5c798c0d40",
        "arn:aws:ecs:eu-central-1:123456789123:task/8bb1f532-1692-4b54-87f4-3ef68c52c754",
        "arn:aws:ecs:eu-central-1:123456789123:task/965a605a-756d-47ef-b2af-3a7d97ea1de8",
        "arn:aws:ecs:eu-central-1:123456789123:task/994bc3c2-2ff5-4e4a-8a57-9b83b923b167",
        "arn:aws:ecs:eu-central-1:123456789123:task/a2c31dcc-c1b6-4029-ba22-7b93cb783222",
        "arn:aws:ecs:eu-central-1:123456789123:task/ac0e543f-5045-40a7-a71a-1af681526227",
        "arn:aws:ecs:eu-central-1:123456789123:task/b30df74b-ba07-401a-a15c-e2b568047b8c",
        "arn:aws:ecs:eu-central-1:123456789123:task/c254f88b-80ff-4a37-b3e7-28c8371761eb",
        "arn:aws:ecs:eu-central-1:123456789123:task/c9d57886-be2e-4422-8191-f36a505b9578",
        "arn:aws:ecs:eu-central-1:123456789123:task/cb22b941-1d03-4e6b-b315-1dcd91bc9055",
        "arn:aws:ecs:eu-central-1:123456789123:task/e3154ac9-2d17-4d5e-89d2-408063ebee64",
        "arn:aws:ecs:eu-central-1:123456789123:task/f9cd702b-62c2-416d-92bf-b0ce7d3eb684",
    ],
    "ResponseMetadata": {
        "RequestId": "01234567-8901-2345-6789-012345678901",
        "HTTPStatusCode": 200,
        "HTTPHeaders": {
            "x-amzn-requestid": "01234567-8901-2345-6789-012345678901",
            "content-type": "application/x-amz-json-1.1",
            "content-length": "1326",
            "date": "Tue, 20 Jul 2020 20:00:00 GMT",
        },
        "RetryAttempts": 0,
    },
}

describe_tasks_parameters = {
    "cluster": list_clusters_response["clusterArns"][0],
    "tasks": list_tasks_response["taskArns"]
}
describe_tasks_response = {
    "tasks": [
        {
            "attachments": [],
            "availabilityZone": "eu-central-1a",
            "clusterArn": "arn:aws:ecs:eu-central-1:123456789123:cluster/cluster-name",
            "connectivity": "CONNECTED",
            "connectivityAt": datetime.datetime(
                2020, 7, 28, 17, 25, 25, 33000, tzinfo=tzlocal()
            ),
            "containerInstanceArn": "arn:aws:ecs:eu-central-1:123456789123:container-instance/01234567-8901-8325-6789-012345678901",
            "containers": [
                {
                    "containerArn": "arn:aws:ecs:eu-central-1:123456789123:container/f4cbd3a6-3498-b4af-9a8d-9389c9a74dfb",
                    "taskArn": "arn:aws:ecs:eu-central-1:123456789123:task/36f40835-a5d5-4750-95d1-6c9aa56fd3d9",
                    "name": "datasource-template",
                    "image": "x",
                    "imageDigest": "sha256:1233",
                    "runtimeId": "123",
                    "lastStatus": "RUNNING",
                    "networkBindings": [
                        {
                            "bindIP": "0.0.0.0",
                            "containerPort": 80,
                            "hostPort": 32789,
                            "protocol": "tcp",
                        }
                    ],
                    "networkInterfaces": [],
                    "healthStatus": "UNKNOWN",
                    "cpu": "8",
                    "memoryReservation": "500",
                }
            ],
            "cpu": "8",
            "createdAt": datetime.datetime(
                2020, 7, 28, 17, 25, 25, 33000, tzinfo=tzlocal()
            ),
            "desiredStatus": "RUNNING",
            "group": "mygroup",
            "healthStatus": "UNKNOWN",
            "lastStatus": "RUNNING",
            "launchType": "EC2",
            "memory": "500",
            "overrides": {
                "containerOverrides": [{"name": "datasource-template"}],
                "inferenceAcceleratorOverrides": [],
            },
            "pullStartedAt": datetime.datetime(
                2020, 7, 28, 17, 25, 46, 52000, tzinfo=tzlocal()
            ),
            "pullStoppedAt": datetime.datetime(
                2020, 7, 28, 17, 25, 46, 52000, tzinfo=tzlocal()
            ),
            "startedAt": datetime.datetime(
                2020, 7, 28, 17, 25, 47, 52000, tzinfo=tzlocal()
            ),
            "startedBy": "foo",
            "tags": [],
            "taskArn": "arn:aws:ecs:eu-central-1:123456789123:task/36f40835-a5d5-4750-95d1-6c9aa56fd3d9",
            "taskDefinitionArn": "arn:aws:ecs:eu-central-1:123456789123:task-definition/webapp-template:4",
            "version": 2,
        },
        {
            "attachments": [],
            "availabilityZone": "eu-central-1a",
            "clusterArn": "arn:aws:ecs:eu-central-1:123456789123:cluster/cluster-name",
            "connectivity": "CONNECTED",
            "connectivityAt": datetime.datetime(
                2020, 7, 28, 13, 28, 33, 103000, tzinfo=tzlocal()
            ),
            "containerInstanceArn": "arn:aws:ecs:eu-central-1:123456789123:container-instance/01234567-8901-8325-6789-012345678901",
            "containers": [
                {
                    "containerArn": "arn:aws:ecs:eu-central-1:123456789123:container/e5c308b5-a21c-411b-8d3b-0f159f8607f8",
                    "taskArn": "arn:aws:ecs:eu-central-1:123456789123:task/39d7befd-fe02-43dc-bc2a-6ae5b254fa38",
                    "name": "cloudwatch-agent",
                    "image": "x",
                    "runtimeId": "123",
                    "lastStatus": "RUNNING",
                    "networkBindings": [],
                    "networkInterfaces": [],
                    "healthStatus": "UNKNOWN",
                    "cpu": "0",
                }
            ],
            "cpu": "128",
            "createdAt": datetime.datetime(
                2020, 7, 28, 13, 28, 33, 103000, tzinfo=tzlocal()
            ),
            "desiredStatus": "RUNNING",
            "group": "mygroup",
            "healthStatus": "UNKNOWN",
            "lastStatus": "RUNNING",
            "launchType": "EC2",
            "memory": "64",
            "overrides": {
                "containerOverrides": [{"name": "cloudwatch-agent"}],
                "inferenceAcceleratorOverrides": [],
            },
            "pullStartedAt": datetime.datetime(
                2020, 7, 28, 13, 28, 33, 162000, tzinfo=tzlocal()
            ),
            "pullStoppedAt": datetime.datetime(
                2020, 7, 28, 13, 28, 37, 162000, tzinfo=tzlocal()
            ),
            "startedAt": datetime.datetime(
                2020, 7, 28, 13, 28, 40, 162000, tzinfo=tzlocal()
            ),
            "startedBy": "foo",
            "tags": [],
            "taskArn": "arn:aws:ecs:eu-central-1:123456789123:task/39d7befd-fe02-43dc-bc2a-6ae5b254fa38",
            "taskDefinitionArn": "arn:aws:ecs:eu-central-1:123456789123:task-definition/cloudwatch-superman:2",
            "version": 2,
        },
        {
            "attachments": [],
            "availabilityZone": "eu-central-1b",
            "clusterArn": "arn:aws:ecs:eu-central-1:123456789123:cluster/cluster-name",
            "connectivity": "CONNECTED",
            "connectivityAt": datetime.datetime(
                2020, 7, 28, 16, 49, 19, 266000, tzinfo=tzlocal()
            ),
            "containerInstanceArn": "arn:aws:ecs:eu-central-1:123456789123:container-instance/e0e32bca-2890-4988-9c04-ebdef8085892",
            "containers": [
                {
                    "containerArn": "arn:aws:ecs:eu-central-1:123456789123:container/213d21d5-4718-4b7f-9f7d-a1b3a8e57ad8",
                    "taskArn": "arn:aws:ecs:eu-central-1:123456789123:task/550b823c-288a-4f31-b3e1-69f9ea15060d",
                    "name": "datasource-test-3",
                    "image": "x",
                    "imageDigest": "sha256:1233",
                    "runtimeId": "123",
                    "lastStatus": "RUNNING",
                    "networkBindings": [
                        {
                            "bindIP": "0.0.0.0",
                            "containerPort": 80,
                            "hostPort": 32794,
                            "protocol": "tcp",
                        }
                    ],
                    "networkInterfaces": [],
                    "healthStatus": "UNKNOWN",
                    "cpu": "8",
                    "memory": "200",
                    "memoryReservation": "50",
                }
            ],
            "cpu": "8",
            "createdAt": datetime.datetime(
                2020, 7, 28, 16, 49, 19, 266000, tzinfo=tzlocal()
            ),
            "desiredStatus": "RUNNING",
            "group": "mygroup",
            "healthStatus": "UNKNOWN",
            "lastStatus": "RUNNING",
            "launchType": "EC2",
            "memory": "50",
            "overrides": {
                "containerOverrides": [{"name": "datasource-test-3"}],
                "inferenceAcceleratorOverrides": [],
            },
            "pullStartedAt": datetime.datetime(
                2020, 7, 28, 16, 49, 41, 153000, tzinfo=tzlocal()
            ),
            "pullStoppedAt": datetime.datetime(
                2020, 7, 28, 16, 49, 41, 153000, tzinfo=tzlocal()
            ),
            "startedAt": datetime.datetime(
                2020, 7, 28, 16, 49, 42, 153000, tzinfo=tzlocal()
            ),
            "startedBy": "foo",
            "tags": [],
            "taskArn": "arn:aws:ecs:eu-central-1:123456789123:task/550b823c-288a-4f31-b3e1-69f9ea15060d",
            "taskDefinitionArn": "arn:aws:ecs:eu-central-1:123456789123:task-definition/webapp-test-3:2",
            "version": 2,
        },
        {
            "attachments": [],
            "availabilityZone": "eu-central-1b",
            "clusterArn": "arn:aws:ecs:eu-central-1:123456789123:cluster/cluster-name",
            "connectivity": "CONNECTED",
            "connectivityAt": datetime.datetime(
                2020, 7, 28, 17, 25, 25, 33000, tzinfo=tzlocal()
            ),
            "containerInstanceArn": "arn:aws:ecs:eu-central-1:123456789123:container-instance/e0e32bca-2890-4988-9c04-ebdef8085892",
            "containers": [
                {
                    "containerArn": "arn:aws:ecs:eu-central-1:123456789123:container/5deaffe8-0e84-4604-bda8-faa934bc4f09",
                    "taskArn": "arn:aws:ecs:eu-central-1:123456789123:task/5b8a1891-52ea-4357-8fd9-838478fd98f5",
                    "name": "datasource-template",
                    "image": "x",
                    "imageDigest": "sha256:1233",
                    "runtimeId": "123",
                    "lastStatus": "RUNNING",
                    "networkBindings": [
                        {
                            "bindIP": "0.0.0.0",
                            "containerPort": 80,
                            "hostPort": 32796,
                            "protocol": "tcp",
                        }
                    ],
                    "networkInterfaces": [],
                    "healthStatus": "UNKNOWN",
                    "cpu": "8",
                    "memoryReservation": "500",
                }
            ],
            "cpu": "8",
            "createdAt": datetime.datetime(
                2020, 7, 28, 17, 25, 25, 33000, tzinfo=tzlocal()
            ),
            "desiredStatus": "RUNNING",
            "group": "mygroup",
            "healthStatus": "UNKNOWN",
            "lastStatus": "RUNNING",
            "launchType": "EC2",
            "memory": "500",
            "overrides": {
                "containerOverrides": [{"name": "efefffe"}],
                "inferenceAcceleratorOverrides": [],
            },
            "pullStartedAt": datetime.datetime(
                2020, 7, 28, 17, 25, 46, 589000, tzinfo=tzlocal()
            ),
            "pullStoppedAt": datetime.datetime(
                2020, 7, 28, 17, 25, 46, 589000, tzinfo=tzlocal()
            ),
            "startedAt": datetime.datetime(
                2020, 7, 28, 17, 25, 47, 589000, tzinfo=tzlocal()
            ),
            "startedBy": "foo",
            "tags": [],
            "taskArn": "arn:aws:ecs:eu-central-1:123456789123:task/5b8a1891-52ea-4357-8fd9-838478fd98f5",
            "taskDefinitionArn": "arn:aws:ecs:eu-central-1:123456789123:task-definition/webapp-template:4",
            "version": 2,
        },
        {
            "attachments": [],
            "availabilityZone": "eu-central-1b",
            "clusterArn": "arn:aws:ecs:eu-central-1:123456789123:cluster/cluster-name",
            "connectivity": "CONNECTED",
            "connectivityAt": datetime.datetime(
                2020, 7, 28, 17, 28, 10, 453000, tzinfo=tzlocal()
            ),
            "containerInstanceArn": "arn:aws:ecs:eu-central-1:123456789123:container-instance/e0e32bca-2890-4988-9c04-ebdef8085892",
            "containers": [
                {
                    "containerArn": "arn:aws:ecs:eu-central-1:123456789123:container/5d8d4dcb-49bf-46fc-afa5-ee5091e794ca",
                    "taskArn": "arn:aws:ecs:eu-central-1:123456789123:task/867a60d8-895d-44de-930f-da5c798c0d40",
                    "name": "datasource-test-1",
                    "image": "x",
                    "imageDigest": "sha256:1233",
                    "runtimeId": "123",
                    "lastStatus": "RUNNING",
                    "networkBindings": [
                        {
                            "bindIP": "0.0.0.0",
                            "containerPort": 80,
                            "hostPort": 32798,
                            "protocol": "tcp",
                        }
                    ],
                    "networkInterfaces": [],
                    "healthStatus": "UNKNOWN",
                    "cpu": "8",
                    "memory": "200",
                    "memoryReservation": "50",
                }
            ],
            "cpu": "8",
            "createdAt": datetime.datetime(
                2020, 7, 28, 17, 28, 10, 453000, tzinfo=tzlocal()
            ),
            "desiredStatus": "RUNNING",
            "group": "mygroup",
            "healthStatus": "UNKNOWN",
            "lastStatus": "RUNNING",
            "launchType": "EC2",
            "memory": "50",
            "overrides": {
                "containerOverrides": [{"name": "x"}],
                "inferenceAcceleratorOverrides": [],
            },
            "pullStartedAt": datetime.datetime(
                2020, 7, 28, 17, 28, 32, 269000, tzinfo=tzlocal()
            ),
            "pullStoppedAt": datetime.datetime(
                2020, 7, 28, 17, 28, 33, 269000, tzinfo=tzlocal()
            ),
            "startedAt": datetime.datetime(
                2020, 7, 28, 17, 28, 34, 269000, tzinfo=tzlocal()
            ),
            "startedBy": "foo",
            "tags": [],
            "taskArn": "arn:aws:ecs:eu-central-1:123456789123:task/867a60d8-895d-44de-930f-da5c798c0d40",
            "taskDefinitionArn": "arn:aws:ecs:eu-central-1:123456789123:task-definition/webapp-test-1:2",
            "version": 2,
        },
        {
            "attachments": [],
            "availabilityZone": "eu-central-1b",
            "clusterArn": "arn:aws:ecs:eu-central-1:123456789123:cluster/cluster-name",
            "connectivity": "CONNECTED",
            "connectivityAt": datetime.datetime(
                2020, 7, 28, 13, 35, 26, 707000, tzinfo=tzlocal()
            ),
            "containerInstanceArn": "arn:aws:ecs:eu-central-1:123456789123:container-instance/e0e32bca-2890-4988-9c04-ebdef8085892",
            "containers": [
                {
                    "containerArn": "arn:aws:ecs:eu-central-1:123456789123:container/30a6c9bf-c013-4b58-bc85-e3caa3da5c53",
                    "taskArn": "arn:aws:ecs:eu-central-1:123456789123:task/8bb1f532-1692-4b54-87f4-3ef68c52c754",
                    "name": "testapp",
                    "image": "x",
                    "runtimeId": "123",
                    "lastStatus": "RUNNING",
                    "networkBindings": [
                        {
                            "bindIP": "0.0.0.0",
                            "containerPort": 80,
                            "hostPort": 32770,
                            "protocol": "tcp",
                        }
                    ],
                    "networkInterfaces": [],
                    "healthStatus": "UNKNOWN",
                    "cpu": "8",
                    "memoryReservation": "500",
                }
            ],
            "cpu": "8",
            "createdAt": datetime.datetime(
                2020, 7, 28, 13, 35, 26, 707000, tzinfo=tzlocal()
            ),
            "desiredStatus": "RUNNING",
            "group": "mygroup",
            "healthStatus": "UNKNOWN",
            "lastStatus": "RUNNING",
            "launchType": "EC2",
            "memory": "500",
            "overrides": {
                "containerOverrides": [{"name": "testapp"}],
                "inferenceAcceleratorOverrides": [],
            },
            "pullStartedAt": datetime.datetime(
                2020, 7, 28, 13, 35, 26, 713000, tzinfo=tzlocal()
            ),
            "pullStoppedAt": datetime.datetime(
                2020, 7, 28, 13, 35, 29, 713000, tzinfo=tzlocal()
            ),
            "startedAt": datetime.datetime(
                2020, 7, 28, 13, 35, 30, 713000, tzinfo=tzlocal()
            ),
            "startedBy": "foo",
            "tags": [],
            "taskArn": "arn:aws:ecs:eu-central-1:123456789123:task/8bb1f532-1692-4b54-87f4-3ef68c52c754",
            "taskDefinitionArn": "arn:aws:ecs:eu-central-1:123456789123:task-definition/eoifjioejffew:41",
            "version": 2,
        },
        {
            "attachments": [],
            "availabilityZone": "eu-central-1a",
            "clusterArn": "arn:aws:ecs:eu-central-1:123456789123:cluster/cluster-name",
            "connectivity": "CONNECTED",
            "connectivityAt": datetime.datetime(
                2020, 7, 28, 17, 28, 10, 453000, tzinfo=tzlocal()
            ),
            "containerInstanceArn": "arn:aws:ecs:eu-central-1:123456789123:container-instance/01234567-8901-8325-6789-012345678901",
            "containers": [
                {
                    "containerArn": "arn:aws:ecs:eu-central-1:123456789123:container/dfe94709-9729-48ff-960e-eaf057af5ebb",
                    "taskArn": "arn:aws:ecs:eu-central-1:123456789123:task/965a605a-756d-47ef-b2af-3a7d97ea1de8",
                    "name": "datasource-test-1",
                    "image": "x",
                    "imageDigest": "sha256:1233",
                    "runtimeId": "123",
                    "lastStatus": "RUNNING",
                    "networkBindings": [
                        {
                            "bindIP": "0.0.0.0",
                            "containerPort": 80,
                            "hostPort": 32790,
                            "protocol": "tcp",
                        }
                    ],
                    "networkInterfaces": [],
                    "healthStatus": "UNKNOWN",
                    "cpu": "8",
                    "memory": "200",
                    "memoryReservation": "50",
                }
            ],
            "cpu": "8",
            "createdAt": datetime.datetime(
                2020, 7, 28, 17, 28, 10, 453000, tzinfo=tzlocal()
            ),
            "desiredStatus": "RUNNING",
            "group": "mygroup",
            "healthStatus": "UNKNOWN",
            "lastStatus": "RUNNING",
            "launchType": "EC2",
            "memory": "50",
            "overrides": {
                "containerOverrides": [{"name": "x"}],
                "inferenceAcceleratorOverrides": [],
            },
            "pullStartedAt": datetime.datetime(
                2020, 7, 28, 17, 28, 31, 655000, tzinfo=tzlocal()
            ),
            "pullStoppedAt": datetime.datetime(
                2020, 7, 28, 17, 28, 31, 655000, tzinfo=tzlocal()
            ),
            "startedAt": datetime.datetime(
                2020, 7, 28, 17, 28, 32, 655000, tzinfo=tzlocal()
            ),
            "startedBy": "foo",
            "tags": [],
            "taskArn": "arn:aws:ecs:eu-central-1:123456789123:task/965a605a-756d-47ef-b2af-3a7d97ea1de8",
            "taskDefinitionArn": "arn:aws:ecs:eu-central-1:123456789123:task-definition/webapp-test-1:2",
            "version": 2,
        },
        {
            "attachments": [],
            "availabilityZone": "eu-central-1a",
            "clusterArn": "arn:aws:ecs:eu-central-1:123456789123:cluster/cluster-name",
            "connectivity": "CONNECTED",
            "connectivityAt": datetime.datetime(
                2020, 7, 28, 13, 41, 20, 963000, tzinfo=tzlocal()
            ),
            "containerInstanceArn": "arn:aws:ecs:eu-central-1:123456789123:container-instance/01234567-8901-8325-6789-012345678901",
            "containers": [
                {
                    "containerArn": "arn:aws:ecs:eu-central-1:123456789123:container/1e3553e3-2c1a-4448-a9aa-7043beb82e5d",
                    "taskArn": "arn:aws:ecs:eu-central-1:123456789123:task/994bc3c2-2ff5-4e4a-8a57-9b83b923b167",
                    "name": "gitlabci-dataloader",
                    "image": "x",
                    "imageDigest": "sha256:1233",
                    "runtimeId": "123",
                    "lastStatus": "RUNNING",
                    "networkBindings": [
                        {
                            "bindIP": "0.0.0.0",
                            "containerPort": 80,
                            "hostPort": 32774,
                            "protocol": "tcp",
                        }
                    ],
                    "networkInterfaces": [],
                    "healthStatus": "UNKNOWN",
                    "cpu": "2",
                    "memoryReservation": "100",
                }
            ],
            "cpu": "2",
            "createdAt": datetime.datetime(
                2020, 7, 28, 13, 41, 20, 963000, tzinfo=tzlocal()
            ),
            "desiredStatus": "RUNNING",
            "group": "mygroup",
            "healthStatus": "UNKNOWN",
            "lastStatus": "RUNNING",
            "launchType": "EC2",
            "memory": "100",
            "overrides": {
                "containerOverrides": [{"name": "gitlabci-dataloader"}],
                "inferenceAcceleratorOverrides": [],
            },
            "pullStartedAt": datetime.datetime(
                2020, 7, 28, 13, 41, 21, 65000, tzinfo=tzlocal()
            ),
            "pullStoppedAt": datetime.datetime(
                2020, 7, 28, 13, 41, 36, 65000, tzinfo=tzlocal()
            ),
            "startedAt": datetime.datetime(
                2020, 7, 28, 13, 41, 37, 65000, tzinfo=tzlocal()
            ),
            "startedBy": "foo",
            "tags": [],
            "taskArn": "arn:aws:ecs:eu-central-1:123456789123:task/994bc3c2-2ff5-4e4a-8a57-9b83b923b167",
            "taskDefinitionArn": "arn:aws:ecs:eu-central-1:123456789123:task-definition/hello:9",
            "version": 2,
        },
        {
            "attachments": [],
            "availabilityZone": "eu-central-1b",
            "clusterArn": "arn:aws:ecs:eu-central-1:123456789123:cluster/cluster-name",
            "connectivity": "CONNECTED",
            "connectivityAt": datetime.datetime(
                2020, 7, 28, 17, 22, 24, 237000, tzinfo=tzlocal()
            ),
            "containerInstanceArn": "arn:aws:ecs:eu-central-1:123456789123:container-instance/e0e32bca-2890-4988-9c04-ebdef8085892",
            "containers": [
                {
                    "containerArn": "arn:aws:ecs:eu-central-1:123456789123:container/dfae2aea-adc7-469b-bf29-21af40065a27",
                    "taskArn": "arn:aws:ecs:eu-central-1:123456789123:task/a2c31dcc-c1b6-4029-ba22-7b93cb783222",
                    "name": "datasource-test-4",
                    "image": "x",
                    "imageDigest": "sha256:1233",
                    "runtimeId": "123",
                    "lastStatus": "RUNNING",
                    "networkBindings": [
                        {
                            "bindIP": "0.0.0.0",
                            "containerPort": 80,
                            "hostPort": 32795,
                            "protocol": "tcp",
                        }
                    ],
                    "networkInterfaces": [],
                    "healthStatus": "UNKNOWN",
                    "cpu": "8",
                    "memory": "200",
                    "memoryReservation": "50",
                }
            ],
            "cpu": "8",
            "createdAt": datetime.datetime(
                2020, 7, 28, 17, 22, 24, 237000, tzinfo=tzlocal()
            ),
            "desiredStatus": "RUNNING",
            "group": "mygroup",
            "healthStatus": "UNKNOWN",
            "lastStatus": "RUNNING",
            "launchType": "EC2",
            "memory": "50",
            "overrides": {
                "containerOverrides": [{"name": "datasource-test-4"}],
                "inferenceAcceleratorOverrides": [],
            },
            "pullStartedAt": datetime.datetime(
                2020, 7, 28, 17, 22, 25, 358000, tzinfo=tzlocal()
            ),
            "pullStoppedAt": datetime.datetime(
                2020, 7, 28, 17, 22, 25, 358000, tzinfo=tzlocal()
            ),
            "startedAt": datetime.datetime(
                2020, 7, 28, 17, 22, 26, 358000, tzinfo=tzlocal()
            ),
            "startedBy": "foo",
            "tags": [],
            "taskArn": "arn:aws:ecs:eu-central-1:123456789123:task/a2c31dcc-c1b6-4029-ba22-7b93cb783222",
            "taskDefinitionArn": "arn:aws:ecs:eu-central-1:123456789123:task-definition/webapp-test-4:1",
            "version": 2,
        },
        {
            "attachments": [],
            "availabilityZone": "eu-central-1b",
            "clusterArn": "arn:aws:ecs:eu-central-1:123456789123:cluster/cluster-name",
            "connectivity": "CONNECTED",
            "connectivityAt": datetime.datetime(
                2020, 7, 28, 13, 37, 46, 256000, tzinfo=tzlocal()
            ),
            "containerInstanceArn": "arn:aws:ecs:eu-central-1:123456789123:container-instance/e0e32bca-2890-4988-9c04-ebdef8085892",
            "containers": [
                {
                    "containerArn": "arn:aws:ecs:eu-central-1:123456789123:container/15b485ab-1394-4994-aeea-52a9c10861ca",
                    "taskArn": "arn:aws:ecs:eu-central-1:123456789123:task/ac0e543f-5045-40a7-a71a-1af681526227",
                    "name": "prometheus",
                    "image": "x",
                    "runtimeId": "123",
                    "lastStatus": "RUNNING",
                    "networkBindings": [
                        {
                            "bindIP": "0.0.0.0",
                            "containerPort": 9090,
                            "hostPort": 32773,
                            "protocol": "tcp",
                        }
                    ],
                    "networkInterfaces": [],
                    "healthStatus": "UNKNOWN",
                    "cpu": "64",
                    "memoryReservation": "256",
                },
                {
                    "containerArn": "arn:aws:ecs:eu-central-1:123456789123:container/6a386c3b-ddd2-4651-84cc-905938e855a0",
                    "taskArn": "arn:aws:ecs:eu-central-1:123456789123:task/ac0e543f-5045-40a7-a71a-1af681526227",
                    "name": "loki",
                    "image": "x",
                    "runtimeId": "123",
                    "lastStatus": "RUNNING",
                    "networkBindings": [
                        {
                            "bindIP": "0.0.0.0",
                            "containerPort": 3100,
                            "hostPort": 32771,
                            "protocol": "tcp",
                        }
                    ],
                    "networkInterfaces": [],
                    "healthStatus": "UNKNOWN",
                    "cpu": "64",
                    "memoryReservation": "128",
                },
                {
                    "containerArn": "arn:aws:ecs:eu-central-1:123456789123:container/a5751e27-dab1-4c58-a9a0-d7335083debf",
                    "taskArn": "arn:aws:ecs:eu-central-1:123456789123:task/ac0e543f-5045-40a7-a71a-1af681526227",
                    "name": "grafana",
                    "image": "x",
                    "runtimeId": "123",
                    "lastStatus": "RUNNING",
                    "networkBindings": [
                        {
                            "bindIP": "0.0.0.0",
                            "containerPort": 3000,
                            "hostPort": 32772,
                            "protocol": "tcp",
                        }
                    ],
                    "networkInterfaces": [],
                    "healthStatus": "UNKNOWN",
                    "cpu": "64",
                    "memoryReservation": "128",
                },
                {
                    "containerArn": "arn:aws:ecs:eu-central-1:123456789123:container/ac71b6de-bf9f-4c54-9cd2-0813ad39266c",
                    "taskArn": "arn:aws:ecs:eu-central-1:123456789123:task/ac0e543f-5045-40a7-a71a-1af681526227",
                    "name": "nginx",
                    "image": "x",
                    "runtimeId": "123",
                    "lastStatus": "RUNNING",
                    "networkBindings": [
                        {
                            "bindIP": "0.0.0.0",
                            "containerPort": 80,
                            "hostPort": 32774,
                            "protocol": "tcp",
                        }
                    ],
                    "networkInterfaces": [],
                    "healthStatus": "UNKNOWN",
                    "cpu": "32",
                    "memoryReservation": "32",
                },
                {
                    "containerArn": "arn:aws:ecs:eu-central-1:123456789123:container/f4ee662b-b918-419e-94eb-33bb80588f0e",
                    "taskArn": "arn:aws:ecs:eu-central-1:123456789123:task/ac0e543f-5045-40a7-a71a-1af681526227",
                    "name": "prometheus_discovery",
                    "image": "x",
                    "runtimeId": "123",
                    "lastStatus": "RUNNING",
                    "networkBindings": [],
                    "networkInterfaces": [],
                    "healthStatus": "UNKNOWN",
                    "cpu": "8",
                    "memoryReservation": "32",
                },
            ],
            "cpu": "232",
            "createdAt": datetime.datetime(
                2020, 7, 28, 13, 37, 46, 256000, tzinfo=tzlocal()
            ),
            "desiredStatus": "RUNNING",
            "group": "mygroup",
            "healthStatus": "UNKNOWN",
            "lastStatus": "RUNNING",
            "launchType": "EC2",
            "memory": "576",
            "overrides": {
                "containerOverrides": [
                    {"name": "prometheus"},
                    {"name": "loki"},
                    {"name": "grafana"},
                    {"name": "nginx"},
                    {"name": "prometheus_discovery"},
                ],
                "inferenceAcceleratorOverrides": [],
            },
            "pullStartedAt": datetime.datetime(
                2020, 7, 28, 13, 37, 47, 605000, tzinfo=tzlocal()
            ),
            "pullStoppedAt": datetime.datetime(
                2020, 7, 28, 13, 38, 10, 605000, tzinfo=tzlocal()
            ),
            "startedAt": datetime.datetime(
                2020, 7, 28, 13, 38, 11, 605000, tzinfo=tzlocal()
            ),
            "startedBy": "foo",
            "tags": [],
            "taskArn": "arn:aws:ecs:eu-central-1:123456789123:task/ac0e543f-5045-40a7-a71a-1af681526227",
            "taskDefinitionArn": "arn:aws:ecs:eu-central-1:123456789123:task-definition/dockertest:25",
            "version": 2,
        },
        {
            "attachments": [],
            "availabilityZone": "eu-central-1b",
            "clusterArn": "arn:aws:ecs:eu-central-1:123456789123:cluster/cluster-name",
            "connectivity": "CONNECTED",
            "connectivityAt": datetime.datetime(
                2020, 7, 28, 13, 31, 44, 323000, tzinfo=tzlocal()
            ),
            "containerInstanceArn": "arn:aws:ecs:eu-central-1:123456789123:container-instance/e0e32bca-2890-4988-9c04-ebdef8085892",
            "containers": [
                {
                    "containerArn": "arn:aws:ecs:eu-central-1:123456789123:container/09cdfef3-caf7-4e9a-be75-bd224179f379",
                    "taskArn": "arn:aws:ecs:eu-central-1:123456789123:task/b30df74b-ba07-401a-a15c-e2b568047b8c",
                    "name": "ssh-forward",
                    "image": "x",
                    "imageDigest": "sha256:1233",
                    "runtimeId": "123",
                    "lastStatus": "RUNNING",
                    "networkBindings": [],
                    "networkInterfaces": [],
                    "healthStatus": "UNKNOWN",
                    "cpu": "8",
                    "memoryReservation": "50",
                }
            ],
            "cpu": "8",
            "createdAt": datetime.datetime(
                2020, 7, 28, 13, 31, 44, 323000, tzinfo=tzlocal()
            ),
            "desiredStatus": "RUNNING",
            "group": "mygroup",
            "healthStatus": "UNKNOWN",
            "lastStatus": "RUNNING",
            "launchType": "EC2",
            "memory": "50",
            "overrides": {
                "containerOverrides": [{"name": "ssh-forward"}],
                "inferenceAcceleratorOverrides": [],
            },
            "pullStartedAt": datetime.datetime(
                2020, 7, 28, 13, 31, 45, 611000, tzinfo=tzlocal()
            ),
            "pullStoppedAt": datetime.datetime(
                2020, 7, 28, 13, 31, 46, 611000, tzinfo=tzlocal()
            ),
            "startedAt": datetime.datetime(
                2020, 7, 28, 13, 31, 47, 611000, tzinfo=tzlocal()
            ),
            "startedBy": "foo",
            "tags": [],
            "taskArn": "arn:aws:ecs:eu-central-1:123456789123:task/b30df74b-ba07-401a-a15c-e2b568047b8c",
            "taskDefinitionArn": "arn:aws:ecs:eu-central-1:123456789123:task-definition/what:13",
            "version": 2,
        },
        {
            "attachments": [],
            "availabilityZone": "eu-central-1b",
            "clusterArn": "arn:aws:ecs:eu-central-1:123456789123:cluster/cluster-name",
            "connectivity": "CONNECTED",
            "connectivityAt": datetime.datetime(
                2020, 7, 28, 13, 28, 33, 103000, tzinfo=tzlocal()
            ),
            "containerInstanceArn": "arn:aws:ecs:eu-central-1:123456789123:container-instance/e0e32bca-2890-4988-9c04-ebdef8085892",
            "containers": [
                {
                    "containerArn": "arn:aws:ecs:eu-central-1:123456789123:container/9bb3110e-e0f2-47bf-9ed0-04be6f45d263",
                    "taskArn": "arn:aws:ecs:eu-central-1:123456789123:task/c254f88b-80ff-4a37-b3e7-28c8371761eb",
                    "name": "cloudwatch-agent",
                    "image": "x",
                    "runtimeId": "123",
                    "lastStatus": "RUNNING",
                    "networkBindings": [],
                    "networkInterfaces": [],
                    "healthStatus": "UNKNOWN",
                    "cpu": "0",
                }
            ],
            "cpu": "128",
            "createdAt": datetime.datetime(
                2020, 7, 28, 13, 28, 33, 103000, tzinfo=tzlocal()
            ),
            "desiredStatus": "RUNNING",
            "group": "mygroup",
            "healthStatus": "UNKNOWN",
            "lastStatus": "RUNNING",
            "launchType": "EC2",
            "memory": "64",
            "overrides": {
                "containerOverrides": [{"name": "cloudwatch-agent"}],
                "inferenceAcceleratorOverrides": [],
            },
            "pullStartedAt": datetime.datetime(
                2020, 7, 28, 13, 28, 33, 661000, tzinfo=tzlocal()
            ),
            "pullStoppedAt": datetime.datetime(
                2020, 7, 28, 13, 28, 37, 661000, tzinfo=tzlocal()
            ),
            "startedAt": datetime.datetime(
                2020, 7, 28, 13, 28, 40, 661000, tzinfo=tzlocal()
            ),
            "startedBy": "foo",
            "tags": [],
            "taskArn": "arn:aws:ecs:eu-central-1:123456789123:task/c254f88b-80ff-4a37-b3e7-28c8371761eb",
            "taskDefinitionArn": "arn:aws:ecs:eu-central-1:123456789123:task-definition/cloudwatch-superman:2",
            "version": 2,
        },
        {
            "attachments": [],
            "availabilityZone": "eu-central-1a",
            "clusterArn": "arn:aws:ecs:eu-central-1:123456789123:cluster/cluster-name",
            "connectivity": "CONNECTED",
            "connectivityAt": datetime.datetime(
                2020, 7, 28, 13, 35, 26, 707000, tzinfo=tzlocal()
            ),
            "containerInstanceArn": "arn:aws:ecs:eu-central-1:123456789123:container-instance/01234567-8901-8325-6789-012345678901",
            "containers": [
                {
                    "containerArn": "arn:aws:ecs:eu-central-1:123456789123:container/d06f3b06-ab34-4bda-85bc-d50011fadd67",
                    "taskArn": "arn:aws:ecs:eu-central-1:123456789123:task/c9d57886-be2e-4422-8191-f36a505b9578",
                    "name": "testapp",
                    "image": "x",
                    "runtimeId": "123",
                    "lastStatus": "RUNNING",
                    "networkBindings": [
                        {
                            "bindIP": "0.0.0.0",
                            "containerPort": 80,
                            "hostPort": 32772,
                            "protocol": "tcp",
                        }
                    ],
                    "networkInterfaces": [],
                    "healthStatus": "UNKNOWN",
                    "cpu": "8",
                    "memoryReservation": "500",
                }
            ],
            "cpu": "8",
            "createdAt": datetime.datetime(
                2020, 7, 28, 13, 35, 26, 707000, tzinfo=tzlocal()
            ),
            "desiredStatus": "RUNNING",
            "group": "mygroup",
            "healthStatus": "UNKNOWN",
            "lastStatus": "RUNNING",
            "launchType": "EC2",
            "memory": "500",
            "overrides": {
                "containerOverrides": [{"name": "testapp"}],
                "inferenceAcceleratorOverrides": [],
            },
            "pullStartedAt": datetime.datetime(
                2020, 7, 28, 13, 35, 28, 793000, tzinfo=tzlocal()
            ),
            "pullStoppedAt": datetime.datetime(
                2020, 7, 28, 13, 35, 30, 793000, tzinfo=tzlocal()
            ),
            "startedAt": datetime.datetime(
                2020, 7, 28, 13, 35, 30, 793000, tzinfo=tzlocal()
            ),
            "startedBy": "foo",
            "tags": [],
            "taskArn": "arn:aws:ecs:eu-central-1:123456789123:task/c9d57886-be2e-4422-8191-f36a505b9578",
            "taskDefinitionArn": "arn:aws:ecs:eu-central-1:123456789123:task-definition/eoifjioejffew:41",
            "version": 2,
        },
        {
            "attachments": [],
            "availabilityZone": "eu-central-1a",
            "clusterArn": "arn:aws:ecs:eu-central-1:123456789123:cluster/cluster-name",
            "connectivity": "CONNECTED",
            "connectivityAt": datetime.datetime(
                2020, 7, 28, 16, 43, 56, 801000, tzinfo=tzlocal()
            ),
            "containerInstanceArn": "arn:aws:ecs:eu-central-1:123456789123:container-instance/01234567-8901-8325-6789-012345678901",
            "containers": [
                {
                    "containerArn": "arn:aws:ecs:eu-central-1:123456789123:container/ce20a29e-bb51-4aa1-ba55-ff27817e23e4",
                    "taskArn": "arn:aws:ecs:eu-central-1:123456789123:task/cb22b941-1d03-4e6b-b315-1dcd91bc9055",
                    "name": "datasource-test-2",
                    "image": "x",
                    "imageDigest": "sha256:1233",
                    "runtimeId": "123",
                    "lastStatus": "STOPPED",
                    "exitCode": 137,
                    "networkBindings": [
                        {
                            "bindIP": "0.0.0.0",
                            "containerPort": 80,
                            "hostPort": 32788,
                            "protocol": "tcp",
                        }
                    ],
                    "networkInterfaces": [],
                    "healthStatus": "UNKNOWN",
                    "cpu": "8",
                    "memory": "200",
                    "memoryReservation": "50",
                }
            ],
            "cpu": "8",
            "createdAt": datetime.datetime(
                2020, 7, 28, 16, 43, 56, 801000, tzinfo=tzlocal()
            ),
            "desiredStatus": "STOPPED",
            "executionStoppedAt": datetime.datetime(
                2020, 7, 28, 17, 30, 53, tzinfo=tzlocal()
            ),
            "group": "mygroup",
            "healthStatus": "UNKNOWN",
            "lastStatus": "STOPPED",
            "launchType": "EC2",
            "memory": "50",
            "overrides": {
                "containerOverrides": [{"name": "datasource-test-2"}],
                "inferenceAcceleratorOverrides": [],
            },
            "pullStartedAt": datetime.datetime(
                2020, 7, 28, 16, 43, 58, 696000, tzinfo=tzlocal()
            ),
            "pullStoppedAt": datetime.datetime(
                2020, 7, 28, 16, 43, 58, 696000, tzinfo=tzlocal()
            ),
            "startedAt": datetime.datetime(
                2020, 7, 28, 16, 43, 59, 696000, tzinfo=tzlocal()
            ),
            "startedBy": "foo",
            "stoppedAt": datetime.datetime(
                2020, 7, 28, 17, 30, 53, 181000, tzinfo=tzlocal()
            ),
            "stoppedReason": "Task failed ELB health checks in (target-group arn:aws:elasticloadbalancing:eu-central-1:123456789123:targetgroup/datasource-test-2/8a07041d49ee2114)",
            "stoppingAt": datetime.datetime(
                2020, 7, 28, 17, 30, 20, 941000, tzinfo=tzlocal()
            ),
            "tags": [],
            "taskArn": "arn:aws:ecs:eu-central-1:123456789123:task/cb22b941-1d03-4e6b-b315-1dcd91bc9055",
            "taskDefinitionArn": "arn:aws:ecs:eu-central-1:123456789123:task-definition/webapp-test-2:2",
            "version": 4,
        },
        {
            "attachments": [],
            "availabilityZone": "eu-central-1b",
            "clusterArn": "arn:aws:ecs:eu-central-1:123456789123:cluster/cluster-name",
            "connectivity": "CONNECTED",
            "connectivityAt": datetime.datetime(
                2020, 7, 28, 13, 41, 20, 963000, tzinfo=tzlocal()
            ),
            "containerInstanceArn": "arn:aws:ecs:eu-central-1:123456789123:container-instance/e0e32bca-2890-4988-9c04-ebdef8085892",
            "containers": [
                {
                    "containerArn": "arn:aws:ecs:eu-central-1:123456789123:container/f264dfbc-5039-4eed-adce-8ec07f538367",
                    "taskArn": "arn:aws:ecs:eu-central-1:123456789123:task/e3154ac9-2d17-4d5e-89d2-408063ebee64",
                    "name": "gitlabci-dataloader",
                    "image": "x",
                    "imageDigest": "sha256:1233",
                    "runtimeId": "123",
                    "lastStatus": "RUNNING",
                    "networkBindings": [
                        {
                            "bindIP": "0.0.0.0",
                            "containerPort": 80,
                            "hostPort": 32775,
                            "protocol": "tcp",
                        }
                    ],
                    "networkInterfaces": [],
                    "healthStatus": "UNKNOWN",
                    "cpu": "2",
                    "memoryReservation": "100",
                }
            ],
            "cpu": "2",
            "createdAt": datetime.datetime(
                2020, 7, 28, 13, 41, 20, 963000, tzinfo=tzlocal()
            ),
            "desiredStatus": "RUNNING",
            "group": "mygroup",
            "healthStatus": "UNKNOWN",
            "lastStatus": "RUNNING",
            "launchType": "EC2",
            "memory": "100",
            "overrides": {
                "containerOverrides": [{"name": "gitlabci-dataloader"}],
                "inferenceAcceleratorOverrides": [],
            },
            "pullStartedAt": datetime.datetime(
                2020, 7, 28, 13, 41, 21, 104000, tzinfo=tzlocal()
            ),
            "pullStoppedAt": datetime.datetime(
                2020, 7, 28, 13, 41, 36, 104000, tzinfo=tzlocal()
            ),
            "startedAt": datetime.datetime(
                2020, 7, 28, 13, 41, 38, 104000, tzinfo=tzlocal()
            ),
            "startedBy": "foo",
            "tags": [],
            "taskArn": "arn:aws:ecs:eu-central-1:123456789123:task/e3154ac9-2d17-4d5e-89d2-408063ebee64",
            "taskDefinitionArn": "arn:aws:ecs:eu-central-1:123456789123:task-definition/hello:9",
            "version": 3,
        },
        {
            "attachments": [],
            "availabilityZone": "eu-central-1b",
            "clusterArn": "arn:aws:ecs:eu-central-1:123456789123:cluster/cluster-name",
            "connectivity": "CONNECTED",
            "connectivityAt": datetime.datetime(
                2020, 7, 28, 17, 28, 10, 453000, tzinfo=tzlocal()
            ),
            "containerInstanceArn": "arn:aws:ecs:eu-central-1:123456789123:container-instance/e0e32bca-2890-4988-9c04-ebdef8085892",
            "containers": [
                {
                    "containerArn": "arn:aws:ecs:eu-central-1:123456789123:container/a5aa86ea-fa2f-4103-9869-6a6b57efef39",
                    "taskArn": "arn:aws:ecs:eu-central-1:123456789123:task/f9cd702b-62c2-416d-92bf-b0ce7d3eb684",
                    "name": "datasource-test-1",
                    "image": "x",
                    "imageDigest": "sha256:1233",
                    "runtimeId": "123",
                    "lastStatus": "RUNNING",
                    "networkBindings": [
                        {
                            "bindIP": "0.0.0.0",
                            "containerPort": 80,
                            "hostPort": 32797,
                            "protocol": "tcp",
                        }
                    ],
                    "networkInterfaces": [],
                    "healthStatus": "UNKNOWN",
                    "cpu": "8",
                    "memory": "200",
                    "memoryReservation": "50",
                }
            ],
            "cpu": "8",
            "createdAt": datetime.datetime(
                2020, 7, 28, 17, 28, 10, 453000, tzinfo=tzlocal()
            ),
            "desiredStatus": "RUNNING",
            "group": "mygroup",
            "healthStatus": "UNKNOWN",
            "lastStatus": "RUNNING",
            "launchType": "EC2",
            "memory": "50",
            "overrides": {
                "containerOverrides": [{"name": "x"}],
                "inferenceAcceleratorOverrides": [],
            },
            "pullStartedAt": datetime.datetime(
                2020, 7, 28, 17, 28, 32, 121000, tzinfo=tzlocal()
            ),
            "pullStoppedAt": datetime.datetime(
                2020, 7, 28, 17, 28, 33, 121000, tzinfo=tzlocal()
            ),
            "startedAt": datetime.datetime(
                2020, 7, 28, 17, 28, 34, 121000, tzinfo=tzlocal()
            ),
            "startedBy": "foo",
            "tags": [],
            "taskArn": "arn:aws:ecs:eu-central-1:123456789123:task/f9cd702b-62c2-416d-92bf-b0ce7d3eb684",
            "taskDefinitionArn": "arn:aws:ecs:eu-central-1:123456789123:task-definition/webapp-test-1:2",
            "version": 2,
        },
    ],
    "failures": [],
    "ResponseMetadata": {
        "RequestId": "01234567-8901-2345-6789-012345678901",
        "HTTPStatusCode": 200,
        "HTTPHeaders": {
            "x-amzn-requestid": "01234567-8901-2345-6789-012345678901",
            "content-type": "application/x-amz-json-1.1",
            "content-length": "27735",
            "date": "Tue, 20 Jul 2020 20:00:00 GMT",
        },
        "RetryAttempts": 0,
    },
}

describe_task_definition_parameters = list_task_definitions_response["taskDefinitionArns"]
describe_task_definition_responses = [
    {
        "taskDefinition": {
            "taskDefinitionArn": "arn:aws:ecs:eu-central-1:123456789123:task-definition/hello-world:1",
            "containerDefinitions": [
                {
                    "name": "ww",
                    "image": "x",
                    "cpu": 0,
                    "memory": 128,
                    "portMappings": [],
                    "essential": True,
                    "environment": [],
                    "mountPoints": [],
                    "volumesFrom": [],
                }
            ],
            "family": "aa",
            "networkMode": "host",
            "revision": 1,
            "volumes": [],
            "status": "ACTIVE",
            "requiresAttributes": [
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.18"}
            ],
            "placementConstraints": [],
            "compatibilities": ["EC2"],
            "requiresCompatibilities": ["EC2"],
            "cpu": "1024",
            "memory": "1024",
        },
        "ResponseMetadata": {
            "RequestId": "01234567-8901-2345-6789-012345678901",
            "HTTPStatusCode": 200,
            "HTTPHeaders": {
                "x-amzn-requestid": "01234567-8901-2345-6789-012345678901",
                "content-type": "application/x-amz-json-1.1",
                "content-length": "543",
                "date": "Tue, 20 Jul 2020 20:00:00 GMT",
            },
            "RetryAttempts": 0,
        },
    },
    {
        "taskDefinition": {
            "taskDefinitionArn": "arn:aws:ecs:eu-central-1:123456789123:task-definition/cloudwatch-superman:2",
            "containerDefinitions": [
                {
                    "name": "cloudwatch-agent",
                    "image": "x",
                    "cpu": 0,
                    "portMappings": [],
                    "essential": True,
                    "environment": [{"name": "USE_DEFAULT_CONFIG", "value": "True"}],
                    "mountPoints": [
                        {
                            "sourceVolume": "proc",
                            "containerPath": "/rootfs/proc",
                            "readOnly": True,
                        },
                        {
                            "sourceVolume": "dev",
                            "containerPath": "/rootfs/dev",
                            "readOnly": True,
                        },
                        {
                            "sourceVolume": "al2_cgroup",
                            "containerPath": "/sys/fs/cgroup",
                            "readOnly": True,
                        },
                        {
                            "sourceVolume": "al1_cgroup",
                            "containerPath": "/cgroup",
                            "readOnly": True,
                        },
                        {
                            "sourceVolume": "al2_cgroup",
                            "containerPath": "/rootfs/sys/fs/cgroup",
                            "readOnly": True,
                        },
                        {
                            "sourceVolume": "al1_cgroup",
                            "containerPath": "/rootfs/cgroup",
                            "readOnly": True,
                        },
                    ],
                    "volumesFrom": [],
                    "logConfiguration": {
                        "logDriver": "awslogs",
                        "options": {
                            "awslogs-create-group": "True",
                            "awslogs-group": "loggroup",
                            "awslogs-region": "eu-central-1",
                            "awslogs-stream-prefix": "ecs",
                        },
                    },
                }
            ],
            "family": "cloudwatch-agent",
            "taskRoleArn": "arn:aws:iam::123456789123:role/cluster-name_ecs_task_role_cloudwatch_agent",
            "executionRoleArn": "arn:aws:iam::123456789123:role/cluster-name_ecs_task_execution_role",
            "networkMode": "bridge",
            "revision": 2,
            "volumes": [
                {"name": "al2_cgroup", "host": {"sourcePath": "/sys/fs/cgroup"}},
                {"name": "proc", "host": {"sourcePath": "/proc"}},
                {"name": "dev", "host": {"sourcePath": "/dev"}},
                {"name": "al1_cgroup", "host": {"sourcePath": "/cgroup"}},
            ],
            "status": "ACTIVE",
            "requiresAttributes": [
                {"name": "com.amazonaws.ecs.capability.logging-driver.awslogs"},
                {"name": "ecs.capability.execution-role-awslogs"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.19"},
                {"name": "com.amazonaws.ecs.capability.task-iam-role"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.29"},
            ],
            "placementConstraints": [],
            "compatibilities": ["EC2"],
            "requiresCompatibilities": ["EC2"],
            "cpu": "128",
            "memory": "64",
        },
        "ResponseMetadata": {
            "RequestId": "01234567-8901-2345-6789-012345678901",
            "HTTPStatusCode": 200,
            "HTTPHeaders": {
                "x-amzn-requestid": "01234567-8901-2345-6789-012345678901",
                "content-type": "application/x-amz-json-1.1",
                "content-length": "1901",
                "date": "Tue, 20 Jul 2020 20:00:00 GMT",
            },
            "RetryAttempts": 0,
        },
    },
    {
        "taskDefinition": {
            "taskDefinitionArn": "arn:aws:ecs:eu-central-1:123456789123:task-definition/webapp-template:4",
            "containerDefinitions": [
                {
                    "name": "datasource-template",
                    "image": "x",
                    "cpu": 8,
                    "memoryReservation": 500,
                    "portMappings": [
                        {"containerPort": 80, "hostPort": 0, "protocol": "tcp"}
                    ],
                    "essential": True,
                    "environment": [],
                    "mountPoints": [],
                    "volumesFrom": [],
                    "secrets": [],
                    "logConfiguration": {
                        "logDriver": "awslogs",
                        "options": {
                            "awslogs-datetime-format": "%Y%m%d-%H%M%S",
                            "awslogs-group": "loggroup",
                            "awslogs-region": "eu-central-1",
                            "awslogs-stream-prefix": "ecs",
                        },
                    },
                }
            ],
            "family": "datasource-template",
            "executionRoleArn": "arn:aws:iam::123456789123:role/cluster-name_ecs_task_execution_role",
            "revision": 4,
            "volumes": [],
            "status": "ACTIVE",
            "requiresAttributes": [
                {"name": "com.amazonaws.ecs.capability.logging-driver.awslogs"},
                {"name": "ecs.capability.execution-role-awslogs"},
                {"name": "com.amazonaws.ecs.capability.ecr-auth"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.19"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.21"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.30"},
                {"name": "ecs.capability.execution-role-ecr-pull"},
                {"name": "ecs.capability.secrets.ssm.environment-variables"},
            ],
            "placementConstraints": [],
            "compatibilities": ["EC2"],
        },
        "ResponseMetadata": {
            "RequestId": "01234567-8901-2345-6789-012345678901",
            "HTTPStatusCode": 200,
            "HTTPHeaders": {
                "x-amzn-requestid": "01234567-8901-2345-6789-012345678901",
                "content-type": "application/x-amz-json-1.1",
                "content-length": "1490",
                "date": "Tue, 20 Jul 2020 20:00:00 GMT",
            },
            "RetryAttempts": 0,
        },
    },
    {
        "taskDefinition": {
            "taskDefinitionArn": "arn:aws:ecs:eu-central-1:123456789123:task-definition/webapp-test-1:2",
            "containerDefinitions": [
                {
                    "name": "datasource-test-1",
                    "image": "x",
                    "cpu": 8,
                    "memory": 200,
                    "memoryReservation": 50,
                    "portMappings": [
                        {"containerPort": 80, "hostPort": 0, "protocol": "tcp"}
                    ],
                    "essential": True,
                    "environment": [
                        {
                            "name": "PROMETHEUS_ENDPOINT",
                            "value": "/app-1/metrics",
                        },
                        {
                            "name": "APP_BASE_PATH",
                            "value": "/app-1",
                        },
                        {"name": "PROMETHEUS_TARGET", "value": "true"},
                    ],
                    "mountPoints": [],
                    "volumesFrom": [],
                    "secrets": [
                
                    ],
                    "logConfiguration": {
                        "logDriver": "awslogs",
                        "options": {
                            "awslogs-datetime-format": "%Y%m%d-%H%M%S",
                            "awslogs-group": "loggroup",
                            "awslogs-region": "eu-central-1",
                            "awslogs-stream-prefix": "ecs",
                        },
                    },
                }
            ],
            "family": "datasource-test-1",
            "executionRoleArn": "arn:aws:iam::123456789123:role/cluster-name_ecs_task_execution_role",
            "revision": 2,
            "volumes": [],
            "status": "ACTIVE",
            "requiresAttributes": [
                {"name": "com.amazonaws.ecs.capability.logging-driver.awslogs"},
                {"name": "ecs.capability.execution-role-awslogs"},
                {"name": "com.amazonaws.ecs.capability.ecr-auth"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.19"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.21"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.30"},
                {"name": "ecs.capability.execution-role-ecr-pull"},
                {"name": "ecs.capability.secrets.ssm.environment-variables"},
            ],
            "placementConstraints": [],
            "compatibilities": ["EC2"],
        },
        "ResponseMetadata": {
            "RequestId": "01234567-8901-2345-6789-012345678901",
            "HTTPStatusCode": 200,
            "HTTPHeaders": {
                "x-amzn-requestid": "01234567-8901-2345-6789-012345678901",
                "content-type": "application/x-amz-json-1.1",
                "content-length": "1684",
                "date": "Tue, 20 Jul 2020 20:00:00 GMT",
            },
            "RetryAttempts": 0,
        },
    },
    {
        "taskDefinition": {
            "taskDefinitionArn": "arn:aws:ecs:eu-central-1:123456789123:task-definition/webapp-test-2:2",
            "containerDefinitions": [
                {
                    "name": "datasource-test-2",
                    "image": "x",
                    "cpu": 8,
                    "memory": 200,
                    "memoryReservation": 50,
                    "portMappings": [
                        {"containerPort": 80, "hostPort": 0, "protocol": "tcp"}
                    ],
                    "essential": True,
                    "environment": [
                        {
                            "name": "PROMETHEUS_ENDPOINT",
                            "value": "/app-2/metrics",
                        },
                        {
                            "name": "APP_BASE_PATH",
                            "value": "/app-2",
                        },
                        {"name": "PROMETHEUS_TARGET", "value": "true"},
                    ],
                    "mountPoints": [],
                    "volumesFrom": [],
                    "secrets": [],
                    "logConfiguration": {
                        "logDriver": "awslogs",
                        "options": {
                            "awslogs-datetime-format": "%Y%m%d-%H%M%S",
                            "awslogs-group": "loggroup",
                            "awslogs-region": "eu-central-1",
                            "awslogs-stream-prefix": "ecs",
                        },
                    },
                }
            ],
            "family": "datasource-test-2",
            "executionRoleArn": "arn:aws:iam::123456789123:role/cluster-name_ecs_task_execution_role",
            "revision": 2,
            "volumes": [],
            "status": "ACTIVE",
            "requiresAttributes": [
                {"name": "com.amazonaws.ecs.capability.logging-driver.awslogs"},
                {"name": "ecs.capability.execution-role-awslogs"},
                {"name": "com.amazonaws.ecs.capability.ecr-auth"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.19"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.21"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.30"},
                {"name": "ecs.capability.execution-role-ecr-pull"},
                {"name": "ecs.capability.secrets.ssm.environment-variables"},
            ],
            "placementConstraints": [],
            "compatibilities": ["EC2"],
        },
        "ResponseMetadata": {
            "RequestId": "01234567-8901-2345-6789-012345678901",
            "HTTPStatusCode": 200,
            "HTTPHeaders": {
                "x-amzn-requestid": "01234567-8901-2345-6789-012345678901",
                "content-type": "application/x-amz-json-1.1",
                "content-length": "1684",
                "date": "Tue, 20 Jul 2020 20:00:00 GMT",
            },
            "RetryAttempts": 0,
        },
    },
    {
        "taskDefinition": {
            "taskDefinitionArn": "arn:aws:ecs:eu-central-1:123456789123:task-definition/webapp-test-3:2",
            "containerDefinitions": [
                {
                    "name": "datasource-test-3",
                    "image": "x",
                    "cpu": 8,
                    "memory": 200,
                    "memoryReservation": 50,
                    "portMappings": [
                        {"containerPort": 80, "hostPort": 0, "protocol": "tcp"}
                    ],
                    "dockerLabels": {"promed.custom_labels": "foo=bar, high=fi"},
                    "essential": True,
                    "environment": [
                        {
                            "name": "PROMETHEUS_ENDPOINT",
                            "value": "/app-3/metrics",
                        },
                        {
                            "name": "APP_BASE_PATH",
                            "value": "/app-3",
                        },
                        {"name": "PROMETHEUS_TARGET", "value": "true"},
                    ],
                    "mountPoints": [],
                    "volumesFrom": [],
                    "secrets": [],
                    "logConfiguration": {
                        "logDriver": "awslogs",
                        "options": {
                            "awslogs-datetime-format": "%Y%m%d-%H%M%S",
                            "awslogs-group": "loggroup",
                            "awslogs-region": "eu-central-1",
                            "awslogs-stream-prefix": "ecs",
                        },
                    },
                }
            ],
            "family": "datasource-test-3",
            "executionRoleArn": "arn:aws:iam::123456789123:role/cluster-name_ecs_task_execution_role",
            "revision": 2,
            "volumes": [],
            "status": "ACTIVE",
            "requiresAttributes": [
                {"name": "com.amazonaws.ecs.capability.logging-driver.awslogs"},
                {"name": "ecs.capability.execution-role-awslogs"},
                {"name": "com.amazonaws.ecs.capability.ecr-auth"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.19"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.21"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.30"},
                {"name": "ecs.capability.execution-role-ecr-pull"},
                {"name": "ecs.capability.secrets.ssm.environment-variables"},
            ],
            "placementConstraints": [],
            "compatibilities": ["EC2"],
        },
        "ResponseMetadata": {
            "RequestId": "01234567-8901-2345-6789-012345678901",
            "HTTPStatusCode": 200,
            "HTTPHeaders": {
                "x-amzn-requestid": "01234567-8901-2345-6789-012345678901",
                "content-type": "application/x-amz-json-1.1",
                "content-length": "1684",
                "date": "Tue, 20 Jul 2020 20:00:00 GMT",
            },
            "RetryAttempts": 0,
        },
    },
    {
        "taskDefinition": {
            "taskDefinitionArn": "arn:aws:ecs:eu-central-1:123456789123:task-definition/webapp-test-4:1",
            "containerDefinitions": [
                {
                    "name": "datasource-test-4",
                    "image": "x",
                    "cpu": 8,
                    "memory": 200,
                    "memoryReservation": 50,
                    "portMappings": [
                        {"containerPort": 80, "hostPort": 0, "protocol": "tcp"}
                    ],
                    "essential": True,
                    "environment": [
                        {
                            "name": "PROMETHEUS_ENDPOINT",
                            "value": "/app-4/metrics",
                        },
                        {"name": "PROMETHEUS_TARGET", "value": "true"},
                    ],
                    "mountPoints": [],
                    "volumesFrom": [],
                    "secrets": [],
                    "logConfiguration": {
                        "logDriver": "awslogs",
                        "options": {
                            "awslogs-datetime-format": "%Y%m%d-%H%M%S",
                            "awslogs-group": "loggroup",
                            "awslogs-region": "eu-central-1",
                            "awslogs-stream-prefix": "ecs",
                        },
                    },
                }
            ],
            "family": "datasource-test-4",
            "executionRoleArn": "arn:aws:iam::123456789123:role/cluster-name_ecs_task_execution_role",
            "revision": 1,
            "volumes": [],
            "status": "ACTIVE",
            "requiresAttributes": [
                {"name": "com.amazonaws.ecs.capability.logging-driver.awslogs"},
                {"name": "ecs.capability.execution-role-awslogs"},
                {"name": "com.amazonaws.ecs.capability.ecr-auth"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.19"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.21"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.30"},
                {"name": "ecs.capability.execution-role-ecr-pull"},
                {"name": "ecs.capability.secrets.ssm.environment-variables"},
            ],
            "placementConstraints": [],
            "compatibilities": ["EC2"],
        },
        "ResponseMetadata": {
            "RequestId": "01234567-8901-2345-6789-012345678901",
            "HTTPStatusCode": 200,
            "HTTPHeaders": {
                "x-amzn-requestid": "01234567-8901-2345-6789-012345678901",
                "content-type": "application/x-amz-json-1.1",
                "content-length": "1619",
                "date": "Tue, 20 Jul 2020 20:00:00 GMT",
            },
            "RetryAttempts": 0,
        },
    },
    {
        "taskDefinition": {
            "taskDefinitionArn": "arn:aws:ecs:eu-central-1:123456789123:task-definition/daemon-service:1",
            "containerDefinitions": [
                {
                    "name": "cloudwatch-agent",
                    "image": "x",
                    "cpu": 0,
                    "portMappings": [],
                    "essential": True,
                    "environment": [{"name": "USE_DEFAULT_CONFIG", "value": "True"}],
                    "mountPoints": [
                        {
                            "sourceVolume": "proc",
                            "containerPath": "/rootfs/proc",
                            "readOnly": True,
                        },
                        {
                            "sourceVolume": "dev",
                            "containerPath": "/rootfs/dev",
                            "readOnly": True,
                        },
                        {
                            "sourceVolume": "al2_cgroup",
                            "containerPath": "/sys/fs/cgroup",
                            "readOnly": True,
                        },
                        {
                            "sourceVolume": "al1_cgroup",
                            "containerPath": "/cgroup",
                            "readOnly": True,
                        },
                        {
                            "sourceVolume": "al2_cgroup",
                            "containerPath": "/rootfs/sys/fs/cgroup",
                            "readOnly": True,
                        },
                        {
                            "sourceVolume": "al1_cgroup",
                            "containerPath": "/rootfs/cgroup",
                            "readOnly": True,
                        },
                    ],
                    "volumesFrom": [],
                    "logConfiguration": {
                        "logDriver": "awslogs",
                        "options": {
                            "awslogs-create-group": "True",
                            "awslogs-group": "loggroup",
                            "awslogs-region": "eu-central-1",
                            "awslogs-stream-prefix": "ecs",
                        },
                    },
                }
            ],
            "family": "ecs-cwagent-daemon-service",
            "taskRoleArn": "arn:aws:iam::123456789123:role/cluster-name_ecs_task_role_cloudwatch_agent",
            "executionRoleArn": "arn:aws:iam::123456789123:role/cluster-name_ecs_task_execution_role",
            "networkMode": "bridge",
            "revision": 1,
            "volumes": [
                {"name": "proc", "host": {"sourcePath": "/proc"}},
                {"name": "dev", "host": {"sourcePath": "/dev"}},
                {"name": "al1_cgroup", "host": {"sourcePath": "/cgroup"}},
                {"name": "al2_cgroup", "host": {"sourcePath": "/sys/fs/cgroup"}},
            ],
            "status": "ACTIVE",
            "requiresAttributes": [
                {"name": "com.amazonaws.ecs.capability.logging-driver.awslogs"},
                {"name": "ecs.capability.execution-role-awslogs"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.19"},
                {"name": "com.amazonaws.ecs.capability.task-iam-role"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.29"},
            ],
            "placementConstraints": [],
            "compatibilities": ["EC2"],
            "requiresCompatibilities": ["EC2"],
            "cpu": "128",
            "memory": "64",
        },
        "ResponseMetadata": {
            "RequestId": "01234567-8901-2345-6789-012345678901",
            "HTTPStatusCode": 200,
            "HTTPHeaders": {
                "x-amzn-requestid": "01234567-8901-2345-6789-012345678901",
                "content-type": "application/x-amz-json-1.1",
                "content-length": "1921",
                "date": "Tue, 20 Jul 2020 20:00:00 GMT",
            },
            "RetryAttempts": 0,
        },
    },
    {
        "taskDefinition": {
            "taskDefinitionArn": "arn:aws:ecs:eu-central-1:123456789123:task-definition/hello:9",
            "containerDefinitions": [
                {
                    "name": "gitlabci-dataloader",
                    "image": "x",
                    "cpu": 2,
                    "memoryReservation": 100,
                    "portMappings": [
                        {"containerPort": 80, "hostPort": 0, "protocol": "tcp"}
                    ],
                    "essential": True,
                    "environment": [{"name": "RUNNER_TAG", "value": "dataloader_dev"}],
                    "mountPoints": [],
                    "volumesFrom": [],
                    "secrets": [],
                    "logConfiguration": {
                        "logDriver": "awslogs",
                        "options": {
                            "awslogs-group": "loggroup",
                            "awslogs-region": "eu-central-1",
                            "awslogs-stream-prefix": "ecs",
                        },
                    },
                }
            ],
            "family": "gitlabci-dataloader",
            "taskRoleArn": "arn:aws:iam::123456789123:role/cluster-name_ecs_task_role_dataloader",
            "executionRoleArn": "arn:aws:iam::123456789123:role/cluster-name_ecs_task_execution_role",
            "revision": 9,
            "volumes": [],
            "status": "ACTIVE",
            "requiresAttributes": [
                {"name": "com.amazonaws.ecs.capability.logging-driver.awslogs"},
                {"name": "ecs.capability.execution-role-awslogs"},
                {"name": "com.amazonaws.ecs.capability.ecr-auth"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.19"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.21"},
                {"name": "com.amazonaws.ecs.capability.task-iam-role"},
                {"name": "ecs.capability.execution-role-ecr-pull"},
                {"name": "ecs.capability.secrets.ssm.environment-variables"},
            ],
            "placementConstraints": [],
            "compatibilities": ["EC2"],
        },
        "ResponseMetadata": {
            "RequestId": "01234567-8901-2345-6789-012345678901",
            "HTTPStatusCode": 200,
            "HTTPHeaders": {
                "x-amzn-requestid": "01234567-8901-2345-6789-012345678901",
                "content-type": "application/x-amz-json-1.1",
                "content-length": "1588",
                "date": "Tue, 20 Jul 2020 20:00:00 GMT",
            },
            "RetryAttempts": 0,
        },
    },
    {
        "taskDefinition": {
            "taskDefinitionArn": "arn:aws:ecs:eu-central-1:123456789123:task-definition/dockertest:25",
            "containerDefinitions": [
                {
                    "name": "nginx",
                    "image": "x",
                    "cpu": 32,
                    "memoryReservation": 32,
                    "links": ["grafana", "prometheus", "loki"],
                    "portMappings": [
                        {"containerPort": 80, "hostPort": 0, "protocol": "tcp"}
                    ],
                    "essential": True,
                    "entryPoint": [],
                    "environment": [],
                    "mountPoints": [],
                    "volumesFrom": [],
                    "dependsOn": [
                        {"containerName": "grafana", "condition": "START"},
                        {"containerName": "prometheus", "condition": "START"},
                    ],
                    "user": "0",
                    "logConfiguration": {
                        "logDriver": "awslogs",
                        "options": {
                            "awslogs-group": "loggroup",
                            "awslogs-region": "eu-central-1",
                            "awslogs-stream-prefix": "promstack",
                        },
                    },
                },
                {
                    "name": "grafana",
                    "image": "x",
                    "cpu": 64,
                    "memoryReservation": 128,
                    "links": ["loki"],
                    "portMappings": [
                        {"containerPort": 3000, "hostPort": 0, "protocol": "tcp"}
                    ],
                    "essential": True,
                    "entryPoint": [],
                    "environment": [],
                    "mountPoints": [
                        {"sourceVolume": "grafana", "containerPath": "/var/lib/grafana"}
                    ],
                    "volumesFrom": [],
                    "user": "0",
                    "logConfiguration": {
                        "logDriver": "awslogs",
                        "options": {
                            "awslogs-group": "loggroup",
                            "awslogs-region": "eu-central-1",
                            "awslogs-stream-prefix": "promstack",
                        },
                    },
                },
                {
                    "name": "prometheus",
                    "image": "x",
                    "cpu": 64,
                    "memoryReservation": 256,
                    "links": ["loki"],
                    "portMappings": [
                        {"containerPort": 9090, "hostPort": 0, "protocol": "tcp"}
                    ],
                    "essential": True,
                    "entryPoint": [],
                    "environment": [],
                    "mountPoints": [
                        {"sourceVolume": "discovery", "containerPath": "/discovery"}
                    ],
                    "volumesFrom": [],
                    "user": "0",
                    "logConfiguration": {
                        "logDriver": "awslogs",
                        "options": {
                            "awslogs-group": "loggroup",
                            "awslogs-region": "eu-central-1",
                            "awslogs-stream-prefix": "promstack",
                        },
                    },
                },
                {
                    "name": "prometheus_discovery",
                    "image": "x",
                    "cpu": 8,
                    "memoryReservation": 32,
                    "portMappings": [],
                    "essential": True,
                    "command": [
                        "--interval",
                        "15",
                        "--directory",
                        "/output",
                        "--region",
                        "eu-central-1",
                    ],
                    "environment": [],
                    "mountPoints": [
                        {"sourceVolume": "discovery", "containerPath": "/output"}
                    ],
                    "volumesFrom": [],
                },
                {
                    "name": "loki",
                    "image": "x",
                    "cpu": 64,
                    "memoryReservation": 128,
                    "portMappings": [
                        {"containerPort": 3100, "hostPort": 0, "protocol": "tcp"}
                    ],
                    "essential": True,
                    "environment": [],
                    "mountPoints": [],
                    "volumesFrom": [],
                    "logConfiguration": {
                        "logDriver": "awslogs",
                        "options": {
                            "awslogs-group": "loggroup",
                            "awslogs-region": "eu-central-1",
                            "awslogs-stream-prefix": "promstack",
                        },
                    },
                },
            ],
            "family": "promstack",
            "taskRoleArn": "arn:aws:iam::123456789123:role/promstack-discovery",
            "executionRoleArn": "arn:aws:iam::123456789123:role/cluster-name_ecs_task_execution_role",
            "revision": 25,
            "volumes": [],
            "status": "ACTIVE",
            "requiresAttributes": [
                {"name": "com.amazonaws.ecs.capability.logging-driver.awslogs"},
                {"name": "ecs.capability.execution-role-awslogs"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.19"},
                {"name": "ecs.capability.efs"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.17"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.21"},
                {"name": "com.amazonaws.ecs.capability.task-iam-role"},
                {"name": "ecs.capability.container-ordering"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.25"},
            ],
            "placementConstraints": [],
            "compatibilities": ["EC2"],
        },
        "ResponseMetadata": {
            "RequestId": "01234567-8901-2345-6789-012345678901",
            "HTTPStatusCode": 200,
            "HTTPHeaders": {
                "x-amzn-requestid": "01234567-8901-2345-6789-012345678901",
                "content-type": "application/x-amz-json-1.1",
                "content-length": "11380",
                "date": "Tue, 20 Jul 2020 20:00:00 GMT",
            },
            "RetryAttempts": 0,
        },
    },
    {
        "taskDefinition": {
            "taskDefinitionArn": "arn:aws:ecs:eu-central-1:123456789123:task-definition/what:13",
            "containerDefinitions": [
                {
                    "name": "ssh-forward",
                    "image": "x",
                    "cpu": 8,
                    "memoryReservation": 50,
                    "portMappings": [],
                    "essential": True,
                    "environment": [
                        {
                            "name": "SSH_PARM",
                            "value": "-v -oStrictHostKeyChecking=accept-new -oExitOnForwardFailure=yes -oServerAliveInterval=60 -R 5434:main.cr5lxi0fhhms.eu-central-1.rds.amazonaws.com:5432 -N",
                        },
                        {"name": "SSH_TARGET", "value": "ubuntu@54.93.114.186"},
                        {"name": "SSH_TARGET_CMD", "value": ""},
                    ],
                    "mountPoints": [],
                    "volumesFrom": [],
                    "secrets": [],
                    "logConfiguration": {
                        "logDriver": "awslogs",
                        "options": {
                            "awslogs-group": "loggroup",
                            "awslogs-region": "eu-central-1",
                            "awslogs-stream-prefix": "ecs",
                        },
                    },
                }
            ],
            "family": "ssh-forward",
            "executionRoleArn": "arn:aws:iam::123456789123:role/cluster-name_ecs_task_execution_role",
            "revision": 13,
            "volumes": [],
            "status": "ACTIVE",
            "requiresAttributes": [
                {"name": "com.amazonaws.ecs.capability.logging-driver.awslogs"},
                {"name": "ecs.capability.execution-role-awslogs"},
                {"name": "com.amazonaws.ecs.capability.ecr-auth"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.19"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.21"},
                {"name": "ecs.capability.execution-role-ecr-pull"},
                {"name": "ecs.capability.secrets.ssm.environment-variables"},
            ],
            "placementConstraints": [],
            "compatibilities": ["EC2"],
        },
        "ResponseMetadata": {
            "RequestId": "01234567-8901-2345-6789-012345678901",
            "HTTPStatusCode": 200,
            "HTTPHeaders": {
                "x-amzn-requestid": "01234567-8901-2345-6789-012345678901",
                "content-type": "application/x-amz-json-1.1",
                "content-length": "1546",
                "date": "Tue, 20 Jul 2020 20:00:00 GMT",
            },
            "RetryAttempts": 0,
        },
    },
    {
        "taskDefinition": {
            "taskDefinitionArn": "arn:aws:ecs:eu-central-1:123456789123:task-definition/eoifjioejffew:41",
            "containerDefinitions": [
                {
                    "name": "testapp",
                    "image": "x",
                    "cpu": 8,
                    "memoryReservation": 500,
                    "portMappings": [
                        {"containerPort": 80, "hostPort": 0, "protocol": "tcp"}
                    ],
                    "essential": True,
                    "environment": [{"name": "PORT", "value": "80"}],
                    "mountPoints": [],
                    "volumesFrom": [],
                    "logConfiguration": {
                        "logDriver": "awslogs",
                        "options": {
                            "awslogs-group": "loggroup",
                            "awslogs-region": "eu-central-1",
                            "awslogs-stream-prefix": "ecs",
                        },
                    },
                }
            ],
            "family": "testapp",
            "executionRoleArn": "arn:aws:iam::123456789123:role/cluster-name_ecs_task_execution_role",
            "revision": 41,
            "volumes": [],
            "status": "ACTIVE",
            "requiresAttributes": [
                {"name": "com.amazonaws.ecs.capability.logging-driver.awslogs"},
                {"name": "ecs.capability.execution-role-awslogs"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.19"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.21"},
            ],
            "placementConstraints": [],
            "compatibilities": ["EC2"],
        },
        "ResponseMetadata": {
            "RequestId": "01234567-8901-2345-6789-012345678901",
            "HTTPStatusCode": 200,
            "HTTPHeaders": {
                "x-amzn-requestid": "01234567-8901-2345-6789-012345678901",
                "content-type": "application/x-amz-json-1.1",
                "content-length": "998",
                "date": "Tue, 20 Jul 2020 20:00:00 GMT",
            },
            "RetryAttempts": 0,
        },
    },
]

describe_container_instances_parameters = {
    "cluster": list_clusters_response["clusterArns"][0],
    "containerInstances": list_container_instances_response["containerInstanceArns"],
}
describe_container_instances_response = {
    "containerInstances": [
        {
            "containerInstanceArn": "arn:aws:ecs:eu-central-1:123456789123:container-instance/01234567-8901-8325-6789-012345678901",
            "ec2InstanceId": "i-08c7123ef038a7cc4",
            "version": 13,
            "versionInfo": {
                "agentVersion": "1.40.0",
                "agentHash": "17e8d834",
                "dockerVersion": "DockerVersion: 19.03.6-ce",
            },
            "remainingResources": [],
            "registeredResources": [],
            "status": "ACTIVE",
            "agentConnected": True,
            "runningTasksCount": 7,
            "pendingTasksCount": 0,
            "attributes": [
                {"name": "ecs.capability.secrets.asm.environment-variables"},
                {
                    "name": "ecs.capability.branch-cni-plugin-version",
                    "value": "ee068761-",
                },
                {"name": "ecs.ami-id", "value": "ami-08c4be469fbdca0fa"},
                {"name": "ecs.capability.secrets.asm.bootstrap.log-driver"},
                {"name": "ecs.capability.task-eia.optimized-cpu"},
                {"name": "com.amazonaws.ecs.capability.logging-driver.none"},
                {"name": "ecs.capability.ecr-endpoint"},
                {"name": "ecs.capability.docker-plugin.local"},
                {"name": "ecs.capability.task-cpu-mem-limit"},
                {"name": "ecs.capability.secrets.ssm.bootstrap.log-driver"},
                {"name": "ecs.capability.efsAuth"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.30"},
                {"name": "ecs.capability.full-sync"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.31"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.32"},
                {"name": "ecs.capability.firelens.options.config.file"},
                {"name": "ecs.availability-zone", "value": "eu-central-1a"},
                {"name": "ecs.capability.aws-appmesh"},
                {"name": "com.amazonaws.ecs.capability.logging-driver.awslogs"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.24"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.25"},
                {"name": "ecs.capability.task-eni-trunking"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.26"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.27"},
                {"name": "com.amazonaws.ecs.capability.privileged-container"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.28"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.29"},
                {"name": "ecs.cpu-architecture", "value": "x86_64"},
                {"name": "ecs.capability.firelens.fluentbit"},
                {"name": "com.amazonaws.ecs.capability.ecr-auth"},
                {"name": "ecs.os-type", "value": "linux"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.20"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.21"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.22"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.23"},
                {"name": "ecs.capability.task-eia"},
                {"name": "ecs.capability.private-registry-authentication.secretsmanager"},
                {"name": "com.amazonaws.ecs.capability.logging-driver.syslog"},
                {"name": "com.amazonaws.ecs.capability.logging-driver.awsfirelens"},
                {"name": "ecs.capability.firelens.options.config.s3"},
                {"name": "com.amazonaws.ecs.capability.logging-driver.json-file"},
                {"name": "ecs.vpc-id", "value": "vpc-0e98052f61664466c"},
                {"name": "ecs.capability.execution-role-awslogs"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.17"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.18"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.19"},
                {"name": "ecs.capability.docker-plugin.amazon-ecs-volume-plugin"},
                {"name": "ecs.capability.task-eni"},
                {"name": "ecs.capability.firelens.fluentd"},
                {"name": "ecs.capability.efs"},
                {"name": "ecs.capability.execution-role-ecr-pull"},
                {"name": "ecs.capability.container-health-check"},
                {"name": "ecs.subnet-id", "value": "subnet-017a912d7d7b5fecc"},
                {"name": "ecs.instance-type", "value": "t3a.medium"},
                {"name": "com.amazonaws.ecs.capability.task-iam-role-network-host"},
                {"name": "ecs.capability.container-ordering"},
                {
                    "name": "ecs.capability.cni-plugin-version",
                    "value": "9066095f-2019.10.0",
                },
                {"name": "ecs.capability.env-files.s3"},
                {"name": "ecs.capability.secrets.ssm.environment-variables"},
                {"name": "ecs.capability.pid-ipc-namespace-sharing"},
                {"name": "com.amazonaws.ecs.capability.task-iam-role"},
            ],
            "registeredAt": datetime.datetime(
                2020, 7, 29, 8, 57, 39, 384000, tzinfo=tzlocal()
            ),
            "attachments": [],
            "tags": [],
        },
        {
            "containerInstanceArn": "arn:aws:ecs:eu-central-1:123456789123:container-instance/e0e32bca-2890-4988-9c04-ebdef8085892",
            "ec2InstanceId": "i-0b967c2479dd4f5af",
            "version": 14,
            "versionInfo": {
                "agentVersion": "1.40.0",
                "agentHash": "17e8d834",
                "dockerVersion": "DockerVersion: 19.03.6-ce",
            },
            "remainingResources": [
                {
                    "name": "CPU",
                    "type": "INTEGER",
                    "doubleValue": 0.0,
                    "longValue": 0,
                    "integerValue": 1638,
                },
                {
                    "name": "MEMORY",
                    "type": "INTEGER",
                    "doubleValue": 0.0,
                    "longValue": 0,
                    "integerValue": 1956,
                },
                {
                    "name": "PORTS",
                    "type": "STRINGSET",
                    "doubleValue": 0.0,
                    "longValue": 0,
                    "integerValue": 0,
                    "stringSetValue": ["22", "2376", "2375", "51678", "51679"],
                },
                {
                    "name": "PORTS_UDP",
                    "type": "STRINGSET",
                    "doubleValue": 0.0,
                    "longValue": 0,
                    "integerValue": 0,
                    "stringSetValue": [],
                },
            ],
            "registeredResources": [
                {
                    "name": "CPU",
                    "type": "INTEGER",
                    "doubleValue": 0.0,
                    "longValue": 0,
                    "integerValue": 2048,
                },
                {
                    "name": "MEMORY",
                    "type": "INTEGER",
                    "doubleValue": 0.0,
                    "longValue": 0,
                    "integerValue": 3896,
                },
                {
                    "name": "PORTS",
                    "type": "STRINGSET",
                    "doubleValue": 0.0,
                    "longValue": 0,
                    "integerValue": 0,
                    "stringSetValue": ["22", "2376", "2375", "51678", "51679"],
                },
                {
                    "name": "PORTS_UDP",
                    "type": "STRINGSET",
                    "doubleValue": 0.0,
                    "longValue": 0,
                    "integerValue": 0,
                    "stringSetValue": [],
                },
            ],
            "status": "ACTIVE",
            "agentConnected": True,
            "runningTasksCount": 9,
            "pendingTasksCount": 0,
            "attributes": [
                {"name": "ecs.capability.secrets.asm.environment-variables"},
                {
                    "name": "ecs.capability.branch-cni-plugin-version",
                    "value": "ee068761-",
                },
                {"name": "ecs.ami-id", "value": "ami-08c4be469fbdca0fa"},
                {"name": "ecs.capability.secrets.asm.bootstrap.log-driver"},
                {"name": "ecs.capability.task-eia.optimized-cpu"},
                {"name": "com.amazonaws.ecs.capability.logging-driver.none"},
                {"name": "ecs.capability.ecr-endpoint"},
                {"name": "ecs.capability.docker-plugin.local"},
                {"name": "ecs.capability.task-cpu-mem-limit"},
                {"name": "ecs.capability.secrets.ssm.bootstrap.log-driver"},
                {"name": "ecs.capability.efsAuth"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.30"},
                {"name": "ecs.capability.full-sync"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.31"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.32"},
                {"name": "ecs.capability.firelens.options.config.file"},
                {"name": "ecs.availability-zone", "value": "eu-central-1b"},
                {"name": "ecs.capability.aws-appmesh"},
                {"name": "com.amazonaws.ecs.capability.logging-driver.awslogs"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.24"},
                {"name": "ecs.capability.task-eni-trunking"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.25"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.26"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.27"},
                {"name": "com.amazonaws.ecs.capability.privileged-container"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.28"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.29"},
                {"name": "ecs.cpu-architecture", "value": "x86_64"},
                {"name": "com.amazonaws.ecs.capability.ecr-auth"},
                {"name": "ecs.capability.firelens.fluentbit"},
                {"name": "ecs.os-type", "value": "linux"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.20"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.21"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.22"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.23"},
                {"name": "ecs.capability.task-eia"},
                {"name": "ecs.capability.private-registry-authentication.secretsmanager"},
                {"name": "com.amazonaws.ecs.capability.logging-driver.syslog"},
                {"name": "com.amazonaws.ecs.capability.logging-driver.awsfirelens"},
                {"name": "ecs.capability.firelens.options.config.s3"},
                {"name": "com.amazonaws.ecs.capability.logging-driver.json-file"},
                {"name": "ecs.vpc-id", "value": "vpc-0e98052f61664466c"},
                {"name": "ecs.capability.execution-role-awslogs"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.17"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.18"},
                {"name": "com.amazonaws.ecs.capability.docker-remote-api.1.19"},
                {"name": "ecs.capability.docker-plugin.amazon-ecs-volume-plugin"},
                {"name": "ecs.capability.task-eni"},
                {"name": "ecs.capability.firelens.fluentd"},
                {"name": "ecs.capability.efs"},
                {"name": "ecs.capability.execution-role-ecr-pull"},
                {"name": "ecs.capability.container-health-check"},
                {"name": "ecs.subnet-id", "value": "subnet-032157d2370144a5c"},
                {"name": "ecs.instance-type", "value": "t3a.medium"},
                {"name": "com.amazonaws.ecs.capability.task-iam-role-network-host"},
                {"name": "ecs.capability.container-ordering"},
                {
                    "name": "ecs.capability.cni-plugin-version",
                    "value": "9066095f-2019.10.0",
                },
                {"name": "ecs.capability.env-files.s3"},
                {"name": "ecs.capability.secrets.ssm.environment-variables"},
                {"name": "ecs.capability.pid-ipc-namespace-sharing"},
                {"name": "com.amazonaws.ecs.capability.task-iam-role"},
            ],
            "registeredAt": datetime.datetime(
                2020, 7, 29, 8, 57, 40, 648000, tzinfo=tzlocal()
            ),
            "attachments": [],
            "tags": [],
        },
    ],
    "failures": [],
    "ResponseMetadata": {
        "RequestId": "01234567-8901-2345-6789-012345678901",
        "HTTPStatusCode": 200,
        "HTTPHeaders": {
            "x-amzn-requestid": "01234567-8901-2345-6789-012345678901",
            "content-type": "application/x-amz-json-1.1",
            "content-length": "9386",
            "date": "Tue, 20 Jul 2020 20:00:00 GMT",
        },
        "RetryAttempts": 0,
    },
}

describe_instances_parameters = {"InstanceIds": []}
for container_instance in describe_container_instances_response["containerInstances"]:
    describe_instances_parameters["InstanceIds"].append(
        container_instance["ec2InstanceId"]
    )
describe_instances_response = {
    "Reservations": [
        {
            "Groups": [],
            "Instances": [
                {
                    "AmiLaunchIndex": 0,
                    "ImageId": "ami-08c4be469fbdca0fa",
                    "InstanceId": "i-08c7123ef038a7cc4",
                    "InstanceType": "t3a.medium",
                    "KeyName": "data-dev",
                    "LaunchTime": datetime.datetime(
                        2020, 7, 29, 6, 56, 33, tzinfo=tzutc()
                    ),
                    "Monitoring": {"State": "enabled"},
                    "Placement": {
                        "AvailabilityZone": "eu-central-1a",
                        "GroupName": "",
                        "Tenancy": "default",
                    },
                    "PrivateDnsName": "ip-10-0-1-73.eu-central-1.compute.internal",
                    "PrivateIpAddress": "10.0.1.73",
                    "ProductCodes": [],
                    "PublicDnsName": "",
                    "State": {"Code": 16, "Name": "running"},
                    "StateTransitionReason": "",
                    "SubnetId": "subnet-017a912d7d7b5fecc",
                    "VpcId": "vpc-0e98052f61664466c",
                    "Architecture": "x86_64",
                    "BlockDeviceMappings": [
                        {
                            "DeviceName": "/dev/xvda",
                            "Ebs": {
                                "AttachTime": datetime.datetime(
                                    2020, 7, 29, 6, 56, 34, tzinfo=tzutc()
                                ),
                                "DeleteOnTermination": True,
                                "Status": "attached",
                                "VolumeId": "vol-09595d7c24c463548",
                            },
                        },
                        {
                            "DeviceName": "/dev/xvds",
                            "Ebs": {
                                "AttachTime": datetime.datetime(
                                    2020, 7, 29, 6, 56, 34, tzinfo=tzutc()
                                ),
                                "DeleteOnTermination": True,
                                "Status": "attached",
                                "VolumeId": "vol-097b3fd039a2062b6",
                            },
                        },
                    ],
                    "ClientToken": "7c55ce65-6ee2-2e87-b927-2c4d0d37b913",
                    "EbsOptimized": False,
                    "EnaSupport": True,
                    "Hypervisor": "xen",
                    "IamInstanceProfile": {
                        "Arn": "arn:aws:iam::123456789123:instance-profile/cluster-name",
                        "Id": "AIPA3ZZY5WMSYDKBUKM3U",
                    },
                    "NetworkInterfaces": [
                        {
                            "Attachment": {
                                "AttachTime": datetime.datetime(
                                    2020, 7, 29, 6, 56, 33, tzinfo=tzutc()
                                ),
                                "AttachmentId": "eni-attach-06bbff614335d2a60",
                                "DeleteOnTermination": True,
                                "DeviceIndex": 0,
                                "Status": "attached",
                            },
                            "Description": "",
                            "Groups": [
                                {
                                    "GroupName": "terraform-20190906062328155300000001",
                                    "GroupId": "sg-0b6a05f14d26f4be8",
                                }
                            ],
                            "Ipv6Addresses": [],
                            "MacAddress": "02:3b:d2:1d:af:9e",
                            "NetworkInterfaceId": "eni-09de93eb056ea7c7f",
                            "OwnerId": "123456789123",
                            "PrivateDnsName": "ip-10-0-1-73.eu-central-1.compute.internal",
                            "PrivateIpAddress": "10.0.1.73",
                            "PrivateIpAddresses": [
                                {
                                    "Primary": True,
                                    "PrivateDnsName": "ip-10-0-1-73.eu-central-1.compute.internal",
                                    "PrivateIpAddress": "10.0.1.73",
                                }
                            ],
                            "SourceDestCheck": True,
                            "Status": "in-use",
                            "SubnetId": "subnet-017a912d7d7b5fecc",
                            "VpcId": "vpc-0e98052f61664466c",
                            "InterfaceType": "interface",
                        }
                    ],
                    "RootDeviceName": "/dev/xvda",
                    "RootDeviceType": "ebs",
                    "SecurityGroups": [],
                    "SourceDestCheck": True,
                    "Tags": [],
                    "VirtualizationType": "hvm",
                    "CpuOptions": {"CoreCount": 1, "ThreadsPerCore": 2},
                    "CapacityReservationSpecification": {
                        "CapacityReservationPreference": "open"
                    },
                    "HibernationOptions": {"Configured": False},
                    "MetadataOptions": {
                        "State": "applied",
                        "HttpTokens": "optional",
                        "HttpPutResponseHopLimit": 1,
                        "HttpEndpoint": "enabled",
                    },
                }
            ],
            "OwnerId": "123456789123",
            "RequesterId": "053592188284",
            "ReservationId": "r-0d8935cfaa871752b",
        },
        {
            "Groups": [],
            "Instances": [
                {
                    "AmiLaunchIndex": 0,
                    "ImageId": "ami-08c4be469fbdca0fa",
                    "InstanceId": "i-0b967c2479dd4f5af",
                    "InstanceType": "t3a.medium",
                    "KeyName": "data-dev",
                    "LaunchTime": datetime.datetime(
                        2020, 7, 29, 6, 56, 33, tzinfo=tzutc()
                    ),
                    "Monitoring": {"State": "enabled"},
                    "Placement": {
                        "AvailabilityZone": "eu-central-1b",
                        "GroupName": "",
                        "Tenancy": "default",
                    },
                    "PrivateDnsName": "ip-10-0-2-85.eu-central-1.compute.internal",
                    "PrivateIpAddress": "10.0.2.85",
                    "ProductCodes": [],
                    "PublicDnsName": "",
                    "State": {"Code": 16, "Name": "running"},
                    "StateTransitionReason": "",
                    "SubnetId": "subnet-032157d2370144a5c",
                    "VpcId": "vpc-0e98052f61664466c",
                    "Architecture": "x86_64",
                    "BlockDeviceMappings": [
                        {
                            "DeviceName": "/dev/xvda",
                            "Ebs": {
                                "AttachTime": datetime.datetime(
                                    2020, 7, 29, 6, 56, 34, tzinfo=tzutc()
                                ),
                                "DeleteOnTermination": True,
                                "Status": "attached",
                                "VolumeId": "vol-041ec6e0ec30a0e4e",
                            },
                        },
                        {
                            "DeviceName": "/dev/xvds",
                            "Ebs": {
                                "AttachTime": datetime.datetime(
                                    2020, 7, 29, 6, 56, 34, tzinfo=tzutc()
                                ),
                                "DeleteOnTermination": True,
                                "Status": "attached",
                                "VolumeId": "vol-032638c297d2c0a2a",
                            },
                        },
                    ],
                    "ClientToken": "fa25ce65-6ee1-3aed-3818-8c76049b2de2",
                    "EbsOptimized": False,
                    "EnaSupport": True,
                    "Hypervisor": "xen",
                    "IamInstanceProfile": {
                        "Arn": "arn:aws:iam::123456789123:instance-profile/cluster-name",
                        "Id": "AIPA3ZZY5WMSYDKBUKM3U",
                    },
                    "NetworkInterfaces": [
                        {
                            "Attachment": {
                                "AttachTime": datetime.datetime(
                                    2020, 7, 29, 6, 56, 33, tzinfo=tzutc()
                                ),
                                "AttachmentId": "eni-attach-007bf25e91d0886d7",
                                "DeleteOnTermination": True,
                                "DeviceIndex": 0,
                                "Status": "attached",
                            },
                            "Description": "",
                            "Groups": [
                                {
                                    "GroupName": "terraform-20190906062328155300000001",
                                    "GroupId": "sg-0b6a05f14d26f4be8",
                                }
                            ],
                            "Ipv6Addresses": [],
                            "MacAddress": "06:cf:03:07:1e:cc",
                            "NetworkInterfaceId": "eni-009595c5146831515",
                            "OwnerId": "123456789123",
                            "PrivateDnsName": "ip-10-0-2-85.eu-central-1.compute.internal",
                            "PrivateIpAddress": "10.0.2.85",
                            "PrivateIpAddresses": [
                                {
                                    "Primary": True,
                                    "PrivateDnsName": "ip-10-0-2-85.eu-central-1.compute.internal",
                                    "PrivateIpAddress": "10.0.2.85",
                                }
                            ],
                            "SourceDestCheck": True,
                            "Status": "in-use",
                            "SubnetId": "subnet-032157d2370144a5c",
                            "VpcId": "vpc-0e98052f61664466c",
                            "InterfaceType": "interface",
                        }
                    ],
                    "RootDeviceName": "/dev/xvda",
                    "RootDeviceType": "ebs",
                    "SecurityGroups": [],
                    "SourceDestCheck": True,
                    "Tags": [],
                    "VirtualizationType": "hvm",
                    "CpuOptions": {"CoreCount": 1, "ThreadsPerCore": 2},
                    "CapacityReservationSpecification": {
                        "CapacityReservationPreference": "open"
                    },
                    "HibernationOptions": {"Configured": False},
                    "MetadataOptions": {
                        "State": "applied",
                        "HttpTokens": "optional",
                        "HttpPutResponseHopLimit": 1,
                        "HttpEndpoint": "enabled",
                    },
                }
            ],
            "OwnerId": "123456789123",
            "RequesterId": "053592188284",
            "ReservationId": "r-0a736f9e68e77c5f2",
        },
    ],
    "ResponseMetadata": {
        "RequestId": "01234567-8901-2345-6789-012345678901",
        "HTTPStatusCode": 200,
        "HTTPHeaders": {
            "x-amzn-requestid": "01234567-8901-2345-6789-012345678901",
            "content-type": "text/xml;charset=UTF-8",
            "transfer-encoding": "chunked",
            "vary": "accept-encoding",
            "date": "Tue, 20 Jul 2020 20:00:00 GMT",
            "server": "AmazonEC2",
        },
        "RetryAttempts": 0,
    },
}
