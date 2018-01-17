#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon.dal import Field
from gluon.validators import IS_NOT_EMPTY, IS_SLUG

def init_models(db):
    db.define_table('post',
               Field('title',requires=IS_NOT_EMPTY()),
               Field('author','reference auth_user'),
               Field('subtitle','text',requires=IS_NOT_EMPTY()),
               Field('description', 'text',requires=IS_NOT_EMPTY()),
               Field('slug', compute=lambda row: IS_SLUG()(row.title)[0]),
               Field('created_at','datetime',requires=IS_NOT_EMPTY())),
    db.define_table('files',
               Field('title', 'string'),
               Field('uploaded_data', 'upload'))
