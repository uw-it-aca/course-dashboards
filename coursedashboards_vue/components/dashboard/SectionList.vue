<template>
  <div>
    <div>
      <span class="fs-6 fw-bold">{{ title }}</span>
      <div class="d-inline-block text-primary">
        <PopoverIcon :title="infoTitle" :content="infoContent">
          <i class="bi bi-info-circle-fill" />
        </PopoverIcon>
      </div>
    </div>
    <div>
      {{ subtitle }}
    </div>
    <hr />
    <slot name="content"></slot>
  </div>
</template>

<script>
import PopoverIcon from "../popover/PopoverIcon.vue";
export default {
  name: "SectionList",
  components: {
    PopoverIcon,
  },
  props: {
    title: String,
    subtitle: String,
    infoTitle: String,
    infoContent: String,
  },
  data() {
    return {
    };
  },
  computed: {
  },
  methods: {
  },
  created: function () {
  },
};
</script>

<style scoped>
</style>
