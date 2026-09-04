<div align="center">

🎨 STYLOMERA

✨ Transform Images. Create Art. Powered by AI. ✨

An AI-powered Neural Style Transfer web application built with PyTorch, AdaIN, Flask & Supabase.

<p>
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/PyTorch-Deep%20Learning-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white" alt="PyTorch">
  <img src="https://img.shields.io/badge/Flask-Backend-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/Supabase-Database%20%26%20Auth-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white" alt="Supabase">
</p>

<p>
  <b>Computer Vision</b> • <b>Neural Style Transfer</b> • <b>Adaptive Instance Normalization</b> • <b>Deep Learning</b>
</p>

</div>

🌌 What is Stylomera?

Stylomera is a web-based Neural Style Transfer application that uses deep learning to transform the visual appearance of a content image using the artistic characteristics of a style image.

Simply choose:

🖼️ Content Image + 🎨 Style Image
             ↓
        🧠 AI Processing
             ↓
      ✨ Stylized Artwork

Behind the scenes, Stylomera uses VGG-19 feature extraction, Adaptive Instance Normalization (AdaIN), and a trained decoder network to generate the final artwork.

✨ Features

Feature

Description

🖼️ Content Image

Upload the image whose structure you want to preserve

🎨 Style Image

Upload the artwork whose visual style you want to apply

🧠 AI Style Transfer

Generate stylized images using AdaIN

🎚️ Style Strength

Control how strongly the style is applied

⚡ PyTorch Inference

Fast neural-network based image generation

🔐 Authentication

Secure user authentication with Supabase

✉️ Email OTP

Email verification through OTP

☁️ Cloud Storage

Store generated images using Supabase Storage

🗂️ My Creations

View previously generated artworks

📥 Download

Save generated artwork locally

📱 Responsive UI

Designed for desktop and mobile screens

🧠 How Stylomera Works

Stylomera follows the AdaIN Neural Style Transfer pipeline.

                         ┌──────────────────────┐
                         │     Content Image    │
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
                         ┌──────────┴──────────┐
                         │     Style Image    │
                         └─────────────────────┘

                                    │
                                    ▼
                           ┌────────────────┐
                           │ Trained Decoder │
                           └───────┬────────┘
                                   │
                                   ▼
                          ✨ Stylized Artwork ✨

🔹 1. VGG-19 Encoder

The VGG-19 network extracts meaningful visual features from both images.

🔹 2. Adaptive Instance Normalization

AdaIN aligns the statistical properties of the content features with the style features.

In simple terms:

The content provides the structure, while the style provides the appearance.

🔹 3. Trained Decoder

The transformed feature representation is passed through the trained decoder to reconstruct the final RGB image.

🔹 4. Alpha Blending

The style strength can be controlled using the alpha parameter.

α = 0     → Original content
α = 1     → Full stylization
0 < α < 1 → Partial stylization

🛠️ Technology Stack

🤖 Artificial Intelligence

PyTorch

Torchvision

VGG-19

Adaptive Instance Normalization (AdaIN)

Convolutional Neural Networks

⚙️ Backend

Python

Flask

Flask-WTF

Pillow

☁️ Backend Services

Supabase Authentication

Supabase PostgreSQL

Supabase Storage

🎨 Frontend

HTML

CSS

JavaScript

Bootstrap

📁 Project Architecture

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

🚀 Getting Started

1️⃣ Clone the Repository

git clone https://github.com/Dhruv05-hue/stylomera-neural-style-transfer.git
cd stylomera

2️⃣ Create a Virtual Environment

python -m venv venv

Windows

venv\Scripts\activate

3️⃣ Install Dependencies

pip install -r requirements.txt

4️⃣ Configure Environment Variables

Create a .env file in the project root.

Use .env.example as your template:

SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_publishable_key
SUPABASE_SECRET_KEY=your_supabase_secret_key

SECRET_KEY=your_flask_secret_key

SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_EMAIL=your_email@gmail.com
SMTP_PASSWORD=your_gmail_app_password

🔒 Important: Never commit your real .env file or expose your Supabase secret key, SMTP password, or other credentials.

▶️ Run Stylomera

Activate the virtual environment and run:

python app.py

Then open:

http://127.0.0.1:5000

🎉 Stylomera is ready!

🗄️ Supabase Architecture

Stylomera uses Supabase for authentication, database storage, and image storage.

👤 profiles

Stores user profile information.

🎨 generations

Stores information about generated artworks:

User ID
Content Image Path
Style Image Path
Generated Image Path
Alpha
Created At

☁️ Storage

Images are stored in the private:

styleforge-images

bucket.

The logical structure is:

styleforge-images/
│
└── USER_ID/
    ├── content/
    ├── style/
    └── generated/

🧠 Required Model Files

Stylomera requires the following trained/pretrained model files:

vgg_normalised.pth
experiment/trained_decoder/decoder_final.pth

These files are required for Neural Style Transfer inference.

🎯 User Journey

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

🖼️ Examples

Place your best generated results inside the examples/ directory.

You can showcase:

🎨 Different artistic styles

🏙️ Landscape transformations

🧑 Portrait transformations

🌌 Abstract styles

🖌️ Painting-inspired results

💡 Tip: A few high-quality examples make the GitHub repository much more attractive than uploading a large number of random outputs.

📚 What This Project Demonstrates

Stylomera combines multiple areas of software engineering and AI:

             Stylomera
                 │
       ┌─────────┼─────────┐
       ▼         ▼         ▼
  Computer     Deep      Web
   Vision     Learning   Development
       │         │         │
       ▼         ▼         ▼
     VGG-19    PyTorch    Flask
       │         │         │
       └──────┬──┴─────────┘
              ▼
             AdaIN
              │
              ▼
       Neural Style Transfer

Core concepts

🧠 Convolutional Neural Networks

🔍 Feature Extraction

🎨 Neural Style Transfer

📊 Feature Statistics

🔄 Adaptive Instance Normalization

🖥️ Deep Learning Inference

🌐 Flask Web Applications

🔐 Authentication

☁️ Cloud Storage

🔮 Future Improvements

Some possible future enhancements:

🎚️ Live style-strength preview

🎨 Multiple-style blending

🖼️ Batch style transfer

🔍 Higher-resolution generation

⚡ Faster inference

🧠 Additional style-transfer models

☁️ GPU-enabled cloud deployment

📱 Further mobile optimization

⭐ Why Stylomera?

Stylomera is more than an image filter.

It demonstrates how a deep learning model can be integrated into a complete production-style web application, combining:

AI Model + Backend + Authentication + Database + Cloud Storage + User Interface

👨‍💻 Author

<div align="center">

Dhruv Pawar

AI / ML • Computer Vision • Deep Learning

Built with 🧠 PyTorch and ❤️ curiosity.

</div>

<div align="center">

⭐ If you like Stylomera, consider starring the repository!

Made with Python • PyTorch • Flask • Supabase

</div>