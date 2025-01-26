# Neighborhood Traces

This repo contains the code used in the explainable.

The website can be found here:
[https://www.moritzdueck.com/neighborhood-traces/](https://www.moritzdueck.com/neighborhood-traces/)

## Abstract
While convolutional neural networks have been widely studied, their inner workings remain hard to interpret for humans. Tailored explainability methods for these models often focus on saliency. For language models and generative models in general, on the other hand, analysis approaches frequently aim at exploring the latent spaces of the model, which is less commonly done for image classification models. At the same time, inspecting neighboring samples within intermediate representations generated by the layers of CNNs has already proven useful to enhance model robustness. 
In this work, we derive tailored visualizations for a convolutional neural network classifier where we treat the multidimensional output range of each layer as an embedding space. Guided by the previous results on the significance of locality, we visualize effects on the local surrounding of samples in Euclidean space, focusing on the layer-wise transformation the network applies to the data. By comparing distances between samples across layers, we contribute a global and two local views showing the neighborhood development of samples throughout the network. Our visualizations help to gain insights into what the model has learned and the contribution of each layer to the classification. Our global visualization captures aspects of the interplay between data and model architecture, where future work might result in useful tools for analyzing, comparing or improving neural network architectures.


## Structure

### **`frontend/collaiborate-frontend`** 
Where all of the frontend code lives. This includes d3.js plots, the scrolly-telling code and the underlying vue project. 
 * **`src/App.vue`**: The main class of the vue application, and a useful entry-point to any edits to the overall web app.
 * **`src/components`**: All visualizations in the story are created using D3.js. This code is spread across the vue components and relies on the frameworks lifecycle, so cannot be run in isolation as of now.
   
### **`collaiborate`** 
Contains both, a flask backend serving inference results for neighborhood computations as well as jupyter notebooks containing experiments run during the discovery of the project.

 * **`api.py`**: The main class of the flask application calling inference functions for interactive explorations.
 * **`train_script.py`**: The pytorch script to train the CNN model used for the analysis
 * **`Evaluation.ipynb`**: A jupyter notebook running through the initial discovery steps and plots created during the project.

### **`docker-compose.yml`** 
If you want to run the service locally, this docker compose file should start the backend and frontend services locally. The backend container is NOT built from the local code, so for development you need to start frontend and backend locally.

## Deployment

Currently, the whole system runs in a self-contained docker container defined in the `Dockerfile` and is published to the Docker Hub at https://hub.docker.com/repository/docker/moritzdueck/collaiborate/general.
For the moment, the whole dataset is kept in memory to ease deployment yet leading to a high demand in computational resources.
