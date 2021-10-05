#written by sai teja using bottom up method
from boltiot import Bolt
import json
import math
import time#will be used to create wait time for api
import requests
freq=20#enter in seconds
api_key = "72207486-0705-4f3c-a544-1dfa816db220"
device_id  = "BOLT14918157"
mybolt = Bolt(api_key, device_id)
web_hook_addr='https://hook.integromat.com/63i89umrgiu6d3akp8bccfle1hxjr4jw'
def std(data_frame):#used to calculate standard deviation
   k=len(data_frame)
   M=0
   for val in data_frame:
      M+=val
   M/=k
   ans=0
   for val in data_frame:
      ans+=(val-M)*(val-M)
   ans/=k
   ans=math.sqrt(ans)
   return ans
def trigger_integromat_webhook(msg):
    URL = web_hook_addr # REPLACE WITH CORRECT URL
    response = requests.request("POST", URL,data={'message':msg})
    print(response.text)
def bounds(history,frame_size,c_factor):#pass in history as an array to get bounds of next prediction(in form of array [lower_bound, upper_bound], if values are inconsistent you get false
   tot=len(history)
   if(tot-1<frame_size):
       return [False]
   else:
       ans=[]
       data_frame=history[tot-1-frame_size:tot-1]
       z_sigma=c_factor*std(data_frame)
       ans.append(True)
       ans.append(history[-2]-z_sigma)
       ans.append(history[-2]+z_sigma)
       return ans
history=[]
while(True):
      response=mybolt.analogRead('A0')
      fin_res=json.loads(response)
      if fin_res['success']!=1:
         print('error reading::'+fin_res['value'])
         time.sleep(freq)
         continue
      data=0
      try:
         data=int(fin_res['value'])
         history.append(data)
         print(data)
      except error as e:
          print('error in value::'+e)
          time.sleep(freq)
          continue
      bound=bounds(history,7,0.45)#frame size==7 , c factor==2
      if bound[0]==False:
         time.sleep(freq)
         continue
      if bound[0]==True:
           print('bound: ',bound[1])
           if (data<bound[1]):
              trigger_integromat_webhook('sudden drop of '+str(bound[1]-data)+'mods in light')
              time.sleep(freq)
              continue
      time.sleep(freq)
   
   
       

       
      
