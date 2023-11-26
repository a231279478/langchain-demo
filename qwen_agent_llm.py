from typing import List, Mapping, Optional ,Any
from langchain.llms.base import LLM
from langchain.callbacks.manager import CallbackManagerForLLMRun  
import openai

openai.api_base = "http://region-9.seetacloud.com:25540/v1"
openai.api_key = ""

class QwenLLM(LLM):
    model:str = "qwen-turbo"  

    @property
    def _llm_type(self) -> str:
        return self.model

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        if stop is not None:
            print('call qwen content:',prompt)
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{'role':'user','content':prompt}],
                temperature=0,

            )
            print('result qwen content:', response.choices[0].message.content.split('\nObservation')[0])
            print('-------------------------------------------------------------------------------')
            return response.choices[0].message.content.split('\nObservation')[0]
        else:
            print('else 执行了')
            print('call qwen content:',prompt)
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{'role':'user','content':prompt}],
                temperature=0,

            )
            print('result qwen content:', response.choices[0].message.content.split('\nObservation')[0])
            print('-------------------------------------------------------------------------------')
            return response.choices[0].message.content.split('\nObservation')[0]


    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"model": self.model}
    
if __name__ == '__main__':
    llm = QwenLLM()
    result = llm.predict('深圳有什么好吃的？')
    print(result)
