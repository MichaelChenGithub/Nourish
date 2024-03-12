from langchain.tools import StructuredTool
from langchain.pydantic_v1 import BaseModel, Field
from langchain_community.utilities import GoogleSearchAPIWrapper
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain.tools.retriever import create_retriever_tool
from pymongo.mongo_client import MongoClient
import os
import requests

class NutritionTools:
    def __init__(self):
        self.headers = {
            "Content-Type": "application/json",
            "x-app-id": os.getenv("NUTRITIONNIX_APP_ID"),
            "x-app-key": os.getenv("NUTRITIONNIX_APP_KEY"),
            "API-key": "1"
        }
        self.db_uri = "mongodb+srv://michael:XtDdgICBBjQtEUuX@nourish.optsg9l.mongodb.net/?retryWrites=true&w=majority&appName=Nourish"
    # def search_meal_by_name(self, query):
    #     """
    #     Searches for meal information by name using TheMealDB API.
    #     """
    #     url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={query}"

    #     try:
    #         response = requests.get(url, headers={"API-key": self.headers["API-key"]})
    #         response.raise_for_status()
    #         return response.text
    #     except requests.exceptions.RequestException as e:
    #         return f"Error: {e}"

    def get_nutrition_with_nlp(self, query):
        """
        Retrieves nutritional information for foods using NLP from the Nutritionix API.
        """
        url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
        payload = {"query": query}

        try:
            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            saved_response = []
            for food in response.json()["foods"]:
                keys_to_remove = set(['full_nutrients', 'nix_brand_name', 'nix_brand_id', 'nix_item_name', 'nix_item_id', 'upc', 'consumed_at', 'source', 'ndb_no', 'lat', 'lng', 'meal_type', 'photo', 'sub_recipe', 'class_code', 'brick_code', 'tag_id'])
                saved_food_info = {key: value for key, value in food.items() if key not in keys_to_remove}
                saved_response.append(saved_food_info)
            return saved_response
        except requests.exceptions.RequestException as e:
            return f"Error: {e}"

    # def find_restaurant_food(self, query):
    #     """
    #     Searches for branded foods in the Nutritionix API based on the search query.
    #     """
    #     url = f"https://trackapi.nutritionix.com/v2/search/instant/?query={query}"

    #     try:
    #         response = requests.get(url, headers=self.headers)
    #         response.raise_for_status()
    #         branded_food = response.json()["branded"]
    #         saved_response = []
    #         for food in branded_food:
    #             keys_to_save = set(['food_name', 'brand_name_item_name', 'brand_name'])
    #             saved_food_info = {key: value for key, value in food.items() if key in keys_to_save}
    #             saved_response.append(saved_food_info)
    #         return saved_response
    #     except requests.exceptions.RequestException as e:
    #         return f"Error: {e}"
        
    def top_results(self, query):
        search = GoogleSearchAPIWrapper()
        return search.results(query, 3)
    
    def rag_knowledge(self):
        uri = self.db_uri
        # Create a new client and connect to the server
        client = MongoClient(uri)
        dbName = "nutri_knowledge"
        collectionName = "usaid_handbook"
        collection = client[dbName][collectionName]
        embeddings = OpenAIEmbeddings()
        vectorStore = MongoDBAtlasVectorSearch(collection, embeddings)
        retriever = vectorStore.as_retriever()
        return retriever
    
# class RecipeInput(BaseModel):
#     query: str = Field(description="food name")

class NutritionInput(BaseModel):
    query: str = Field(description="serving size and food name")

# class RestaurantInput(BaseModel):
#     query: str = Field(description="general food name")

class GoogleSearch(BaseModel):
    query: str = Field(description="search query")

def get_tools():
    nutrition_tools = NutritionTools()
    
    # recipe_tool = StructuredTool.from_function(
    #     func=nutrition_tools.search_meal_by_name,
    #     name="search_meal_by_name",
    #     description="Fetch recipes and cusine ingredient and steps",
    #     args_schema=RecipeInput
    # )
    
    nutrition_tool = StructuredTool.from_function(
        func=nutrition_tools.get_nutrition_with_nlp,
        name="get_nutrition_with_nlp",
        description="Fetch Food nutrition",
        args_schema=NutritionInput
    )
    
    # restaurant_food_tool = StructuredTool.from_function(
    #     func=nutrition_tools.find_restaurant_food,
    #     name="find_restaurant_food",
    #     description="Find restaurant food options",
    #     args_schema=RestaurantInput
    # )
    google_search_tool = StructuredTool.from_function(
        func=nutrition_tools.top_results,
        name="google_search",
        description="Search Google for related results",
        args_schema=GoogleSearch
    )
    

    retriever = nutrition_tools.rag_knowledge()

    rag_knowledge_tool = create_retriever_tool(
        retriever,
        "search_nutrition_knowledge",
        "Searches and returns nutrition knowledge.",
    )
    # tools = [recipe_tool, nutrition_tool, restaurant_food_tool, google_search_tool]
    tools = [nutrition_tool, google_search_tool, rag_knowledge_tool]
    return tools