import Vue from 'vue';
import VueRouter from 'vue-router';
import { Administration, Comprehension, Execution } from './../templates';
import * as pages from './../pages';

Vue.use(VueRouter);

export default function createRouter() {
  return new VueRouter({
    routes: [
      {
        name: 'home',
        path: '/',
        component: pages.Chat,
        meta: {
          breadcrumb: 'Home',
        },
      },
      {
        component: Administration,
        path: '/administration',
        meta: {
          breadcrumb: 'Administration',
        },
        children: [
          {
            path: 'comprehension',
            meta: {
              breadcrumb: 'Comprehension',
            },
            component: Comprehension,
            children: [
              {
                name: 'intents',
                path: 'intents',
                component: pages.Administration.Intents,
                meta: {
                  breadcrumb: 'Intents',
                },
              },
              {
                name: 'entities',
                path: 'entities',
                component: pages.Administration.Entities,
                meta: {
                  breadcrumb: 'Entities',
                },
              },
            ],
          },
          {
            path: 'execution',
            meta: {
              breadcrumb: 'Execution',
            },
            component: Execution,
            children: [
              {
                name: 'skills',
                path: 'skills',
                component: pages.Administration.Skills,
                meta: {
                  breadcrumb: 'Skills',
                },
              },
              {
                name: 'settings',
                path: 'settings',
                component: pages.Administration.Settings,
                meta: {
                  breadcrumb: 'Settings',
                },
              },
            ],
          },
        ]
      },
    ],
  });
}
