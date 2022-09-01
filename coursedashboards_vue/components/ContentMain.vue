<template>
  <div>
    <div v-if="chosenCourse">
      <h1 class="h2 my-4 fw-bold">
        Course Dashboard for
        <div class="d-inline-block">
          <select
            class="form-select form-select mb-3"
            aria-label=""
            @change="setChosenCourse"
            :value="chosenCourseLabel"
          >
            <option
              v-for="(courses, course_id) in uniqueSections"
              :key="course_id"
              :value="course_id"
            >
              {{ courseSelectionLabel(courses[0]) }}
            </option>
          </select>
        </div>
      </h1>
      <CourseDashboard />
    </div>
    <div v-else-if="courses.length == 0">
      <p>
        We're sorry, but it does not appear you have instructed any courses
        recently.
      </p>
    </div>
    <div v-else>
      This course does not exist or you are not the instructor of this course.
    </div>
  </div>
</template>

<script>
import { MqResponsive } from "vue3-mq";
import { toSectionLabel } from "../helpers/utils";
import CourseDashboard from "./dashboard/CourseDashboard.vue";
export default {
  name: "ContentMain",
  components: {
    MqResponsive,
    CourseDashboard,
  },
  inject: ["mq"],
  data() {
    return {
      chosenCourse: null,
      courses: [],
      year: 0,
      quarter: "",
    };
  },
  watch: {
    chosenCourse(newCourse) {
      // In case there is an invalid course label entered
      // the chosenCourse will be null and we do nothing.
      if (newCourse) {
        this.$router.push("/" + newCourse.section_label);
      }
    },
  },
  methods: {
    compareLowerCase(s1, s2) {
      return s1.toLowerCase() == s2.toLowerCase();
    },
    courseSelectionLabel(course) {
      return (
        course.curriculum +
        " " +
        course.course_number +
        " " +
        course.section_id +
        " - " +
        course.course_title
      );
    },
    setChosenCourse(e) {
      const courseLabel = e.target.value;
      this.chosenCourse =
        this.uniqueSections[courseLabel][
          this.uniqueSections[courseLabel].length - 1
        ];
    },
  },
  computed: {
    firstCourseRecentQuarter() {
      const mostRecentCourse = this.courses[this.courses.length - 1];
      return this.courses.filter((section) => {
        return (
          section.year == mostRecentCourse.year &&
          this.compareLowerCase(section.quarter, mostRecentCourse.quarter)
        );
      })[0];
    },
    uniqueSections() {
      return this.courses.slice().reduce((prev, curr) => {
        const course_id =
          curr.curriculum + "-" + curr.course_number + "-" + curr.section_id;
        if (prev[course_id] == undefined) {
          prev[course_id] = [curr];
        } else {
          prev[course_id].push(curr);
        }
        return prev;
      }, {});
    },
    chosenCourseLabel() {
      return (
        this.chosenCourse.curriculum +
        "-" +
        this.chosenCourse.course_number +
        "-" +
        this.chosenCourse.section_id
      );
    },
  },
  created: function () {
    this.year = JSON.parse(document.getElementById("year").textContent);
    this.quarter = JSON.parse(document.getElementById("quarter").textContent);
    this.courses = JSON.parse(
      document.getElementById("section_data").textContent
    );
    console.log(this.courses);

    if (JSON.stringify(this.$route.params) == "{}") {
      if (this.courses.length > 0) {
        this.chosenCourse = this.firstCourseRecentQuarter;
      }
    } else {
      let sectionLabel = toSectionLabel(this.$route.params);
      this.chosenCourse = this.courses.slice().find((course) => {
        return course.section_label == sectionLabel;
      });
    }
  },
};
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
