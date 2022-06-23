<template>
  <div>
    <h2 class="my-4">
      Course Dashboard for
      <div class="dropdown d-inline-block">
        <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton1" data-bs-toggle="dropdown" aria-expanded="false">
          {{ currentCourse.section_label }}
        </button>
        <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
          <li
            v-for="(course, index) in courses.filter((c) => c != currentCourse)"
            :key="index"
            @click="currentCourse = course"
          >
            <a class="dropdown-item" href="#">
              {{ course.section_label }}
            </a>
          </li>
        </ul>
      </div>
    </h2>
    
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: "ContentMain",
  data() {
    return {
      currentCourse: null,
      courses: null,
    };
  },
  watch: {
    currentCourse(newCourse) {
      this.$router.push('/vue/' + newCourse.section_label);
    }
  },
  methods: {
    compareLowerCase(s1, s2) {
      return s1.toLowerCase() == s2.toLowerCase();
    },
  },
  created: function () {
    const year = JSON.parse(document.getElementById('year').textContent);
    const quarter = JSON.parse(document.getElementById('quarter').textContent);
    
    let section_data = JSON.parse(document.getElementById('section_data').textContent);
    this.courses = section_data.filter((section) => {
      return section.year == year && this.compareLowerCase(section.quarter, quarter)
    });
    this.currentCourse = this.courses[0];
  },
};
</script>
