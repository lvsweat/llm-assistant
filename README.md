
# LLM-Assistant

LLM-Assistant is meant to be a home assistant that can help the user with home automations, their computer, general questions, and their schedule using Qwen2.5:3b through Ollama.

## Run Locally

To run locally you are required to have Ollama installed and running. You can find a rundown of Ollama and install instructions [here](https://github.com/ollama/ollama)

This specific project uses a locally configured version of the LLM Qwen2.5:3b. Unconfigured as well as less distilled versions of Qwen2.5 should work just fine as is, just remember to change the ```LLM_NAME``` variable in your ```.env``` file to whatever name you set on for it in Ollama.

There are various API keys that are needed as well. All of which are free, and you can find here:

- [API Ninjas](https://www.api-ninjas.com/) (For resolving coordinates based on the city, state, and country provided)
- Likely more to come.


After installing and starting Ollama, as well as running Qwen2.5, refer to the following step-by-step guide to install and run llm-assistant.

### Step-By-Step

Clone the project
```bash
  git clone https://github.com/lvsweat/llm-assistant
```

Go to the project directory

```bash
  cd llm-assistant
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Configure environment variables

In the project directory add the following to a file named ```.env``` replacing the placeholder values for ```API_NINJAS_KEY``` and ```LLM_NAME``` accordingly.
```bash
  API_NINJAS_KEY=YOUR_API_NINJAS_KEY
  LLM_NAME=YOUR_OLLAMA_MODEL_NAME
```

Run the assistant

```bash
  python main.py
```