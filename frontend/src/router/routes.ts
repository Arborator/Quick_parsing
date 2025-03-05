import type { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('layouts/AppLayout.vue'),
    children: [
      { path: '', component: () => { return import('src/pages/IndexPage.vue'); }  },
    ]

  },

  // Always leave this as last one,
  // but you can also remove it
 
];

export default routes;
