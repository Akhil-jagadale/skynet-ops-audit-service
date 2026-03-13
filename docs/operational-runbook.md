# Operational Runbook

## Deploying the Service

cd terraform
terraform init
terraform apply

## Restarting the Container

sudo docker restart <container_id>

## Viewing Running Containers

sudo docker ps

## Viewing Logs

sudo docker logs <container_id>

## Troubleshooting

If the API is not reachable:

Check container status:
sudo docker ps

Check security group ports:
22 and 3000 must be open.

## Scaling Considerations

Future improvements may include:
- Load balancer
- Auto Scaling
- Container orchestration