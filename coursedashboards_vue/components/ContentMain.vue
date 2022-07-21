<template>
  <div>
    <div v-if="chosenCourse">
      <h2 class="my-4">
        Course Dashboard for
        <div class="dropdown d-inline-block">
          <button class="btn btn-outline-dark dropdown-toggle" type="button" id="dropdownMenuButton1"
            data-bs-toggle="dropdown" aria-expanded="false">
            <MqResponsive target="mobile" class="d-inline-block">
              {{ chosenCourse.curriculum + " " + chosenCourse.course_number + " " + chosenCourse.section_id }}
            </MqResponsive>
            <MqResponsive target="tablet+" class="d-inline-block">
              {{ courseSelectionLabel(chosenCourse) }}
            </MqResponsive>
          </button>
          <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
            <li v-for="(course, index) in currentCourses.filter((c) => c != chosenCourse)" :key="index"
              @click="chosenCourse = course">
              <a class="dropdown-item" href="#">
                {{ courseSelectionLabel(course) }}
              </a>
            </li>
          </ul>
        </div>
      </h2>

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
        We're sorry, but it does not appear you have instructed any courses recently.
      </p>
    </div>
    <div v-else>
      This course does not exist or you are not the instructor of this course.
    </div>
  </div>
</template>

<script>
import { MqResponsive } from "vue3-mq";
import { toSectionLabel } from '../utils';
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
      quarter: '',
    };
  },
  watch: {
    chosenCourse(newCourse) {
      // In case there is an invalid course label entered
      // the chosenCourse will be null and we do nothing.
      if (newCourse) {
        this.$router.push('/' + newCourse.section_label);
      }
    }
  },
  methods: {
    compareLowerCase(s1, s2) {
      return s1.toLowerCase() == s2.toLowerCase();
    },
    courseSelectionLabel(course) {
      return course.curriculum + ' ' + course.course_number + ' ' + course.section_id + ' - ' + course.course_title;
    },
  },
  computed: {
    currentCourses() {
      return this.courses.filter(section => {
        return section.year == this.year && this.compareLowerCase(section.quarter, this.quarter)
      })
    },
    currentMq() {
      console.log(this.mq.current);
      return this.mq.current;
    }
  },
  created: function () {
    this.year = JSON.parse(document.getElementById('year').textContent);
    this.quarter = JSON.parse(document.getElementById('quarter').textContent);
    this.courses = JSON.parse(document.getElementById('section_data').textContent);

    if (JSON.stringify(this.$route.params) == '{}') {
      if (this.currentCourses.length > 0) {
        this.chosenCourse = this.currentCourses[0];
      }
    } else {
      let sectionLabel = toSectionLabel(this.$route.params);
      this.chosenCourse = this.currentCourses.find(course => {
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
