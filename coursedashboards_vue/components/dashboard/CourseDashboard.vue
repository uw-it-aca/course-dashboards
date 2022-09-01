<template>
  <div class="row">
    <div class="col-sm-12 col-lg-6 mb-4 border-end">
      <MyDataSelector />
      <router-view v-slot="{ Component }" name="MyData">
        <KeepAlive max="5">
          <component :is="Component" :key="$route.fullPath" />
        </KeepAlive>
      </router-view>
    </div>
    <div class="col-sm-12 col-lg-6 mb-4">
      <router-view v-slot="{ Component }" name="HistoricData">
        <KeepAlive max="5">
          <component :is="Component" :key="historicKey" />
        </KeepAlive>
      </router-view>
      <!-- <Suspense>
        <historic-section :section-label="sectionLabel" />
        <template #fallback> Loading... </template>
      </Suspense> -->
    </div>
  </div>
</template>

<script>
import CurrentSection from "../dashboard/CurrentSection.vue";
import HistoricSection from "../dashboard/HistoricSection.vue";
import MyDataSelector from "./MyDataSelector.vue";
import { toSectionLabel } from "../../helpers/utils";
export default {
  name: "CourseDashboard",
  components: {
    "current-section": CurrentSection,
    "historic-section": HistoricSection,
    MyDataSelector,
  },
  computed: {
    historicKey() {
      const params = this.$route.params;
      return (
        params.curriculum + "-" + params.course_number + "-" + params.section_id
      );
    },
  },
};
</script>
