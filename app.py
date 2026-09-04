import os
import uuid
import secrets
import hashlib
import smtplib
from datetime import datetime, timedelta, timezone
from email.message import EmailMessage

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    send_from_directory,
    flash,
    session
)

from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
from wtforms import FileField, SubmitField, FloatField, HiddenField
from PIL import Image
from torchvision import transforms
import torch

from utils.models import VGGEncoder, Decoder
from utils.utils import adaptive_instance_normalization, calc_mean_std

# Supabase connection
from supabase_client import (
    supabase,
    supabase_admin,
    supabase_auth_request
)


app = Flask(__name__)


app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# OTP settings
OTP_EXPIRY_MINUTES = 5
OTP_MAX_ATTEMPTS = 5


def hash_otp(otp):
    return hashlib.sha256(
        f"{otp}{app.config['SECRET_KEY']}".encode()
    ).hexdigest()


def generate_otp():
    return f"{secrets.randbelow(1000000):06d}"


def send_otp_email(email, otp):
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_email = os.getenv("SMTP_EMAIL")
    smtp_password = os.getenv("SMTP_PASSWORD")

    if not smtp_email or not smtp_password:
        raise RuntimeError(
            "SMTP_EMAIL and SMTP_PASSWORD are not configured."
        )

    message = EmailMessage()
    message["Subject"] = "Stylomera Email Verification Code"
    message["From"] = smtp_email
    message["To"] = email
    message.set_content(
        f"Your Stylomera verification code is: {otp}\n\n"
        f"This code will expire in {OTP_EXPIRY_MINUTES} minutes.\n"
        "If you did not create a Stylomera account, you can ignore this email."
    )

    with smtplib.SMTP(smtp_server, smtp_port, timeout=20) as server:
        server.starttls()
        server.login(smtp_email, smtp_password)
        server.send_message(message)


def is_otp_valid(otp_record, otp):
    if not otp_record:
        return False

    expires_at = datetime.fromisoformat(
        otp_record["expires_at"].replace("Z", "+00:00")
    )

    if datetime.now(timezone.utc) > expires_at:
        return False

    return secrets.compare_digest(
        otp_record["otp_hash"],
        hash_otp(otp)
    )



Bootstrap(app)


os.makedirs(
    app.config['UPLOAD_FOLDER'],
    exist_ok=True
)


class UploadForm(FlaskForm):

    content = FileField('Content Image')

    style = FileField('Style Image')

    content_path = HiddenField()

    style_path = HiddenField()

    alpha = FloatField(
        'Alpha',
        default=1.0
    )

    submit = SubmitField(
        'Transfer Style'
    )


device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)


encoder = VGGEncoder(
    "vgg_normalised.pth"
).to(device)


decoder = Decoder().to(device)


decoder.load_state_dict(
    torch.load(
        "experiment/trained_decoder/decoder_final.pth",
        map_location=device
    )
)


decoder.eval()
encoder.eval()


def allowed_file(filename):

    return "." in filename and \
           filename.rsplit(
               '.',
               1
           )[1].lower() in app.config['ALLOWED_EXTENSIONS']


def style_transfer(
    content_image,
    style_image,
    encoder,
    decoder,
    alpha,
    device
):

    content_transform = transforms.Compose([
        transforms.Resize(512),
        transforms.ToTensor()
    ])


    style_transform = transforms.Compose([
        transforms.Resize(512),
        transforms.ToTensor()
    ])


    content_image = content_transform(
        content_image
    ).unsqueeze(0).to(device)


    style_image = style_transform(
        style_image
    ).unsqueeze(0).to(device)


    with torch.no_grad():

        content_feats = encoder(
            content_image,
            is_test=True
        )


        style_feats = encoder(
            style_image,
            is_test=True
        )


        stylized_feats = adaptive_instance_normalization(
            content_feats,
            style_feats
        )


        stylized_feats = (
            alpha * stylized_feats
            + (1 - alpha) * content_feats
        )


        stylized_image = decoder(
            stylized_feats
        )


    return stylized_image


def save_image(image, path):

    image = image.cpu().clone()

    image = image.squeeze(0)

    image = image.clamp(
        0,
        1
    )

    image = transforms.ToPILImage()(image)

    image.save(path)


def is_logged_in():
    return 'user_id' in session


