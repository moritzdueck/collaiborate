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

RUN curl -o val_data.npy https://polybox.ethz.ch/index.php/s/T3PNmkWiDH1xwEl/download
RUN curl -o umap_extended.csv https://polybox.ethz.ch/index.php/s/xy2UMmlL7zMNi9p/download
RUN curl -o model_lessCapacity.pth https://polybox.ethz.ch/index.php/s/XK6OcQQzyl29CQP/download
RUN curl -o knn_analysis_quickdraw_10000_100.csv https://polybox.ethz.ch/index.php/s/MU6c3qOq8NdzKkI/download
RUN curl -o base_slim.csv https://polybox.ethz.ch/index.php/s/mBsfssjPjBW0uh9/download

ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "collaiborate", "python", "api.py"]
