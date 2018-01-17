# -*- coding: utf-8 -*-
# Index
def index():
    if not request.vars.page:
        redirect(URL(vars={'page':1}))
    else:
        page = int(request.vars.page)
    start = (page-1)*10
    end = page*10
    rows = db(db.doc).select(orderby=~db.doc.id, limitby=(start,end))
    return locals()

def article():
    row_article = db.doc(request.args(0))
    return dict(row_article=row_article)

# People
def people():
    if not request.vars.page:
        redirect(URL(vars={'page':1}))
    else:
        page = int(request.vars.page)
    start = (page-1)*10
    end = page*10
    rows = db(db.person).select(orderby=~db.person.id, limitby=(start,end))
    return dict(rows=rows)

def person():
    row_person = db.person(request.args(0))
    return dict(row_person=row_person)

def gender():
    if request.args(0)=="male": 
        return dict(row = db(db.person.gender=="Male").select(orderby=~db.person.id))
    elif request.args(0)=="female":
        return dict(row = db(db.person.gender=="Female").select(orderby=~db.person.id))

def name():
    if request.args(0)=="Jane": 
        return dict(row = db(db.person.first_name=="Jane").select(orderby=~db.person.id))
    elif request.args(0)=="Frank":
        return dict(row = db(db.person.first_name=="Frank").select(orderby=~db.person.id))
    elif request.args(0)=="Terry":
        return dict(row = db(db.person.first_name=="Terry").select(orderby=~db.person.id))
    elif request.args(0)=="Maria":
        return dict(row = db(db.person.first_name=="Maria").select(orderby=~db.person.id))

#Products
def products():
    rows = db(db.product).select(orderby=~db.product.id)
    return dict(rows=rows)

def product():
    row_product = db(db.product.slug == request.args(0)).select().first()
    return dict(row_product=row_product)

def country():
    if request.args(0)=="usa": 
        return dict(row = db(db.product.country=="USA").select(orderby=~db.product.id))
    elif request.args(0)=="eu":
        return dict(row = db(db.product.country=="EU").select(orderby=~db.product.id))
    elif request.args(0)=="jar":
        return dict(row = db(db.product.country=="JAR").select(orderby=~db.product.id))
    elif request.args(0)=="uk":
        return dict(row = db(db.product.country=="UK").select(orderby=~db.product.id))
    elif request.args(0)=="cro":
        return dict(row = db(db.product.country=="CRO").select(orderby=~db.product.id))
    elif request.args(0)=="prc":
        return dict(row = db(db.product.country=="PRC").select(orderby=~db.product.id))

def product_type():
    if request.args(0)=="software":
        return dict(row = db(db.product.product_type=="Software").select(orderby=~db.product.id))
    elif request.args(0)=="instruments":
        return dict(row = db(db.product.product_type=="Instruments").select(orderby=~db.product.id))
    elif request.args(0)=="smartphone":
        return dict(row = db(db.product.product_type=="Smartphone").select(orderby=~db.product.id))

#Companies
def companies():
    rows = db(db.company).select(orderby=~db.company.id)
    return dict(rows=rows)

def company():
    row_company = db(db.company.slug == request.args(0)).select().first()
    return dict(row_company=row_company)

def company_country():
    if request.args(0)=="usa":
        return dict(row = db(db.company.country=="USA").select(orderby=~db.company.id))
    elif request.args(0)=="eu":
        return dict(row = db(db.company.country=="EU").select(orderby=~db.company.id))

