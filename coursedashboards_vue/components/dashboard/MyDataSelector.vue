<template>
  <h2 class="h3 fw-bold">
    My Data for
    <span class="text-danger">{{ courseId.replaceAll("-", " ") }}</span>
    <a
      class="float-end fs-5"
      href="https://my.uw.edu/teaching/"
      target="_blank"
      title="View course details in Teaching page"
    >
      <i class="bi bi-box-arrow-up-right me-1" />Course Details
      <!-- <span class="sr-only">
        for {{ curriculum }} {{ course_number }} {{ section_id }}</span
      > -->
    </a>
  </h2>

  <div class="row mb-5">
    <div class="col-6">
      <select
        class="form-select form-select-sm"
        aria-label=""
        @change="setTerm"
      >
        <option
          v-for="term in terms"
          :key="term"
          :value="term.section_label"
          :selected="term.section_label == selectedTerm.section_label"
        >
          {{ termTextLabel(term) }}
        </option>
      </select>
    </div>
  </div>
</template>

<script>
import { toSectionLabel } from "../../helpers/utils";
export default {
  name: "MyDataSelector",
  data() {
    return {
      courses: [],
    };
  },
  computed: {
    courseId() {
      const params = this.$route.params;
      return (
        params.curriculum + "-" + params.course_number + "-" + params.section_id
      );
    },
    terms() {
      return this.courses.filter((course) => {
        return (
          course.curriculum +
            "-" +
            course.course_number +
            "-" +
            course.section_id ==
          this.courseId
        );
      });
    },
    selectedTerm() {
      return this.terms.find((term) => {
        return term.section_label == toSectionLabel(this.$route.params);
      });
    },
  },
  methods: {
    setTerm(e) {
      const newTerm = e.target.value;
      this.$router.push("/" + newTerm);
    },
    termTextLabel(term) {
      return (
        term.quarter[0].toUpperCase() + term.quarter.slice(1) + " " + term.year
      );
    },
  },
  created: function () {
    this.courses = JSON.parse(
      document.getElementById("section_data").textContent
    );
  },
};
</script>
