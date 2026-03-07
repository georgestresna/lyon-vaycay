from pymongo import MongoClient

def setup_cities_data():

    client = MongoClient('localhost', 27017)

    db = client['busScraper'] #nume database
    ## nu creeaza db decat data ii dau date

    mycol = db["cities"]
    #nu creeaza colectie decat dupa ce ii dai continut
    return mycol

def enterData(mycol):
    city = {
        "city_name": "Lyon",
        "city_uuid": "whatever_the_fuck"
    }

    x = mycol.insert_one(city)
    print(x.inserted_id)

def check(mycol):
    x =mycol.find()
    print(list(x))

# check(setup())

def deletion(mycol):
    x = mycol.delete_many({'city_name': "Lyon"})

#deletion(setup())

def load_data2db(monster_matrix):
    client = MongoClient('localhost', 27017)
    db = client['busScraper'] #nume database
    mycol = db["dummy_data"]
    monster_dic = {
        "name": "full_monthly_scrape",
        "data": monster_matrix
    }
    result = mycol.insert_many(monster_dic)
    return list(mycol.find())

