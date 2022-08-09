<template>
  <div>
    <div v-if="chosenCourse">
      <h1 class="my-4">
        Course Dashboard for:
        <div class="d-inline-block">
          <select
            class="form-select form-select-lg mb-3"
            aria-label=".form-select-lg example"
            v-model="chosenCourse"
          >
            <option
              v-for="(course, index) in currentCourses"
              :key="index"
              :value="course"
            >
              {{ courseSelectionLabel(course) }}
            </option>
          </select>
        </div>
      </h1>

      <router-view v-slot="{ Component }">
        <!-- <Transition name="fade" mode="out-in"> -->
        <KeepAlive max="5">
          <component :is="Component" :key="$route.fullPath" />
        </KeepAlive>
        <!-- </Transition> -->
      </router-view>
    </div>
    <div v-else-if="currentCourses.length == 0">
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
export default {
  name: "ContentMain",
  components: {
    MqResponsive,
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
    onChange(event) {
      console.log(event.target.value);
    },
  },
  computed: {
    currentCourses() {
      return this.courses.filter((section) => {
        return (
          section.year == this.year &&
          this.compareLowerCase(section.quarter, this.quarter)
        );
      });
    },
    currentMq() {
      console.log(this.mq.current);
      return this.mq.current;
    },
  },
  created: function () {
    this.year = JSON.parse(document.getElementById("year").textContent);
    this.quarter = JSON.parse(document.getElementById("quarter").textContent);
    this.courses = JSON.parse(
      document.getElementById("section_data").textContent
    );

    if (JSON.stringify(this.$route.params) == "{}") {
      if (this.currentCourses.length > 0) {
        this.chosenCourse = this.currentCourses[0];
      }
    } else {
      let sectionLabel = toSectionLabel(this.$route.params);
      this.chosenCourse = this.currentCourses.find((course) => {
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
