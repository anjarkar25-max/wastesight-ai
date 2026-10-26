# ♻️ WasteSight AI

> **AI-powered computer vision edge-sorting system for real-time waste segregation.**  
> *Built for **Arbiter Hacks V1** — Theme Track: Rethinking Waste*

![Status](https://img.shields.io/badge/Status-In%20Development-eab308?style=flat-square)
![Track](https://img.shields.io/badge/Track-Rethinking%20Waste-22c55e?style=flat-square)
![AI](https://img.shields.io/badge/Model-YOLOv8%20%7C%20TFLite-3b82f6?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-purple?style=flat-square)

---

## 📖 Overview
**WasteSight AI** is a mobile computer vision application that eliminates guesswork at the trash bin. By pointing a smartphone camera at an item, users get instant, real-time detection telling them whether the item belongs in **Dry Recycling, Wet/Compost, E-Waste, or Landfill**—mapped directly to local municipal segregation rules.

---

## 🎯 The Problem & Impact Measurement *(Theme Track)*
**The Problem Targeted:**  
Household waste contamination and "wish-cycling" (tossing non-recyclable items into recycling bins hoping they can be recycled) ruin entire batches of recyclable materials at municipal sorting facilities. In rapidly growing urban areas, confusion over multi-category segregation (Dry, Wet, Domestic Hazardous, and E-Waste) leads to low compliance at the source.

**How We Measure Success:**  
1. **Model Performance:** Achieving >85% mean Average Precision (mAP@50) across common household waste classes and <100ms on-device inference latency.
2. **Real-World Impact:** Measuring the **Source Contamination Reduction Rate**—tracked via user scan logs and pre/post-app sorting accuracy tests where participants sort 20 mixed household items with and without WasteSight AI.

---

## ✨ Key Features
* **⚡ Real-Time Edge AI:** Runs a quantized YOLOv8 `.tflite` model directly on the device—no internet connection or cloud latency required.
* **🗺️ Localized Sorting Rules:** Maps detected items (e.g., multilayered plastic wrappers, PET bottles, organic scraps, batteries) to local municipal Dry/Wet/Hazardous bin standards.
* **📊 Personal Impact Tracker:** Logs scanned items to estimate the weight of waste properly diverted from landfills.
* **💡 Preparation Tips:** Tells users *how* to dispose of an item (e.g., *"Rinse plastic container and crush before placing in the Dry Bin"*).

---

## 🛠️ Tech Stack
* **Machine Learning:** Python, Ultralytics YOLOv8, PyTorch, OpenCV
* **Edge Deployment:** TensorFlow Lite (`.tflite`)
* **Dataset:** TACO (Trash Annotations in Context), TrashNet + Custom Local Packaging Dataset (Roboflow)
* **Frontend / Mobile:** Flutter / React Native *(in progress)*

---

## 🎥 Demo Video
* 📌 **[Link to 2–3 Minute YouTube/Vimeo Demo Video — Coming Soon]**

---

## 🗺️ Development Roadmap (8-Week Sprint)
- [x] **Phase 1:** Initialize public repository & project architecture
- [ ] **Phase 2:** Curate dataset (TACO + custom local waste images) on Roboflow
- [ ] **Phase 3:** Train & fine-tune YOLOv8 model on Google Colab
- [ ] **Phase 4:** Export model to `.tflite` for mobile edge inference
- [ ] **Phase 5:** Build mobile camera UI & municipal bin-mapping logic
- [ ] **Phase 6:** Field testing, UI polish & final demo video production

---

## 🚀 Getting Started

### Clone the Repository
```bash
git clone [https://github.com/anjarkar25-max/wastesight-ai.git](https://github.com/anjarkar25-max/wastesight-ai.git)
cd wastesight-ai
