# -*- coding: utf-8 -*-

def index():
    return dict(rows = db(db.product).select(orderby=~db.product.id),total=db(db.product).count())

def product():
    return dict(row = db(db.product.slug==request.args(0)).select().first())

def filter():
    rows = db(db.product).select()
    total = db(db.product).count()
    if request.args(0)=="lowest" and request.vars:
        query = reduce(lambda a, b: (a & b),
            (db.product[var].contains(request.vars[var]) for var in request.vars))
        rows = db(query).select(orderby=db.product.price)
        total = db(query).count()
    elif request.args(0)=="highest" and request.vars:
        query = reduce(lambda a, b: (a & b),
            (db.product[var].contains(request.vars[var]) for var in request.vars))
        rows = db(query).select(orderby=~db.product.price)
        total = db(query).count()
    elif request.args(0)=="ascending" and request.vars:
        query = reduce(lambda a, b: (a & b),
            (db.product[var].contains(request.vars[var]) for var in request.vars))
        rows = db(query).select(orderby=db.product.manufacturer)
        total = db(query).count()
    elif request.args(0)=="descending" and request.vars:
        query = reduce(lambda a, b: (a & b),
            (db.product[var].contains(request.vars[var]) for var in request.vars))
        rows = db(query).select(orderby=~db.product.manufacturer)
        total = db(query).count()
    elif request.vars.manufacturer:
        query = reduce(lambda a, b: (a & b),
            (db.product[var].contains(request.vars[var]) for var in request.vars))
        rows = db(query).select()
        total = db(query).count()
    elif request.vars.dual_sim:
        query = reduce(lambda a, b: (a & b),
            (db.product[var].contains(request.vars[var]) for var in request.vars))
        rows = db(query).select()
        total = db(query).count()
    elif request.vars.product_type:
        query = reduce(lambda a, b: (a & b),
            (db.product[var].contains(request.vars[var]) for var in request.vars))
        rows = db(query).select()
        total = db(query).count()
    elif request.vars.color:
        query = reduce(lambda a, b: (a & b),
            (db.product[var].contains(request.vars[var]) for var in request.vars))
        rows = db(query).select()
        total = db(query).count()
    elif request.vars.country:
        query = reduce(lambda a, b: (a & b),
            (db.product[var].contains(request.vars[var]) for var in request.vars))
        rows = db(query).select()
        total = db(query).count()
    return dict(rows=rows,msg="No results",total=total)

def select():
    if request.args(0)=="lowest-price": 
        return dict(row = db(db.product).select(orderby=db.product.price),total = db(db.product).count())
    elif request.args(0)=="highest-price":
        return dict(row = db(db.product).select(orderby=~db.product.price),total = db(db.product).count())
    elif request.args(0)=="ascending":
        return dict(row = db(db.product).select(orderby=db.product.manufacturer),total = db(db.product).count())
    elif request.args(0)=="descending":
        return dict(row = db(db.product).select(orderby=~db.product.manufacturer),total = db(db.product).count())

def upload():
    #form = FORM(LABEL("Ime proizvoda"), INPUT(_name='title', _type='text', requires=IS_NOT_EMPTY()), BR(),
    form = FORM(LABEL("Dodaj slike"), INPUT(_name='up_files', _type='file', _multiple='', requires=IS_NOT_EMPTY()), BR(), INPUT(_type='submit', _value='Upload'))
    if form.accepts(request.vars, session, formname="form"):
        files = request.vars['up_files']
        if not isinstance(files, list):
            files = [files]
        for f in files:
            up_file = db.uploads.up_file.store(f,f.filename)
            id = db.uploads.insert(up_file=up_file,filename=f.filename)#,title=form.vars.title)
            db.commit()
        redirect(URL('upload'))
    rows = db(db.uploads).select()
    return dict(form=form,rows=rows)


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
