<template>
  <div>Historic Section</div>
  <div class="container">
    <div class="row">
      <div class="col-sm-6">
        <SectionProperty
          :propertyTitle="'Students / ' + performance.offering_count + ' Offerings'"
          :property="performance.enrollment"
        >
          <template #property-icon>
            <i class="bi bi-people-fill" />
          </template>
        </SectionProperty>
      </div>
      <div class="col-sm-6">
        <SectionProperty propertyTitle="Percent Failure" :property="failureRate + '%'">
          <template #title-icon>
            <i class="bi bi-info-circle-fill" />
          </template>
          <template #property-icon>
            <i class="bi bi-flag-fill" />
          </template>
        </SectionProperty>
      </div>
    </div>
    <div class="row">
      <div class="col-sm-6">
        <SectionProperty propertyTitle="Median Cumulative GPA" :property="medianGpas">
          <template #title-icon>
            <i class="bi bi-info-circle-fill" />
          </template>
          <template #property-icon>
            <i class="bi bi-bar-chart-fill"></i>
          </template>
        </SectionProperty>
      </div>
      <div class="col-sm-6">
        <SectionProperty propertyTitle="Median Course Grade" :property="medianCourseGrades">
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
          title="Declared Majors"
          subtitle="When taking the course"
          :items="studentMajorsList"
        >
        </CourseMajorList>
      </div>
      <div class="col-sm-6">
        <CourseMajorList
          title="Declared Majors"
          subtitle="Upon Graduation"
          :items="graduatedMajorsList"
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
  name: "HistoricSection",
  async setup(props) {
    
    const pastPerformanceRes = await get("api/v1/course/" + props.sectionLabel + "/past/performance");
    const performance = pastPerformanceRes.data.performance;

    const pastStudentMajorsRes = await get("api/v1/course/" + props.sectionLabel + "/past/studentmajor");
    const studentMajors = pastStudentMajorsRes.data.student_majors;

    const pastGraduatedMajorsRes = await get("api/v1/course/" + props.sectionLabel + "/past/graduatedmajor");
    const graduatedMajors = pastGraduatedMajorsRes.data.graduated_majors;

    console.log(performance);
    return {
      performance,
      studentMajors,
      graduatedMajors,
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
    medianGpas() {
      return this.median(this.performance.gpas); 
    },
    medianCourseGrades() {
      return this.median(this.performance.course_grades);
    },
    studentMajorsList() {
      return this.studentMajors.slice(0).map(obj => {
        return {
          percent: obj.percent_students,
          title: obj.major_name,
        }
      })
    },
    graduatedMajorsList() {
      return this.graduatedMajors.slice(0).map(obj => {
        return {
          percent: obj.percent_students,
          title: obj.major_name,
        }
      })
    },
    failureRate() {
      return Math.round(
        this.performance.course_grades.filter((grade) => grade <= 0.7).length /
        this.performance.course_grades.length * 100
      ) 
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
    };
  },
  created: function () {
  },
};
</script>
