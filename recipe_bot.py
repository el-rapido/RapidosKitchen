import telebot
import requests

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

# Welcoming message when bot is initialised
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello! I'm your Recipe Bot. You can ask me for recipes by typing /recipe")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Type /recipe followed by ingredients to get a recipe suggestion!")

@bot.message_handler(commands=['about'])
def about(message):
    bot.reply_to(message, "Rapido's kitchen helps you with finding a recipe when you have can't figure out what to cook. I can send you a random recipe or tailor-make a recipe for you based on the ingredients at hand.")

# Asking for user's ingredients
@bot.message_handler(commands=['recipe'])
def handle_recipe(message):
    bot.send_message(message.chat.id, "Please enter ingredients separated by commas (e.g., chicken, rice, tomatoes)")
    
    # Set the user state to 'waiting_for_ingredients'
    user_state[message.chat.id] = 'waiting_for_ingredients'

# Step 2: Handle user input based on their state
@bot.message_handler(func=lambda m: True)
def handle_user_input(message):
    chat_id = message.chat.id
    
    # Step 2.1: If the bot is waiting for ingredients, ask for dietary preferences
    if user_state.get(chat_id) == 'waiting_for_ingredients':
        ingredients = message.text
        
        # Store ingredients in user state
        user_state[chat_id] = {
            'step': 'waiting_for_preferences',
            'ingredients': ingredients
        }
        
        bot.send_message(chat_id, "Do you have any dietary preferences? (e.g., vegetarian, vegan, gluten-free)")
    
    # Step 2.2: If the bot is waiting for dietary preferences, fetch and send recipes
    elif user_state.get(chat_id) and user_state[chat_id]['step'] == 'waiting_for_preferences':
        dietary_preference = message.text.lower()
        
        # Get the stored ingredients from the user's state
        ingredients = user_state[chat_id]['ingredients']
        
        # Fetch recipes
        recipes = get_recipes_by_ingredients(ingredients, dietary_preference)
        
        # Reset user state after getting preferences
        user_state.pop(chat_id, None)
        
        # Send recipe results
        if recipes:
            response_text = "Here are some recipes you can make:\n"
            for recipe in recipes:
                response_text += f"{recipe['title']} - [Link to Recipe](https://spoonacular.com/recipes/{recipe['title'].replace(' ', '-')}-{recipe['id']})\n"
            bot.send_message(chat_id, response_text, parse_mode='Markdown')
        else:
            bot.send_message(chat_id, "No recipes found.")

# Start polling to keep the bot running
bot.polling()
