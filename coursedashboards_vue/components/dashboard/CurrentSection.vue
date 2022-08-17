<template>
  <h2 class="h3 fw-bold">
    My Data for <span class="text-danger">POL S 201 A</span>
    <a
      class="float-end fs-5"
      href="https://my.uw.edu/teaching/"
      target="_blank"
      title="View course details in Teaching page"
    >
      <i class="bi bi-box-arrow-up-right me-1" />Course Details
      <!-- <span class="sr-only">
        for {{ curriculum }} {{ course_number }} {{ section_id }}</span
      > -->
    </a>
  </h2>

  <div class="row mb-5">
    <div class="col-6">
      <select class="form-select form-select-sm" aria-label="">
        <option selected>Autumn 2022 (current)</option>
        <option value="1">Spring 2022</option>
      </select>
    </div>
  </div>
  <div class="alert alert-dark-beige border-0 small" role="alert">
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
            <li>10% EOP</li>
            <li>20% Transfer</li>
            <li>2% Disabled</li>
            <li>8% Academic Probation</li>
            <li>20% Repeating Students</li>
          </ul>
        </template>
      </SectionProperty>
    </div>
    <div class="col-sm-6">
      <SectionProperty propertyTitle="Median Cumulative GPA" :property="dfsa">
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

  <div class="row mt-5">
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
  </div>
</template>

<script>
import { get } from "axios";
import SectionProperty from "./SectionProperty.vue";
import SectionList from "./SectionList.vue";
import PercentList from "./PercentList.vue";
import PopoverIcon from "../popover/PopoverIcon.vue";
export default {
  name: "CurrentSection",
  async setup(props) {
    const res = await get("api/v1/course/" + props.sectionLabel);
    const data = await res.data;
    return {
      data,
    };
  },
  components: {
    SectionProperty,
    SectionList,
    PercentList,
    PopoverIcon,
  },
  props: {
    sectionLabel: String,
  },
  computed: {
    registeredString() {
      return (
        this.data.current_enrollment +
        " / " +
        this.data.limit_estimate_enrollment
      );
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
  data() {
    return {};
  },
  created: function () {},
};
</script>