# ==========================================================
# SIGNUP ROUTE
# ==========================================================

@app.route(
    '/signup',
    methods=['GET', 'POST']
)
def signup():

    error = None

    if request.method == 'POST':

        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        try:

            # Create the user in Supabase Auth.
            response = supabase_auth_request(
                "signup",
                {
                    "email": email,
                    "password": password
                }
            )

            user = response.get("user")

            if user is None:
                error = "Unable to create account."

            else:

                user_id = user["id"]

                # New accounts must complete our OTP verification
                # before they can log in.
                supabase_admin.table('profiles').insert({
                    "id": user_id,
                    "username": username,
                    "email": email,
                    "email_verified": False
                }).execute()

                otp = generate_otp()

                supabase_admin.table('otp_verifications').upsert({
                    "user_id": user_id,
                    "email": email,
                    "otp_hash": hash_otp(otp),
                    "expires_at": (
                        datetime.now(timezone.utc)
                        + timedelta(minutes=OTP_EXPIRY_MINUTES)
                    ).isoformat(),
                    "attempts": 0
                }).execute()

                send_otp_email(
                    email,
                    otp
                )

                session['pending_otp_user_id'] = user_id
                session['pending_otp_email'] = email

                flash(
                    "We sent a verification code to your email.",
                    "success"
                )

                return redirect(
                    url_for('verify_otp')
                )

        except Exception as e:

            error = str(e)

    return render_template(
        'signup.html',
        error=error
    )


# ==========================================================
# OTP VERIFICATION ROUTE
# ==========================================================

@app.route(
    '/verify-otp',
    methods=['GET', 'POST']
)
def verify_otp():

    error = None

    user_id = session.get(
        'pending_otp_user_id'
    )

    email = session.get(
        'pending_otp_email'
    )

    if not user_id or not email:

        flash(
            "Please create an account first.",
            "error"
        )

        return redirect(
            url_for('signup')
        )

    if request.method == 'POST':

        otp = request.form.get(
            'otp',
            ''
        ).strip()

        try:

            response = (
                supabase_admin
                .table('otp_verifications')
                .select('*')
                .eq('user_id', user_id)
                .single()
                .execute()
            )

            otp_record = response.data

            attempts = otp_record.get(
                "attempts",
                0
            ) if otp_record else 0

            if attempts >= OTP_MAX_ATTEMPTS:

                error = (
                    "Too many incorrect attempts. "
                    "Please request a new code."
                )

            elif not is_otp_valid(
                otp_record,
                otp
            ):

                supabase_admin.table(
                    'otp_verifications'
                ).update({
                    "attempts": attempts + 1
                }).eq(
                    "user_id",
                    user_id
                ).execute()

                error = "Invalid or expired verification code."

            else:

                supabase_admin.table(
                    'profiles'
                ).update({
                    "email_verified": True
                }).eq(
                    "id",
                    user_id
                ).execute()

                supabase_admin.table(
                    'otp_verifications'
                ).delete().eq(
                    "user_id",
                    user_id
                ).execute()

                session.pop(
                    'pending_otp_user_id',
                    None
                )

                session.pop(
                    'pending_otp_email',
                    None
                )

                flash(
                    "Email verified successfully! Please sign in.",
                    "success"
                )

                return redirect(
                    url_for('login')
                )

        except Exception as e:

            error = str(e)

    return render_template(
        'verify_otp.html',
        email=email,
        error=error
    )


# ==========================================================
# LOGIN ROUTE
# ==========================================================

@app.route(
    '/login',
    methods=['GET', 'POST']
)
def login():

    error = None

    if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')

        try:

            # Sign in through Supabase Authentication.
            response = supabase_auth_request(
                "token?grant_type=password",
                {
                    "email": email,
                    "password": password
                }
            )

            user = response.get("user")

            if user is None:

                error = "Invalid email or password."

            else:

                # Check our own OTP verification status.
                profile_response = (
                    supabase_admin
                    .table('profiles')
                    .select('email_verified')
                    .eq('id', user['id'])
                    .single()
                    .execute()
                )

                profile = profile_response.data

                if not profile or not profile.get(
                    'email_verified',
                    False
                ):

                    error = (
                        "Please verify your email with the OTP "
                        "before signing in."
                    )

                else:

                    # Store authenticated user information
                    # in the Flask session.
                    session['user_id'] = user['id']
                    session['email'] = user['email']

                    session['access_token'] = (
                        response['access_token']
                    )

                    session['refresh_token'] = (
                        response['refresh_token']
                    )

                    flash(
                        "Login successful! Welcome to Stylomera.",
                        "success"
                    )

                    return redirect(
                        url_for('style_transfer_page')
                    )

        except Exception as e:

            error_message = str(e)

            if "Invalid login credentials" in error_message:
                error = "Invalid email or password."
            else:
                error = error_message

    return render_template(
        'login.html',
        error=error
    )


