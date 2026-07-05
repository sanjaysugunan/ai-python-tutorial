import streamlit as st
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Initialize the Gemini client
client = genai.Client()

def generate_recipe(ingredients, cuisine, diet):
    """Generate a recipe using the provided ingredients, cuisine, and diet preferences."""
    prompt = f'''
    Generate one food recipe using these ingredients: {','.join(ingredients)}
    Recipe should not be more than 100 words
    Cuisine: {cuisine}
    Diet: {diet}
    '''
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )
    return response.text

# Streamlit app
st.set_page_config(
    page_title="AI Recipe Generator",
    page_icon="🍳",
    layout="centered"
)

st.title("🍳 AI Recipe Generator")
st.markdown("Generate delicious recipes using your available ingredients!")

# Input form
with st.form("recipe_form"):
    st.subheader("What ingredients do you have?")
    
    # Multi-select for ingredients
    available_ingredients = [
        "Chicken", "Dal", "Onion", "Tomatoes", "Potatoes", "Rice", 
        "Pasta", "Eggs", "Milk", "Butter", "Masalas", "Garlic",
        "Ginger", "Carrots", "Beef", "Fish", "Paneer", "Cheese",
        "Yogurt", "Lentils", "Quinoa", "Bread", "Flour", "Sugar"
    ]
    
    selected_ingredients = st.multiselect(
        "Select your ingredients:",
        options=available_ingredients,
        default=["Chicken", "Tomatoes"]
    )
    
    # Custom ingredients
    custom_ingredients = st.text_input(
        "Add custom ingredients (comma separated):",
        placeholder="e.g., bell peppers, mushrooms"
    )
    
    # Cuisine selection
    cuisine = st.selectbox(
        "Select Cuisine:",
        options=["Indian", "Italian", "Mexican", "Chinese", "Thai", "American", "Mediterranean", "Any"]
    )
    
    # Diet selection
    diet = st.selectbox(
        "Select Diet Preference:",
        options=["Non-veg", "Vegetarian", "Vegan", "Gluten-free", "Any"]
    )
    
    submit_button = st.form_submit_button("Generate Recipe 🚀")

# Process and display results
if submit_button:
    # Combine selected and custom ingredients
    all_ingredients = list(selected_ingredients)
    if custom_ingredients:
        all_ingredients.extend([ing.strip() for ing in custom_ingredients.split(",") if ing.strip()])
    
    if not all_ingredients:
        st.error("Please select or enter at least one ingredient!")
    else:
        with st.spinner("Generating your recipe..."):
            try:
                recipe = generate_recipe(all_ingredients, cuisine, diet)
                st.success("Here's your recipe!")
                st.markdown(f"**Ingredients used:** {', '.join(all_ingredients)}")
                st.markdown("---")
                st.markdown(recipe)
            except Exception as e:
                st.error(f"Error generating recipe: {str(e)}")