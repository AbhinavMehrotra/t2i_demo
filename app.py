import streamlit as st
from PIL import Image
import time
import requests  # For making API calls (if needed)
import io       # For handling image bytes
import numpy as np
import pandas as pd
import altair as alt
from threading import Thread


# st.set_page_config(layout="centered")
st.set_page_config(
    page_title="Demo",
    layout="wide")
# Inject CSS to st right/left padding
st.markdown("""
    <style>
        .block-container {
            padding-top: 1rem;
            padding-bottom: 0rem;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }
}
    </style>
""", unsafe_allow_html=True)

# --- Function to interact with the image generation model ---
# This is a placeholder. You'll need to replace this with your actual logic
def generate_image_from_text(prompt, model):
    if model == "flux_12b":
        time.sleep(5)
        # Dummy image (replace this with your actual image generation model output)
        img = Image.new("RGB", (1024, 1024), color="lightblue")
    else:
        time.sleep(1)
        # Dummy image (replace this with your actual image generation model output)
        img = Image.new("RGB", (1024, 1024), color="green")
    return img

# Sample data for stacked bar chart
data = pd.DataFrame({
    'Model': ['Flux 12B', 'Flux 12B', 'Flux 5B', 'Flux 5B', 'SD v3.5M', 'SD v3.5M', 'SD v3.5M Edit', 'SD v3.5M Edit'],
    'Component': ['X', 'Y', 'X', 'Y', 'X', 'Y', 'X', 'Y'],
    'Latency': [10, 15, 20, 5, 30, 10, 30, 10]
})

# Create stacked bar chart
chart = alt.Chart(data).mark_bar().encode(
    x=alt.X('Model:N', axis=alt.Axis(labelAngle=-45)),
    y='Latency:Q',
    color='Component:N'
).properties(
    width=500,
    height=400,
    title='Latency per inference'
)

# Function to create a gray placeholder image
def gray_placeholder_image(size=(1024, 1024)) -> Image.Image:
    return Image.new("RGB", size, color="gray")
def white_placeholder_image(size=(1024, 1024)) -> Image.Image:
    return Image.new("RGB", size, color="white")

# --- Streamlit UI ---
# st.title("Demo: LVM Foundation Model")

# Input
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.text("")
    # st.title("***LVM Demo***")
    st.markdown('<div style="text-align: center; font-size: 40px; font-style: italic; ">LVM Demo</div>', unsafe_allow_html=True)
with col2:
    prompt = st.text_area("", "", placeholder="Enter prompt", height=68)
with col3:
    st.image(white_placeholder_image(), caption="", width=25)
    generate_btn = st.button("Generate Image")

# Processing and status update fields
processing_spinner = st.empty()
status_update = st.empty()

# Image display placeholder
col1, col2, col3 = st.columns([2, 2, 2])
with col1:
    image_slot_flux_12b = st.empty()
    image_slot_sd35 = st.empty()
with col2:
    image_slot_flux_5b = st.empty()
    image_slot_sd35_edit = st.empty()
with col3:
    # Show chart
    st.image(white_placeholder_image(), caption="", width=150)
    st.altair_chart(chart, use_container_width=True)

# Show gray placeholder initially
placeholder_image = gray_placeholder_image()
image_slot_flux_12b.image(placeholder_image, caption="Flux 12B", width=300)
image_slot_flux_5b.image(placeholder_image, caption="Flux 5B", width=300)
image_slot_sd35.image(placeholder_image, caption="SD 3.5M", width=300)
image_slot_sd35_edit.image(placeholder_image, caption="SD 3.5M EDiT", width=300)




class DisplayImage(Thread):
    def __init__(self, prompt, model, st_img):
        super().__init__()
        self.prompt = prompt
        self.model = model
        self.st_img = st_img

    def run(self):
        img = generate_image_from_text(self.prompt, self.model)
        # st_img.image(img, caption=model, width=300)
        self.return_value = (img, self.model, self.st_img)


if generate_btn:
    # result_containers = []
    threads = []
    for model, st_img in zip(["flux_12b", "flux_5b"], [image_slot_flux_12b, image_slot_flux_5b]):
        print("model: ", model)
        # result_containers.append(st.container())
        threads.append(DisplayImage(prompt, model, st_img))

    for thread in threads:
        thread.start()
    thread_lives = [True] * len(threads)

    while any(thread_lives):
        for i, thread in enumerate(threads):
            if thread_lives[i] and not thread.is_alive():
                img, model, st_img = thread.return_value
                # with result_containers[i]:
                st_img.image(img, caption=model, width=300)
                # result_containers[i].write(thread.return_value)
                thread_lives[i] = False
        time.sleep(0.1)

    for thread in threads:
        thread.join()

    # if prompt:
    #     # Display a processing message
    #     with st.spinner("Generating image..."):
    #         image_slot_flux_12b.image(placeholder_image, caption="", width=250)
    #         image_slot_flux_5b.image(placeholder_image, caption="", width=250)
    #         try:
    #             generated_image_flux_12b = generate_image_from_text(prompt, "flux_12b")
    #             generated_image_flux_5b = generate_image_from_text(prompt, "flux_5b")
    #             status_update.success("Images generated successfully!")
    #             image_slot_flux_12b.image(generated_image_flux_12b, caption=f"Flux 12B", width=250)
    #             image_slot_flux_5b.image(generated_image_flux_5b, caption=f"Flux 5B", width=250)
    #         except requests.exceptions.RequestException as e:
    #             st.error(f"Error fetching placeholder image: {e}")
    #         except Exception as e:
    #             st.error(f"An error occurred during image generation: {e}")
    # else:
    #     st.warning("Please enter some text.")

