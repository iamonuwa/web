'''
    Copyright (C) 2018 Gitcoin Core

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.

'''
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap
from django.urls import path, re_path
from django.views.i18n import JavaScriptCatalog

import avatar.views
import bounty_requests.views
import chat.views
import credits.views
import dashboard.embed
import dashboard.gas_views
import dashboard.helpers
import dashboard.tip_views
import dashboard.views
import dataviz.d3_views
import dataviz.views
import enssubdomain.views
# event:ethdenver2019
import event_ethdenver2019.views
import faucet.views
import gitcoinbot.views
import healthcheck.views
import kudos.views
import linkshortener.views
import marketing.views
import marketing.webhookviews
import perftools.views
import quests.views
import retail.emails
import retail.views
import revenue.views
import tdi.views
from avatar.router import router as avatar_router
from dashboard.router import router as dbrouter
from grants.router import router as grant_router
from kudos.router import router as kdrouter

from .sitemaps import sitemaps

urlpatterns = [
    # oauth2 provider
    url('^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    # Health check endpoint
    re_path(r'^health/', include('health_check.urls')),
    re_path(r'^lbcheck/?', healthcheck.views.lbcheck, name='lbcheck'),
    re_path(r'^spec/?', healthcheck.views.spec, name='spec'),

    # dashboard views
    re_path(r'^$', dashboard.views.builder, name='index'),

    # Avatars
    path('avatar/', include('avatar.urls', namespace='avatar')),

    # Interests
    path('dynamic/js/tokens_dynamic.js', retail.views.tokens, name='tokens'),

    # sync methods
    url(r'^sync/web3/?', dashboard.views.sync_web3, name='sync_web3'),
    url(r'^sync/get_amount/?', dashboard.helpers.amount, name='helpers_amount'),
    re_path(r'^sync/get_issue_details/?', dashboard.helpers.issue_details, name='helpers_issue_details'),

    re_path(r'^legal/cookie/?', dashboard.views.cookie, name='cookie'),

    # for robots
    url(r'^robots.txt/?', retail.views.robotstxt, name='robotstxt'),
    url(r'^sitemap.xml/?', perftools.views.sitemap, name='django.contrib.sitemaps.views.sitemap'),
    path('', include('social_django.urls', namespace='social')),
    # webhook routes
    # sendgrid webhook processing
    path(settings.SENDGRID_EVENT_HOOK_URL, marketing.webhookviews.process, name='sendgrid_event_process'),

    # ENS urls
    re_path(r'^ens/', enssubdomain.views.ens_subdomain, name='ens'),
]

if settings.ENABLE_SILK:
    urlpatterns += [url(r'^silk/', include('silk.urls', namespace='silk'))]

if not settings.AWS_STORAGE_BUCKET_NAME:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# If running in DEBUG, expose the error handling pages.
if settings.DEBUG:
    urlpatterns += [
        re_path(r'^400/$', retail.views.handler400, name='400'),
        re_path(r'^403/$', retail.views.handler403, name='403'),
        re_path(r'^404/$', retail.views.handler404, name='404'),
        re_path(r'^500/$', retail.views.handler500, name='500'),
    ]

handler403 = 'retail.views.handler403'
handler404 = 'retail.views.handler404'
handler500 = 'retail.views.handler500'
handler400 = 'retail.views.handler400'
