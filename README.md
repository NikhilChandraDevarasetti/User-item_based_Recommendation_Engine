# User-item_based_Recommendation_Engine
Building a movie recommendation engine based on movie and users

## Clone the Repo
git clone https://github.com/NikhilChandraDevarasetti/User-item_based_Recommendation_Engine.git

## Create vertual environment of your own
python -m venv ./venv/
.\venv\Scripts\activate
pip install -r requirements.txt

## Run the below command in your command line to see the results in your browser
python movie_recommendations.py

### Note:  Now that the api is up and running at port:5000(by default) or you can set the port of your choice in code

# Now run the get request url for seeing recommendations
http://127.0.0.1:5000/recommend-movie?q=Thor%20(2011)
