// home.vue

<template>
  <layout :page-title="pageTitle">
    <!-- page content -->
    <template #title>
      {{ pageTitle }}
    </template>

    <template #content>
      <intro-modal />
      <content-main />
    </template>
  </layout>
</template>

<script>
import Layout from "../layout.vue";
import ContentMain from '../components/content-main.vue';
import IntroModal from '../components/intro-modal.vue';

export default {
  name: "PagesHome",
  components: {
    'layout': Layout,
    'content-main': ContentMain,
    'intro-modal': IntroModal,
  },
  data() {
    return {
      pageTitle: "Course Dashboard",
    };
  },
  methods: {},
};
</script>