#Search
def search():
    result = db(db.product.name.contains(request.vars.q) | 
                db.product.country.contains(request.vars.q)).select(cache=(cache.ram, 3600), cacheable=True)
    result2 = db(db.company.name.contains(request.vars.q) | 
                 db.company.country.contains(request.vars.q)).select(cache=(cache.ram, 3600), cacheable=True)
    result3 = db(db.person.first_name.contains(request.vars.q) | 
                 db.person.last_name.contains(request.vars.q) |     
                 db.person.email.contains(request.vars.q) | 
                 db.person.ip_address.contains(request.vars.q)).select(cache=(cache.ram, 3600), cacheable=True)
    result4 = db(db.doc.title.contains(request.vars.q) | 
                 db.doc.body.contains(request.vars.q)).select()
    total_result = db(db.product.name.contains(request.vars.q) | db.product.country.contains(request.vars.q)).count()
    total_result2 = db(db.company.name.contains(request.vars.q) | db.company.country.contains(request.vars.q)).count()
    total_result3 = db(db.person.first_name.contains(request.vars.q) | db.person.last_name.contains(request.vars.q) |     
        db.person.email.contains(request.vars.q) | db.person.ip_address.contains(request.vars.q)).count()
    total_result4 = db(db.doc.title.contains(request.vars.q) | db.doc.body.contains(request.vars.q)).count()
    row_product=row_product = db(db.product.slug == request.args(0)).select().first()
    row_person = db.person(request.args(0))
    row_company = db(db.company.slug == request.args(0)).select().first()
    row_article = db.doc(request.args(0))
    return locals()

# User admin
@auth.requires_login()
def profile():
    user = db.auth_user(request.args(0) or log_usr)
    user_product = db(db.product.product_id==user.id).select(orderby=~db.product.id)
    return locals()


@auth.requires_login()
def edit():
    form_product = crud.update(db.product,request.args(0))
    if form_product.accepted:
        redirect(URL('profile'))
    return locals()


@auth.requires_login()
def create():
    form_product = crud.create(db.product)
    if form_product.accepted:
        redirect(URL('profile'))
    return locals()


@auth.requires_login()
def delete():
    query = db(db.product.id==request.args(0)).select().first()
    remove = db(db.product.id==query).delete()
    if remove:
        session.flash = 'Record deleted'
        redirect(URL('profile'))
    return dict(remove=remove)

# Upload pictures in CKEditor
def upload():
    url = ""
    form = SQLFORM(db.files, showid=False, formstyle='bootstrap3_stacked')
    if form.accepts(request.vars, session):
        response.flash = T('File uploaded successfully!')
        url = URL(r=request, f="download", args = db(db.files.title==request.vars.title).select(orderby=~db.files.id)[0].uploaded_data)
    return dict(form=form, cknum=request.vars.CKEditorFuncNum, url=url)

# Contact
def contact():
	form = SQLFORM.factory(Field('name',requires=IS_NOT_EMPTY()),
                           Field('email',requires=IS_EMAIL()),
                           Field('body','text'),formstyle = 'bootstrap3_stacked')
	if form.process().accepted:
		mail.send(to='you@gmail.com',
                  subject='Upit od %(name)s %(email)s' % form.vars,
                  message = form.vars.body)
		redirect(URL('index'))
	return dict(form=form)

# Web service (rest api)
#@auth.requires_membership('administrator')
@request.restful()
def api():
	if request.env.http_origin:
		response.headers['Access-Control-Allow-Origin'] = request.env.http_origin
		response.headers['Access-Control-Allow-Credentials'] = 'true'
		response.headers['Access-Control-Max-Age'] = 86400
	if request.env.request_method == 'OPTIONS':
		if request.env.http_access_control_request_method:
			response.headers['Access-Control-Allow-Methods'] = request.env.http_access_control_request_method
		if request.env.http_access_control_request_headers:
			response.headers['Access-Control-Allow-Headers'] = request.env.http_access_control_request_headers
			return HTTP(200)
	response.view = 'generic.json'

	def GET(*args,**vars):
		patterns = 'auto'
		parser = db.parse_as_rest(patterns, args, vars)
		if parser.status == 200:
			content=parser.response
			return content.as_json()
			#return dict(content=parser.response)
		else:
			raise HTTP(parser.status, parser.error)
	return locals()

# Auth user
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
    if request.args(0) == 'register':
        form = auth.register(next=auth.settings.register_next)
    else:
        form=auth()
    return dict(form=form)

# Sending mail after registration
@auth.requires_login() 
def welcome():
    usr_email = auth.user.email
    mail.send(usr_email,'Welcome To website','Welcome To website')
    redirect(URL('index'))


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
