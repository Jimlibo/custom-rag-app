# Custom RAG App

![Python](https://img.shields.io/badge/python-v3.9-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-v1.36-green.svg)
![LangChain](https://img.shields.io/badge/langchain-v0.2.6-orange.svg)
![Ollama](https://img.shields.io/badge/ollama-v0.1.48-yellow.svg)

## General
An app that utilizes streamlit to offer a  user-friendly interface for 
creating a rag pipeline. The app allows the user to upload his/her own 
PDF fies, which are then processed and stored in a new (or existing) vector
database.

The user can then query the database, and receive the most relevant
response generated from an llm model. The LLM that we chose to use is the 
gemma:2b model, and for model serving we use [Ollama](https://ollama.com/).

The app also offers the ability to delete an existing database, although currently
this functionality is limited for Windows.

## Setup
In order to get the app running, first you need to clone this repository.
This can be done with the command:
```bash
git clone https://github.com/Jimlibo/custom-rag-app.git
```
After you have cloned the repository, you can navigate to the app's directory:
```bash
cd custom-rag-app
```


### Run using Docker
If you have docker and docker-compose installed, you can run the app with the following commands:
```sh
docker-compose up
```


### Run using Streamlit
If you do not have docker installed, you can first install the required packages from
[requirements.txt](https://github.com/Jimlibo/custom-rag-app/blob/main/src/requirements.txt) and then
run the app through streamlit. This can be done with the following commands:
```sh
cd src
pip install -r requirements.txt
streamlit run app.py
```

In order to run inference on a LLM, you also need to have the Ollama service up and running. If it's the
first time you run the app, you have to pull the **gemma:2b** model from ollama repository before serving it.
To pull the model, open another terminal and execute the command:
```sh
ollama pull gemma:2b
```

To serve the model, run:
```sh
ollama serve
```

⚠️ If the app does not open automatically, you can navigate to http://localhost:8501/ in the browser
of your choice.

## License
Distributed under the MIT License. See 
[LICENSE](https://github.com/Jimlibo/custom-rag-app/blob/main/LICENSE) for more information.



