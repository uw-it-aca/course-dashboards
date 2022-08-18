<template>
  <div
    class="modal fade"
    id="introModal"
    tabindex="-1"
    aria-labelledby="introModalLabel"
    aria-hidden="true"
    data-bs-backdrop="static"
    data-bs-keyboard="false"
  >
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="introModalLabel">Welcome to CODA</h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <p>
            Course Dashboard (CODA) is a course statistics dashboard that offers
            insights on the courses you teach:
          </p>
          <h5 class="fw-bold">Student Engagement</h5>
          <p>
            Knowing your current students' majors and other courses they are
            taking helps you make connections between student interests and your
            course&lsquo;s subject matter.
          </p>
          <h5 class="fw-bold">First Time Teaching a Course</h5>
          <p>
            View your course's past offerings median final grade and student
            failure percentage to get an idea of how the course is typically
            graded.
          </p>
          <h5 class="fw-bold">Student Success</h5>
          <p>
            Compare your current students' average cumulative GPA with those of
            past offerings to determine how much time you should spend on the
            most challenging topics.
          </p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-primary" data-bs-dismiss="modal">
            OK
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Modal } from "bootstrap";
import courseDataMixin from "../mixins/courseDataMixin";
export default {
  name: "IntroModal",
  mixins: [courseDataMixin],
  data() {
    return {
      netid: "",
      introductionVersion: 1,
    };
  },
  watch: {},
  methods: {
    closeModal() {
      this.setIntroModalSeen(this.netid);
    },
  },
  created: function () {},
  mounted: function () {
    const modalEl = document.getElementById("introModal");
    const modal = new Modal(modalEl);
    const user = JSON.parse(document.getElementById("user").textContent);
    this.netid = user.netid;

    // Mixin
    this.getIntroModalStatus(this.netid).then((res) => {
      if (!res.data.seen) {
        modal.show();
      }
    });

    modalEl.addEventListener("hidden.bs.modal", (event) => {
      this.closeModal();
    });
  },
};
</script>
