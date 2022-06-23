<template>
  <axdd-topbar
    :app-name="'Course Dashboards'"
    :user-name="this.user.netid"
  >
    <template #main>
      <slot name="content" />
    </template>
    <template #footer />
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
      user: null,
    };
  },
  created: function () {
    this.user = JSON.parse(document.getElementById('user').textContent);
    // constructs page title in the following format "Page Title - AppName"
    document.title = this.pageTitle + " - " + this.appName;
  },
};
</script>
