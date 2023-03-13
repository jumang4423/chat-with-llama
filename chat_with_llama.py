#!/usr/bin/env python3
import json
import argparse

USER_NAME="User"

parser = argparse.ArgumentParser(description="Chat with a character specified llama")
parser.add_argument("-c", "--character", type=str, help="Path to the Character JSON file (.json)", required=True)
parser.add_argument("-m", "--model", type=str, help="Path to the Quantized Model File (.bin)", required=True)
args = parser.parse_args()

# Load the character JSON file
try:
    with open(args.character, "r") as f:
        character_json = json.load(f)
except FileNotFoundError:
    print(f"Error: File not found: {args.json}")
    exit(1)
except json.JSONDecodeError as e:
    print(f"Error: Failed to parse JSON file: {args.json}")
    print(f"Reason: {str(e)}")
    exit(1)

# run llama.cpp
model = args.model
temperature = character_json["temperature"]
reverse_prompt_string = f"{USER_NAME}:"
prompt = f"{character_json['system']} \n<CHAT LOG>\n"
for history in character_json["conversation_examples"]:
    userName = USER_NAME if history["isUser"] else character_json["character_name"]
    prompt += f"{userName}: {history['content']} \n"

prompt += reverse_prompt_string

commands = ['./main', "-m", model, "-t", "8", "-n", "256", "--repeat_penalty", "1.0", "--temp", str(temperature), "--color", "-i", "-r", "'" + reverse_prompt_string + "'", "-p", "'" + prompt + "'"]


# print out commands to eval from terminal
print(" ".join(commands))
