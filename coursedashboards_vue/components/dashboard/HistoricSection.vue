<template>
  <h2 class="h3 fw-bold">
    Historical Student Data <span class="text-danger">POL S 201 A</span>
  </h2>

  <div class="row mb-5">
    <div class="col-4 border-end">
      <select class="form-select form-select-sm" aria-label="">
        <option selected>All Courses</option>
        <option value="1">Only My Courses</option>
      </select>
    </div>
    <div class="col-6">
      <div class="d-flex">
        <select class="form-select form-select-sm me-2" aria-label="">
          <option selected>All Quarters</option>
          <option value="1">Autumn</option>
          <option value="2">Winter</option>
          <option value="3">Spring</option>
          <option value="4">Summer</option>
        </select>
        <select class="form-select form-select-sm" aria-label="">
          <option selected>All Years</option>
          <option value="1">2022</option>
          <option value="2">2021</option>
          <option value="3">2020</option>
        </select>
      </div>
      <div>
        <select class="form-select form-select-sm" aria-label="">
          <option disabled>Autumn 2022 (current)</option>
          <option value="1">Spring 2022</option>
        </select>
      </div>
    </div>
  </div>

  <div class="alert alert-dark-beige border-0 small" role="alert">
    <p class="mb-0">
      The query you requested will not generate data. This is a new course, and
      there is no historical information to draw upon.
    </p>
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
        propertyTitle="Median Cumulative GPA"
        :property="medianGpas"
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
          <Histogram :data="performance.gpas" />
        </template>
      </SectionProperty>
    </div>
    <div class="col-sm-6">
      <SectionProperty
        propertyTitle="Percent Failure"
        :property="failureRate + '%'"
      >
        <template #title-icon>
          <i class="bi bi-info-circle-fill" />
        </template>
        <template #property-icon>
          <i class="bi bi-flag-fill" />
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
    <div class="col-sm-12">
      <SectionList
        title="Concurrent courses"
        infoTitle="Concurrent courses"
        infoContent="Lorem ipsum dolor sit amet, consectetur adipisicing elit. Provident accusamus cum eius suscipit, ex explicabo magnam, deleniti perspiciatis iste hic dignissimos ducimus officia nemo pariatur nisi magni quo autem accusantium?"
      >
        <template #content
          >Lorem ipsum dolor sit amet, consectetur adipisicing elit. Provident
          accusamus cum eius suscipit, ex explicabo magnam, deleniti
          perspiciatis iste hic dignissimos ducimus officia nemo pariatur nisi
          magni quo autem accusantium?</template
        >
      </SectionList>
    </div>

    <div class="col-sm-12">
      <SectionList
        title="Previous Instructors or TAs for this course"
        infoTitle="Previous Instructors or TAs"
        infoContent="Lorem ipsum dolor sit amet, consectetur adipisicing elit. Provident accusamus cum eius suscipit, ex explicabo magnam, deleniti perspiciatis iste hic dignissimos ducimus officia nemo pariatur nisi magni quo autem accusantium?"
      >
        <template #content
          >Lorem ipsum dolor sit amet, consectetur adipisicing elit. Provident
          accusamus cum eius suscipit, ex explicabo magnam, deleniti
          perspiciatis iste hic dignissimos ducimus officia nemo pariatur nisi
          magni quo autem accusantium?</template
        >
      </SectionList>
    </div>
  </div>
</template>

<script>
import { get } from "axios";

import { TabsList, TabsDisplay, TabsItem, TabsPanel } from "axdd-components";

import SectionProperty from "./SectionProperty.vue";
import SectionList from "./SectionList.vue";
import PercentList from "./PercentList.vue";
import Histogram from "../popover/Histogram.vue";
import PopoverIcon from "../popover/PopoverIcon.vue";
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
    "axdd-tabs-list": TabsList,
    "axdd-tabs-display": TabsDisplay,
    "axdd-tabs-item": TabsItem,
    "axdd-tabs-panel": TabsPanel,
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