@app.route('/resend-otp')
def resend_otp():

    user_id = session.get('pending_otp_user_id')
    email = session.get('pending_otp_email')

    if not user_id or not email:
        return redirect(url_for('signup'))

    try:

        otp = generate_otp()

        supabase_admin.table(
            'otp_verifications'
        ).upsert({
            "user_id": user_id,
            "email": email,
            "otp_hash": hash_otp(otp),
            "expires_at": (
                datetime.now(timezone.utc)
                + timedelta(minutes=OTP_EXPIRY_MINUTES)
            ).isoformat(),
            "attempts": 0
        }).execute()

        send_otp_email(
            email,
            otp
        )

        flash(
            "A new verification code has been sent.",
            "success"
        )

    except Exception as e:

        flash(
            f"Unable to send a new code: {str(e)}",
            "error"
        )

    return redirect(
        url_for('verify_otp')
    )


@app.route('/logout')
def logout():

    session.clear()

    flash(
        "You have been logged out.",
        "success"
    )

    return redirect(
        url_for('index')
    )



# ==========================================================
# STYLE TRANSFER ROUTE
# ==========================================================

@app.route(
    '/style-transfer',
    methods=['GET', 'POST']
)
def style_transfer_page():

    if not is_logged_in():

        flash(
            "Please sign in to use Style Transfer.",
            "error"
        )

        return redirect(
            url_for('login')
        )

    form = UploadForm()

    result_image = None
    content_filename = None
    style_filename = None
    error = None

    if form.validate_on_submit():

        if (
            form.content.data
            and form.content.data.filename
        ):

            if allowed_file(
                form.content.data.filename
            ):

                content_filename = secure_filename(
                    form.content.data.filename
                )

                form.content.data.save(
                    os.path.join(
                        app.config['UPLOAD_FOLDER'],
                        content_filename
                    )
                )

                form.content_path.data = content_filename

            else:

                error = "Invalid content image format."

        else:

            content_filename = form.content_path.data


        if (
            form.style.data
            and form.style.data.filename
        ):

            if allowed_file(
                form.style.data.filename
            ):

                style_filename = secure_filename(
                    form.style.data.filename
                )

                form.style.data.save(
                    os.path.join(
                        app.config['UPLOAD_FOLDER'],
                        style_filename
                    )
                )

                form.style_path.data = style_filename

            else:

                error = "Invalid style image format."

        else:

            style_filename = form.style_path.data


        if (
            content_filename
            and style_filename
            and error is None
        ):

            content_path = os.path.join(
                app.config['UPLOAD_FOLDER'],
                content_filename
            )

            style_path = os.path.join(
                app.config['UPLOAD_FOLDER'],
                style_filename
            )

            try:

                content_image = Image.open(
                    content_path
                ).convert("RGB")

                style_image = Image.open(
                    style_path
                ).convert("RGB")

                alpha = float(
                    form.alpha.data
                )

                stylized_image = style_transfer(
                    content_image,
                    style_image,
                    encoder,
                    decoder,
                    alpha,
                    device
                )

                content_name, content_ext = os.path.splitext(
                    content_filename
                )

                result_filename = (
                    'stylized_' +
                    content_name +
                    '_' +
                    uuid.uuid4().hex[:8] +
                    content_ext
                )

                result_path = os.path.join(
                    app.config['UPLOAD_FOLDER'],
                    result_filename
                )

                save_image(
                    stylized_image,
                    result_path
                )

                result_image = result_filename

                # Save generation information for the logged-in user
                supabase_admin.table('generations').insert({
                    "user_id": session['user_id'],
                    "content_image_path": content_filename,
                    "style_image_path": style_filename,
                    "generated_image_path": result_filename,
                    "alpha": alpha
                }).execute()

            except Exception as e:

                error = str(e)


        elif error is None:

            if not content_filename:

                error = "Please upload content image."

            elif not style_filename:

                error = "Please upload style image."


    elif request.method == 'POST':

        error = str(
            form.errors
        )


    return render_template(
        'style_transfer.html',
        form=form,
        result_image=result_image,
        content_image=content_filename,
        style_image=style_filename,
        error=error
    )


