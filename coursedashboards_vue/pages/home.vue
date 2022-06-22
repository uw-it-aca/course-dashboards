// home.vue

<template>
  <layout :page-title="pageTitle">
    <!-- page content -->
    <template #title>
      {{ pageTitle }}
    </template>

    <template #content>
      <content-main />
    </template>
  </layout>
</template>

<script>
import Layout from "../layout.vue";
import ContentMain from '../components/content-main.vue';

export default {
  name: "PagesHome",
  components: {
    layout: Layout,
    'content-main': ContentMain,
  },
  data() {
    return {
      pageTitle: "Course Dashboard",
    };
  },
  methods: {},
};
</script>
