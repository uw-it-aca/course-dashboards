<template>
  <h2 class="h3 fw-bold">
    Historical Student Data for <span class="text-danger">{{ route.params.curriculum }} {{ route.params.course_number}}</span>
  </h2>

  <div class="row mb-5">
    <div class="col-4 border-end">
      <select
        v-model="selectedOption"
        class="form-select form-select-sm"
        aria-label=""
      >
        <option value="allCourses" selected>All Courses</option>
        <option value="myCourses">Only My Courses</option>
      </select>
    </div>
    <div class="col-6">
      <div v-if="selectedOption === 'allCourses'" class="d-flex">
        <select class="form-select form-select-sm me-2" aria-label="">
          <option selected>All Quarters</option>
          <option value="1">Autumn</option>
          <option value="2">Winter</option>
          <option value="3">Spring</option>
          <option value="4">Summer</option>
        </select>
        <select class="form-select form-select-sm" aria-label="">
          <option selected>All Years</option>
          <option value="1">2022</option>
          <option value="2">2021</option>
          <option value="3">2020</option>
        </select>
      </div>
      <div v-else>
        <select class="form-select form-select-sm" aria-label="">
          <option disabled>Autumn 2022 (current)</option>
          <option value="1">Spring 2022</option>
        </select>
      </div>
    </div>
  </div>

  <div class="alert alert-dark-beige border-0 small" role="alert">
    <p class="mb-0">
      The query you requested will not generate data. This is a new course, and
      there is no historical information to draw upon.
    </p>
  </div>

  <!-- <PastPerformance :section-label="sectionLabel" /> -->
</template>

<script>
import { get } from "axios";

//import { TabsList, TabsDisplay, TabsItem, TabsPanel } from "axdd-components";

import SectionProperty from "./SectionProperty.vue";
import SectionList from "./SectionList.vue";
import PercentList from "./PercentList.vue";
import Histogram from "../popover/Histogram.vue";
import PopoverIcon from "../popover/PopoverIcon.vue";
import PastPerformance from "./PastPerformance.vue";
import { useRoute } from "vue-router";
export default {
  name: "HistoricSection",
  setup(props) {
    const route = useRoute();
    const sectionLabel = route.fullPath.substring(1);

    return { sectionLabel, route };
  },
  components: {
    SectionProperty,
    SectionList,
    PercentList,
    Histogram,
    PopoverIcon,
    PastPerformance
},
  props: {
    sectionLabel: String,
  },
  computed: {
  },
  methods: {
  },
  data() {
    return {
      selectedOption: "allCourses", // default
    };
  },
};
</script>
