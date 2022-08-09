<template>
  <div class="row">
    <div class="col-sm-12 col-lg-6 mb-4 border-end">
      <Suspense>
        <current-section :section-label="sectionLabel" />
        <template #fallback> Loading... </template>
      </Suspense>
    </div>
    <div class="col-sm-12 col-lg-6 mb-4">
      <Suspense>
        <historic-section :section-label="sectionLabel" />
        <template #fallback> Loading... </template>
      </Suspense>
    </div>
  </div>
</template>

<script>
import CurrentSection from "../dashboard/CurrentSection.vue";
import HistoricSection from "../dashboard/HistoricSection.vue";
import { toSectionLabel } from "../../helpers/utils";
export default {
  name: "CourseDashboard",
  components: {
    "current-section": CurrentSection,
    "historic-section": HistoricSection,
  },
  computed: {
    sectionLabel() {
      return toSectionLabel(this.$route.params);
    },
  },
};
</script>
