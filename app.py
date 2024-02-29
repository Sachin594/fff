from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as urlreq
import pymongo
import logging
logging.basicConfig(filename="scrapper.log" , level=logging.INFO)
import os

app = Flask(__name__)

@app.route("/", methods = ['GET'])
def homepage():
    return render_template("index.html")

@app.route("/review" , methods = ['POST' , 'GET'])
def index():
    if request.method == 'POST':
                try:
                        save_dir='image/'
                        if not os.path.exists(save_dir):
                            os.makedirs(save_dir)
                        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}
                        query=request.form['content'].replace(" ","")
                        response=requests.get(f"https://www.google.com/search?q={query}&tbm=isch&ved=2ahUKEwi20JLin86EAxUOa2wGHVI9D6oQ2-cCegQIABAA&oq=selmon+bhoi&gs_lp=EgNpbWciC3NlbG1vbiBiaG9pMgUQABiABDIKEAAYgAQYigUYQzIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAESNwhUK4IWOIbcAB4AJABAJgB4wGgAdsRqgEGMC4xMS4xuAEDyAEA-AEBigILZ3dzLXdpei1pbWfCAg0QABiABBiKBRhDGLEDwgIIEAAYgAQYsQPCAgQQIxgniAYB&sclient=img&ei=iUPfZfbnDY7WseMP0vq80Ao&bih=742&biw=1536&rlz=1C1RXQR_en-GBIN1071IN1071")
                        responce_bs=bs(response.content,'html.parser')
                        img_tags=responce_bs.find_all("img")
                        del img_tags[0]
                        image_data_mongo=[]
                        for index,i in enumerate(img_tags) :
                            image_url=i['src']
                            image_data=requests.get(image_url).content
                            mydict={"index":image_url,"image":image_data}
                            image_data_mongo.append(mydict)
                            with open(os.path.join(save_dir,f"{query}_{img_tags.index(i)}.jpg"),"wb") as f :
                                f.write(image_data)


                        from pymongo.mongo_client import MongoClient
                        from pymongo.server_api import ServerApi

                        uri = "mongodb+srv://Sachin947:sachin@cluster947.n1o4otf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster947"

                        # Create a new client and connect to the server
                        client = MongoClient(uri, server_api=ServerApi('1'))

                        # Send a ping to confirm a successful connection
                        try:
                            client.admin.command('ping')
                            print("Pinged your deployment. You successfully connected to MongoDB!")
                        except Exception as e:
                            print(e)
                        db=client["image_scrap"]
                        col=db["image_scrap_data"]
                        col.insert_many(image_data_mongo)
                        return "image loaded"
                except Exception as e :
                    logging.info(e)
                    return "something is wrong"
    else :
        return render_template("index.html")



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
