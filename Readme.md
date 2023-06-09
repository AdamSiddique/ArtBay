# Artbay

Source code for Artbay, the online ecommerce site for buying and selling art.

## Initialising the Database
1. Modify the Artbay/Artbay/.env file to the correct credentials of a running postgresql database.

2. Run Artbay/Artbay/utils/init_db

## Running the webserver

Navigate into Artbay/Artbay

Use the command: flask.run

## Access the website

To access the website go to http://127.0.0.1:5000 with your webbrowser.

## Interact with the website

To interact with the website you will first have to create som art listing, you can do this by first creating a user of type Artist by navigating to http://127.0.0.1:5000/signup or using the links on the webpage.

### Creating art listing

To create an art listing navigate to http://127.0.0.1:5000/add-art and fill out the formula, your art pieces will now be displayed at http://127.0.0.1:5000/art.

### Purchase art listing

To purchase an art listing, create a user of type Customer and navigate to http://127.0.0.1:5000/art. Click on the purchase button below the art piece that you would like to purchase, you will be redirected to a confirmation page where you can press on "Yes, buy it", which will confirm your purchase and put the art piece on the customers' your orders page: http://127.0.0.1:5000/art/your-orders.
