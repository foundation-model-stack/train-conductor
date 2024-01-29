### Local Development

```
# Delete existing KinD locally
make delete-cluster

# Build and Deploy train-conductor
 make python-pb docker-image cluster load-docker-image deploy
```