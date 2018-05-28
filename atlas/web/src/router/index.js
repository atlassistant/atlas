import Vue from 'vue';
import VueRouter from 'vue-router';
import * as pages from './../pages';

Vue.use(VueRouter);

export default function createRouter() {
  return new VueRouter({
    routes: [
      {
        name: 'home',
        path: '/',
        component: pages.Chat,
      },
    ],
  });
}
