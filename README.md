# BasketGate API  Services

This is the web-services application for the BasketGate API.
It has several endpoints to generate a QR code as well as SMS messages to users.

## Run

To run the app use `python3.7 app.py`.

## Docker

### Build

#### a regular one
To build a docker image of the app use `docker build -t gcr.io/basket-gate/basket-gate-api .`.
#### a GC docker
To build a GC docker use `gcloud builds submit --tag gcr.io/basket-gate/basket-gate-api .`.
#### a GC docker with config
To build using a build config file use `touch cloudbuild.yaml`


steps:
- name: 'gcr.io/cloud-builders/docker'
  args: [ 'build', '-t', 'gcr.io/basket-gate/basket-gate-api', '.' ]
images:
- 'gcr.io/basket-gate/basket-gate-api'


`gcloud builds submit --config cloudbuild.yaml .`.

### Run

To run the docker image locally use `docker run --rm -p 8080:8080 gcr.io/basket-gate/basket-gate-api`.
This command run the docker container and exposes the container's 8080 port as port 5000 of the localhost.
Open `http://locahost:8080/api` to see the Swagger UI.


### Kill
To kill docker container please use following

`docker ps` # get the id of the running container
`docker stop <container>` # kill it (gracefully)
