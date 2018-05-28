import Vue from 'vue';
import VueRouter from 'vue-router';
import { Administration } from './../templates';
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
      {
        component: Administration,
        path: '/administration',
        children: [
          {
            name: 'intents',
            path: 'intents',
            component: pages.Administration.Intents,
          },
        ],
      },
    ],
  });
}
