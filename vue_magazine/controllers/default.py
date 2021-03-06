# -*- coding: utf-8 -*-

def index():
    return locals()

def people():
    rows = db(db.person).select(cache=(cache.ram,3600),cacheable=True)
    return dict(rows=rows)


def products():
    rows = db(db.product).select(cache=(cache.ram,3600),cacheable=True)
    return dict(rows=rows)


def companies():
    rows = db(db.company).select(cache=(cache.ram,3600),cacheable=True)
    return dict(rows=rows)


def magazine():
    rows = db(db.doc).select(cache=(cache.ram,3600),cacheable=True)
    return dict(rows=rows)


def company():
    row_company = db(db.company.slug == request.args(0)).select().first()
    return dict(row_company=row_company)

@cache.action(time_expire=3600, cache_model=cache.ram, quick='SVP')
def person():
    row_person = db.person(request.args(0))
    return dict(row_person=row_person)


def product():
    row_product = db(db.product.slug == request.args(0)).select(cache=(cache.ram,3600),cacheable=True).first()
    return dict(row_product=row_product)

@cache.action(time_expire=3600, cache_model=cache.ram, quick='SVP')
def article():
    row_article = db.doc(request.args(0))
    return dict(row_article=row_article)


def search():
    result = db(db.product.name.contains(request.vars.q) | 
                db.product.country.contains(request.vars.q)).select(cache=(cache.ram,3600),cacheable=True)
    result2 = db(db.company.name.contains(request.vars.q) | 
                 db.company.country.contains(request.vars.q)).select(cache=(cache.ram,3600),cacheable=True)
    result3 = db(db.person.first_name.contains(request.vars.q) | 
                 db.person.last_name.contains(request.vars.q) |     
                 db.person.email.contains(request.vars.q) | 
                 db.person.ip_address.contains(request.vars.q)).select(cache=(cache.ram,3600),cacheable=True)
    result4 = db(db.doc.title.contains(request.vars.q) | 
                 db.doc.body.contains(request.vars.q)).select(cache=(cache.ram,3600),cacheable=True)
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


def upload():
    url = ""
    form = SQLFORM(db.files, showid=False, formstyle='bootstrap3_stacked')
    if form.accepts(request.vars, session):
        response.flash = T('File uploaded successfully!')
        url = URL(r=request, f="download", args = db(db.files.title==request.vars.title).select(orderby=~db.files.id)[0].uploaded_data)
    return dict(form=form, cknum=request.vars.CKEditorFuncNum, url=url)


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
