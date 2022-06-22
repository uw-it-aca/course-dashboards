<template>
  <axdd-topbar :app-name="'Course Dashboards'" :user-name="'javerage'">
    <template #main>
      <slot name="content" />
    </template>
  </axdd-topbar>
</template>

<script>
import { Topbar } from "axdd-components"
export default {
  name: "LayoutComp",
  components: {
    "axdd-topbar": Topbar
  },
  props: {
    pageTitle: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      // minimum application setup overrides
      appName: "CODA",
      // automatically set year
      currentYear: new Date().getFullYear(),
    };
  },
  created: function () {
    // constructs page title in the following format "Page Title - AppName"
    document.title = this.pageTitle + " - " + this.appName;
  },
};
</script>
