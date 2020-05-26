"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'mq(e+aga2zmp%w-cwtisuc+o&a2rgat+ln8zp-gk^@hl91*yco'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Config allowed hosts here
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'localhost'
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'couchdb',
    'twitter'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # CORS
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware'
]

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

# Config the couchdb endpoint here
# COUCH_SERVER_URL = 'http://admin:gcsvn123@localhost:5984'
# COUCH_DATABASE_NAME = 'twitter_database'

COUCH_SERVER_URL = 'http://admin:password@localhost:5984'
COUCH_DATABASE_NAME = 'tweets'

COUCH_VIEWS = {
    'movement': {
        "_id": "_design/movement",
        "views": {
            "movement": {
                "reduce": "function (keys, values, rereduce) {\n  if (rereduce) {\n    var result = [];\n    values.forEach(function (value) {\n      value.forEach(function (point) {\n          result.push(point);\n        }\n      )\n    });\n    \n    var uniquePoints = [];\n    result.forEach(function (point) {\n        var existing = false;\n        for (var i = 0; i < uniquePoints.length; i++) {\n            if (uniquePoints[i][0] === point[0] && uniquePoints[i][1] === point[1]) {\n                existing = true;\n                break;\n            }\n        }\n        \n        if (existing === false) {\n            uniquePoints.push(point);\n        }\n    });\n    \n    if (uniquePoints.length > 1) {\n      return uniquePoints;\n    } else {\n      return [];\n    }\n  } else {\n    return values;\n  }\n}",
                "map": "function (doc) {\n   if (doc.user && doc.calculated_coordinates) {\n    if (doc.calculated_coordinates.length == 2) {\n        emit(doc.user, [doc.calculated_coordinates[1].toFixed(3), doc.calculated_coordinates[0].toFixed(3)]);\n    }\n   }\n}"
            },
            "find-route": {
                "map": "function (doc) {\n  if (doc.raw_data && doc.calculated_coordinates.length === 2) {\n    var raw_data = doc.raw_data\n    emit([raw_data.user.id, raw_data.user.screen_name], [[doc.calculated_coordinates[1], doc.calculated_coordinates[0]], doc.created_at], 1);\n  }\n}",
                "reduce": "function (keys, values, rereduce) {\n  if (rereduce) {\n    return sum(values);\n  } else {\n    return values.length;\n  }\n}"
            },
            "noisy-data": {
                "map": "function (doc) {\n  if (doc.calculated_coordinates.length == 2) {\n    geo = doc.calculated_coordinates;\n    if (geo[0] < 100 || geo[0] > 160) {\n      emit(geo, 1);\n    }\n    if (geo[1] < -50 || geo[1] > -10) {\n      emit(geo, 1);\n    }\n  }\n}"
            }
        },
        "language": "javascript"
    },
    'sentiment-map': {
        "_id": "_design/sentiment-map",
        "views": {
            "num-positive-tweets-by-location": {
                "reduce": "_sum",
                "map": "function (doc) {\n  if (doc.calculated_coordinates.length == 2 && doc.emotions) {\n    var type = \"\"\n    var emotion_value = -1\n    if (doc.emotions.neg > emotion_value) {\n      type = \"NEGATIVE\";\n      emotion_value = doc.emotions.neg;\n    }\n    if (doc.emotions.neu > emotion_value) {\n      type = \"NEUTRAL\";\n      emotion_value = doc.emotions.neu;\n    }\n    if (doc.emotions.pos > emotion_value) {\n      type = \"POSITIVE\";\n      emotion_value = doc.emotions.pos;\n    }\n    if (type === \"POSITIVE\") {\n      calculated_coordinates = doc.calculated_coordinates\n      emit(calculated_coordinates, 1);\n    }\n  }\n}"
            },
            "num-negative-tweets-by-location": {
                "reduce": "_sum",
                "map": "function (doc) {\n  if (doc.calculated_coordinates.length == 2 && doc.emotions) {\n    var type = \"\"\n    var emotion_value = -1\n    if (doc.emotions.neg > emotion_value) {\n      type = \"NEGATIVE\";\n      emotion_value = doc.emotions.neg;\n    }\n    if (doc.emotions.neu > emotion_value) {\n      type = \"NEUTRAL\";\n      emotion_value = doc.emotions.neu;\n    }\n    if (doc.emotions.pos > emotion_value) {\n      type = \"POSITIVE\";\n      emotion_value = doc.emotions.pos;\n    }\n    if (type === \"NEGATIVE\") {\n      calculated_coordinates = doc.calculated_coordinates\n      emit(calculated_coordinates, 1);\n    }\n  }\n}"
            },
            "num-neutral-tweets-by-location": {
                "reduce": "_sum",
                "map": "function (doc) {\n  if (doc.calculated_coordinates.length == 2 && doc.emotions) {\n    var type = \"\"\n    var emotion_value = -1\n    if (doc.emotions.neg > emotion_value) {\n      type = \"NEGATIVE\";\n      emotion_value = doc.emotions.neg;\n    }\n    if (doc.emotions.neu > emotion_value) {\n      type = \"NEUTRAL\";\n      emotion_value = doc.emotions.neu;\n    }\n    if (doc.emotions.pos > emotion_value) {\n      type = \"POSITIVE\";\n      emotion_value = doc.emotions.pos;\n    }\n    if (type === \"NEUTRAL\") {\n      calculated_coordinates = doc.calculated_coordinates\n      emit(calculated_coordinates, 1);\n    }\n  }\n}"
            }
        },
        "language": "javascript"
    },
    'statistics': {
        "_id": "_design/statistics",
        "views": {
            "tweets-with-emo-val-and-pro-cnt": {
                "map": "function (doc) {\n  if (doc.emotions && doc.pronoun_count) {\n      emit(doc._id, [doc.emotions, doc.pronoun_count], 1);\n  }\n}"
            },
            "total-tweets-by-day-n-hour": {
                "reduce": "function (keys, values, rereduce) {\n  if (rereduce) {\n    return sum(values);\n  } else {\n    return values.length;\n  }\n}",
                "map": "function (doc) {\n  if (doc.raw_data) {\n    var data = doc.raw_data;\n    var date = new Date(data.created_at)\n    var day = date.getDay();\n    var hour = date.getHours()\n    \n    emit([day, hour], 1);\n  }\n}"
            },
            "tweets-by-categories": {
                "reduce": "function (keys, values, rereduce) {\n  if (rereduce) {\n    return sum(values);\n  } else {\n    return values.length;\n  }\n}",
                "map": "function (doc) {\n  if (doc.match_track_filter === true) {\n    emit(\"Covid19\", 1)\n  } else {\n    emit(\"Others\", 1)\n  }\n}"
            },
            "tweets-with-coordinates": {
                "reduce": "function (keys, values, rereduce) {\n  if (rereduce) {\n    return sum(values);\n  } else {\n    return values.length;\n  }\n}",
                "map": "function (doc) {\n  if (doc.calculated_coordinates) {\n    if (doc.calculated_coordinates.length == 2) {\n      if (doc.match_track_filter) {\n        emit([\"With Coordinates\", \"covid\"], 1)\n      } else {\n        emit([\"With Coordinates\", \"basic\"], 1)\n      }\n    } else {\n      if (doc.match_track_filter) {\n        emit([\"Without Coordinates\", \"covid\"], 1)\n      } else {\n        emit([\"Without Coordinates\", \"basic\"], 1)\n      }\n    }\n  }\n}"
            },
            "language": {
                "reduce": "_sum",
                "map": "function (doc) {\n  emit(doc.raw_data.lang, 1);\n}"
            },
            "tweets-per-hour": {
                "reduce": "function (keys, values, rereduce) {\n  if (rereduce) {\n    return sum(values);\n  } else {\n    return values.length;\n  }\n}",
                "map": "function (doc) {\n  if (doc.raw_data) {\n    var data = doc.raw_data;\n    var date = new Date(data.created_at)\n    var hour = date.getHours()\n    emit(hour, 1);\n  }\n}"
            },
            "tweets-by-political-parties": {
                "reduce": "function (keys, values, rereduce) {\n  if (rereduce) {\n    return sum(values);\n  } else {\n    return values.length;\n  }\n}",
                "map": "function (doc) {\n  if (doc.politician.length > 0) {\n    emit([doc.politician, doc.match_track_filter, doc.user], 1);  \n  }\n}"
            },
            "tweets-by-politicians": {
                "reduce": "function (keys, values, rereduce) {\n  if (rereduce) {\n    return sum(values);\n  } else {\n    return values.length;\n  }\n}",
                "map": "function (doc) {\n  if (doc.politician.length > 0) {\n    emit([doc.politician, doc.match_track_filter, doc.raw_data.user.name], 1);  \n  }\n}"
            },
            "feelings-about-covid": {
                "reduce": "_sum",
                "map": "function (doc) {\n  if (doc.match_track_filter) {\n    emotion = \"NEUTRAL\";\n    emotions = doc.emotions\n    if (emotions.neg >= emotions.neu && emotions.neg >= emotions.pos) {\n      emotion = \"NEGATIVE\";\n    }\n    if (emotions.pos >= emotions.neu && emotions.pos >= emotions.neg) {\n      emotion = \"POSITIVE\";\n    }\n    emit(emotion, 1);\n  }\n}"
            },
            "feelings-about-non-covid": {
                "reduce": "_sum",
                "map": "function (doc) {\n  if (doc.match_track_filter === false) {\n    emotion = \"NEUTRAL\";\n    emotions = doc.emotions\n    if (emotions.neg >= emotions.neu && emotions.neg >= emotions.pos) {\n      emotion = \"NEGATIVE\";\n    }\n    if (emotions.pos >= emotions.neu && emotions.pos >= emotions.neg) {\n      emotion = \"POSITIVE\";\n    }\n    emit(emotion, 1);\n  }\n}"
            },
            "most-positive-hours": {
                "reduce": "_stats",
                "map": "function (doc) {\n  if (doc.raw_data) {\n    var data = doc.raw_data;\n    var date = new Date(data.created_at)\n    var hour = date.getHours()\n    emit(hour, doc.emotions.pos);\n  }\n}"
            },
            "most-negative-hours": {
                "reduce": "_stats",
                "map": "function (doc) {\n  if (doc.raw_data) {\n    var data = doc.raw_data;\n    var date = new Date(data.created_at)\n    var hour = date.getHours()\n    emit(hour, doc.emotions.neg);\n  }\n}"
            }
        },
        "language": "javascript"
    },
    'user': {
        "_id": "_design/user",
        "views": {
            "user": {
                "map": "function (doc) {\n  if (doc.calculated_coordinates) {\n    emit(doc.raw_data.user.id, doc.raw_data.user); \n  }\n}"
            }
        },
        "language": "javascript"
    }
}
