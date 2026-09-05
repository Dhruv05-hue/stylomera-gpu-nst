🎨 Stylomera — AI Neural Style Transfer

Stylomera is a web-based Neural Style Transfer application that combines the structure of a content image with the visual style of an artwork.

The project uses VGG-19 feature extraction, Adaptive Instance Normalization (AdaIN), and a trained decoder network to generate stylized images.

🚀 Architecture

The project has two implementations:

V1 — CPU-based inference

The original implementation performs Neural Style Transfer directly inside the Flask application.

User
 ↓
Flask / Render
 ↓
PyTorch CPU inference
 ↓
VGG-19 + AdaIN + Decoder
 ↓
Generated Image

This worked locally, but CPU-based inference was computationally expensive for a small web-service instance.

V2 — GPU-assisted inference

The optimized implementation separates the web application from the GPU-intensive inference workload.

User Browser
     │
     ├──────────────► Render
     │                │
     │                ├── Authentication
     │                ├── Application logic
     │                └── Save generation
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

This architecture allows the GPU-intensive NST inference to run on Hugging Face ZeroGPU while Render handles the web application and persistence layer.

✨ Features

🖼️ Content image upload

🎨 Style image upload

🧠 Neural Style Transfer using AdaIN

🎚️ Adjustable style strength

⚡ GPU-assisted inference through Hugging Face ZeroGPU

🔐 User authentication

✉️ Email OTP verification

☁️ Supabase PostgreSQL database

🗂️ Supabase Storage for generated images

🖼️ Personal My Creations gallery

📥 Generated image download

📱 Responsive web interface

🧠 How Neural Style Transfer Works

Stylomera uses the AdaIN approach.

1. Feature Extraction

VGG-19 extracts deep visual features from both the content and style images.

2. Adaptive Instance Normalization

AdaIN aligns the channel-wise mean and variance of the content features with those of the style features.

3. Alpha Blending

The transformed feature representation is blended with the original content representation using the selected style strength.

4. Decoding

A trained decoder converts the transformed feature representation back into an image.

🛠️ Tech Stack

Frontend

HTML

CSS

JavaScript

Bootstrap

Backend

Python

Flask

Flask-WTF

Gunicorn

Machine Learning

PyTorch

Torchvision

VGG-19

Adaptive Instance Normalization (AdaIN)

Convolutional Neural Networks

Trained Decoder

GPU Inference

Hugging Face Spaces

Hugging Face ZeroGPU

Gradio Client

Authentication & Persistence

Supabase Auth

Supabase PostgreSQL

Supabase Storage

📁 Project Structure

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

🚀 Local Setup

1. Clone the repository

git clone https://github.com/Dhruv05-hue/stylomera-gpu-nst.git
cd stylomera

2. Create a virtual environment

python -m venv venv

Windows:

venv\Scripts\activate

3. Install dependencies

pip install -r requirements.txt

4. Configure environment variables

Create a .env file in the project root.

Use .env.example as the template.

Required configuration includes:

SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_publishable_key
SUPABASE_SECRET_KEY=your_supabase_secret_key

SECRET_KEY=your_flask_secret_key

SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_EMAIL=your_email@gmail.com
SMTP_PASSWORD=your_gmail_app_password

Never commit real credentials or secret keys to GitHub.

5. Run the application

python app.py

Then open:

http://127.0.0.1:5000

☁️ Supabase Storage

The application stores user images in the styleforge-images bucket.

Files are organized by user ID:

styleforge-images/
└── USER_ID/
    ├── content/
    ├── style/
    └── generated/

The generations table stores the paths and metadata associated with each generated artwork.

🤗 Hugging Face GPU Inference

The GPU version uses a separate Hugging Face Space for Neural Style Transfer inference.

The browser sends the content image, style image, and alpha value to the Space. The Space performs inference on a GPU and returns the generated image.

The current ZeroGPU function is configured with a short maximum GPU duration because normal inference completes in approximately a few seconds.

The web application does not need to perform the expensive NST calculation on its Render CPU instance.

⚡ Optimization: CPU → GPU

One of the main engineering challenges in the project was the computational cost of running Neural Style Transfer on CPU-based web infrastructure.

Instead of simply increasing the server resources, the inference workload was separated from the web application.

Before

Render CPU
   ↓
PyTorch
   ↓
VGG-19
   ↓
AdaIN
   ↓
Decoder

After

Render
   ↓
Application + Authentication + Storage
   │
   └────────► Hugging Face ZeroGPU
                    ↓
              GPU inference
                    ↓
              Generated image

This separation makes the architecture more suitable for resource-constrained web deployments.

🎯 User Workflow

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

📊 What This Project Demonstrates

Computer Vision

Convolutional Neural Networks

VGG feature extraction

Adaptive Instance Normalization

PyTorch model inference

Deep learning model deployment

GPU inference integration

Flask backend development

JavaScript client-side API integration

Authentication and OTP verification

Supabase database and object storage

Separation of web and ML workloads

Performance-oriented cloud architecture

🔮 Future Improvements

Batch style transfer

Multiple style blending

Higher-resolution generation

More pretrained style-transfer models

Improved GPU resource management

Production-grade inference queueing

Dedicated GPU infrastructure for larger workloads

👨‍💻 Author

Dhruv Pawar

Built as a deep learning and computer vision project focused on Neural Style Transfer.

⭐ Project Highlight

The most important engineering aspect of Stylomera is not only implementing Neural Style Transfer, but also identifying the CPU inference bottleneck and redesigning the deployment architecture to use GPU-based inference while keeping the web application and persistent storage separate.