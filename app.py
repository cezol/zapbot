from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from pymongo import MongoClient
from datetime import datetime
#nodemon main.py
#ngrok http 5000 --domain fit-ghost-feasible.ngrok-free.app

cluster = MongoClient("mongodb+srv://cezol:Cezol@cluster0.zggdytv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = cluster["bakery"]
users = db["users"]
orders = db["orders"]

app = Flask(__name__)
@app.route("/", methods=["get", 'post'])
def reply():

    text = request.form.get("Body") or ''
    number = request.form.get("From") or ''
    number = number.replace("whatsapp:+5527", "")
    res = MessagingResponse()
    user = users.find_one({"number": number})
    if bool(user) == False:
        res.message('\n' + ("Hi, thanks for contacting *The Red Velvet*.\nYou can choose from one of the options below: "
                    "\n\n*Type*\n\n 1️⃣ To *contact* us \n 2️⃣ To *order* snacks \n 3️⃣ To know our *working hours* \n 4️⃣ "
                    "To get our *address*"))
        users.insert_one({"number": number, "status": "main", "messages": []})
    elif user["status"] == 'main':

        try:
            option = int(text)
            res.message(str(option))
        except:
            res.message('\n' + ("\nYou can choose from one of the options below: "
                                "\n\n*Type*\n\n 1️⃣ To *contact* us \n 2️⃣ To *order* snacks \n 3️⃣ To know our *working hours* \n 4️⃣ "
                                "To get our *address*"))
            return str(res)
        if option == 1:
            res.message('j.cezar.bf@gmail')
        elif option == 2:
            res.message('ok, heres the ordering menu*.')
            users.update_one({"number": number},{'$set': {'status':'ordering'}})
            res.message("You can select one of the following cakes to order: \n\n1️⃣ Red Velvet  \n2️⃣ Dark Forest \n3️⃣ Ice Cream Cake"
                "\n4️⃣ Plum Cake \n5️⃣ Sponge Cake \n6️⃣ Genoise Cake \n7️⃣ Angel Cake \n8️⃣ Carrot Cake \n9️⃣ Fruit Cake  \n0️⃣ Go Back")
    elif user["status"] == 'ordering':
        try:
            option = int(text)
        except:
            res.message(
                "You can select one of the following cakes to order: \n\n1️⃣ Red Velvet  \n2️⃣ Dark Forest \n3️⃣ Ice Cream Cake"
                "\n4️⃣ Plum Cake \n5️⃣ Sponge Cake \n6️⃣ Genoise Cake \n7️⃣ Angel Cake \n8️⃣ Carrot Cake \n9️⃣ Fruit Cake  \n0️⃣ Go Back")
            return str(res)
        if option == 0:
            users.update_one({"number":number}, {"$set": {'status':'main'}})
            res.message('\n' + ("\nYou can choose from one of the options below: "
                    "\n\n*Type*\n\n 1️⃣ To *contact* us \n 2️⃣ To *order* snacks \n 3️⃣ To know our *working hours* \n 4️⃣ "
                    "To get our *address*"))
        elif 1 <= option <= 3:
            cakes = ['Red Velvet', 'Dark Forest' , 'Ice Cream']
            selected = cakes[option-1]
            users.update_one({'number':number}, {"$set": {'status':'addres'}})
            users.update_one({'number': number}, {"$set": {'item': selected}})
            res.message('Please enter your address to confirm the order')

        else:
            res.message('ERRO')
    elif user["status"] == 'addres':
        orders.insert_one({"number": number, 'item': user['item'], 'addres': text})
        users.update_one({"number": number}, {"$set": {'status': 'main'}})
    else:
        res.message('macacos velhos')
    users.update_one({"number": number}, {"$push": {"messages": {"text": text, "date": datetime.now()}}})

    return str(res)

if __name__ == "__main__":
    app.run()
