import type { RouteRecordRaw } from "vue-router";

export const appTabs = [
  { name: "about", label: "About", path: "/about" },
  { name: "parsing", label: "Parsing", path: "/parsing" },
  { name: "results", label: "Results", path: "/results" },
];

const routes: RouteRecordRaw[] = [
  {
    path: "/",
    component: () => import("layouts/AppLayout.vue"),
    children: [
      { path: "", redirect: "parsing" },
      {
        path: "parsing",
        name: "parsing",
        component: () => import("pages/ParsingPage.vue"),
      },
      {
        path: "results",
        name: "results",
        component: () => import("pages/ResultsPage.vue"),
      },
      {
        path: "about",
        name: "about",
        component: () => import("pages/AboutPage.vue"),
      },
    ],
  },
];

export default routes;
