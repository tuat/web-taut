# coding: utf-8

import importlib
import hashlib
from flask import g
from flask import request, flash, redirect, url_for
from flask_oauthlib.client import OAuthException
from ..models import AccountConnection, Account
from ..helpers.account import login_user

def authorized_callback(response, provider_name, kind):
    if response is None:
        error = request.args.get('error'),
        error_description = request.args.get('error_description')

        flash('Access denied: reason={0}, error={1}'.format(''.join(error), error_description), 'error')

        return redirect(url_for('settings.connection' if g.user else 'index.login'))
    elif 'access_token' not in response:
        flash('Authentication failed, Can not get the access token, Please sign in again', 'error')
        return redirect(url_for('settings.connection' if g.user else 'index.login'))
    else:
        access_token = response['access_token']

        current_package  = __name__.split('.')[0]
        provider_modules = importlib.import_module(".providers", package=current_package)
        provider_class   = getattr(provider_modules, '{0}Provider'.format(provider_name.capitalize()))

        provider              = provider_class(access_token)
        provider_user_id      = str(provider.user_id())
        provider_display_name = provider.display_name()
        provider_email        = provider.email()

        # Make user login if the connection is already connected
        user_connection = AccountConnection.query.filter_by(provider_name=provider_name, provider_user_id=provider_user_id).first()

        if user_connection:
            user_connection.provider_user_id = provider_user_id
            user_connection.access_token     = access_token
            user_connection.display_name     = provider_display_name
            user_connection.save()

            user = Account.query.get(user_connection.user_id)

            login_user(user)

            return redirect(url_for('settings.connection' if g.user else 'index.index'))

        # If kind is normal,
        # - no
        #   - check the username is registered, yes: redirect, no create user
        # - yes
        #   - just connect like dropbox
        if kind == 'normal':
            # Redirect to sign in page if the provider.email() is registered in website
            if provider_email:
                user = User.query.filter_by(email=provider.email()).first()

                if user:
                    flash('You already registered, Please sign in by email account', 'error')
                    return redirect(url_for('settings.connection' if g.user else 'index.login'))

            # Check the username is or not exists, if exists, it will md5 email for username
            username = provider_email.split('@')[0]

            if Account.query.filter_by(username=username).first():
                username = hashlib.md5(provider_email).hexdigest()[0:10]

            # Create new user if not connected and email is not registered
            user = Account(
                username = username,
                email    = provider_email,
                password = Account.generate_token(20)
            ).save()
        else:
            user = g.user

        AccountConnection(
            user_id          = user.id,
            provider_name    = provider_name,
            provider_user_id = provider_user_id,
            access_token     = access_token,
            display_name     = provider_display_name
        ).save()

        login_user(user)

        return redirect(url_for('settings.connection' if g.user else 'index.index'))

def is_aouth_login():
    return AccountConnection.query.filter(
        AccountConnection.user_id == g.user.id,
        AccountConnection.provider_name != 'dropbox'
    ).first() is not None
