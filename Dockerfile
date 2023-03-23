# frontend build stage
FROM node:lts-alpine as frontend
WORKDIR /app
COPY frontend/collaiborate-frontend/package*.json ./
RUN npm install
COPY frontend/collaiborate-frontend/. .
RUN npm run build


# backend build stage
FROM continuumio/miniconda3
WORKDIR /app


# Create the environment:
COPY collaiborate/environment.yml .
RUN apt-get update
RUN apt-get install -y gcc
RUN conda install conda=23.1.0
RUN conda update -n base -c defaults conda
RUN conda env create -f environment.yml

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "collaiborate", "/bin/bash", "-c"]

# Copy frontend:
COPY --from=frontend /app/dist/. ./frontend-build/dist

# The code to run when container is started:
COPY collaiborate/api.py .
COPY collaiborate/backend.py .
COPY collaiborate/utils.py .
COPY collaiborate/val_data.npy .
COPY collaiborate/umap_extended.csv .
COPY collaiborate/model_lessCapacity.pth .
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "collaiborate", "python", "api.py"]
