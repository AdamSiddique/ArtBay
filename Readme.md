

# ArtBay

Source code for ArtBay, the online C2C site for buying and selling art.

ArtBay uses the following dataset: https://www.kaggle.com/datasets/momanyc/museum-collection?select=artworks.csv


## Initialising the Database

1. Modify the `ArtBay/.env` file to contain the correct credentials of a running PostgreSQL database.

> Note: The SECRET_KEY parameter must be non empty

2. Navigate to `ArtBay/` and use pip to install the required modules e.g. with the command `pip3 install -r requirements.txt`.

3. Navigate to `ArtBay/utils/` and run `python init_db.py` using your local Python 3 installation. This will initialise the database with the values from the dataset.

> Note: Currently only the first 100 artworks from the dataset are put into the database as the process takes a lot of time. This can be modified by changing the `MAX_NUM` variable in `init_db.py`


## Running the webserver

1. Navigate into `Artbay/`

2. Start the webserver with: `flask run`

  

## Accessing the website

To access the website go to http://127.0.0.1:5000 with your webbrowser.

## Interacting with the webpage

This section will go through some of the features that the webpage has. 

### Creating a user
To create a user click on `Sign Up` on the top right corner. Fill out the presented formula with your new login information and press on the button labelled `Sign Up`.

### Purchasing an art listing
To purchase an art listing you will need to be logged in as a user. On the navigation bar click on the button labelled `All Art`. Next click on the green button labelled `Buy`, which is placed after the information pertaining to an art piece. You will be redirected to a confirmation page where you can confirm your purchase by clicking on `Yes, buy it`. All purchases by the currently logged in user can always be accessed by going to `Your Orders`.

### Creating an art listing
To create an art listing you will need to be logged in as a user. To create your first art listin, click on the `Create Stall` button on the navbar and confirm by clicking on the green `Create Stall` button. Fill in the information pertaining to the art piece that you would like to sell. An image can be added to the art listing by providing a url to the image. Lastly, click on the `Add Art` button. Subsequent art listings can be added by going to `Àdd Art`. All art pieces by the currently logged in user can always be accessed by going to `Your Art`.

### Known issues
When first creating a stall, the user is taken directly to the `Add Art` page. However, the navbar tab for `Create Stall` isn't replaced by the ones for `Add Art` and `Your Art` until after the next refresh or page jump. This is not an actual issue, since returning to `Create Stall` won't introduce any errors, and there is no reason to go to `Your Art` before having added any. Nonetheless, it is at the very least a known annoyance.
