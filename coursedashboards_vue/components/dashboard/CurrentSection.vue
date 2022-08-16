<template>
  <h2>Current Section</h2>

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
          <PopoverIcon title="ASD" content="ASDASD">
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
          <PopoverIcon title="ASD" content="ASDASD">
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
        infoContent="Compare the proportion of certain majors in your class..."
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
        infoContent="Compare the proportion of certain majors in your class..."
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
