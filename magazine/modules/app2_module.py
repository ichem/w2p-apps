#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon.dal import Field
from gluon.validators import IS_IN_SET, IS_SLUG

def app2_models(db):
    db.define_table('product',
               Field('product_id', 'reference auth_user', readable=False, writable=False),
               Field('name'),
               Field('description', 'text'),
               Field('slug', compute=lambda row: IS_SLUG()(row.name)[0]),
               Field('product_type', requires=IS_IN_SET(('Instruments', 'Software', 'Smartphone'))),
               Field('country',requires=IS_IN_SET(('USA', 'UK', 'EU', 'CRO','JAPAN','PRC','JAR'))))
    db.define_table('company',
               Field('name'),
               Field('slug', compute=lambda row: IS_SLUG()(row.name)[0]),
               Field('country',requires=IS_IN_SET(('USA', 'UK', 'EU', 'CRO'))))
    db.define_table('person',
               Field('first_name'),
               Field('last_name'),
               Field('email'),
               Field('gender'),
               Field('ip_address'))
    db.define_table('doc',
               Field('title'),
               Field('body'))
    db.define_table('files',
               Field('title', 'string'),
               Field('uploaded_data', 'upload'))
