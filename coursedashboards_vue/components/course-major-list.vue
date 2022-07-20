<template>
  <div>
    <div>
      <span class="fs-6 fw-bold">{{ title }}</span>
      <div class="d-inline-block text-primary">
        <slot name="title-icon" />
      </div>
    </div>
    <div>
      {{ subtitle }}
    </div>
    <hr />
    <TransitionGroup name="list" tag="ul">
      <li v-for="item in itemsToBeDisplayed" :key="item">
        <span v-if="item.percent < 1">&lt;1% </span>
        <span v-else>{{ Math.round(item.percent) }}% </span>
        {{ item.title }}
      </li>
    </TransitionGroup>
    <button v-if="length < items.length" class="btn btn-small btn-primary" @click="viewAll">View all</button>
    <button v-else-if="length == items.length && length > 5" @click="viewLess">View less</button>
    <!-- <div class="">
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
    </div> -->
  </div>
</template>

<script>
export default {
  name: "CourseMajorList",
  components: {
  },
  props: {
    title: String,
    subtitle: String,
    items: Array,
  },
  data() {
    return {
      length: 5,
    };
  },
  computed: {
    itemsToBeDisplayed() {
      return this.items.slice(0, this.length);
    }
  },
  methods: {
    viewAll() {
      this.length = this.items.length;
    },
    viewLess() {
      this.length = 5;
    },
  },
  created: function () {
  },
};
</script>

<style scoped>
ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.list-enter-active,
.list-leave-active {
  transition: all 0.5s ease;
}
.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
</style>
