import { createWebHistory, createRouter } from "vue-router";
import { trackRouter } from "vue-gtag-next";

// page components
import Home from "../pages/home.vue";
import Customize from "../pages/customize.vue";
import CourseDashboard from "../components/course-dashboard.vue";

const routes = [
  {
    // TODO: Replace /vue with /
    path: "",
    name: "Home",
    component: Home,
    children: [
      {
        path: ':year(\\d{4})-:quarter([A-Za-z]+)-:curriculum([&% 0-9A-Za-z]+)-:course_number(\\d{3})-:section_id([A-Za-z][0-9A-Za-z]?)',
        component: CourseDashboard,
      },
    ]
  },
  {
    path: "/customize",
    name: "Customize",
    component: Customize,
    pathToRegexpOptions: { strict: true },
  },
  // {
  //   path: "/:pathMatch(.*)*",
  //   name: "PageNotFound",
  //   component: Cu,
  //   pathToRegexpOptions: { strict: true },
  // },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// vue-gtag-next router tracking
trackRouter(router);

export default router;
