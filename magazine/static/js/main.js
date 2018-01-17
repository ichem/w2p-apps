Vue.component('product',{
    template: ` <div class="row"> <div class="col-md-3"> <i><h5>Search by country</h5></i> <select v-model="search"> <option>EU</option> <option>USA</option> <option>JAPAN</option> <option>UK</option> <option>PRC</option> <option>JAR</option> <option>CRO</option> <option value="{{Product | orderBy 'id' -1}}">ALL</option> </select> <hr> <i><h5>Search by type</h5></i> <select v-model="search"> <option>INSTRUMENTS</option> <option>SOFTWARE</option> <option>SMARTPHONE</option> <option value="{{Product | orderBy 'id' -1}}">ALL</option> </select> </div><br><div class="col-md-9"> <div v-for="item in product | orderBy 'id' -1 | filterBy search"> <h2><a href="/app7/product/{{item.slug}}">{{item.name}}</a></h2> <p>{{{item.description.slice(0,250)}}}</p><p>{{item.product_type}}</p><h4><b>{{item.country}}</b></h4> <hr> </div></div></div>`,
    data() {
        return {
            product: [],
            search: [],
        }
    },
    ready() {
        this.$http.get('/app7/api/product').then((response) => {
            this.$set('product', response.json())
        })
    },
});

Vue.component('person', {
    template: ` <div class="row"> <div class="col-md-3"> <i><h5>Search by name</h5></i> <select v-model="search"> <option>Frank</option> <option>Louise</option> <option>Jane</option> <option>Mary</option> <option>Sean</option> <option>Ronald</option> <option>Maria</option> <option value="{{Product | orderBy 'id' -1}}">ALL</option> </select> </div><br><div class="col-md-9"> <div v-for="item in person | orderBy 'id' 1 | filterBy search"> <h2><a href="/app7/person/{{item.id}}/{{item.first_name.toLowerCase() + '-' + item.last_name.toLowerCase()}}">{{item.first_name}} {{item.last_name}}</a></h2> <p>{{item.email}}</p><p>{{item.ip_address}}</p><hr> </div></div></div>`,
    data() {
        return {
            person: [],
            search: [],
        }
    },
    ready() {
        this.$http.get('/app7/api/person').then((response) => {
            this.$set('person', response.json())
        })
    },
});

Vue.component('company', {
    template: ` <div class="row"> <div class="col-md-3"> <i><h5>Search by country</h5></i> <select v-model="search"> <option>EU</option> <option>USA</option> <option value="{{Company | orderBy 'id' -1}}">ALL</option> </select> </div><br><div class="col-md-9"> <div v-for="item in company | orderBy 'id' -1 | filterBy search"> <h2><a href="/app7/company/{{item.slug}}">{{item.name}}</a></h2> <p>{{item.country}}</p><hr> </div></div></div></div>`,
    data() {
        return {
            company: [],
            search: [],
        }
    },
    ready() {
        this.$http.get('/app7/api/company').then((response) => {
            this.$set('company', response.json())
        })
    },
});
Vue.component('magazine', {
    template: ` <div class="row"> <div class="col-md-3"> <i><h5>Search by country</h5></i> <select v-model="search"> <option>USA</option> <option>EU</option> <option value="{{Doc | orderBy 'id' -1}}">ALL</option> </select> </div><br><div class="col-md-9"> <div v-for="item in doc | orderBy 'id' -1 | filterBy search"> <h2><a href="/app7/article/{{item.id}}">{{item.title}}</a></h2> <p>{{item.body}}</p><hr> </div></div></div>`,
    data() {
        return {
            doc: [],
            search: [],
        }
    },
    ready() {
        this.$http.get('/app7/api/doc').then((response) => {
            this.$set('doc', response.json())
        })
    },
});
new Vue({
    el: '#app',
})
