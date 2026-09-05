<div align="center">

# 🎨 STYLOMERA

### ✨ Transform Images. Create Art. Powered by AI. ✨

**An AI-powered Neural Style Transfer web application built with PyTorch, AdaIN, Flask, Hugging Face ZeroGPU & Supabase.**

<br>

<img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/PyTorch-Deep%20Learning-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white" alt="PyTorch">
<img src="https://img.shields.io/badge/Flask-Backend-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
<img src="https://img.shields.io/badge/Hugging%20Face-ZeroGPU-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black" alt="Hugging Face">
<img src="https://img.shields.io/badge/Supabase-Database%20%26%20Auth-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white" alt="Supabase">

<br><br>

**Computer Vision** • **Neural Style Transfer** • **AdaIN** • **Deep Learning** • **GPU Inference**

</div>

---

# 🌌 What is Stylomera?

**Stylomera** is a web-based **Neural Style Transfer** application that uses deep learning to transform the visual appearance of a content image using the artistic characteristics of a style image.

The concept is simple:

- 🖼️ Choose a **Content Image** whose structure you want to preserve.
- 🎨 Choose a **Style Image** whose artistic appearance you want to apply.
- 🎚️ Adjust the desired **Style Strength**.
- 🧠 Let the Neural Style Transfer pipeline process the images.
- ✨ Receive a new stylized artwork.

**Content Image + Style Image → AI Processing → Stylized Artwork**

Behind the scenes, Stylomera combines:

- 🧠 VGG-19 feature extraction
- 🔄 Adaptive Instance Normalization (AdaIN)
- 🧩 A trained decoder network
- 🔥 PyTorch deep learning inference
- ⚡ Hugging Face ZeroGPU for GPU-assisted inference
- ☁️ Supabase for authentication, database and storage

---

# ✨ Features

- 🖼️ **Content Image Upload**
  - Upload the image whose structure you want to preserve.

- 🎨 **Style Image Upload**
  - Upload the artwork whose visual style you want to apply.

- 🧠 **AI Neural Style Transfer**
  - Generate artistic transformations using the AdaIN approach.

- 🎚️ **Adjustable Style Strength**
  - Control how strongly the artistic style is applied.

- ⚡ **GPU-Assisted Inference**
  - Run computationally intensive NST inference using Hugging Face ZeroGPU.

- 🔐 **User Authentication**
  - Secure user authentication using Supabase.

- ✉️ **Email OTP Verification**
  - Verify user accounts through email-based OTP verification.

- ☁️ **Cloud Storage**
  - Store generated artworks using Supabase Storage.

- 🗂️ **My Creations**
  - View previously generated artworks associated with your account.

- 📥 **Download Generated Artwork**
  - Download generated images locally.

- 📱 **Responsive UI**
  - Designed for desktop and mobile screens.

---

# 🧠 How Stylomera Works

Stylomera follows the **Adaptive Instance Normalization (AdaIN)** Neural Style Transfer pipeline.

## 🔹 1. VGG-19 Feature Extraction

VGG-19 is used as a feature extractor for both images.

- 🖼️ Content features capture the structural information of the content image.
- 🎨 Style features capture the visual characteristics of the style image.

## 🔹 2. Adaptive Instance Normalization

AdaIN transfers the statistical characteristics of the style features into the content features.

In simple terms:

> 🖼️ **Content provides the structure.**

> 🎨 **Style provides the appearance.**

AdaIN aligns the channel-wise mean and variance of the content features with those of the style features.

## 🔹 3. Trained Decoder

The transformed feature representation is passed through a trained decoder.

The decoder reconstructs the transformed representation into the final RGB image.

## 🔹 4. Alpha Blending

The style intensity is controlled using an **alpha parameter**.

- `α = 0` → Original content
- `α = 1` → Full stylization
- `0 < α < 1` → Partial stylization

This allows users to create anything from a subtle style effect to a strong artistic transformation.

---

# 🏗️ Deployment Architecture

Stylomera contains two deployment approaches.

## 🖥️ V1 — CPU-Based Inference

The original implementation performs Neural Style Transfer directly inside the Flask application.

**Flow:**

**User → Flask / Render → PyTorch CPU → VGG-19 → AdaIN → Decoder → Generated Image**

