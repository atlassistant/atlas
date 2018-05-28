import Vue from 'vue';
import createRouter from './router';
import createStore from './store';

import './_vars.scss';
import './_main.scss';

const router = createRouter();
const store = createStore();

const app = new Vue({
    router,
    store,
    render: h => h('router-view'),
});

app.$mount('#root');
