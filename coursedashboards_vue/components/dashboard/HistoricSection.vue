<template>
  <h2>Historic Section</h2>
  <div class="d-flex">
    <ul class="nav nav-pills">
      <li class="nav-item dropdown">
        <a
          class="nav-link dropdown-toggle"
          data-bs-toggle="dropdown"
          href="#"
          role="button"
          aria-expanded="false"
          >All Offerings</a
        >
        <ul class="dropdown-menu">
          <li><a class="dropdown-item" href="#">All Offerings</a></li>
          <li><a class="dropdown-item" href="#">Only My Offerings</a></li>
        </ul>
      </li>
      <li class="nav-item dropdown">
        <a
          class="nav-link dropdown-toggle"
          data-bs-toggle="dropdown"
          href="#"
          role="button"
          aria-expanded="false"
          >All Quarters</a
        >
        <ul class="dropdown-menu">
          <li><a class="dropdown-item" href="#">All Quarters</a></li>
          <li><hr class="dropdown-divider" /></li>
          <li><a class="dropdown-item" href="#">Autumn</a></li>
          <li><a class="dropdown-item" href="#">Winter</a></li>
          <li><a class="dropdown-item" href="#">Spring</a></li>
        </ul>
      </li>
      <li class="nav-item dropdown">
        <a
          class="nav-link dropdown-toggle"
          data-bs-toggle="dropdown"
          href="#"
          role="button"
          aria-expanded="false"
          >All Years</a
        >
        <ul class="dropdown-menu">
          <li><a class="dropdown-item" href="#">All Years</a></li>
          <li><hr class="dropdown-divider" /></li>
          <li><a class="dropdown-item" href="#">2013</a></li>
          <li><a class="dropdown-item" href="#">2014</a></li>
        </ul>
      </li>
    </ul>
  </div>
  <div class="row">
    <div class="col-sm-6">
      <SectionProperty
        :propertyTitle="
          'Students / ' + performance.offering_count + ' Offerings'
        "
        :property="performance.enrollment"
      >
        <template #property-icon>
          <i class="bi bi-people-fill" />
        </template>
      </SectionProperty>
    </div>
    <div class="col-sm-6">
      <SectionProperty
        propertyTitle="Percent Failure"
        :property="failureRate + '%'"
      >
        <template #title-icon>
          <PopoverIcon
            title="Percent Failure"
            content="This is the percent of students who received a 0.0 in the course(s) based on the time frame selected above.  Get a sense of how much time you should spend on challenging topics, considering how much students have struggled with the course in the past."
          >
            <i class="bi bi-info-circle-fill" />
          </PopoverIcon>
        </template>
        <template #property-icon>
          <i class="bi bi-flag-fill" />
        </template>
      </SectionProperty>
    </div>

    <div class="col-sm-6">
      <SectionProperty
        propertyTitle="Median Cumulative GPA"
        :property="medianGpas"
      >
        <template #title-icon>
          <i class="bi bi-info-circle-fill" />
        </template>
        <template #property-icon>
          <Histogram :data="performance.gpas" />
        </template>
      </SectionProperty>
    </div>
    <div class="col-sm-6">
      <SectionProperty
        propertyTitle="Median Course Grade"
        :property="medianCourseGrades"
      >
        <template #title-icon>
          <i class="bi bi-info-circle-fill" />
        </template>
        <template #property-icon>
          <i class="bi bi-bar-chart-fill"></i>
        </template>
      </SectionProperty>
    </div>
  </div>

  <div class="row mt-3">
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
    <div class="col-sm-6">
      <SectionList
        title="Declared Majors"
        subtitle="Upon Graduation"
        infoTitle="Declared Majors"
        infoContent="Compare the proportion of certain majors in your class..."
      >
        <template #content>
          <PercentList :items="graduatedMajorsList"> </PercentList>
        </template>
      </SectionList>
    </div>
  </div>
</template>

<script>
import { get } from "axios";
import SectionProperty from "./SectionProperty.vue";
import SectionList from "./SectionList.vue";
import PercentList from "./PercentList.vue";
import Histogram from "../popover/Histogram.vue";
import PopoverIcon from "../popover/PopoverIcon.vue";
import { TabsList, TabsDisplay, TabsItem, TabsPanel } from "axdd-components";
export default {
  name: "HistoricSection",
  async setup(props) {
    const pastPerformanceRes = await get(
      "api/v1/course/" + props.sectionLabel + "/past/performance"
    );
    const performance = pastPerformanceRes.data.performance;

    const pastStudentMajorsRes = await get(
      "api/v1/course/" + props.sectionLabel + "/past/studentmajor"
    );
    const studentMajors = pastStudentMajorsRes.data.student_majors;

    const pastGraduatedMajorsRes = await get(
      "api/v1/course/" + props.sectionLabel + "/past/graduatedmajor"
    );
    const graduatedMajors = pastGraduatedMajorsRes.data.graduated_majors;

    console.log(performance);
    return {
      performance,
      studentMajors,
      graduatedMajors,
    };
  },
  components: {
    SectionProperty,
    SectionList,
    PercentList,
    Histogram,
    PopoverIcon,
    "axdd-tabs-list": TabsList,
    "axdd-tabs-display": TabsDisplay,
    "axdd-tabs-item": TabsItem,
    "axdd-tabs-panel": TabsPanel,
  },
  props: {
    sectionLabel: String,
  },
  computed: {
    medianGpas() {
      return this.median(this.performance.gpas);
    },
    medianCourseGrades() {
      return this.median(this.performance.course_grades);
    },
    studentMajorsList() {
      return this.studentMajors.slice(0).map((obj) => {
        return {
          percent: obj.percent_students,
          title: obj.major_name,
        };
      });
    },
    graduatedMajorsList() {
      return this.graduatedMajors.slice(0).map((obj) => {
        return {
          percent: obj.percent_students,
          title: obj.major_name,
        };
      });
    },
    failureRate() {
      return Math.round(
        (this.performance.course_grades.filter((grade) => grade <= 0.7).length /
          this.performance.course_grades.length) *
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
    return {};
  },
  created: function () {},
};
</script>
