import telebot
import requests
import re

API_KEY = ''
SPOONACULAR_API_KEY = ''
bot = telebot.TeleBot(API_KEY)

user_state = {}

def get_recipes_by_ingredients(ingredients, preference):
    url = 'https://api.spoonacular.com/recipes/findByIngredients'
    params = {
        'ingredients': ingredients,
        'number': 5,
        'diet': preference, 
        'apiKey': SPOONACULAR_API_KEY
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        recipes = response.json()
        if isinstance(recipes, list):
            return recipes
        else:
            print("Unexpected response format:", recipes)
            return []
    else:
        print("API request failed with status code:", response.status_code)
        return []

def get_recipe_nutrition(recipe_id):
    url = f'https://api.spoonacular.com/recipes/{recipe_id}/information'
    params = {
        'apiKey':SPOONACULAR_API_KEY,
        'includeNutrition': True
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        recipe_data = response.json()
        nutrition = recipe_data.get('nutrition', {})
        nutrients = nutrition.get('nutrients', [])

        nutrition_info = ""
        for nutrient in nutrients:
            if nutrient['name'] in ['Calories', 'Fat', 'Protein', 'Carbohydrates']:
                nutrition_info += f"{nutrient['name']}: {nutrient['amount']} {nutrient['unit']}\n"

        return nutrition_info if nutrition_info else "No nutrition info available"
    else:
        return "Failed to fetch nutritional information."

# Function to escape special MarkdownV1 characters
def escape_markdown_v1(text):
    escape_chars = r"([\_\*\[\]\(\)\-\&])"
    return re.sub(escape_chars, r"\\\1", text)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello! I'm your Recipe Bot. You can ask me for recipes by typing /recipe")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Type /recipe followed by ingredients to get a recipe suggestion!")

@bot.message_handler(commands=['about'])
def about(message):
    bot.reply_to(message, "Rapido's kitchen helps you with finding a recipe when you can't figure out what to cook. I can send you a random recipe or tailor-make a recipe for you based on the ingredients at hand.")

@bot.message_handler(commands=['recipe'])
def handle_recipe(message):
    bot.send_message(message.chat.id, "Please enter ingredients separated by commas (e.g., chicken, rice, tomatoes)")
    user_state[message.chat.id] = 'waiting_for_ingredients'

@bot.message_handler(commands=['nutrition'])
def handle_nutrition(message):
    chat_id = message.chat.id
    # Extract the recipe ID from the message
    try:
        recipe_id = message.text.split()[1]  # Get the second part (after /nutrition)
        nutrition_info = get_recipe_nutrition(recipe_id)

        if nutrition_info:
            bot.send_message(chat_id, nutrition_info)
        else:
            bot.send_message(chat_id, "No nutrition information found.")
    except IndexError:
        bot.send_message(chat_id, "Please provide a valid recipe ID. Usage: /nutrition <recipe_id>")

@bot.message_handler(func=lambda m: True)
def handle_user_input(message):
    chat_id = message.chat.id
    
    if user_state.get(chat_id) == 'waiting_for_ingredients':
        ingredients = message.text
        user_state[chat_id] = {
            'step': 'waiting_for_preferences',
            'ingredients': ingredients
        }
        bot.send_message(chat_id, "Do you have any dietary preferences? (e.g., vegetarian, vegan, gluten-free)")
    
    elif user_state.get(chat_id) and user_state[chat_id]['step'] == 'waiting_for_preferences':
        dietary_preference = message.text.lower()
        ingredients = user_state[chat_id]['ingredients']
        recipes = get_recipes_by_ingredients(ingredients, dietary_preference)
        user_state.pop(chat_id, None)

        if recipes:
            response_text = "Here are some recipes you can make:\n"
            for recipe in recipes:
                recipe_title = recipe['title']
                recipe_id = recipe['id']
                
                # Escape special characters
                recipe_title_escaped = escape_markdown_v1(recipe_title)
                
                # Send plain text for the URL (no link, for debugging)
                recipe_url = f"https://spoonacular.com/recipes/{recipe_title.replace(' ', '-')}-{recipe_id}"

                response_text += f"{recipe_title_escaped} - ID: {recipe_id}\nURL: {recipe_url}\n\n"
            
            response_text += "Send /nutrition <recipe_id> to get nutritional information for a recipe."

            # Split message into chunks if it's too long
            if len(response_text) > 4096:
                chunks = [response_text[i:i+4096] for i in range(0, len(response_text), 4096)]
                for chunk in chunks:
                    bot.send_message(chat_id, chunk)
            else:
                bot.send_message(chat_id, response_text)  # No more parsing mode
        else:
            bot.send_message(chat_id, "No recipes found.")

bot.polling()
