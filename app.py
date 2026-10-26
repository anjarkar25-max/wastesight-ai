import streamlit as st
from ultralytics import YOLO
from PIL import Image
import numpy as np

st.set_page_config(page_title="WasteSight AI", page_icon="♻️", layout="centered")

st.title("♻️ WasteSight AI")
st.subheader("Real-Time Computer Vision Waste Segregation")
st.write("Scan an item with your camera or upload a photo to check which municipal bin it belongs in.")

# Map the 6 trained model classes to English names, municipal bins, and disposal tips
SORTING_RULES = {
    "plastik": {
        "name": "Plastic",
        "bin": "🟦 Dry Waste (Recyclable)",
        "tip": "Rinse off any food residue, remove the cap, and crush the bottle/container before placing it in the Dry Bin."
    },
    "metal": {
        "name": "Metal / Can",
        "bin": "🟦 Dry Waste (Recyclable)",
        "tip": "Empty all liquid, rinse briefly, and place in the Dry Recyclable bin. Ensure sharp edges are tucked in."
    },
    "cam": {
        "name": "Glass",
        "bin": "🟦 Dry Waste (Recyclable / Glass)",
        "tip": "Rinse clean. If broken, wrap securely in newspaper and label clearly before handing to waste collectors."
    },
    "kagit": {
        "name": "Paper",
        "bin": "🟦 Dry Waste (Recyclable)",
        "tip": "Keep clean and dry. Greasy or food-soiled paper (like used tissues) should go into Wet/Compost or Reject waste."
    },
    "karton": {
        "name": "Cardboard / Carton",
        "bin": "🟦 Dry Waste (Recyclable)",
        "tip": "Flatten the box completely to save space and remove any plastic tape or bubble wrap."
    },
    "kopuk": {
        "name": "Styrofoam / Thermocol",
        "bin": "🟥 Domestic Reject / Landfill Waste",
        "tip": "Styrofoam is not accepted in standard municipal recycling. Place in the Reject/Landfill bin and avoid mixing with Dry recyclables."
    }
}

@st.cache_resource
def load_model():
    return YOLO("best.pt")

model = load_model()

# Input tabs for live camera scan or image upload
tab1, tab2 = st.tabs(["📷 Scan with Camera", "📁 Upload Photo"])

with tab1:
    camera_img = st.camera_input("Point your camera at a waste item")

with tab2:
    uploaded_img = st.file_uploader("Upload an image of waste", type=["jpg", "jpeg", "png", "webp"])

input_file = camera_img if camera_img is not None else uploaded_img

if input_file is not None:
    image = Image.open(input_file).convert("RGB")
    img_array = np.array(image)

    with st.spinner("Analyzing material..."):
        results = model.predict(img_array, conf=0.25)
        annotated_img = results[0].plot()[:, :, ::-1]  # Convert BGR to RGB

    st.image(annotated_img, caption="WasteSight AI Detection", use_container_width=True)

    boxes = results[0].boxes
    if len(boxes) == 0:
        st.warning("No waste item detected clearly. Try moving closer or improving lighting.")
    else:
        st.success(f"Detected {len(boxes)} item(s)!")
        for box in boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0]) * 100
            raw_label = model.names[cls_id]
            rule = SORTING_RULES.get(raw_label, {
                "name": raw_label.capitalize(),
                "bin": "🟦 Dry Waste",
                "tip": "Check local municipal guidelines."
            })

            with st.container(border=True):
                st.markdown(f"### {rule['name']} ({conf:.1f}% confidence)")
                st.markdown(f"**Recommended Bin:** {rule['bin']}")
                st.info(f"**Preparation Tip:** {rule['tip']}")
