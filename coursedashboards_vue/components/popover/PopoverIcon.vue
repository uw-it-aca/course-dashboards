<template>
  <a ref="popover" tabindex="0" role="button" data-bs-toggle="popover" data-bs-trigger="focus" :data-bs-title="title"
    :data-bs-content="content" data-bs-placement="top">
    <slot />
  </a>
</template>

<script>
import { Popover } from "bootstrap";
export default {
  name: "PopoverIcon",
  props: {
    title: String,
    content: String,
  },
  mounted: function () {
    const popoverTriggerEl = new Popover(this.$refs.popover);
  },
};
</script>
