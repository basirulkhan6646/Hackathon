
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import requests
from speech_to_text import get_order_details_from_audio
from speech_to_text import exotel_audio_url
import time

load_dotenv()



llm = ChatOpenAI(api_key= os.getenv("OPENAI_API_KEY"), )

multiple_prompt= """You are a Sales representive who analyze a text with sales quotation or sales order details and Return a desired Json format. The text is {input}.
User: Based on this {note} addtional iformation. Give me the json packet in this format {json_format}"""

prompt  =  ChatPromptTemplate.from_template(multiple_prompt) 

output_parser = JsonOutputParser()

chain = prompt | llm | output_parser


def fetch_b2b_order_deatils( transcribed_text, extra_info, desired_json):

    try:
        response = chain.invoke({"input": transcribed_text ,  "note": extra_info, "json_format": desired_json})   
        return { "order_details": response}
    except Exception as e:
        return {"error": str(e)}


def webhook_trigger_func():
    pf_url = os.getenv("WEBHOOK_URL")
    exotel_url = exotel_audio_url() 
    if exotel_url:
        desired_json = '{"company_name":"company test" , "company_email":"company_test@gmail.com" "contact_email":"cp_test@gmail.com", "contact_no":"234567899" "contact_name" :"Anna Joy" ,"sales_person":"Anna","items":[{"sku":"Add Value of Item SKU If available or leave it as blank" , "item_desc":"Add Value of Item name or Item Description If available or leave it as blank","quantity":"10"}, {"SKU":"Add Value of Item SKU If available or leave it as blank","item_desc":"Add Value of Item Name or Item description If available or leave it as blank","quantity":"6"} ] }'
        extra_info = "In email 'AtTheRate' = '@' and email id always in a lower case. Also 'theregofoods' = 'gofoods' and 'gfoods.com' = 'gofoods.com'. On Product Item or SKU no space is required."
        transcribed_text = get_order_details_from_audio()
        requests_packet = fetch_b2b_order_deatils(transcribed_text, extra_info, desired_json)
        if (requests_packet.get('error')):
             print(f"Spam Call detected: {requests_packet['error']}")
        else:
            try: 
                res = requests.post(pf_url, json= requests_packet  )
                print(f"Response status code: {res.status_code}")
            except Exception as e:
                print(f"Error sending webhook: {str(e)}")

    else:
         print(f"New call recordings not found.") 





if __name__ == "__main__":
  
  while True:
    webhook_trigger_func()
    time.sleep(150) # wait for 1 minute before sending the next request
 

