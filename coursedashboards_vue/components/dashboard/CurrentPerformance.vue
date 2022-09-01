<template>
  <div class="row">
    <div class="col-sm-6">
      <SectionProperty
        propertyTitle="Currently Registered"
        :loading="!courseIsFinished"
      >
        <template #property-content>
          {{
            courseData.current_enrollment +
            " / " +
            courseData.limit_estimate_enrollment
          }}
        </template>
        <template #property-icon>
          <i class="bi bi-people-fill" />
        </template>
      </SectionProperty>
      <ul class="list-unstyled">
        <li>
          <span v-if="!profileIsFinished" class="placeholder-glow placeholder"
            >12%</span
          >
          <span v-else
            >{{ Math.round(profileData.disability.percent, 2) }}%</span
          >
          Disability
        </li>
        <li>
          <span v-if="!profileIsFinished" class="placeholder-glow placeholder"
            >12%</span
          >
          <span v-else>{{ Math.round(profileData.eop.percent, 2) }}%</span> EOP
        </li>
        <li>
          <span v-if="!profileIsFinished" class="placeholder-glow placeholder"
            >12%</span
          >
          <span v-else
            >{{ Math.round(profileData.probation.percent, 2) }}%</span
          >
          Probation
        </li>
        <li>
          <span v-if="!profileIsFinished" class="placeholder-glow placeholder"
            >12%</span
          >
          <span v-else>{{ Math.round(profileData.transfer.percent, 2) }}%</span>
          transfer
        </li>
      </ul>
    </div>
    <div class="col-sm-6">
      <SectionProperty
        propertyTitle="Median Cumulative GPA"
        :loading="!courseIsFinished"
      >
        <template #title-icon>
          <PopoverIcon
            title="Median Cumulative GPA"
            content="This is the midpoint of the cumulative GPAs of the students who are currently in your class.  If the median is lower than past offerings, spend more time on the most challenging topics."
          >
            <i class="bi bi-info-circle-fill" />
          </PopoverIcon>
        </template>
        <template #property-content>
          {{
            courseData.current_enrollment +
            " / " +
            courseData.limit_estimate_enrollment
          }}
        </template>
        <template #property-icon>
          <i class="bi bi-bar-chart-fill"></i>
        </template>
      </SectionProperty>

      <SectionProperty propertyTitle="Drop/Fail Prediction" :property="'10%'">
        <template #title-icon>
          <i class="bi bi-info-circle-fill" />
        </template>
        <template #property-icon>
          <i class="bi bi-flag-fill" />
        </template>
      </SectionProperty>
    </div>
  </div>
</template>

<script>
import { useAxios } from "@vueuse/integrations/useAxios";
import SectionProperty from "./SectionProperty.vue";
import PopoverIcon from "../popover/PopoverIcon.vue";
export default {
  name: "CurrentPerformance",
  setup(props) {
    const { data: courseData, isFinished: courseIsFinished } = useAxios(
      "api/v1/course" + props.sectionLabel
    );

    const { data: profileData, isFinished: profileIsFinished } = useAxios(
      "api/v1/course" + props.sectionLabel + "/profile"
    );

    return { profileData, profileIsFinished, courseData, courseIsFinished };
  },
  components: {
    SectionProperty,
    PopoverIcon,
  },
  props: {
    sectionLabel: String,
  },
  methods: {},
  computed: {
    // currentStudentMajors() {
    //   return this.data.current_student_majors.slice(0).map((obj) => {
    //     return {
    //       percent: obj.percent_students,
    //       title: obj.major_name,
    //     };
    //   });
    // },
    // concurrentCourses() {
    //   return this.data.concurrent_courses.slice(0).map((obj) => {
    //     return {
    //       percent: obj.percent_students,
    //       title: obj.course_ref,
    //     };
    //   });
    // },
  },
  created: function () {},
};
</script>
