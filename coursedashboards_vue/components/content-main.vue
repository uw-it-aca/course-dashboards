// hello-world.vue

<template>
  <div>
    <h2 class="d-inline">
      Course Dashboard for
    </h2>
    <div class="dropdown d-inline">
      <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton1" data-bs-toggle="dropdown" aria-expanded="false">
        {{ currentCourse }}
      </button>
      <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
        <li
          v-for="(course, index) in courses.filter((c) => c != currentCourse)"
          :key="index"
          @click="currentCourse = course"
        >
          <a class="dropdown-item" href="#">{{ course }}</a>
        </li>
      </ul>
    </div>
    <div>
      DASHBOARD
    </div>
  </div>
</template>

<script>
export default {
  name: "ContentMain",
  data() {
    return {
      currentCourse: 'None',
      courses: ['Course 1', 'Course 2', 'Course 3', 'Course 4'],
    };
  },
  methods: {},
};
</script>