This approach worked locally, but Neural Style Transfer is computationally expensive for a small CPU-based web-service instance.

### ⚠️ The Problem

The web server was responsible for both:

- 🌐 Running the web application
- 🧠 Performing computationally intensive deep learning inference

This created a CPU bottleneck during image generation.

---

# ⚡ V2 — GPU-Assisted Inference

The optimized implementation separates the web application from the GPU-intensive machine learning workload.

**Flow:**

**User Browser**

↓

**Render**

- Authentication
- Application logic
- Save generation

↓

**Hugging Face ZeroGPU**

- VGG-19
- AdaIN
- Trained Decoder
- GPU inference

↓

**Generated Image**

↓

**Render**

↓

**Supabase**

- Database
- Storage
- Generation history

### 🚀 Benefits of the New Architecture

- ⚡ GPU-intensive NST inference runs on Hugging Face ZeroGPU.
- 🌐 Render focuses on the web application.
- 🔐 Authentication remains part of the application layer.
- ☁️ Supabase handles persistent data and image storage.
- 🔀 Web and ML workloads are separated.
- 💰 The application does not need to simply scale CPU resources to handle NST inference.
- 📦 The ML inference service can be deployed independently.

---

# 🔄 CPU → GPU Optimization

One of the main engineering challenges in Stylomera was the computational cost of Neural Style Transfer.

### ❌ Before

**Render CPU**

↓

**PyTorch**

↓

**VGG-19**

↓

**AdaIN**

↓

**Decoder**

↓

**Generated Image**

### ✅ After

**Render**

- Application
- Authentication
- Application logic
- Persistence

↓

**Hugging Face ZeroGPU**

- VGG-19
- AdaIN
- Decoder
- GPU inference

↓

**Generated Image**

↓

**Supabase**

### 💡 Key Engineering Decision

Instead of simply increasing the resources of the web server, the architecture was redesigned to separate:

- 🌐 Application workload
- 🧠 Machine learning workload
- ☁️ Persistence workload

This makes the system more suitable for resource-constrained web deployments.

---

# 🛠️ Technology Stack

## 🤖 Artificial Intelligence

- 🔥 **PyTorch**
- 👁️ **Torchvision**
- 🧠 **VGG-19**
- 🔄 **Adaptive Instance Normalization (AdaIN)**
- 🧩 **Convolutional Neural Networks**
- 🎯 **Trained Decoder**

## ⚙️ Backend

- 🐍 **Python**
- 🌐 **Flask**
- 📝 **Flask-WTF**
- 🖼️ **Pillow**
- 🚀 **Gunicorn**

## ⚡ GPU Inference

- 🤗 **Hugging Face Spaces**
- ⚡ **Hugging Face ZeroGPU**
- 🔌 **Gradio Client**

## ☁️ Backend Services

- 🔐 **Supabase Authentication**
- 🗄️ **Supabase PostgreSQL**
- ☁️ **Supabase Storage**

## 🎨 Frontend

- HTML
- CSS
- JavaScript
- Bootstrap

---

# 📁 Project Architecture

    NST_Project/
    │
    ├── 📂 content_data/
    ├── 📂 style_data/
    ├── 📂 examples/
    │
    ├── 📂 experiment/
    │   ├── 📂 exp2/
    │   ├── 📂 exp3/
    │   ├── 📂 experiment1/
    │   ├── 📂 trial/
    │   │
    │   └── 📂 trained_decoder/
    │       ├── 🧠 decoder_final.pth
    │       ├── 📄 options.txt
    │       └── 🖼️ sample_iter_*.png
    │
    ├── 📂 static/
    │   └── 📂 uploads/
    │
    ├── 📂 templates/
    │   ├── 🎨 creations.html
    │   ├── 🏠 index.html
    │   ├── 🔐 login.html
    │   ├── 📝 signup.html
    │   ├── ✉️ verify_otp.html
    │   └── 🖼️ style_transfer.html
    │
    ├── 📂 utils/
    │   ├── 🧠 models.py
    │   └── 🔧 utils.py
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

# 🚀 Getting Started

## 1️⃣ Clone the Repository

    git clone https://github.com/Dhruv05-hue/stylomera-gpu-nst.git
    cd stylomera-gpu-nst

