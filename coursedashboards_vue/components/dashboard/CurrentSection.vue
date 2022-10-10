<template>
  <div class="alert alert-beige small" role="alert">
    <p>
      The query you requested will not generate data for one of the following
      reasons:
    </p>
    <ul class="mb-0">
      <li>
        The course you've selected has fewer than 5 students. To protect
        students' privacy, we do not show data on courses with fewer than 5
        students enrolled.
      </li>
      <li>
        To protect you and your colleagues' privacy, we do not show data for a
        single course, unless it's a course you've taught.
      </li>
    </ul>
  </div>

  <CurrentPerformance v-if="isCurrent" :section-label="sectionLabel" />
  <PastPerformance v-else :section-label="sectionLabel" />

  <!-- <div class="row mt-5">
    <div class="col-sm-6">
      <SectionList
        title="Concurrent Courses"
        subtitle="When taking the course"
        infoTitle="Concurrent Courses"
        infoContent="Make connections between your course and other courses your students are taking. The number in parenthesis is the median grade of the course. This provides insight into the difficulty of your students' course load."
      >
        <template #content>
          <PercentList :items="concurrentCourses"> </PercentList>
        </template>
      </SectionList>
    </div>
    <div class="col-sm-6">
      <SectionList
        title="Declared Majors"
        subtitle="When taking the course"
        infoTitle="Declared Majors"
        infoContent="Make the topics you teach more engaging for non-majors who are taking your course."
      >
        <template #content>
          <PercentList :items="currentStudentMajors"> </PercentList>
        </template>
      </SectionList>
    </div>
  </div> -->
</template>

<script>
import { useAxios } from "@vueuse/integrations/useAxios";
import { useRoute } from "vue-router";
import SectionProperty from "./SectionProperty.vue";
import SectionList from "./SectionList.vue";
import PercentList from "./PercentList.vue";
import PopoverIcon from "../popover/PopoverIcon.vue";
import CurrentPerformance from "./CurrentPerformance.vue";
import PastPerformance from "./PastPerformance.vue";
export default {
  name: "CurrentSection",
  data() {
    return {
      courses: null,
    };
  },
  setup(props) {
    const route = useRoute();
    const sectionLabel = route.fullPath.substring(1);

    return { sectionLabel, route };
  },
  components: {
    // SectionProperty,
    // SectionList,
    // PercentList,
    // PopoverIcon,
    PastPerformance,
    CurrentPerformance,
  },
  props: {},
  computed: {
    isCurrent() {
      return this.$store.state.year == this.route.params.year &&
             this.$store.state.quarter == this.route.params.quarter;
    }
  },
  created: function () {},
};
</script>
