#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon.dal import Field
from gluon.validators import IS_IN_SET, IS_SLUG

def app1_models(db):
    db.define_table('product',
               #Field('product_id', 'reference auth_user', readable=False, writable=False),
               Field('manufacturer'),
               Field('description', 'text'),
               Field('price'),
               Field('slug', compute=lambda row: IS_SLUG()(row.manufacturer)[0]),
               Field('product_type', requires=IS_IN_SET(('Mobilephone', 'Smartphone'))),
               Field('dual_sim', requires=IS_IN_SET(('Yes', 'No'))),
               Field('color', requires=IS_IN_SET(('Black', 'White', 'Gray'))),
               Field('country',requires=IS_IN_SET(('USA', 'UK', 'EU', 'CRO','JAPAN','PRC','JAR')))),
    db.define_table('uploads',
               Field('up_file','upload', autodelete=True),
               Field('filename'))