## 2️⃣ Create a Virtual Environment

    python -m venv venv

### Windows

    venv\Scripts\activate

## 3️⃣ Install Dependencies

    pip install -r requirements.txt

## 4️⃣ Configure Environment Variables

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

- ❌ `.env` files
- ❌ Supabase secret/service-role keys
- ❌ SMTP passwords
- ❌ Flask secret keys
- ❌ API keys
- ❌ Other private credentials

## 5️⃣ Run Stylomera

    python app.py

Then open:

    http://127.0.0.1:5000

🎉 **Stylomera is ready!**

---

# 🗄️ Supabase Architecture

Stylomera uses Supabase for:

- 🔐 User authentication
- 🗄️ PostgreSQL database
- ☁️ Image storage
- 🖼️ Generated artwork persistence

## 👤 `profiles`

The `profiles` table stores:

- User ID
- Username
- Email
- Account creation timestamp

## 🎨 `generations`

The `generations` table stores:

- User ID
- Content image path
- Style image path
- Generated image path
- Alpha/style strength
- Creation timestamp

## ☁️ Storage

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

# 🤗 Hugging Face GPU Inference

The GPU implementation uses a separate **Hugging Face Space** for Neural Style Transfer inference.

The browser sends:

- 🖼️ Content image
- 🎨 Style image
- 🎚️ Alpha value

to the Hugging Face Space.

The Space then:

1. Loads the VGG-19 encoder.
2. Extracts content and style features.
3. Performs Adaptive Instance Normalization.
4. Applies the selected style strength.
5. Passes the transformed features through the trained decoder.
6. Returns the generated image.

The web application does not need to perform the expensive NST calculation on its Render CPU instance.

The current ZeroGPU function uses a short maximum GPU duration because normal inference completes within a few seconds under typical conditions.

---

# 🧠 Required Model Files

Stylomera requires the following trained/pretrained model files:

- 🧠 `vgg_normalised.pth`
- 🧠 `experiment/trained_decoder/decoder_final.pth`

These files are required for Neural Style Transfer inference.

---

# 🎯 User Journey

**👤 Create Account**

↓

**✉️ Verify Email with OTP**

↓

**🔐 Sign In**

↓

**🖼️ Choose Content Image**

↓

**🎨 Choose Style Image**

↓

**🎚️ Adjust Style Strength**

↓

**🧠 Generate Artwork**

↓

**⚡ GPU Inference**

↓

**✨ View Result**

↓

**☁️ Save to Supabase**

↓

**🗂️ My Creations**

↓

**📥 Download**

---

# 🖼️ Examples

Place your best generated results inside the `examples/` directory.

Recommended examples include:

- 🎨 Different artistic styles
- 🏙️ Landscape transformations
- 🧑 Portrait transformations
- 🌌 Abstract styles
- 🖌️ Painting-inspired results

### 💡 Showcase Tip

A small collection of high-quality examples is more effective than a large collection of random outputs.

For a portfolio-oriented repository, consider showcasing:

- 🖼️ Original content image
- 🎨 Style image
- ✨ Final generated image
- 🎚️ Different alpha/style-strength results

---

# 📚 What This Project Demonstrates

Stylomera combines multiple areas of **Artificial Intelligence, Computer Vision, Backend Development and Cloud Deployment**.

## 🧠 Computer Vision & Deep Learning

- 👁️ Computer Vision
- 🧠 Convolutional Neural Networks
- 🔍 VGG-19 feature extraction
- 🎨 Neural Style Transfer
- 🔄 Adaptive Instance Normalization
- 📊 Feature statistics
- 🔥 PyTorch model inference
- 🧩 Trained neural network decoder

## 🌐 Web Development

- 🐍 Flask web application development
- 🎨 HTML/CSS frontend development
- 🌐 JavaScript client-side integration
- 📱 Responsive UI design
- 🔌 API integration

## 🔐 Authentication

- 🔐 Supabase authentication
- ✉️ Email OTP verification
- 👤 User sessions
- 🗂️ User-specific data management

## ☁️ Cloud & Deployment

- 🤗 Hugging Face Spaces
- ⚡ Hugging Face ZeroGPU
- 🚀 GPU-based ML inference
- ☁️ Render web deployment
- 🔀 Separation of application and ML workloads
- 📦 Cloud-based deployment architecture

