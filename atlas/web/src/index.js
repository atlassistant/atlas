import Vue from 'vue';
import App from './app.vue';

import './_vars.scss';

const app = new Vue({
    render: h => h(App),
});

app.$mount('#root');
