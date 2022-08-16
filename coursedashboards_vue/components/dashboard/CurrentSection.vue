<template>
  <h2>
    Current Section
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

  <div class="row">
    <div class="col-sm-6">
      <SectionProperty
        propertyTitle="Currently Registered"
        :property="registeredString"
      >
        <template #property-icon>
          <i class="bi bi-people-fill" />
        </template>
      </SectionProperty>
    </div>
    <div class="col-sm-6">
      <SectionProperty
        propertyTitle="Repeating Students"
        :property="data.current_repeating"
      >
        <template #title-icon>
          <PopoverIcon
            title="Repeating Students"
            content="This is the number of students who have received a grade in a previous offering of the course.  Help gauge the amount of support you should provide your students, especially for required courses."
          >
            <i class="bi bi-info-circle-fill" />
          </PopoverIcon>
        </template>
        <template #property-icon>
          <i class="bi bi-arrow-clockwise" />
        </template>
      </SectionProperty>
    </div>
  </div>
  <div class="row">
    <div class="col-sm-6">
      <SectionProperty
        propertyTitle="Median Cumulative GPA"
        :property="data.current_median"
      >
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
    </div>
  </div>
  <div class="row mt-3">
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
