#!/usr/bin/env bash

export SECRET_KEY='*8emke^-jjiyszpisib-f@xjt9b72_x465cdx^(gj0jl_70v&)'
export DEBUG='False' # always False for deployment
export DB_HOST='/cloudsql/my-beta-blog:us-central1:my-beta-blog'
export DB_PORT='5432' # PostgreSQL port
export DB_NAME='blog'
export DB_USER='postgres' # either 'postgres' (default) or one you created on the PostgreSQL instance page
export DB_PASSWORD='lmzongolo8754'
export GS_PROJECT_ID='my-beta-blog'
export STATIC_URL='https://storage.googleapis.com/my-beta-blog-static/static/' # this is the url that you sync static files to