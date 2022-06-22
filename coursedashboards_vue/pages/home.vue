// home.vue

<template>
  <layout :page-title="pageTitle">
    <!-- page content -->
    <template #title>
      {{ pageTitle }}
    </template>

    <template #description>
      <p class="p-0 col-md-8 lead">
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas eget
        pulvinar est. Sed gravida neque justo, pellentesque finibus velit
        scelerisque eu. Curabitur et dolor luctus, convallis magna at, mollis
        purus. Nunc tincidunt risus quis nisl bibendum volutpat. Praesent ut
        tincidunt ex.
      </p>
    </template>

    <template #content>
      <div class="row">
        <div class="col-md-6">
          <h2>Deployment</h2>
          <ul>
            <li>
              <a
                href="https://github.com/uw-it-aca/django-container"
                target="_blank"
                >Django-Container (1.4.0)</a
              >
            </li>
            <li>Webpack (5.x)</li>
          </ul>

          <h2>Development</h2>
          <p>
            What's included? This template repository is intended to start you
            off with AXDD's supported development stack.
          </p>
          <ul>
            <li>Django (3.2.8)</li>
            <li>Vue (3.x)</li>
          </ul>

          <h2>Design</h2>
          <ul>
            <li>Bootstrap (5.1.3)</li>
            <li>Bootstrap Icons (1.6.0)</li>
          </ul>
        </div>
        <div class="col-md-6">
          <h2>Testing</h2>
          <ul>
            <li>Jest (27.x)</li>
            <li>Vue-Jest (27.x)</li>
            <li>Vue Test Utils (2.x)</li>
          </ul>

          <h2>Linting (code quality)</h2>
          <ul>
            <li>Pycodestyle for Python</li>
            <li>ESLint for JS</li>
            <li>Stylelint for CSS</li>
          </ul>

          <h2>AXDD Libraries</h2>
          <p>
            The following is a list of specific AXDD libraries used in building
            applications.
          </p>
          <ul>
            <li>
              <a
                href="https://github.com/uw-it-aca/django-container"
                target="_blank"
                >Django-Container (1.4.0)</a
              >
            </li>
            <li>
              <a
                href="https://github.com/uw-it-aca/axdd-components"
                target="_blank"
                >AXDD-Components (1.0.4)</a
              >
            </li>
          </ul>
        </div>

        <hr />

        <div class="col-md-6">
          <h2>JS Libraries</h2>
          <p>
            The following is a list of common JS libraries included in this
            repository.
          </p>
          <ul>
            <li>
              <a href="https://axios-http.com/" target="_blank">axios</a>
            </li>
          </ul>

          <h2>Vue Libraries</h2>
          <p>
            The following is a list of common Vue libraries included in this
            repository.
          </p>
          <ul>
            <li>
              <a
                href="https://matteo-gabriele.gitbook.io/vue-gtag/v/next/"
                target="_blank"
                >vue-gtag-next (vue3)</a
              >
            </li>
            <li>
              <a href="https://github.com/KanHarI/vue3-cookies" target="_blank"
                >vue3-cookies</a
              >
            </li>
            <li>
              <a href="https://github.com/craigrileyuk/vue3-mq" target="_blank"
                >vue3-mq</a
              >
            </li>
          </ul>
        </div>
        <div class="col-md-6">
          <h2>Customization</h2>
          <p>
            Ready to go beyond the starter template and start buidling your
            application? Read about how to
            <a href="/customize">customize</a> your application.
          </p>
        </div>
      </div>
    </template>
  </layout>
</template>

<script>
import Layout from "../layout.vue";

export default {
  name: "PagesHome",
  components: {
    layout: Layout,
  },
  data() {
    return {
      pageTitle: "Getting started",
    };
  },
  methods: {},
};
</script>
