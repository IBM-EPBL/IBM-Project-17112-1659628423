from flask import Flask, render_template, redirect, url_for, request, flash, escape, session
import openapi_client
from com.spoonacular import misc_api
import ibm_db

conn = ibm_db.connect(f"DATABASE=bludb;HOSTNAME=?;PORT=?;SECURITY=SSL;SSLServerCertificate=SSLCertificate.crt;UID=?;PWD=?",'','')

def nutitionapi(imagelink,image_id):
    configuration = openapi_client.Configuration(
        host = "https://api.spoonacular.com"
    )
    configuration.api_key['apiKeyScheme'] = os.getenv("NUTRITION_API_KEY")

    with openapi_client.ApiClient(configuration) as api_client:
        api_instance = misc_api.MiscApi(api_client)
        image_url = imagelink
    try:
        api_response = api_instance.image_analysis_by_url(image_url)
        y = api_response
        cal= y["nutrition"]["calories"]["value"]
        Carb= y["nutrition"]["carbs"]["value"]
        fat= y["nutrition"]["fat"]["value"]
        protein= y["nutrition"]["protein"]["value"]
        name=y["category"]["name"]
        image=image_id["ID"]
        sql = f"INSERT INTO nutritiondetails(calories,carbs,fat,protein,ref_id,name) VALUES('{escape(cal)}','{escape(Carb)}','{escape(fat)}','{escape(protein)}','{escape(image)}','{escape(name)}')"
        
        prep_stmt = ibm_db.prepare(conn, sql)

        ibm_db.execute(prep_stmt)
        flash("Successful db operation", "success")
        
    except openapi_client.ApiException as e:
        print("Exception when calling MiscApi->image_analysis_by_url: %s\n" % e) 
