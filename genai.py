import google.generativeai as genai


class AI:
    def __init__(self, history, token):
        genai.configure(api_key=token)

        self.generation_config = {"temperature": 0.9, "top_p": 1, "top_k": 1, "max_output_tokens": 2048,
                                  "stop_sequences": ["", ], }

        self.safety_settings = [{"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}, ]

        self.gemini = genai.GenerativeModel(model_name="gemini-1.0-pro", generation_config=self.generation_config,
                                            safety_settings=self.safety_settings)

        self.ai_chat = self.gemini.start_chat(history=history)

    def chat(self, prompt):
        response = self.ai_chat.send_message(prompt, stream=True)
        response.resolve()
        return {'raw': response, 'text': "\n\u001b[32m" + str(response.text) + "\u001b[0m"}

    def generate_content_warning(self, prompt_feedback):
        return content_warning
