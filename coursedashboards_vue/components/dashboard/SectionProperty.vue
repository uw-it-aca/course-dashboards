<template>
  <div>
    <div class="">
      <span class="text-black-50">
        {{ propertyTitle }}
      </span>
      <div class="d-inline-block text-primary">
        <slot name="title-icon" />
      </div>
    </div>
    <div class="fs-1">
      <span v-if="property != null" v-text="property"></span>
      <span v-else>N/A</span>
      <div class="d-inline-block text-black-50 fs-3">
        <slot name="property-icon" />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "SectionProperty",
  components: {
  },
  props: {
    propertyTitle: String,
    property: [String, Number],
  },
  data() {
    return {
    };
  },
  methods: {
    asd() {
      console.log('asd');
    }
  },
  created: function () {
  },
};
</script>