# ==========================================================
# MY CREATIONS ROUTE
# ==========================================================

@app.route('/creations')
def creations():

    if not is_logged_in():
        flash(
            "Please sign in to view your creations.",
            "error"
        )

        return redirect(
            url_for('login')
        )

    try:
        generations_response = (
            supabase_admin
            .table('generations')
            .select('*')
            .eq('user_id', session['user_id'])
            .order('created_at', desc=True)
            .execute()
        )

        generations = generations_response.data or []

    except Exception as e:
        generations = []

        flash(
            f"Unable to load your creations: {str(e)}",
            "error"
        )

    return render_template(
        'creations.html',
        generations=generations
    )


# ==========================================================
# EXISTING HOME ROUTE
# ==========================================================

@app.route(
    '/',
    methods=['GET', 'POST']
)
def index():

    form = UploadForm()

    result_image = None
    content_filename = None
    style_filename = None
    error = None

    if form.validate_on_submit():

        if (
            form.content.data
            and form.content.data.filename
        ):

            if allowed_file(
                form.content.data.filename
            ):

                content_filename = secure_filename(
                    form.content.data.filename
                )

                form.content.data.save(
                    os.path.join(
                        app.config['UPLOAD_FOLDER'],
                        content_filename
                    )
                )

                form.content_path.data = content_filename

            else:

                error = "Invalid content image format."

        else:

            content_filename = form.content_path.data


        if (
            form.style.data
            and form.style.data.filename
        ):

            if allowed_file(
                form.style.data.filename
            ):

                style_filename = secure_filename(
                    form.style.data.filename
                )

                form.style.data.save(
                    os.path.join(
                        app.config['UPLOAD_FOLDER'],
                        style_filename
                    )
                )

                form.style_path.data = style_filename

            else:

                error = "Invalid style image format."

        else:

            style_filename = form.style_path.data


        if (
            content_filename
            and style_filename
            and error is None
        ):

            content_path = os.path.join(
                app.config['UPLOAD_FOLDER'],
                content_filename
            )

            style_path = os.path.join(
                app.config['UPLOAD_FOLDER'],
                style_filename
            )

            try:

                content_image = Image.open(
                    content_path
                ).convert("RGB")

                style_image = Image.open(
                    style_path
                ).convert("RGB")

                alpha = float(
                    form.alpha.data
                )

                stylized_image = style_transfer(
                    content_image,
                    style_image,
                    encoder,
                    decoder,
                    alpha,
                    device
                )

                result_filename = (
                    'stylized_' + content_filename
                )

                result_path = os.path.join(
                    app.config['UPLOAD_FOLDER'],
                    result_filename
                )

                save_image(
                    stylized_image,
                    result_path
                )

                result_image = result_filename

            except Exception as e:

                error = str(e)

        elif error is None:

            if not content_filename:

                error = "Please upload content image."

            elif not style_filename:

                error = "Please upload style image."


    elif request.method == 'POST':

        error = str(
            form.errors
        )


    return render_template(
        'index.html',
        form=form,
        result_image=result_image,
        content_image=content_filename,
        style_image=style_filename,
        error=error
    )


# ==========================================================
# SERVE UPLOADED IMAGES
# ==========================================================

@app.route(
    "/uploads/<filename>"
)
def send_image(filename):

    return send_from_directory(
        app.config['UPLOAD_FOLDER'],
        filename
    )


# ==========================================================
# SERVE EXAMPLE IMAGES
# ==========================================================

@app.route(
    "/examples/<filename>"
)
def send_example(filename):

    return send_from_directory(
        'examples',
        filename
    )


# ==========================================================
# RUN APPLICATION
# ==========================================================

if __name__ == '__main__':

    from werkzeug.serving import run_simple

    run_simple(
        'localhost',
        5000,
        app,
        use_reloader=True,
        use_debugger=True
    )