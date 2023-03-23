FROM continuumio/miniconda3

WORKDIR /app

# Create the environment:
COPY environment.yml .
RUN apt-get update
RUN apt-get install -y gcc
RUN conda install conda=23.1.0
RUN conda update -n base -c defaults conda
RUN conda env create -f environment.yml

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "collaiborate", "/bin/bash", "-c"]


# The code to run when container is started:
COPY api.py .
COPY backend.py .
COPY utils.py .
COPY val_data.npy .
COPY umap.csv .
COPY model_lessCapacity.pth .
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "collaiborate", "python", "api.py"]