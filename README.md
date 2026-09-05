# 🎨 Stylomera — AI Neural Style Transfer

Stylomera is a web-based **Neural Style Transfer** application that combines the structure of a content image with the visual style of an artwork.

The project uses **VGG-19 feature extraction, Adaptive Instance Normalization (AdaIN), and a trained decoder network** to generate stylized images.

---

## 🚀 Architecture

The project has two implementations.

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

This implementation worked locally, but CPU-based inference was computationally expensive for a small web-service instance.

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
- 🌐 Flask to handle the web application
- 🔐 Render to handle authentication and application logic
- ☁️ Supabase to handle database and image storage
- 🔄 The browser to communicate directly with the Hugging Face inference Space

---

## ✨ Features

- 🖼️ Content image upload
- 🎨 Style image upload
- 🧠 Neural Style Transfer using AdaIN
- 🎚️ Adjustable style strength
- ⚡ GPU-assisted inference through Hugging Face ZeroGPU
- 🔐 User authentication
- ✉️ Email OTP verification
- ☁️ Supabase PostgreSQL database
- 🗂️ Supabase Storage for generated images
- 🖼️ Personal My Creations gallery
- 📥 Generated image download
- 📱 Responsive web interface

---

## 🧠 How Neural Style Transfer Works

Stylomera uses the **Adaptive Instance Normalization (AdaIN)** approach.

### 1. Feature Extraction

- VGG-19 extracts deep visual features from the content image.
- VGG-19 also extracts deep visual features from the style image.

### 2. Adaptive Instance Normalization

- AdaIN aligns the channel-wise mean and variance of the content features with the style features.
- This transfers the statistical properties of the style into the content representation.

### 3. Alpha Blending

- The transformed feature representation is blended with the original content representation.
- The selected alpha value controls the strength of the applied style.

### 4. Decoding

- A trained decoder converts the transformed feature representation back into an image.
- The resulting image contains the structure of the content image with the visual characteristics of the style image.

---

## 🛠️ Tech Stack

### Frontend

- HTML
- CSS
- JavaScript
- Bootstrap

### Backend

- Python
- Flask
- Flask-WTF
- Gunicorn

### Machine Learning

- PyTorch
- Torchvision
- VGG-19
- Adaptive Instance Normalization (AdaIN)
- Convolutional Neural Networks
- Trained Decoder

### GPU Inference

- Hugging Face Spaces
- Hugging Face ZeroGPU
- Gradio Client

### Authentication & Persistence

- Supabase Auth
- Supabase PostgreSQL
- Supabase Storage

---

## 📁 Project Structure

    NST_Project/
    │
    ├── content_data/
    ├── style_data/
    ├── examples/
    │
    ├── experiment/
    │   └── trained_decoder/
    │       ├── decoder_final.pth
    │       ├── options.txt
    │       └── sample_iter_*.png
    │
    ├── static/
    │   └── uploads/
    │
    ├── templates/
    │   ├── creations.html
    │   ├── index.html
    │   ├── login.html
    │   ├── signup.html
    │   ├── verify_otp.html
    │   └── style_transfer.html
    │
    ├── utils/
    │   ├── models.py
    │   └── utils.py
    │
    ├── app.py
    ├── supabase_client.py
    ├── train.py
    ├── vgg_normalised.pth
    ├── requirements.txt
    ├── .env.example
    └── .gitignore

---

## 🚀 Local Setup

### 1. Clone the Repository

    git clone https://github.com/Dhruv05-hue/stylomera-gpu-nst.git
    cd stylomera-gpu-nst

### 2. Create a Virtual Environment

    python -m venv venv

### Windows

    venv\Scripts\activate

### 3. Install Dependencies

    pip install -r requirements.txt

### 4. Configure Environment Variables

Create a `.env` file in the project root.

Use `.env.example` as the template.

Required configuration includes:

    SUPABASE_URL=your_supabase_project_url
    SUPABASE_KEY=your_supabase_publishable_key
    SUPABASE_SECRET_KEY=your_supabase_secret_key

    SECRET_KEY=your_flask_secret_key

    SMTP_SERVER=smtp.gmail.com
    SMTP_PORT=587
    SMTP_EMAIL=your_email@gmail.com
    SMTP_PASSWORD=your_gmail_app_password

