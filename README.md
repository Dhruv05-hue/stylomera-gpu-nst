<div align="center">

# 🎨 STYLOMERA

### ✨ Transform Images. Create Art. Powered by AI. ✨

An AI-powered **Neural Style Transfer** web application built with **PyTorch, AdaIN, Flask, Hugging Face ZeroGPU & Supabase**.

<p>
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/PyTorch-Deep%20Learning-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white" alt="PyTorch">
  <img src="https://img.shields.io/badge/Flask-Backend-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/Hugging%20Face-ZeroGPU-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black" alt="Hugging Face">
  <img src="https://img.shields.io/badge/Supabase-Database%20%26%20Auth-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white" alt="Supabase">
</p>

<p>
  <b>Computer Vision</b> • <b>Neural Style Transfer</b> • <b>Adaptive Instance Normalization</b> • <b>Deep Learning</b> • <b>GPU Inference</b>
</p>

</div>

---

## 🌌 What is Stylomera?

Stylomera is a web-based **Neural Style Transfer** application that uses deep learning to transform the visual appearance of a content image using the artistic characteristics of a style image.

Simply choose:

- 🖼️ **Content Image** — The image whose structure you want to preserve
- 🎨 **Style Image** — The artwork whose visual style you want to apply

The application then performs Neural Style Transfer and generates a stylized artwork.

    🖼️ Content Image + 🎨 Style Image
                    ↓
               🧠 AI Processing
                    ↓
            ✨ Stylized Artwork

Behind the scenes, Stylomera uses:

- 🧠 VGG-19 feature extraction
- 🔄 Adaptive Instance Normalization (AdaIN)
- 🧠 A trained decoder network
- 🔥 PyTorch-based deep learning inference
- ⚡ Hugging Face ZeroGPU for GPU-assisted inference

---

## ✨ Features

- 🖼️ **Content Image Upload**
  - Upload the image whose structure you want to preserve.

- 🎨 **Style Image Upload**
  - Upload the artwork whose visual style you want to apply.

- 🧠 **AI Neural Style Transfer**
  - Generate stylized images using the AdaIN approach.

- 🎚️ **Adjustable Style Strength**
  - Control how strongly the artistic style is applied.

- ⚡ **GPU-Assisted Inference**
  - Perform computationally intensive NST inference using Hugging Face ZeroGPU.

- 🔐 **User Authentication**
  - Secure user authentication using Supabase.

- ✉️ **Email OTP Verification**
  - Verify user accounts using email-based OTP verification.

- ☁️ **Cloud Storage**
  - Store generated images using Supabase Storage.

- 🗂️ **My Creations**
  - View previously generated artworks associated with the user's account.

- 📥 **Download Generated Artwork**
  - Download generated images locally.

- 📱 **Responsive UI**
  - Designed for desktop and mobile screens.

---

## 🧠 How Stylomera Works

Stylomera follows the **AdaIN Neural Style Transfer pipeline**.

    ┌──────────────────────┐
    │    Content Image     │
    └──────────┬───────────┘
               │
               ▼
        ┌───────────────┐
        │    VGG-19     │
        │    Encoder    │
        └───────┬───────┘
                │
                │ Content Features
                ▼
           ┌───────────┐
           │   AdaIN   │◄────────── Style Features
           └─────┬─────┘
                 ▲
                 │
         ┌───────┴───────┐
         │    VGG-19     │
         │    Encoder    │
         └───────┬───────┘
                 ▲
                 │
        ┌────────┴─────────┐
        │    Style Image   │
        └──────────────────┘

                 │
                 ▼
        ┌─────────────────┐
        │ Trained Decoder │
        └────────┬────────┘
                 │
                 ▼
        ✨ Stylized Artwork ✨

### 🔹 1. VGG-19 Encoder

The VGG-19 network extracts meaningful visual features from both the content and style images.

- Content features represent the structure of the content image.
- Style features represent the visual characteristics of the style image.

### 🔹 2. Adaptive Instance Normalization

AdaIN aligns the statistical properties of the content features with the style features.

In simple terms:

> **The content provides the structure, while the style provides the appearance.**

### 🔹 3. Trained Decoder

The transformed feature representation is passed through the trained decoder to reconstruct the final RGB image.

### 🔹 4. Alpha Blending

The style strength can be controlled using the alpha parameter.

    α = 0       → Original content
    α = 1       → Full stylization
    0 < α < 1   → Partial stylization

---

## 🏗️ Deployment Architecture

Stylomera has two deployment approaches.

### V1 — CPU-Based Inference

The original implementation performs Neural Style Transfer directly inside the Flask application.

    User
     ↓
    Flask / Render
     ↓
    PyTorch CPU Inference
     ↓
    VGG-19 + AdaIN + Decoder
     ↓
    Generated Image

Although this approach works, Neural Style Transfer is computationally expensive for a small CPU-based web-service instance.

### V2 — GPU-Assisted Inference

