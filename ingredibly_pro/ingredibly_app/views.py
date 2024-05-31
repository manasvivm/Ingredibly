from django.shortcuts import render
from google_images_search import GoogleImagesSearch
from .models import Product_db,Ingredient_db
from django.http import HttpResponse
import openai
import easyocr
from cv2 import (VideoCapture, namedWindow, imshow, waitKey, destroyWindow,imwrite)
from . import myapi_keys
chatgpt_api,google_search_api,cx_val=myapi_keys.fun()
model_engine="text-davinci-003"
openai.api_key=chatgpt_api
gis = GoogleImagesSearch(google_search_api, cx_val)
# Create your views here.
res_cat=""

def GPT(query):
    completion = openai.Completion.create(
            engine=model_engine,
            prompt=query,
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.5,
            )
    response=completion.choices[0].text  
    return response 
def fill_ingredient_table(ing):	
    ing=ing.split(', ')	
    for i in ing[0:min(len(ing),5)]:    	
        query="give me the source of "+ i +"in a single line"	
        source1=GPT(query)	
        source1=source1.strip("\n")	
        query="give me the use of  "+i+" in a single line"	
        use1=GPT(query)	
        use1=use1.strip("\n")	
        query="give me the allergies caused by" +i+ "in a single line"	
        allergen_flag1=GPT(query)	
        allergen_flag1=allergen_flag1.strip("\n")	
        data=Ingredient_db(ingredient_name=i,source=source1,use=use1,allergen_flag=allergen_flag1)	
        data.save()	
    return HttpResponse(ing)	
    
def fill_product_table(brand_name1,prod_name1):
    global res_cat

    query="what is the food category of "+brand_name1+prod_name1+" in a word or two WITHOUT EXPLANATION"
    res_cat=GPT(query)
    res_cat=res_cat.strip("\n")
    query="Give me the ingredients of "+brand_name1+prod_name1+"on a single line"
    res_ing=GPT(query)
    res_ing=res_ing.strip("\n")
    fill_ingredient_table(res_ing)
    img=brand_name1+prod_name1
    _search_params = {
        'q': img,
        'num': 1,
        'filetype':'png|jpg'
    }
    gis.search(search_params=_search_params)
    res_url=gis.results()[0].url
    data=Product_db(prod_name=prod_name1,prod_brand=brand_name1,category=res_cat,ingredients=res_ing,product_url=res_url)
    data.save()
    '''query="products similar to "+prod_name1+" in one single line separate each product brand name from it's product name with a comma"
    res_sim=GPT(query)
    a=res_sim
    res_sim=res_sim.strip("\n")
    '''
    def repeat_similar(res_sim):
        pos=-1
        count=0
        while(count<3): 
            count+=1
            try:
                pos1=res_sim.index('(',pos1+1)
                pos2=res_sim.index(')',pos1+1)
                res_sim=res.sim[pos2+1:]
                x=res_sim[pos1+1:pos2]
                a,b=x.split(", ")
                brand_name1=a 
                prod_name1=b
                def GPT(query):
                    completion = openai.Completion.create(
                            engine=model_engine,
                            prompt=query,
                            max_tokens=100,
                            n=1,
                            stop=None,
                            temperature=1,
                            )
                    response=completion.choices[0].text  
                    return response 
                #query="give me the food category of "+brand_name1+" in a word or two WITHOUT EXPLANATION"
                #res_cat=GPT(query)
                if(not Product_db.objects.filter(prod_brand =brand_name1,prod_name=prod_name1).exists() ):
                    query="Give me the ingredients of "+brand_name1+prod_name1+"on a single line"
                    res_ing=GPT(query)
                    res_ing=res_ing.strip("\n")
                    img=brand_name1+prod_name1
                    _search_params = {
                        'q': img,
                        'num': 1,
                        'filetype':'png|jpg'
                    }
                    gis.search(search_params=_search_params)
                    res_url=gis.results()[0].url
                    data=Product_db(prod_name=prod_name1,prod_brand=brand_name1,category=res_cat,ingredients=res_ing,product_url=res_url)
                    data.save()
                    fill_ingredient_table(res_ing)
                
            except:
                pass 
                    
                #query="give me the food category of "+brand_name1+" in a word or two WITHOUT EXPLANATION"
                #res_cat=GPT(query)
                

    #repeat_similar(res_sim)
    return res_ing
    #return HttpResponse(res_sim)
def home(request):
    #return HttpResponse(result_con)
    return render(request,'home.html')
def scan_product(request):
    '''
    cam_port = 0
    cam = VideoCapture(cam_port)
    while(True):
         a,frame=cam.read()#a-True if a frame can be grabbed else false, frame- array of pictures taken from webcam
         #print(frame)
         imshow('Camera',frame)#shows the camera screen
         if waitKey(1) & 0xff==ord('q'):#to take a picture and close the webcam screen
            #string=strftime("%d_%m_%H_%M_%S")   
            pic=frame.copy()#freezes the video at the instant and stores the picture
            #imwrite(filename,pic)
            imwrite("product.png", pic)
            cam.release()#release the image captured
            break
'''
    reader = easyocr.Reader(['en'])
    result = reader.readtext('product.png',detail=0)
    result_con=" ".join(result)
    query="what is the brand name in this and nothing else."+str(result)
    brand=GPT(query)
    brand=brand.strip("\n")
    query="what is the product name in this and nothing else."+str(result)
    prod=GPT(query)
    prod=prod.strip("\n")
    if(not Product_db.objects.filter(prod_brand=brand,prod_name=prod).exists()):
        fill_product_table(brand,prod)
    mhello=Product_db.objects.filter(prod_brand=brand,prod_name=prod).values()
    return render(request,"display_product.html",{'mhello':mhello})
def similar_pro(request,ing):
    mhello=Product_db.objects.filter(ingredients__contains=ing).values()
    return render(request,'similar_products.html',{'mhello':mhello,"ing":ing})
    
def disimilar_pro(request,ing):
    mhello=Product_db.objects.exclude(ingredients__contains=ing).values()
    return render(request,'without_products.html',{'mhello':mhello,"ing":ing})

def description(request,ing):
    mhello=Ingredient_db.objects.filter(ingredient_name__contains=ing).values()
    return render(request,'description.html',{'mhello':mhello,"ing":ing})