import { createWebHistory, createRouter } from "vue-router";
import { trackRouter } from "vue-gtag-next";

// page components
import Home from "../pages/Home.vue";
import Customize from "../pages/Customize.vue";
import CourseDashboard from "../components/dashboard/CourseDashboard.vue";
import CurrentSection from "../components/dashboard/CurrentSection.vue";
import HistoricData from "../components/dashboard/HistoricSection.vue";

const routes = [
  {
    // TODO: Replace /vue with /
    path: "",
    name: "Home",
    component: Home,
    children: [
      {
        path: ":year(\\d{4})-:quarter([A-Za-z]+)-:curriculum([&% 0-9A-Za-z]+)-:course_number(\\d{3})-:section_id([A-Za-z][0-9A-Za-z]?)",
        components: {
          MyData: CurrentSection,
          // HistoricData: HistoricData,
        },
      },
    ],
  },
  {
    path: "/customize",
    name: "Customize",
    component: Customize,
    pathToRegexpOptions: { strict: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// vue-gtag-next router tracking
trackRouter(router);

export default router;
