RapidosKitchen is a Python-based Telegram bot that helps users discover and manage recipes tailored to their available ingredients. It integrates with the Spoonacular API to provide features such as recipe suggestions, nutritional information, and a personalized cooking experience.

# Features
Ingredient-Based Recipe Search: Enter available ingredients, and the bot suggests recipes that match, ranked by the number of missing ingredients.
Nutritional Information: Retrieve detailed nutritional facts for any recipe with a simple command.
Sorted Recipe Suggestions: Recipes are displayed in order of how closely they match the user’s provided ingredients, making it easy to choose what to cook.
Interactive Commands: Designed for seamless interaction through Telegram commands like /nutrition and /findrecipes.
Extensible Design: Built with Python and the pyTelegramBotAPI library, making it modular and easy to enhance.

# Why Use RapidosKitchen?
RapidosKitchen is perfect for home cooks looking to maximize their pantry, reduce food waste, and discover new dishes.

# Tech Stack
Language: Python
Libraries:pyTelegramBotAPI, Requests
API: Spoonacular API

# Future Features
Generate a grocery list for recipes.
Allow users to save favorite recipes.
Recipe filtering (e.g., by cuisine or dietary preferences).

## Deployment Instructions

To deploy this Recipe Bot, follow these steps:

### 1. Set Up Environment Variables:
- Create an API key through Teleram Bot Father.
- Add the following line to store your **Telegram API key* in the code:
  ```plaintext
  TELEGRAM_API_KEY=your_telegram_api_key_here
  ```

### 2. Install Dependencies:
- Install the required Python packages:
  ```bash
  pip install -r requirements.txt
  ```

### 3. Run the Bot Locally:
- Start the bot by running the script:
  ```bash
  python app.py
  ```
- The bot will start polling and will respond to user messages in the Telegram app.
