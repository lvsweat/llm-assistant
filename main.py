import ollama
from ollama import ChatResponse, Message, Tool, Options, Client
from typing import Optional, Literal, Sequence, Union, Mapping, Callable, Any
from pydantic.json_schema import JsonSchemaValue
import os
import time
import speech_recognition as sr
from dotenv import load_dotenv

from tools import *
import tts
import mqtt
import env_vars

# Initialize speech recognition
stt = sr.Recognizer()

# Explicitly defining a client to use in case Ollama is hosted on a LAN device rather than localhost
client = Client(
    host=env_vars.OLLAMA_URL
)

load_dotenv()

# Laying out tool functions for LLM to use
available_functions = {
  'get_weather': get_weather,
  'get_time': get_time,
  'save_file': save_file
}

message_log = []


 # Just a wrapped version of Ollamas chat function to avoid providing extra args that will always be the same
def send_message(
    role: str = 'user',
    message: str = '',
    *,
    stream: Literal[False] = False,
    format: Optional[Union[Literal['', 'json'], JsonSchemaValue]] = None,
    options: Optional[Union[Mapping[str, Any], Options]] = None,
    keep_alive: Optional[Union[float, str]] = None,) -> ChatResponse:
    

    message_log.append({'role': role, 'content': message}) # Append new message to message array so LLM has memory of this

    response = client.chat(
        env_vars.LLM_NAME,
        messages=message_log, # Provide array of past messages so LLM can remember past prompts and responses while handling this one
        tools=[get_weather, get_time, save_file],
    ) # Actually send message to LLM

    message_log.append(response.message) # Append LLM response to message array so LLM remembers how it responded
    return response # return response provided by LLM


def handle_response(response: ChatResponse):
    print(response.message)

    if (response.message.content != ''): # Skip tts if the message content is empty (likely a tool call was made and this is the response from that)
        print(response.message.content)
        tts.say(response.message.content)
    
    for tool in response.message.tool_calls or []: # Iterate through all tools used by LLM in response
      function_to_call = available_functions.get(tool.function.name) # Obtain function to call using the current itiration
      if function_to_call: # Make sure the tool the LLM provided exists
        tool_ret = function_to_call(**tool.function.arguments) # Call the tool function with the arguments provided by the LLM
        res2 = send_message('tool', str(tool_ret)) # Send message to LLM with the tool role so the LLM knows the result of the function call
        print(res2.message.content)
        tts.say(res2.message.content)
      else:
        print('Function not found:', tool.function.name)
    return


def mqtt_on_message_postcall(msg: str):
    res = send_message('tool', msg)
    handle_response(res)
    return


mqtt.on_message_postcall = mqtt_on_message_postcall
mqtt.mqtt_connect()


# Main loop to handle speech-to-text microphone input
while (True):
    try:
       with sr.Microphone() as source2:
            stt.adjust_for_ambient_noise(source2, duration=0.2)
            print('Listening....')
            audio2 = stt.listen(source2) # Record phrase from microphone

            voice_input = stt.recognize_google(audio2) # Transcribe the audio message
            voice_input = str(voice_input).lower()

            print(f'Heard: {voice_input}')
            if (voice_input.startswith(env_vars.LLM_NAME)): # Check to see if the audio message was meant for the LLM
                voice_input = voice_input.removeprefix(env_vars.LLM_NAME)
                res = send_message('user', voice_input) # Send transcribed audio message to LLM
                handle_response(res) # Handle the LLM's response
    except sr.RequestError as e:
        print(f'Could not request results: {e}')
    except sr.UnknownValueError:
        print(f'Unknown error occurred')