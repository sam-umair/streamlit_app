import streamlit as st
from PIL import Image

# Set page title and theme configuration
st.set_page_config(page_title="Lighting & Electrical Products", layout="wide")

# Custom CSS for full-page styling with background image
def load_css():
    st.markdown(
        """
        <style>
            body {
                background: yellow;
                background-size: cover;
                color: black;
                font-family: Arial, sans-serif;
            }
            .stApp {
                background: rgba(255, 255, 255, 0.9);  /* Updated for better visibility */
                padding: 20px;
                border-radius: 10px;
            }
            .stButton>button {
                background-color: #1E90FF;
                color: green;
                border-radius: 5px;
                padding: 10px;
                transition: 0.3s;
            }
            .stButton>button:hover {
                background-color: #0073E6;
            }
            .stTextInput>div>div>input {
                background-color: #FFFFFF;  /* Updated for better visibility */
                color: purple;
                border-radius: 5px;
                padding: 8px;
            }
            .stSidebar {
                color: yellow;  /* Fixed spelling from 'colour' to 'color' */
                background-color: green;
                padding: 20px;
            }
            .stMarkdown {
                color: black;
            }
            h1 {
                color: #FFA500;
                font-weight: bold;
            }
            h2 {
                color: #00FF00;
                font-weight: bold;
            }
            h3 {
                color: #00CED1;
                font-weight: bold;
            }
            .product-card {
                background: rgba(255, 255, 255, 0.1);
                padding: 15px;
                border-radius: 10px;
                margin-bottom: 20px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

load_css()

# Title and description
st.title("🌟 Lighting & Electrical Products")
st.write("Explore our range of energy-efficient lighting solutions and electrical accessories.")
st.write("We offer high-quality products at competitive prices.")
st.write("Order now and get your products delivered to your doorstep!")
st.write("🚚🏡")

# Product details
products = [
    {"name": "💡 LED Bulb 12W", "image": "LED_13W.jpg"},
    {"name": "🔦 SMD Downlight 7W", "image": "SMD_downlight.jpg"},
    {"name": "🔦 SMD Downlight 12W", "image": "SMDDOWN.jpg"},
    {"name": "💡 LED Bulb 20W", "image": "LED bulb.jpg"},
    {"name": "🚀 Flood Lights (On Demand)", "image": "FloodLight.jpg"},
    {"name": "⚡ Energy Savers", "image": "energysaver.jpg"},
    {"name": "🔌 Breakers & Switches", "image": "breaker.jpg"},
]

# Sidebar for customer order
st.sidebar.header("🛒 Place Your Order")
selected_product = st.sidebar.selectbox("Select a product", [product["name"] for product in products])
quantity = st.sidebar.number_input("Enter quantity", min_value=1, step=1)
order_button = st.sidebar.button("🛍 Order Now")

if order_button:
    st.sidebar.success(f"✅ You have ordered {quantity} x {selected_product}. Thank you!")

# Display products
for product in products:
    with st.container():
        col1, col2 = st.columns([1, 3])
        with col1:
            try:
                image = Image.open(product["image"])
                st.image(image, use_container_width=True)
            except FileNotFoundError:
                st.write("[Image not available]")
        with col2:
            st.subheader(product["name"])
            st.write("High-quality and energy-efficient lighting solutions for your needs.")
    st.markdown("---")

# Footer
st.write("📩 For inquiries and bulk orders, visit us at: AR_Universal service station, Lahore road, Saddar Lahore Cantt.")
st.write("📞 Contact us at: +92-333-2193606")
