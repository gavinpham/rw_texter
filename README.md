# rw_texter
Prototyped Texting Service for RefillWise

Requirements:
  - python(2.7)
  - pip
      > pip install twilio

      > pip install flask
      
      > pip install editdistance
        
  - ngrok

Great reference from Twilio
  https://www.twilio.com/docs/quickstart/python/sms#overview
  
Reference Guide for ngrok
  https://www.twilio.com/blog/2015/09/6-awesome-reasons-to-use-ngrok-when-testing-webhooks.html
  
Reference Guide for Screens in Linux
  https://www.rackaid.com/blog/linux-screen-tutorial-and-how-to/

How To Use (Linux Amazon EC2):

1. Confirm that all requirements have been fulfilled
    - Environment variables referenced in receive_text.py must exist in .bash_profile
    - curl ngrok and place into path directory (as referenced in the ngrok starting guide)

2. Start a screen session 
    > screen

2. In a screen, run: 
    > python receive_text.py  
    
   Open another screen by pressing: 
    > ctrl + a, c
    
   In the new screen, run:
    > ngrok http 5000
    
3. Copy the https address given by ngrok (webhook to localhost port 5000) and paste into Twilio phone numbers console under "A message comes in". Don't forget to add /sms to the end of the address! That tells flask where it needs to route the request.

4. Detach from the screen session: 
    > ctrl + a, d

Now the program should be running and will respond to texts! If you're having trouble with it, feel free to contact gpham@smu.edu!

Much Love,

Gavin
