import os
import json
import requests
from oauthlib.oauth2 import WebApplicationClient
from services.auth_service import generate_tokens
from middlewares.auth_middleware import token_required
from flask import Blueprint, redirect, request, url_for, session, make_response, render_template

oauth_routes = Blueprint('oauth_routes', __name__)

# OAuth 2 client setup
client = WebApplicationClient(os.getenv('GOOGLE_CLIENT_ID'))

def get_google_provider_cfg():
    return requests.get(os.getenv('GOOGLE_DISCOVERY_URL')).json()

@oauth_routes.route("/google/login")
def login():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=url_for('oauth_routes.callback', _external=True),
        scope=["openid", "email", "profile"],
    )
    print(request_uri)
    return redirect(request_uri)

@oauth_routes.route("/login/callback")
def callback():
    # Disable HTTPS requirement for local development
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    code = request.args.get("code")

    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=url_for('oauth_routes.callback', _external=True),
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(os.getenv('GOOGLE_CLIENT_ID'), os.getenv('GOOGLE_CLIENT_SECRET')),
    )

    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]

        # Create JWT tokens
        tokens = generate_tokens(users_name)

        # Set tokens as cookies
        response = make_response(redirect(url_for("user_routes.home")))
        response.set_cookie('access_token', tokens.get('access_token'), httponly=True)
        response.set_cookie('refresh_token', tokens.get('refresh_token'), httponly=True)
        return response
    else:
        return "User email not available or not verified by Google.", 400

@oauth_routes.route("/logout")
@token_required
def logout():
    session.clear()
    logout_msg = "You have logged out successfully"
    response = make_response(render_template('login.html', logout=logout_msg))
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return response