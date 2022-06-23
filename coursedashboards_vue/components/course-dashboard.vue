<template>
  <p>Course Dashboard for course:
    {{ $route.params.year }}
    {{ $route.params.quarter }}
    {{ $route.params.curriculum }}
    {{ $route.params.course_number }}
    {{ $route.params.section_id }}
  </p>
</template>

<script>
export default {
  name: "CourseDashboard",
  data() {
    return {
      currentCourse: "POL S 201 A - INTRODUCTION TO POLITICAL THEORY",
      courses: ["POL S 201 A - INTRODUCTION TO POLITICAL THEORY", "ESS 102 A - SPACE & SPACE TRAVEL", "ESS 103 A - SPACE & SPACE TRAVEL"],
    };
  },
  methods: {
  },
  created: function () {
  },
};
</script>
