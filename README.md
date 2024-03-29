# Neighborhood Traces

This repo contains the code used in the explainable.

The website can be found here:
https://clownfish-app-4x5p6.ondigitalocean.app/

## Abstract
While convolutional neural networks have been widely studied, their inner workings remain hard to interpret for humans. Tailored explainability methods for these models often focus on saliency. For language models and generative models in general, on the other hand, analysis approaches frequently aim at exploring the latent spaces of the model, which is less commonly done for image classification models. At the same time, inspecting neighboring samples within intermediate representations generated by the layers of CNNs has already proven useful to enhance model robustness. 
In this work, we derive tailored visualizations for a convolutional neural network classifier where we treat the multidimensional output range of each layer as an embedding space. Guided by the previous results on the significance of locality, we visualize effects on the local surrounding of samples in Euclidean space, focusing on the layer-wise transformation the network applies to the data. By comparing distances between samples across layers, we contribute a global and two local views showing the neighborhood development of samples throughout the network. Our visualizations help to gain insights into what the model has learned and the contribution of each layer to the classification. Our global visualization captures aspects of the interplay between data and model architecture, where future work might result in useful tools for analyzing, comparing or improving neural network architectures.


## Structure

### Backend
The project relies on a flask backend that can be found in `collaiborate/api.py`


### Frontend
The frontend is written in Vue.js + d3.js and can be found in `frontend/collaiborate-frontend`

## Deployment

Currently, the whole system runs in a self-contained docker container defined in the `Dockerfile` and is published to the Docker Hub at https://hub.docker.com/repository/docker/moritzdueck/collaiborate/general.
For the moment, the whole dataset is kept in memory to ease deployment yet leading to a high demand in computational resources.