> ⚠️ Never commit real credentials, API keys, passwords, or secret keys to GitHub.

### 5. Run the Application

    python app.py

Then open:

    http://127.0.0.1:5000

---

## ☁️ Supabase Storage

The application stores user images in the `styleforge-images` bucket.

Files are organized by user ID:

    styleforge-images/
    └── USER_ID/
        ├── content/
        ├── style/
        └── generated/

The `generations` table stores:

- User ID
- Content image path
- Style image path
- Generated image path
- Alpha/style strength
- Creation timestamp

---

## 🤗 Hugging Face GPU Inference

The GPU version uses a separate **Hugging Face Space** for Neural Style Transfer inference.

The browser sends:

- Content image
- Style image
- Alpha value

to the Hugging Face Space.

The Space then:

- Loads the VGG-19 encoder
- Extracts content and style features
- Performs Adaptive Instance Normalization
- Applies the selected style strength
- Runs the trained decoder
- Returns the generated image

The web application does not need to perform the expensive NST calculation on its Render CPU instance.

The current ZeroGPU function is configured with a short maximum GPU duration because normal inference completes in approximately a few seconds.

---

## ⚡ Optimization: CPU → GPU

One of the main engineering challenges in the project was the computational cost of running Neural Style Transfer on CPU-based web infrastructure.

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
- 🔀 The application and ML workloads were separated.
- 🌐 Render can focus on application responsibilities.
- ⚡ Hugging Face ZeroGPU can handle the GPU-intensive NST workload.

This separation makes the architecture more suitable for resource-constrained web deployments.

---

## 🎯 User Workflow

    Create Account
          ↓
    Verify Email with OTP
          ↓
    Sign In
          ↓
    Choose Content Image
          ↓
    Choose Style Image
          ↓
    Adjust Style Strength
          ↓
    Generate Artwork
          ↓
    GPU Inference
          ↓
    View Result
          ↓
    Save to Supabase
          ↓
    My Creations
          ↓
    Download

---

## 📊 What This Project Demonstrates

### Computer Vision & Deep Learning

- 👁️ Computer Vision
- 🧠 Convolutional Neural Networks
- 🔍 VGG feature extraction
- 🎨 Adaptive Instance Normalization
- 🔥 PyTorch model inference
- 🖼️ Neural Style Transfer
- ☁️ Deep learning model deployment

### Cloud & Deployment

- ⚡ GPU inference integration
- 🤗 Hugging Face Spaces
- 🚀 Hugging Face ZeroGPU
- ☁️ Cloud-based ML inference
- 🔀 Separation of web and ML workloads
- 📈 Performance-oriented cloud architecture

### Backend Development

- 🐍 Flask backend development
- 🔌 REST-style API endpoints
- 🌐 JavaScript client-side API integration
- 🔐 Authentication
- ✉️ Email OTP verification

### Database & Storage

- 🔐 Supabase authentication
- 🗄️ PostgreSQL database
- ☁️ Supabase Storage
- 👤 User-specific image storage
- 🖼️ Generation history

---

## 🔮 Future Improvements

- 🖼️ Batch style transfer
- 🎨 Multiple style blending
- 🔍 Higher-resolution generation
- 🧠 More pretrained style-transfer models
- ⚡ Improved GPU resource management
- 📦 Production-grade inference queueing
- 🚀 Dedicated GPU infrastructure for larger workloads

---

## 👨‍💻 Author

**Dhruv Pawar**

Built as a deep learning and computer vision project focused on Neural Style Transfer.

---

## ⭐ Project Highlight

The most important engineering aspect of Stylomera is not only implementing Neural Style Transfer, but also identifying the **CPU inference bottleneck** and redesigning the deployment architecture.

The optimized implementation separates:

- 🌐 Web application responsibilities
- 🧠 GPU-intensive ML inference
- ☁️ Persistent data and image storage

The final architecture uses:

- **Render** for the web application
- **Hugging Face ZeroGPU** for GPU-based Neural Style Transfer inference
- **Supabase** for authentication, database, and storage

This demonstrates how a computationally intensive deep learning workload can be separated from a web application to create a more efficient cloud deployment.