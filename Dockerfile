FROM python:3.9

# define starting directory
WORKDIR /custom-rag-app

# install necessary system tools
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*


# copy all files from the ./src local directory to the container /custom-rag-app/src directory
ADD src src

# install necessary python packages
RUN pip install -r src/requirements.txt

# inform docker that container listens on port 8501 (default streamlit port)
EXPOSE 8501

# perform healthchecks to make sure the container is still running
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

WORKDIR /custom-rag-app/src

# run the streamlit app
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]