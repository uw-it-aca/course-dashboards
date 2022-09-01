<template>
  <div class="border border-light p-3 mb-3 rounded-3">
    <div class="">
      <span class="text-black-50">
        {{ propertyTitle }}
      </span>
      <div class="d-inline-block text-primary ms-1">
        <slot name="title-icon" />
      </div>
    </div>
    <div class="fs-1">
      <div v-if="loading" class="d-inline-block w-50">
        <p class="placeholder-glow">
          <span class="placeholder col-12"></span>
        </p>
      </div>
      <slot v-else name="property-content" />
      <!-- <span v-if="loading">Loading</span>
      <span v-else-if="property != null" v-text="property"></span>
      <span v-else>N/A</span> -->
      <div class="d-inline-block text-black-50 fs-3 ms-1">
        <slot name="property-icon" />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "SectionProperty",
  components: {},
  props: {
    propertyTitle: String,
    // property: [String, Number],
    loading: Boolean,
  },
  data() {
    return {};
  },
  methods: {
    asd() {
      console.log("asd");
    },
  },
  created: function () {},
};
</script>
