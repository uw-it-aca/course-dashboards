<template>
  <div class="row">
    <div class="col-sm-6">
      <SectionProperty
        propertyTitle="Currently Registered"
        :property="registeredString"
      >
        <template #property-icon>
          <i class="bi bi-people-fill" />
        </template>
        <template #property-content>
          <ul class="list-unstyled">
            <li>
              <p v-if="true">10%</p>
              <p class="placeholder-glow" v-else>
                <span class="placeholder col-12"></span>
              </p>
              EOP
            </li>
            <li>20% Transfer</li>
            <li>2% Disabled</li>
            <li>8% Academic Probation</li>
            <li>20% Repeating Students</li>
          </ul>
        </template>
      </SectionProperty>
    </div>
    <div class="col-sm-6">
      <SectionProperty propertyTitle="Median Cumulative GPA" :property="'10%'">
        <template #title-icon>
          <PopoverIcon
            title="Median Cumulative GPA"
            content="This is the midpoint of the cumulative GPAs of the students who are currently in your class.  If the median is lower than past offerings, spend more time on the most challenging topics."
          >
            <i class="bi bi-info-circle-fill" />
          </PopoverIcon>
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
  data() {
    return {
      courses: null,
    };
  },
  setup(props) {
    const { data, isFinished } = useAxios("api/v1/course" + props.sectionLabel);

    return { data, isFinished };
  },
  components: {
    SectionProperty,
    PopoverIcon,
  },
  props: {
    sectionLabel: String,
  },
  computed: {
    registeredString() {
      if (this.isFinished) {
        return (
          this.data.current_enrollment +
          " / " +
          this.data.limit_estimate_enrollment
        );
      }
    },

    currentStudentMajors() {
      return this.data.current_student_majors.slice(0).map((obj) => {
        return {
          percent: obj.percent_students,
          title: obj.major_name,
        };
      });
    },
    concurrentCourses() {
      return this.data.concurrent_courses.slice(0).map((obj) => {
        return {
          percent: obj.percent_students,
          title: obj.course_ref,
        };
      });
    },
  },
  created: function () {},
};
</script>
