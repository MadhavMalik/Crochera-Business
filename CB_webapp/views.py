from django.shortcuts import render
import pandas as pd
import base64
from random import randint

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def product_id_generator(product_type):

    product_id_str = {
        "Doyllies": "DO",
        "Shrugs": "SH",
        "Lace_Borders": "LB",
        "Phone_Covers": "PC",
        "Purses": "PU",
        "Table_Mats": "TM",
        "Lace_Tops": "LT",
        "Saree": "SA",
        "Other": "OT"
    }

    products = pd.read_csv("/Users/madhavmalik/PycharmProjects/Crochera-Business/CB_webapp/products.csv")
    df = pd.DataFrame(products)
    print(df["Product_Type"])
    print((df.Product_Type == product_type).sum())
    print(len(products))

    product_id_num = str((df.Product_Type == product_type).sum() + 1)
    if len(product_id_num) == 1:
        product_id_num = "00"+product_id_num

    elif len(product_id_num) == 2:
        product_id_num = "0"+product_id_num
    else:
        pass

    return product_id_str[product_type] + product_id_num


def home(request):
    return render(request,"home.html")

def upload_products(request):
    return render(request, "upload_products.html")

def generated_barcode(request):
    product_id = request.POST.get("product_id")
    product_price = request.POST.get("product_price")
    product_type = request.POST.get("product_type")
    product_quantity = request.POST.get("product_quantity")
    product_description = request.POST.get("product_description")
    image_data = request.POST.get("image_code")

    print(product_description)
    #product_image = request.FILES['myfile']
    #f = open("image.txt","w")
    #f.write(str(product_image))
    #f.close()
    #print("****", product_image.read()) # this is my file


    if product_type == "Lace Borders": product_type = "Lace_Borders"
    if product_type == "Phone Covers": product_type = "Phone_Covers"
    if product_type == "Lace Tops": product_type = "Lace_Tops"
    if product_type == "Table Mats": product_type = "Table_Mats"

    #product_image = request.FILES['product_image']
    #print(product_image.read())
    '''
    for key, file in request.FILES.items():
        print(key)
        print(file)
        path = file.name
        dest = open(path, 'w')
        if file.multiple_chunks:
            for c in file.chunks():
                print(c)
                dest.write(c)
        else:
            print(file.read())
            dest.write(file.read())
        dest.close()
    '''

    full_product_id = product_id_generator(product_type)
    product_information = {"Product_ID" : full_product_id,
                           "Product_Price": product_price,
                           "Product_Type": product_type,
                           "Product_Quantity": product_quantity,
                           "Available_Quantity": product_quantity,
                           "Product_Description": product_description
                           }

    df = pd.DataFrame([product_information])
    df.to_csv("products.csv", mode='a', header=False, index=False)
    print(product_id)

    index = image_data.find(",")
    #print(image_data[index + 1:])
    with open("product_images/"+ str(full_product_id) + ".png", "wb") as fh:
        fh.write(base64.urlsafe_b64decode(image_data[index+1:]))

    barcode_text = full_product_id + " " +str(product_price)


    return render(request, "generated_barcode.html",{"Product_ID_Barcode": barcode_text})

def scan_barcode(request):
    return render(request, "scan_barcode.html")

orders_details = {}

def customer_details(request):
    quantity_of_products = []
    products_to_be_billed = request.POST.get("products_to_be_billed")
    products_to_be_billed_list = products_to_be_billed.split(",")
    total = 0
    for i in range(len(products_to_be_billed_list)):
        product_quantity = request.POST.get("input"+str(i))
        quantity_of_products.append(product_quantity)
        total += int(products_to_be_billed_list[i][products_to_be_billed_list[i].index(" "):])* int(product_quantity)

    print(quantity_of_products)
    print(products_to_be_billed)
    print(type(products_to_be_billed_list))

    products_in_cart = []
    count = 0
    for product_id in products_to_be_billed_list:
        #orders_details[product_id[:5]] = quantity_of_products[count]
        count+=1
        #products_in_cart.append(product_id[:5])

    orders_details["Product_IDs"] = products_to_be_billed_list
    orders_details["Product_Quantities"] = quantity_of_products
    #orders_details["Product_ID"] = products_in_cart
    orders_details["Customer_ID"] = random_with_N_digits(6)

    #IDEA: {'Product ID' : ['Quantity', 'Price', Customer ID, etc]

    orders_details["Total_Amount"] = total

    print(orders_details)
    #orders_details["Products_Bought"] = products_to_be_billed
    return render(request, "contact.html", {"total":total})

def order_successful(request):
    name = request.POST.get("name")
    cnumber = request.POST.get("cnumber")
    email = request.POST.get("email")
    payment_method = request.POST.get("payment_method")

    orders_details["Name"] = name
    orders_details["Contact_Number"] = cnumber
    orders_details["Email"] = email
    orders_details["Payment_Method"] = payment_method

    df = pd.DataFrame([orders_details])
    df.to_csv("orders.csv", mode='a', header=False, index=False)


    print(orders_details)

    return render(request, "order_successful.html")

def view_products(request):
    return render(request, "view_products.html")