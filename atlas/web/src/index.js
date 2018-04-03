import Vue from 'vue';
import { Chat } from './pages';

import './_vars.scss';
import './_main.scss';

const app = new Vue({
    render: h => h(Chat),
});

app.$mount('#root');
