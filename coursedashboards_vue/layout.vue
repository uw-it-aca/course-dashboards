<template>
  <axdd-topbar
    :app-name="appName"
    :app-root-url="appRootUrl"
    :user-name="user.netid"
    :sign-out-url="signOutUrl"
  >
    <template #profile>
      <a
        href="https://my.uw.edu/profile"
        title="View MyUW Profile"
        class="text-light-gray"
      >
        <i class="bi bi-person-fill me-1" />{{ user.netid }}
      </a>
      <a :href="signOutUrl" class="float-end text-light-gray" title="Sign out">
        <i class="bi bi-box-arrow-in-right me-1" />Sign out
      </a>
    </template>
    <template #main>
      <slot name="content" />
    </template>
    <template #footer />
  </axdd-topbar>
</template>

<script>
import { Topbar } from "axdd-components";
export default {
  name: "LayoutComp",
  components: {
    "axdd-topbar": Topbar,
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
      appName: "Course Dashboard",
      appRootUrl: "/",
      user: null,
      signOutUrl: "/saml/logout",
    };
  },
  created: function () {
    this.user = JSON.parse(document.getElementById("user").textContent);
    // constructs page title in the following format "Page Title - AppName"
    document.title = this.pageTitle + " - " + this.appName;
  },
};
</script>
