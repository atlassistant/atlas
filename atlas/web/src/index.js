import Vue from 'vue';

import './_vars.scss';

const app = new Vue({
    render: h => h('p', 'Hello, world from atlas!'),
});

app.$mount('#root');
