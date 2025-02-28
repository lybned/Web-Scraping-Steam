from ollama import chat
import json
all_text = '''
The following text is a description of a vulnerability, give me a CPE (cpe:<cpe_version>:<part>:<vendor>:<product>:<version>:<update>:<edition>:<language>:<sw_edition>:<target_sw>:<target_hw>:<other>) string for based on the description:
"Multiple IBM Business Automation Workflow versions are vulnerable to cross-site scripting. This vulnerability allows users to embed arbitrary JavaScript code in the Web UI thus altering the intended functionality potentially leading to credentials disclosure within a trusted session.  IBM X-Force ID:  233978."
'''

from pydantic import BaseModel

class Info(BaseModel):
  Software: str
  Affected_Version: str

class InfoString(BaseModel):
  Result: str


stream = chat(
    model='llama3.2',
    messages=[{'role': 'user', 'content': all_text}],
    stream=True,
    format=InfoString.model_json_schema(),
)
total = ""



for chunk in stream:
  total += chunk['message']['content']
  #print(chunk['message']['content'])
  #print(json.loads(chunk['message']['content']))

print(total)
print(json.loads(total))  