The optimized implementation separates the web application from the GPU-intensive inference workload.

    User Browser
         │
         ├──────────────► Render
         │                │
         │                ├── Authentication
         │                ├── Application Logic
         │                └── Save Generation
         │
         └──────────────► Hugging Face ZeroGPU
                           │
                           ├── VGG-19
                           ├── AdaIN
                           └── Decoder
                           │
                           ▼
                     Generated Image
                           │
                           ▼
                        Render
                           │
                           ▼
                       Supabase

This architecture allows:

- ⚡ GPU-intensive NST inference to run on Hugging Face ZeroGPU
- 🌐 Render to handle the web application
- 🔐 Render to handle authentication and application logic
- ☁️ Supabase to handle database and image storage
- 🔄 The browser to communicate directly with the Hugging Face inference Space

---

## ⚡ CPU → GPU Optimization

One of the main engineering challenges in Stylomera was the computational cost of running Neural Style Transfer on CPU-based web infrastructure.

Instead of simply increasing server resources, the inference workload was separated from the web application.

### Before — CPU-Based Architecture

    Render CPU
       ↓
    PyTorch
       ↓
    VGG-19
       ↓
    AdaIN
       ↓
    Decoder
       ↓
    Generated Image

### After — GPU-Assisted Architecture

    Render
       ↓
    Application + Authentication + Storage
       │
       └────────► Hugging Face ZeroGPU
                        ↓
                  GPU Inference
                        ↓
                  Generated Image
                        ↓
                      Render
                        ↓
                    Supabase

### Why This Optimization Was Used

- ⚙️ CPU-based NST inference was computationally expensive.
- 💻 Running deep learning inference on a small web-service instance was inefficient.
- 💰 Increasing server resources would increase deployment cost.
- 🚀 GPU inference is better suited for computationally intensive deep learning operations.
- 🔀 Application and ML workloads were separated.
- 🌐 Render can focus on application responsibilities.
- ⚡ Hugging Face ZeroGPU can handle the GPU-intensive NST workload.

This separation makes the architecture more suitable for resource-constrained web deployments.

---

## 🛠️ Technology Stack

### 🤖 Artificial Intelligence

- PyTorch
- Torchvision
- VGG-19
- Adaptive Instance Normalization (AdaIN)
- Convolutional Neural Networks
- Trained Decoder

### ⚙️ Backend

- Python
- Flask
- Flask-WTF
- Pillow
- Gunicorn

### ⚡ GPU Inference

- Hugging Face Spaces
- Hugging Face ZeroGPU
- Gradio Client

### ☁️ Backend Services

- Supabase Authentication
- Supabase PostgreSQL
- Supabase Storage

### 🎨 Frontend

- HTML
- CSS
- JavaScript
- Bootstrap

---

## 📁 Project Architecture

    NST_Project/
    │
    ├── 📂 content_data/
    ├── 📂 style_data/
    ├── 📂 examples/
    │
    ├── 📂 experiment/
    │   ├── exp2/
    │   ├── exp3/
    │   ├── experiment1/
    │   ├── trial/
    │   │
    │   └── 📂 trained_decoder/
    │       ├── decoder_final.pth
    │       ├── options.txt
    │       └── sample_iter_*.png
    │
    ├── 📂 static/
    │   └── 📂 uploads/
    │
    ├── 📂 templates/
    │   ├── creations.html
    │   ├── index.html
    │   ├── login.html
    │   ├── signup.html
    │   ├── verify_otp.html
    │   └── style_transfer.html
    │
    ├── 📂 utils/
    │   ├── models.py
    │   └── utils.py
    │
    ├── 🐍 app.py
    ├── 🔐 supabase_client.py
    ├── 🧠 train.py
    ├── 🧠 vgg_normalised.pth
    ├── 📦 requirements.txt
    ├── 🔧 .env.example
    ├── 🚫 .gitignore
    └── 📖 README.md

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository

    git clone https://github.com/Dhruv05-hue/stylomera-gpu-nst.git
    cd stylomera-gpu-nst

### 2️⃣ Create a Virtual Environment

    python -m venv venv

### Windows

    venv\Scripts\activate

### 3️⃣ Install Dependencies

    pip install -r requirements.txt

### 4️⃣ Configure Environment Variables

Create a `.env` file in the project root.

Use `.env.example` as your template.

Required configuration includes:

    SUPABASE_URL=your_supabase_project_url
    SUPABASE_KEY=your_supabase_publishable_key
    SUPABASE_SECRET_KEY=your_supabase_secret_key

    SECRET_KEY=your_flask_secret_key

    SMTP_SERVER=smtp.gmail.com
    SMTP_PORT=587
    SMTP_EMAIL=your_email@gmail.com
    SMTP_PASSWORD=your_gmail_app_password

### 🔒 Security

Never commit or expose:

- `.env` files
- Supabase secret/service-role keys
- SMTP passwords
- Flask secret keys
- Other private credentials

### ▶️ Run Stylomera

Activate the virtual environment and run:

    python app.py

Then open:

    http://127.0.0.1:5000

🎉 Stylomera is ready!

---

## 🗄️ Supabase Architecture

Stylomera uses Supabase for:

- 🔐 User authentication
- 🗄️ PostgreSQL database
- ☁️ Image storage
- 🖼️ Generated artwork persistence

