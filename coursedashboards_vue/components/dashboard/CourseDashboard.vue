<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-6">
        <Suspense>
          <current-section :section-label="sectionLabel" />
          <template #fallback>
            Loading...
          </template>
        </Suspense>
      </div>
      <div class="col-sm-6">
        <Suspense>
          <historic-section :section-label="sectionLabel" />
          <template #fallback>
            Loading...
          </template>
        </Suspense>
      </div>
    </div>
  </div>
</template>

<script>
import CurrentSection from "../dashboard/CurrentSection.vue";
import HistoricSection from "../dashboard/HistoricSection.vue";
import { toSectionLabel } from "../../utils";
export default {
  name: "CourseDashboard",
  components: {
    "current-section": CurrentSection,
    "historic-section": HistoricSection,
  },
  data() {
    return {
      asd: '',
      count: 0,
    };
  },
  methods: {
  },
  watch: {
  },
  computed: {
    sectionLabel() {
      return toSectionLabel(this.$route.params);
    }
  },
  created: function () {
  },
};
</script>
