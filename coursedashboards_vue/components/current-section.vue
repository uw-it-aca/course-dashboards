<template>
  <div>Current Section</div>
  <div class="container">
    <div class="row">
      <div class="col-sm-6">
        <SectionProperty propertyTitle="Currently Registered" :property="registeredString">
          <template #property-icon>
            <i class="bi bi-people-fill" />
          </template>
        </SectionProperty>
      </div>
      <div class="col-sm-6">
        <SectionProperty propertyTitle="Repeating Students" :property="data.current_repeating">
          <template #title-icon>
            <i class="bi bi-info-circle-fill" />
          </template>
          <template #property-icon>
            <i class="bi bi-arrow-clockwise" />
          </template>
        </SectionProperty>
      </div>
    </div>
    <div class="row">
      <div class="col-sm-6">
        <SectionProperty propertyTitle="Median Cumulative GPA" :property="data.current_median">
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
        <CourseMajorList
          title="Concurrent Courses"
          subtitle="When taking the course"
          :items="concurrentCourses"
        >
        </CourseMajorList>
      </div>
      <div class="col-sm-6">
        <CourseMajorList
          title="Declared Majors"
          subtitle="When taking the course"
          :items="currentStudentMajors"
        >
        </CourseMajorList>
      </div>
    </div>
  </div>
</template>

<script>
import { get } from "axios";
import SectionProperty from "../components/section-property.vue";
import CourseMajorList from "../components/course-major-list.vue";
export default {
  name: "CurrentSection",
  async setup(props) {
    
    const res = await get("api/v1/course/" + props.sectionLabel);
    const data = await res.data;
    return {
      data,
    }
  },
  components: {
    SectionProperty,
    CourseMajorList,
  },
  props: {
    sectionLabel: String,

  },
  computed: {
    registeredString() {
      return this.data.current_enrollment + " / " + this.data.limit_estimate_enrollment; 
    },
    currentStudentMajors() {
      return this.data.current_student_majors.slice(0).map(obj => {
        return {
          percent: obj.percent_students,
          title: obj.major_name,
        }
      })
    },
    concurrentCourses() {
      return this.data.concurrent_courses.slice(0).map(obj => {
        return {
          percent: obj.percent_students,
          title: obj.course_ref,
        }
      })
    }
  },
  data() {
    return {
    };
  },
  created: function () {
  },
};
</script>