### 👤 `profiles`

Stores user profile information, including:

- User ID
- Username
- Email
- Account creation timestamp

### 🎨 `generations`

Stores information about generated artworks:

- User ID
- Content image path
- Style image path
- Generated image path
- Alpha/style strength
- Creation timestamp

### ☁️ Storage

Images are stored in the:

**`styleforge-images`**

bucket.

The logical structure is:

    styleforge-images/
    │
    └── USER_ID/
        ├── content/
        ├── style/
        └── generated/

This organization keeps each user's images separated by their user ID.

---

## 🤗 Hugging Face GPU Inference

The GPU version uses a separate **Hugging Face Space** for Neural Style Transfer inference.

The browser sends the following inputs to the Space:

- 🖼️ Content image
- 🎨 Style image
- 🎚️ Alpha value

The Hugging Face Space then:

- Loads the VGG-19 encoder.
- Extracts content and style features.
- Performs Adaptive Instance Normalization.
- Applies the selected style strength.
- Passes the transformed features through the trained decoder.
- Returns the generated image.

The web application does not need to perform the expensive NST calculation on its Render CPU instance.

The current ZeroGPU function is configured with a short maximum GPU duration because normal inference completes in approximately a few seconds.

---

## 🧠 Required Model Files

Stylomera requires the following trained/pretrained model files:

- `vgg_normalised.pth`
- `experiment/trained_decoder/decoder_final.pth`

These files are required for Neural Style Transfer inference.

---

## 🎯 User Journey

    👤 Create Account
            │
            ▼
      ✉️ Verify OTP
            │
            ▼
        🔐 Sign In
            │
            ▼
    🖼️ Choose Content
            │
            ▼
     🎨 Choose Style
            │
            ▼
      🎚️ Set Strength
            │
            ▼
      🧠 Generate Art
            │
            ▼
     ✨ View Result
            │
            ▼
     🗂️ My Creations
            │
            ▼
        📥 Download

---

## 🖼️ Examples

Place your best generated results inside the `examples/` directory.

You can showcase:

- 🎨 Different artistic styles
- 🏙️ Landscape transformations
- 🧑 Portrait transformations
- 🌌 Abstract styles
- 🖌️ Painting-inspired results

> 💡 **Tip:** A few high-quality examples make the GitHub repository much more attractive than uploading a large number of random outputs.

---

## 📚 What This Project Demonstrates

Stylomera combines multiple areas of software engineering and Artificial Intelligence.

### 🧠 Computer Vision & Deep Learning

- 👁️ Computer Vision
- 🧠 Convolutional Neural Networks
- 🔍 VGG-19 feature extraction
- 🎨 Neural Style Transfer
- 🔄 Adaptive Instance Normalization
- 📊 Feature statistics
- 🔥 PyTorch model inference
- 🧠 Trained neural network decoder

### 🌐 Web Development

- 🐍 Flask web application development
- 🎨 HTML/CSS frontend development
- 🌐 JavaScript client-side integration
- 📱 Responsive UI design
- 🔌 API integration

### 🔐 Authentication

- 🔐 Supabase authentication
- ✉️ Email OTP verification
- 👤 User sessions
- 🗂️ User-specific data management

### ☁️ Cloud & Deployment

- 🤗 Hugging Face Spaces
- ⚡ Hugging Face ZeroGPU
- 🚀 GPU-based ML inference
- ☁️ Render web deployment
- 🔀 Separation of application and ML workloads
- 📦 Cloud-based deployment architecture

### 🗄️ Database & Storage

- 🗄️ PostgreSQL
- ☁️ Supabase Storage
- 👤 User-specific image organization
- 🖼️ Generation history
- 💾 Cloud-based persistence

---

## 🔮 Future Improvements

Some possible future enhancements include:

- 🎚️ Live style-strength preview
- 🎨 Multiple-style blending
- 🖼️ Batch style transfer
- 🔍 Higher-resolution generation
- ⚡ Faster inference
- 🧠 Additional style-transfer models
- 📦 Production-grade inference queueing
- ☁️ Dedicated GPU infrastructure for larger workloads
- 📱 Further mobile optimization

---

## ⭐ Why Stylomera?

Stylomera is more than an image filter.

It demonstrates how a deep learning model can be integrated into a complete web application by combining:

- 🧠 AI Model
- 🖥️ Backend
- 🎨 Frontend
- 🔐 Authentication
- 🗄️ Database
- ☁️ Cloud Storage
- ⚡ GPU Inference
- 🚀 Cloud Deployment

The project also demonstrates an important engineering concept:

> **Identifying a computational bottleneck and redesigning the architecture instead of simply increasing infrastructure resources.**

---

## 👨‍💻 Author

<div align="center">

### Dhruv Pawar

**AI / ML • Computer Vision • Deep Learning**

Built with 🧠 **PyTorch** and ❤️ **curiosity**.

</div>

---

<div align="center">

⭐ **If you like Stylomera, consider starring the repository!**

Made with Python • PyTorch • Flask • Hugging Face • Supabase

</div>