# predictive-maintenance-ml
Predictive Maintenance of Industrial Equipments using Machine Learning



# Running the Inference:

- Build the docker container
`sudo docker build -f Dockerfile --network=host -t predictive-ml .`

- Run the prediction service
`sudo docker run -p 8080:8080 --network=host --rm predictive-ml serve`


