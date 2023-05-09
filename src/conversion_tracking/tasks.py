from session_management.models import Category, UserSession
from quiz_site.celery import app
from conversion_tracking.models import ConversionExclusionsList, Pixel
import requests
import hashlib
import time
import datetime
from quiz_site.settings import BASE_DIR

@app.task
def conversion_tracking(event_name, event_id, session_id=None, category_id=None, order_number=None, event_source_url=None):


    try:

        if event_source_url.__contains__("http"):
            pass
        else:
            event_source_url = f"https://{event_source_url}"
    except Exception as e:
        print(e)
    #Also use user_agent to detect bots and not fire?


    unix_time = int(time.time())

    timestamp = datetime.datetime.now().replace(microsecond=0).isoformat()
    
    action_source = "website"

    category_object = "No object"
    if category_id:
        category_object = Category.objects.get(id=category_id)


    session = UserSession.objects.get(session_id=session_id)




    user_agent = session.user_agent

    if user_agent:

        if user_agent == 'Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0':
            return
        
        elif ConversionExclusionsList.objects.filter(user_agent=user_agent):
            return
        elif 'bot.html' in user_agent:
            return
        elif UserSession.objects.filter(user_agent=user_agent,add_user_agent_to_exclusion_list=True):
            return

    #Check for session fbp
    latest_fbp_loop_count = 0

    if not event_name == "PageView" or not event_name =="ViewContent":

        while (not session.latest_fbp or not session.email) and latest_fbp_loop_count < 10: 
            #Need to get session.email before increasing loop count
            latest_fbp_loop_count += 1
            session = UserSession.objects.get(session_id=session_id)

            time.sleep(1)

    # check for session email
    hashed_email =  None
    

    if session.email:
        hashed_email = str(hashlib.sha256((str(session.email).lower()).encode('utf-8')).hexdigest())
            

    user_ip = session.ip

    #Get the country code and hash

    hashed_country_code = None

    try:
        if session.country_code:

            country_code = session.country_code
            hashed_country_code = hashlib.sha256((str(country_code).lower()).encode('utf-8')).hexdigest()


    except Exception as e:
        print("Exception when getting country code")
        print(e)

        


    if event_name != "Purchase" and category_object.enable_pixels:
        pixels = Pixel.objects.filter(category__id=category_id)

    
        for pixel in pixels:
            try:
                if pixel.pixel_type == "facebook":
                    endpoint = f"https://graph.facebook.com/v13.0/{pixel.pixel_id}/events?access_token={pixel.conv_api_token}"


                    #Fire when event occurs e.g. post to cart view for atc at end of function and use async
                    data = {
                            "data": [
                                {
                                    "event_name": event_name,
                                    "event_time": unix_time,
                                    "event_id": event_id,
                                    "event_source_url": event_source_url,         
                                    "action_source": action_source,
                                    "user_data": {
                                        "client_ip_address": user_ip,
                                        "client_user_agent": user_agent

                                    }
                                
                                }

                            ]
                            }
                    
                    if session.latest_fb_clid:
                        data['data'][0]['user_data']["fbc"] = str(session.latest_fb_clid)

                    if session.latest_fbp:
                        data['data'][0]['user_data']["fbp"] = str(session.latest_fbp)
                    
                    if session.email:
                        data['data'][0]['user_data']["em"] = hashed_email

                    if hashed_country_code:
                        data['data'][0]['user_data']["country"] = hashed_country_code



                    response = requests.post(endpoint, json=data)

                elif pixel.pixel_type == "tiktok":
                    endpoint = "https://business-api.tiktok.com/open_api/v1.2/pixel/track/"

                    headers = {
                        'Access-Token': str(pixel.conv_api_token),
                        'Content-Type': 'application/json'
                        }
                    
                    data = {
                        "pixel_code": str(pixel.pixel_id),
                        "event": event_name,
                        #   "event_id": "1616318632825_357", #Not required
                        "timestamp": timestamp, 
                        "context": {
                            # "ad": {
                            #   "callback": "123ATXSfe"
                            # },
                            #ad is needed for ttclickid setup and recommended 
                            "page": {
                            "url": event_source_url, #page url of event
                            #   "referrer": "http://demo.mywebsite.com" #referrer not required
                            },
                            "user": {
                            #   "external_id": "f0e388f53921a51f0bb0fc8a2944109ec188b59172935d8f23020b1614cc44bc",
                            #   "phone_number": "2f9d2b4df907e5c9a7b3434351b55700167b998a83dc479b825096486ffcf4ea", #Later on can add phone number
                            # "email": "dd6ff77f54e2106661089bae4d40cdb600979bf7edc9eb65c0942ba55c7c2d7f",
                            },
                            "user_agent": user_agent,
                            "ip": user_ip
                        },
                        "properties": {
                            # "contents": [
                            #   {
                            #     "price": 8,
                            #     "quantity": 2,
                            #     "content_type": "product_group",
                            #     "content_id": "1077218"
                            #   },
                            #   {
                            #     "price": 30,
                            #     "quantity": 1,
                            #     "content_type": "product_group",
                            #     "content_id": "1197218"
                            #   }
                            # ],
                            # "currency": "USD",
                            # "value": 1 #Only required for purchase, for now keep this as 1
                        }
                        }
                    
                    response = requests.post(endpoint, headers=headers, json=data)



            except Exception as e:
                print("Error when sending event")
                print(e)                           








    elif event_name == "Purchase":

 
        if category_object.enable_pixels:
            
                pixels = Pixel.objects.filter(category=category_object)
                
                for pixel in pixels:
                    if pixel.pixel_type == "facebook":
                        endpoint = f"https://graph.facebook.com/v13.0/{pixel.pixel_id}/events?access_token={pixel.conv_api_token}"

                        data = {
                                "data": [
                                    {
                                        "event_name": event_name,
                                        "event_time": unix_time,
                                        "event_id": event_id,
                                        "event_source_url": event_source_url,         
                                        "action_source": action_source,
                                        "user_data": {
                                            "client_ip_address": user_ip,
                                            "client_user_agent": user_agent,
                                            "em": [
                                            str(hashed_email)
                                            ],
                                            # "ph": [
                                            # "254aa248acb47dd654ca3ea53f48c2c26d641d23d7e2e93a1ec56258df7674c4"
                                            # ],
                                            # "fn": [
                                            #     str(hashed_first_name)
                                            # ],
                                            # "ln": [
                                            #     str(hashed_last_name)
                                            # ]

                                        },
                                        # "custom_data": {
                                        #     "value": 100.2,
                                        #     "currency": "USD",
                                        #     "content_ids": [
                                        #     "product.id.123"
                                        #     ],
                                        #     "content_type": "product"
                                        # },
                                    }

                                ]
                                }



                        if session.latest_fb_clid:
                            data['data'][0]['user_data']["fbc"] = str(session.latest_fb_clid)

                        if session.latest_fbp:
                            data['data'][0]['user_data']["fbp"] = str(session.latest_fbp)

                        if session.email:
                            data['data'][0]['user_data']["em"] = hashed_email


                        if hashed_country_code:
                            data['data'][0]['user_data']["country"] = hashed_country_code


                        response = requests.post(endpoint, json=data)


                    elif pixel.pixel_type == "tiktok":
                        endpoint = "https://business-api.tiktok.com/open_api/v1.2/pixel/track/"

                        headers = {
                            'Access-Token': str(pixel.conv_api_token),
                            'Content-Type': 'application/json'
                            }
                        
                        
                        data = {
                            "pixel_code": str(pixel.pixel_id),
                            "event": event_name,
                            #   "event_id": "1616318632825_357", #Not required
                            "timestamp": timestamp, 
                            "context": {
                                # "ad": {
                                #   "callback": "123ATXSfe"
                                # },
                                #ad is needed for ttclickid setup and recommended 
                                "page": {
                                "url": event_source_url, #page url of event
                                #   "referrer": "http://demo.mywebsite.com" #referrer not required
                                },
                                "user": {
                                #   "external_id": "f0e388f53921a51f0bb0fc8a2944109ec188b59172935d8f23020b1614cc44bc",
                                #   "phone_number": "2f9d2b4df907e5c9a7b3434351b55700167b998a83dc479b825096486ffcf4ea", #Later on can add phone number
                                "email": str(hashed_email),
                                },
                                "user_agent": user_agent,
                                "ip": user_ip
                            },
                            "properties": {
                                # "contents": [
                                #   {
                                #     "price": 8,
                                #     "quantity": 2,
                                #     "content_type": "product_group",
                                #     "content_id": "1077218"
                                #   },
                                #   {
                                #     "price": 30,
                                #     "quantity": 1,
                                #     "content_type": "product_group",
                                #     "content_id": "1197218"
                                #   }
                                # ],
                                "currency": "USD",
                                "value": 1 #Only required for purchase, for now keep this as 1
                            }
                            }
                        
                        response = requests.post(endpoint, headers=headers, json=data)



            













    



