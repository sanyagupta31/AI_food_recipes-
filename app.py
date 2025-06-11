import streamlit as st
import google.generativeai as genai
import re
import datetime

# Configure Gemini API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

# Page settings
st.set_page_config(page_title="AI Food Recipe Generator", page_icon=":shallow_pan_of_food:", layout="wide")
st.title("AI Food Recipe Generator :shallow_pan_of_food:")

# Select options
cuisine = st.selectbox("Select Cuisine", ["Italian", "Mexican", "Indian", "Chinese", "American", "French", "Japanese", "Mediterranean"])
meal_type = st.selectbox("Select Meal Type", ["Breakfast", "Lunch", "Dinner", "Snack", "Dessert"])
dietary_restrictions = st.multiselect("Select Dietary Restrictions", ["Vegetarian", "Vegan", "Gluten-Free", "Dairy-Free", "Nut-Free", "Low-Carb", "Keto"])
ingredients = st.text_input("Enter Ingredients (comma separated)", "chicken, rice, vegetables")
cooking_time = st.slider("Select Cooking Time (minutes)", 0, 180, 30)
difficulty_level = st.selectbox("Select Difficulty Level", ["Easy", "Medium", "Hard"])
number_of_servings = st.number_input("Select Number of Servings", min_value=1, max_value=20, value=4)

# Generate Recipe
if st.button("Generate Recipe"):
    prompt = (
        f"Generate a {cuisine} {meal_type} recipe that is {', '.join(dietary_restrictions)} "
        f"with the following ingredients: {ingredients}. The recipe should take less than "
        f"{cooking_time} minutes to prepare, be {difficulty_level} level, and serve {number_of_servings} people."
    )
    response = model.generate_content(prompt)
    recipe = response.text.strip()

    # Format recipe: bold, line breaks, spacing
    recipe = re.sub(r'\n+', '\n', recipe)  # Normalize multiple newlines
    styled_recipe = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', recipe)  # Convert markdown bold to HTML
    styled_recipe = styled_recipe.replace('\n', '<br>')  # Convert newlines to HTML line breaks

    # Display beautifully styled recipe
    st.subheader("Generated Recipe")
    st.markdown(
        f"""
        <div style="
            background-color: #fff8f0;
            padding: 25px;
            border-radius: 12px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-size: 16px;
            line-height: 1.8;
            color: #333;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
        ">
            {styled_recipe}
        </div>
        """,
        unsafe_allow_html=True
    )

    # Timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.write(f"🕒 Recipe generated on: {timestamp}")

    # Download button
    st.download_button(
        label="📥 Download Recipe",
        data=recipe,
        file_name=f"{cuisine}_{meal_type}_recipe.txt",
        mime="text/plain"
    )

# Footer
st.markdown("""
---
Made with ❤️ by [Sanya](https://Aireceipe.com)
""")
