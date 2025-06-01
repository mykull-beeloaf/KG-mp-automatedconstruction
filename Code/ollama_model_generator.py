from ollama import Client, chat
from pathlib import Path

class Model:
    def __init__(self, model_name, system_prompt=None):
        self.client = Client()
        self.base_model = model_name

        # Create the model if a system prompt is given
        if system_prompt:
            self._create_model(system_prompt)

    def _create_model(self, system_prompt):
        try:
            response = self.client.create(
                model=self.base_model,
                from_=self.base_model,
                system=system_prompt,
                stream=False,
            )
            print(f"\n\n{self.base_model} model created: {response['status']}")
        except Exception as e:
            print(f"Failed to create model: {e}")

    def chat(self, user_message, stream=False):
        messages = [{'role': 'user', 'content': user_message}]
        try:
            if stream:
                print("[Streaming response]")
                stream_gen = chat(model=self.base_model, messages=messages, stream=True)
                for chunk in stream_gen:
                    print(chunk['message']['content'], end='', flush=True)
                print()  # for newline
                return None
            else:
                response = chat(model=self.base_model, messages=messages)
                return response['message']['content']
        except Exception as e:
            print(f"Chat error: {e}")
            return None
