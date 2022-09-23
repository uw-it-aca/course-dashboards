<template>
  <div class="row">
    <div class="col-sm-6">
      <SectionProperty
        :propertyTitle="
          'Students / ' + offering + ' Offerings'
        "
        :loading="!pastPerfFinished"
      >
        <template #property-icon>
          <i class="bi bi-people-fill" />
        </template>
        <template #property-content>
          {{ performance.performance?.enrollment }}
        </template>
      </SectionProperty>
    </div>
    <div class="col-sm-6">
      <SectionProperty
        propertyTitle="Median Cumulative GPA"
        :loading="!pastPerfFinished"
      >
        <template #title-icon>
          <PopoverIcon
            title="Percent Failure"
            content="This is the percent of students who received a 0.0 in the course(s) based on the time frame selected above.  Get a sense of how much time you should spend on challenging topics, considering how much students have struggled with the course in the past."
          >
            <i class="bi bi-info-circle-fill" />
          </PopoverIcon>
        </template>
        <template #property-content>
          {{ medianGpas }}
        </template>
        <template #property-icon>
          <!-- <Histogram :data="performance.gpas" /> -->
        </template>
      </SectionProperty>
    </div>
    <div class="col-sm-6">
      <SectionProperty
        propertyTitle="Percent Failure"
        :loading="!pastPerfFinished"
      >
        <template #title-icon>
          <i class="bi bi-info-circle-fill" />
        </template>
        <template #property-icon>
          <i class="bi bi-flag-fill" />
        </template>
        <template #property-content>
          {{ failureRate }}%
        </template>
      </SectionProperty>
    </div>
    <div class="col-sm-6">
      <SectionProperty
        propertyTitle="Median Course Grade"
        :loading="!pastPerfFinished"
      >
        <template #title-icon>
          <i class="bi bi-info-circle-fill" />
        </template>
        <template #property-icon>
          <i class="bi bi-bar-chart-fill"></i>
        </template>
        <template #property-content>
          {{ medianCourseGrades }}
        </template>
      </SectionProperty>
    </div>
  </div>

  <div class="row mt-3">
    <div class="col-sm-6">
      <SectionList
        title="Concurrent Courses"
        subtitle="When taking the course"
        infoTitle="Concurrent Courses"
        infoContent="Compare the proportion of certain majors in your class..."
      >
        <template #content>
          <PercentList :items="studentMajorsList"> </PercentList>
        </template>
      </SectionList>
    </div>
    <div class="col-sm-6">
      <SectionList
        title="Declared Majors"
        subtitle="When taking the course"
        infoTitle="Declared Majors"
        infoContent="Compare the proportion of certain majors in your class..."
      >
        <template #content>
          <PercentList :items="studentMajorsList"> </PercentList>
        </template>
      </SectionList>
    </div>
  </div>
</template>

<script>
import { useAxios } from "@vueuse/integrations/useAxios";
//import { TabsList, TabsDisplay, TabsItem, TabsPanel } from "axdd-components";

import SectionProperty from "./SectionProperty.vue";
import SectionList from "./SectionList.vue";
import PercentList from "./PercentList.vue";
import Histogram from "../popover/Histogram.vue";
import PopoverIcon from "../popover/PopoverIcon.vue";
export default {
  name: "PastPerformance",
  setup(props) {
    const { data: pastPerformance, isFinished: pastPerfFinished } = useAxios(
      "api/v1/course/" + props.sectionLabel + "/past/performance"
    );
    
    const { data: pastStudentMajors, isFinished: pastStuFinished} = useAxios(
      "api/v1/course/" + props.sectionLabel + "/past/studentmajor"
    );

    const { data: pastGraduatedMajors, isFinished: pastGradFinished } = useAxios(
      "api/v1/course/" + props.sectionLabel + "/past/graduatedmajor"
    );

    return {
      performance: pastPerformance,
      studentMajors: pastStudentMajors,
      graduatedMajors: pastGraduatedMajors,
      pastPerfFinished,
      pastStuFinished,
      pastGradFinished
    };
  },
  components: {
    SectionProperty,
    SectionList,
    PercentList,
    Histogram,
    PopoverIcon,
  },
  props: {
    sectionLabel: String,
  },
  computed: {
    offering() {
      if (!this.performance) return "";
      return this.performance.performance?.offering_count;
    },
    medianGpas() {
      if (!this.performance) return null;
      return this.median(this.performance.performance?.gpas);
    },
    medianCourseGrades() {
      if (!this.performance) return null;
      return this.median(this.performance.performance?.course_grades);
    },
    studentMajorsList() {
      if (!this.studentMajors) return [];
      return this.studentMajors.student_majors.slice(0).map((obj) => {
        return {
          percent: obj.percent_students,
          title: obj.major_name,
        };
      });
    },
    graduatedMajorsList() {
      if (!this.graduatedMajors) return [];
      return this.graduatedMajors.graduated_majors.slice(0).map((obj) => {
        return {
          percent: obj.percent_students,
          title: obj.major_name,
        };
      });
    },
    failureRate() {
      if (!this.performance) return null;
      return Math.round(
        (this.performance.performance.course_grades.filter((grade) => grade <= 0.7).length /
          this.performance.performance.course_grades.length) *
          100
      );
    },
  },
  methods: {
    median(arr) {
      const mid = Math.floor(arr.length / 2),
        nums = [...arr].sort((a, b) => a - b);
      return arr.length % 2 !== 0 ? nums[mid] : (nums[mid - 1] + nums[mid]) / 2;
    },
  },
  data() {
    return {
      selectedOption: "allCourses", // default
    };
  },
};
</script>
