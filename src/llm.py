from abc import ABC, abstractmethod
import os 
from openai import OpenAI
from huggingface_hub import InferenceClient

class BaseLLM(ABC):
    def __init__(self, model_name: str, api_key: str = None, **kwargs):
        """
        Initialize the base LLM class with common attributes.

        Parameters:
        - model_name (str): Name of the model to use.
        - api_key (str): API key for authenticating with the LLM provider.
        - kwargs: Additional parameters that may be specific to the provider.
        """
        self.model_name = model_name
        self.api_key = api_key
        self.config = kwargs

    @abstractmethod
    def generate_text(self, messages: dict, **kwargs) -> str:
        """
        Abstract method to generate text from a prompt. Must be implemented by subclasses.

        Parameters:
        - messages (dict): The input prompt for the LLM.
        - kwargs: Additional parameters for the specific provider's implementation.

        Returns:
        - str: The generated text.
        """
        pass

    


class OpenAILLM(BaseLLM):
    def __init__(self, model_name: str, api_key: str = None,**kwargs):
        super().__init__(model_name, api_key, **kwargs)
        self.model = model_name
        if api_key:
            self.client = OpenAI(api_key=api_key)
        else:
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            
    def generate_text(self, messages: dict, **kwargs) -> str:
        completion = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            **kwargs
        )
        # self.client.close()
        return completion.choices[0].message.content
    
    def generate_structured_text(self, messages: dict,*, schema = None, **kwargs):
        completion = self.client.beta.chat.completions.parse(
            model = self.model_name,
            messages = messages,
            response_format = schema,
            **kwargs
        )
        # self.client.close()
        return completion.choices[0].message.parsed
    
    def __repr__(self):
        return f"Service Provider: OpenAI\n Developer: OpenAI\n Model: {self.model_name}"
    
class HuggingFaceLLM(BaseLLM):
    def __init__(self, model_name: str, api_key: str = None, **kwargs):
        super().__init__(model_name, api_key, **kwargs)
        self.model = model_name
        if api_key:
            self.client = InferenceClient(model=model_name ,api_key=api_key)
        else:
            self.client = InferenceClient(model=model_name, api_key=os.getenv("HUGGINGFACEHUB_API_TOKEN"))
    
    def generate_text(self, messages: dict, **kwargs) -> str:
        completion = self.client.chat_completion(
            messages = messages,
            model = self.model_name, 
            **kwargs
        )
        
        return completion.choices[0].message.content

    def generate_structured_text(self, messages: dict,*, schema = None, **kwargs):
        completion = self.client.chat_completion(
            messages = messages,
            model = self.model_name,
            response_format = schema.model_json_schema(),
            **kwargs
        )
        
        return completion.choices[0].message.content

    def __repr__(self):
        return f"Service Provider: Hugging Face\n Developer: {self.model_name.split('/')[0]}\n Model: {self.model_name.split('/')[1]}"