## 🗄️ Database & Storage

- 🗄️ PostgreSQL
- ☁️ Supabase Storage
- 👤 User-specific image organization
- 🖼️ Generation history
- 💾 Cloud-based persistence

---

# 📊 Architecture at a Glance

| Layer | Technology | Responsibility |
| --- | --- | --- |
| 🎨 Frontend | HTML, CSS, JavaScript, Bootstrap | User interface |
| 🌐 Web Application | Flask | Application logic |
| 🔐 Authentication | Supabase Auth | User authentication |
| 🗄️ Database | PostgreSQL / Supabase | User and generation data |
| ☁️ Storage | Supabase Storage | Image persistence |
| 🧠 Feature Extraction | VGG-19 | Content/style features |
| 🔄 Style Transfer | AdaIN | Style transformation |
| 🧩 Reconstruction | Trained Decoder | Image generation |
| ⚡ GPU Inference | Hugging Face ZeroGPU | Accelerated NST |
| 🚀 Deployment | Render + Hugging Face | Cloud hosting |

---

# 🔥 Key Engineering Challenge

## The Problem

Neural Style Transfer is computationally intensive because the inference pipeline performs:

- 🧠 VGG-19 feature extraction
- 📊 Feature transformation
- 🔄 Adaptive Instance Normalization
- 🧩 Decoder inference
- 🖼️ Image processing

Running the complete pipeline directly on a small CPU-based web server creates a significant computational bottleneck.

## The Solution

Instead of simply scaling the CPU infrastructure, Stylomera separates:

- 🌐 Application Layer
- 🧠 ML Inference Layer
- ☁️ Persistence Layer

The resulting architecture is:

**Render → Hugging Face ZeroGPU → Generated Image → Supabase**

This allows each component to focus on its primary responsibility.

---

# 💡 Engineering Takeaway

The main optimization in Stylomera is not simply using a faster machine.

It is an example of **workload separation**.

Instead of forcing one server to perform every task:

- 🌐 Render handles the web application.
- 🔐 Render handles authentication and application logic.
- ⚡ Hugging Face ZeroGPU handles GPU-intensive NST inference.
- ☁️ Supabase handles database and image storage.

This approach demonstrates how AI workloads can be integrated into web applications while keeping computationally intensive operations separate from the main application server.

---

# 🔮 Future Improvements

Potential future enhancements include:

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

# ⭐ Why Stylomera?

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

> **Identify the computational bottleneck, then redesign the architecture instead of simply increasing infrastructure resources.**

---

# 🏆 Project Highlight

## From CPU Bottleneck → GPU-Assisted AI Architecture

The most important engineering aspect of Stylomera is identifying the **CPU inference bottleneck** and redesigning the deployment architecture.

### Original Architecture

**Web Application + ML Inference on CPU**

### Optimized Architecture

**Web Application on Render + GPU Inference on Hugging Face ZeroGPU + Persistence on Supabase**

The optimized implementation separates:

- 🌐 Web application responsibilities
- 🧠 GPU-intensive machine learning inference
- ☁️ Persistent data and image storage

This demonstrates practical experience with:

- 🧠 Deep Learning
- 👁️ Computer Vision
- 🔥 PyTorch
- 🎨 Neural Style Transfer
- 🔄 AdaIN
- 🌐 Flask
- 🤗 Hugging Face
- ⚡ GPU Inference
- ☁️ Supabase
- 🚀 Cloud Deployment
- 🏗️ AI System Architecture

---

# 👨‍💻 Author

<div align="center">

## Dhruv Pawar

**AI / ML • Computer Vision • Deep Learning**

Built with 🧠 **PyTorch** and ❤️ **curiosity**

<br>

<a href="https://github.com/Dhruv05-hue">
<img src="https://img.shields.io/badge/GitHub-Dhruv05--hue-181717?style=for-the-badge&logo=github" alt="GitHub">
</a>

</div>

---

<div align="center">

### ⭐ If you like Stylomera, consider starring the repository!

<br>

**Made with**

🐍 Python • 🔥 PyTorch • 🌐 Flask • 🤗 Hugging Face • ☁️ Supabase

<br><br>

### ✨ Transform Images. Create Art. Powered by AI. ✨

</div>