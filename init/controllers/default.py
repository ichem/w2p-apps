# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------


def index():
    rows = db(db.post).select(orderby=~db.post.id, limitby=(0,4))
    return locals()

def blog():
    if not request.vars.page:
        redirect(URL(vars={'page':1}))
    else:
        page = int(request.vars.page)
    start = (page-1)*10
    end = page*10
    rows = db(db.post).select(orderby=~db.post.id, limitby=(start,end))
    return locals()

def post():
    row = db(db.post.slug == request.args(0)).select().first()
    return dict(row=row)

# Upload pictures in CKEditor
def upload():
    url = ""
    form = SQLFORM(db.files, showid=False, formstyle='bootstrap3_stacked')
    if form.accepts(request.vars, session):
        response.flash = T('File uploaded successfully!')
        url = URL(r=request, f="download", args = db(db.files.title==request.vars.title).select(orderby=~db.files.id)[0].uploaded_data)
    return dict(form=form, cknum=request.vars.CKEditorFuncNum, url=url)


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
