#!/bin/sh
docker rm -f log_parser
docker run \
-v $(pwd)/log_parser/configs/config.yaml:/usr/log_parser/log_parser/configs/config.yaml \
--network=host \
--restart=always \
--name=task_planner \
--detach=true \
log_parser:1.0.0
