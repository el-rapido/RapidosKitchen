import telebot
import requests

API_KEY = ''
SPOONACULAR_API_KEY = ''
bot = telebot.TeleBot(API_KEY)

def get_recipes_by_ingredients(ingredients):
    url = 'https://api.spoonacular.com/recipes/findByIngredients'
    params = {
        'ingredients': ingredients,
        'number': 5,
        'apiKey': SPOONACULAR_API_KEY
    }
    response = requests.get(url, params=params)
    

    #checking if there is an issue with the API Request
    if response.status_code == 200:
        recipes = response.json()

        #ensure that the API returns a list of recipes
        if isinstance(recipes, list):
            return recipes
        
        else:
            print("Unexpected response format:", recipes)
            return[]
        
    else:
        print("API request failed with status code:", response.status_code)
        return[]


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello! I'm your Recipe Bot. You can ask me for recipes by typing /recipe")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Type /recipe followed by ingredients to get a recipe suggestion!")

@bot.message_handler(commands=['about'])
def about(message):
    bot.reply_to(message, "Rapido's kitchen helps you with finding a recipe when you have can't figure out what to cook. I can send you a random recipe or tailor-make a recipe for you based on the ingredients at hand.")

@bot.message_handler(commands= ['recipe'])
def handle_recipe(message):
    bot.send_message(message.chat.id, "Please enter ingredients separated by commas (e.g., chicken, rice, tomatoes):")

    @bot.message_handler(func=lambda m: True) #Function to handle text messages
    def recipe_ingredients(message):
        ingredients = message.text
        recipes = get_recipes_by_ingredients(ingredients)

        if recipes:
            response_text = "Here are some recipes you could try out:\n"
            for recipe in recipes:
                response_text += f"{recipe['title']} - [link to recipe](https://spoonacular.com/recipes/{recipe['title'].replace(' ', '-')}-{recipe['id']})\n"
            bot.send_message(message.chat.id, response_text, parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, "No recipe found.")



bot.polling()
